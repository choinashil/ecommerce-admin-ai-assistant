from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.display_id import to_display_id
from app.schemas.product import Product
from app.services.product_service import list_products

router = APIRouter()


@router.get("/api/products", response_model=list[Product])
def get_products(db: Session = Depends(get_db)):
    products = list_products(db)
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
