from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.shared.database import get_db
from app.shared.display_id import parse_pk
from app.shared.schema import ErrorResponse
from app.seller.schema import SellerDetail, SellerResponse
from app.seller.service import create_seller, get_seller_detail

router = APIRouter()


@router.post("/api/sellers", response_model=SellerResponse)
def register_seller(db: Session = Depends(get_db)):
    seller = create_seller(db)
    return SellerResponse(token=str(seller.token), nickname=seller.nickname)


@router.get(
    "/api/sellers/{seller_id}",
    response_model=SellerDetail,
    responses={404: {"description": "Seller not found", "model": ErrorResponse}},
)
def get_seller(seller_id: str, db: Session = Depends(get_db)):
    pk = parse_pk(seller_id, "sellers")
    detail = get_seller_detail(db, pk)
    if not detail:
        raise HTTPException(status_code=404, detail="Seller not found")
    return detail
