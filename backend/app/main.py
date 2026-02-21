from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.shared.config import APP_NAME, settings
from app.shared.schema import ErrorResponse
from app.shared.database import Base, engine, get_db
from app.seller.model import Seller  # noqa: F401
from app.product.model import Product  # noqa: F401
from app.order.model import Order  # noqa: F401
from app.chat.model import Conversation, Message  # noqa: F401
from app.guide.model import GuideDocument, GuideChunk  # noqa: F401
from app.seller.router import router as seller_router
from app.chat.router import router as chat_router
from app.product.router import router as products_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    with engine.connect() as conn:
        conn.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
        conn.commit()
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=APP_NAME,
    lifespan=lifespan,
    responses={
        500: {"description": "Internal Server Error", "model": ErrorResponse},
    },
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins.split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(seller_router)
app.include_router(chat_router)
app.include_router(products_router)


@app.get("/")
def read_root():
    return {"message": APP_NAME, "status": "ok"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/config-test")
def config_test():
    return {
        "app_name": APP_NAME,
        "debug": settings.debug,
        "config_loaded": True,
    }


@app.get("/db-test")
def db_test(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT 1"))
    result.scalar()

    tables = db.execute(
        text("SELECT tablename FROM pg_tables WHERE schemaname = 'public'")
    ).fetchall()

    return {
        "status": "connected",
        "tables": [t[0] for t in tables],
    }
