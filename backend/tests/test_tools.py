from app.product.service import create_product
from app.chat.tools.executor import ToolContext, execute_tool
from app.seller.service import create_seller


def _ctx(db, seller):
    return ToolContext(db=db, seller_id=seller.id)


class TestExecuteTool:
    def test_create_product(self, db):
        seller = create_seller(db)
        result = execute_tool(
            _ctx(db, seller), "create_product", {"name": "테스트 상품", "price": 10000}
        )

        assert result["id"].startswith("PRD-")
        assert result["name"] == "테스트 상품"
        assert result["price"] == 10000
        assert result["status"] == "active"

    def test_list_products_empty(self, db):
        seller = create_seller(db)
        result = execute_tool(_ctx(db, seller), "list_products", {})

        assert result["products"] == []
        assert result["total"] == 0

    def test_list_products_with_data(self, db):
        seller = create_seller(db)
        create_product(db, name="상품A", price=1000, seller_id=seller.id)
        create_product(db, name="상품B", price=2000, seller_id=seller.id)

        result = execute_tool(_ctx(db, seller), "list_products", {})

        assert result["total"] == 2

    def test_list_products_isolates_by_seller(self, db):
        seller_a = create_seller(db)
        seller_b = create_seller(db)
        create_product(db, name="A의 상품", price=1000, seller_id=seller_a.id)
        create_product(db, name="B의 상품", price=2000, seller_id=seller_b.id)

        result = execute_tool(_ctx(db, seller_a), "list_products", {})

        assert result["total"] == 1
        assert result["products"][0]["name"] == "A의 상품"

    def test_list_products_with_status_filter(self, db):
        seller = create_seller(db)
        ctx = _ctx(db, seller)
        execute_tool(ctx, "create_product", {"name": "상품A", "price": 1000})
        execute_tool(ctx, "create_product", {"name": "상품B", "price": 2000})

        result = execute_tool(ctx, "list_products", {"status": "active"})

        assert result["total"] == 2

    def test_unknown_tool(self, db):
        seller = create_seller(db)
        result = execute_tool(_ctx(db, seller), "unknown_tool", {})

        assert "error" in result
