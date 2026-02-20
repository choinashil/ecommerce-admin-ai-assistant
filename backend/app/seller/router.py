from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.shared.database import get_db
from app.seller.schema import SellerResponse
from app.seller.service import create_seller

router = APIRouter()


@router.post("/api/sellers", response_model=SellerResponse)
def register_seller(db: Session = Depends(get_db)):
    seller = create_seller(db)
    return SellerResponse(token=str(seller.token), nickname=seller.nickname)
