from contextlib import asynccontextmanager

from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import APP_NAME, settings
from app.database import Base, engine, get_db
from app.models import Product, Order, Conversation, Message  # noqa: F401
from app.api.chat import router as chat_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title=APP_NAME, lifespan=lifespan)
app.include_router(chat_router)


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
