from app.product.model import ProductStatus
from app.product.service import create_product, list_products
from app.seller.service import create_seller


class TestCreateProduct:
    def test_creates_product(self, db):
        seller = create_seller(db)
        product = create_product(db, name="테스트 상품", price=10000, seller_id=seller.id)

        assert product.name == "테스트 상품"
        assert product.price == 10000
        assert product.seller_id == seller.id
        assert product.id is not None

    def test_default_status_is_active(self, db):
        seller = create_seller(db)
        product = create_product(db, name="테스트 상품", price=10000, seller_id=seller.id)

        assert product.status == ProductStatus.ACTIVE


class TestListProducts:
    def test_returns_all_products_for_seller(self, db):
        seller = create_seller(db)
        create_product(db, name="상품A", price=1000, seller_id=seller.id)
        create_product(db, name="상품B", price=2000, seller_id=seller.id)

        result = list_products(db, seller_id=seller.id)

        assert len(result) == 2

    def test_filters_by_seller(self, db):
        seller_a = create_seller(db)
        seller_b = create_seller(db)
        create_product(db, name="A의 상품", price=1000, seller_id=seller_a.id)
        create_product(db, name="B의 상품", price=2000, seller_id=seller_b.id)

        result = list_products(db, seller_id=seller_a.id)

        assert len(result) == 1
        assert result[0].name == "A의 상품"

    def test_filter_by_active(self, db):
        seller = create_seller(db)
        create_product(db, name="활성 상품", price=1000, seller_id=seller.id)
        inactive = create_product(db, name="비활성 상품", price=2000, seller_id=seller.id)
        inactive.status = ProductStatus.INACTIVE
        db.commit()

        result = list_products(db, status="active", seller_id=seller.id)

        assert len(result) == 1
        assert result[0].name == "활성 상품"

    def test_filter_by_inactive(self, db):
        seller = create_seller(db)
        create_product(db, name="활성 상품", price=1000, seller_id=seller.id)
        inactive = create_product(db, name="비활성 상품", price=2000, seller_id=seller.id)
        inactive.status = ProductStatus.INACTIVE
        db.commit()

        result = list_products(db, status="inactive", seller_id=seller.id)

        assert len(result) == 1
        assert result[0].name == "비활성 상품"

    def test_empty_list(self, db):
        seller = create_seller(db)

        result = list_products(db, seller_id=seller.id)

        assert result == []

    def test_ordered_by_latest_first(self, db):
        seller = create_seller(db)
        create_product(db, name="먼저", price=1000, seller_id=seller.id)
        create_product(db, name="나중에", price=2000, seller_id=seller.id)

        result = list_products(db, seller_id=seller.id)

        assert result[0].name == "나중에"
        assert result[1].name == "먼저"
