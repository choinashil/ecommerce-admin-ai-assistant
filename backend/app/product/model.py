import enum
from datetime import datetime

from sqlalchemy import Boolean, Integer, Enum, DateTime, String, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.database import Base


class ProductStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    seller_id: Mapped[int] = mapped_column(Integer, ForeignKey("sellers.id"))
    name: Mapped[str] = mapped_column(String(200))
    price: Mapped[int] = mapped_column(Integer)
    status: Mapped[ProductStatus] = mapped_column(
        Enum(ProductStatus), default=ProductStatus.ACTIVE
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    is_deleted: Mapped[bool] = mapped_column(Boolean, default=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
