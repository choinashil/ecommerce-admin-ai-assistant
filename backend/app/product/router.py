from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.shared.auth import require_seller
from app.shared.database import get_db
from app.shared.display_id import to_display_id
from app.seller.model import Seller
from app.product.schema import Product
from app.product.service import list_products

router = APIRouter()


@router.get("/api/products", response_model=list[Product])
def get_products(
    db: Session = Depends(get_db),
    seller: Seller = Depends(require_seller),
):
    products = list_products(db, seller_id=seller.id)
    return [
        Product(
            id=to_display_id("products", p.id),
            name=p.name,
            price=p.price,
            status=p.status.value,
            created_at=p.created_at,
        )
        for p in products
    ]
