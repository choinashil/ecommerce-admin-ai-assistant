from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.shared.database import get_db
from app.seller.model import Seller
from app.seller.service import get_seller_by_token


def get_current_seller(
    db: Session = Depends(get_db),
    authorization: str | None = Header(None),
) -> Seller | None:
    """토큰이 있으면 판매자 반환, 없으면 None."""
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.removeprefix("Bearer ")
    return get_seller_by_token(db, token)


def require_seller(
    seller: Seller | None = Depends(get_current_seller),
) -> Seller:
    """판매자 필수 API용. 토큰 없거나 유효하지 않으면 401."""
    if not seller:
        raise HTTPException(status_code=401, detail="유효한 판매자 토큰이 필요합니다")

    return seller
