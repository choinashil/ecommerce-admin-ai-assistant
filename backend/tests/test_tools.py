from app.product.service import create_product
from app.chat.tools.executor import execute_tool


class TestExecuteTool:
    def test_create_product(self, db):
        result = execute_tool(db, "create_product", {"name": "테스트 상품", "price": 10000})

        assert result["id"].startswith("PRD-")
        assert result["name"] == "테스트 상품"
        assert result["price"] == 10000
        assert result["status"] == "active"

    def test_list_products_empty(self, db):
        result = execute_tool(db, "list_products", {})

        assert result["products"] == []
        assert result["total"] == 0

    def test_list_products_with_data(self, db):
        create_product(db, name="상품A", price=1000)
        create_product(db, name="상품B", price=2000)

        result = execute_tool(db, "list_products", {})

        assert result["total"] == 2

    def test_list_products_with_status_filter(self, db):
        execute_tool(db, "create_product", {"name": "상품A", "price": 1000})
        execute_tool(db, "create_product", {"name": "상품B", "price": 2000})

        result = execute_tool(db, "list_products", {"status": "active"})

        assert result["total"] == 2

    def test_unknown_tool(self, db):
        result = execute_tool(db, "unknown_tool", {})

        assert "error" in result
