from datetime import datetime

from pgvector.sqlalchemy import Vector
from sqlalchemy import DateTime, ForeignKey, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column

from app.shared.config import settings
from app.shared.database import Base


class GuideDocument(Base):
    __tablename__ = "guide_documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(500), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(500))
    content: Mapped[str] = mapped_column(Text)
    breadcrumb: Mapped[str | None] = mapped_column(String(500), nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class GuideChunk(Base):
    __tablename__ = "guide_chunks"

    id: Mapped[int] = mapped_column(primary_key=True)
    document_id: Mapped[int] = mapped_column(
        ForeignKey("guide_documents.id", ondelete="CASCADE")
    )
    content: Mapped[str] = mapped_column(Text)
    embedding: Mapped[list[float]] = mapped_column(
        Vector(settings.openai_embedding_dimension)
    )
    chunk_index: Mapped[int] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
