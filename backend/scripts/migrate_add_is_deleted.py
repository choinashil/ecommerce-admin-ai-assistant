"""
products 테이블에 is_deleted 컬럼 추가.

실행: cd backend && python -m scripts.migrate_add_is_deleted
"""

from sqlalchemy import text

from app.shared.database import SessionLocal


def migrate():
    db = SessionLocal()
    try:
        result = db.execute(text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'products' AND column_name = 'is_deleted'
        """))
        if not result.fetchone():
            db.execute(text(
                "ALTER TABLE products ADD COLUMN is_deleted BOOLEAN NOT NULL DEFAULT FALSE"
            ))
            db.commit()
            print("products.is_deleted 컬럼 추가 완료")
        else:
            print("products.is_deleted 컬럼이 이미 존재합니다")
    finally:
        db.close()


if __name__ == "__main__":
    migrate()
