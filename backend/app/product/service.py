from sqlalchemy.orm import Session

from app.product.model import Product, ProductStatus


def create_product(db: Session, name: str, price: int) -> Product:
    """상품을 생성한다."""
    product = Product(
        name=name,
        price=price,
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


def list_products(db: Session, status: str | None = None) -> list[Product]:
    """상품 목록을 조회한다. status 필터 선택."""
    query = db.query(Product)

    if status is not None:
        query = query.filter(Product.status == ProductStatus(status))

    return query.order_by(Product.id.desc()).all()
