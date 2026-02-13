from app.models.product import ProductStatus
from app.services.product_service import create_product, list_products


class TestCreateProduct:
    def test_creates_product(self, db):
        product = create_product(db, name="테스트 상품", price=10000)

        assert product.name == "테스트 상품"
        assert product.price == 10000
        assert product.id is not None

    def test_default_status_is_active(self, db):
        product = create_product(db, name="테스트 상품", price=10000)

        assert product.status == ProductStatus.ACTIVE


class TestListProducts:
    def test_returns_all_products(self, db):
        create_product(db, name="상품A", price=1000)
        create_product(db, name="상품B", price=2000)

        result = list_products(db)

        assert len(result) == 2

    def test_filter_by_active(self, db):
        create_product(db, name="활성 상품", price=1000)
        inactive = create_product(db, name="비활성 상품", price=2000)
        inactive.status = ProductStatus.INACTIVE
        db.commit()

        result = list_products(db, status="active")

        assert len(result) == 1
        assert result[0].name == "활성 상품"

    def test_filter_by_inactive(self, db):
        create_product(db, name="활성 상품", price=1000)
        inactive = create_product(db, name="비활성 상품", price=2000)
        inactive.status = ProductStatus.INACTIVE
        db.commit()

        result = list_products(db, status="inactive")

        assert len(result) == 1
        assert result[0].name == "비활성 상품"

    def test_empty_list(self, db):
        result = list_products(db)

        assert result == []

    def test_ordered_by_latest_first(self, db):
        create_product(db, name="먼저", price=1000)
        create_product(db, name="나중에", price=2000)

        result = list_products(db)

        assert result[0].name == "나중에"
        assert result[1].name == "먼저"
