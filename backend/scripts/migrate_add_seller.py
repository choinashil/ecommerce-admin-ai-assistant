"""
sellers 테이블 생성 + 기존 conversation에 기본 판매자 할당.

실행: cd backend && python -m scripts.migrate_add_seller
"""

from sqlalchemy import text

from app.shared.database import SessionLocal, engine, Base
from app.seller.model import Seller  # noqa: F401 — create_all 대상 등록
from app.chat.model import Conversation  # noqa: F401


def migrate():
    # 1. sellers 테이블 생성 (없으면)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # 2. conversations에 seller_id 컬럼 추가 (없으면)
        result = db.execute(text("""
            SELECT column_name FROM information_schema.columns
            WHERE table_name = 'conversations' AND column_name = 'seller_id'
        """))
        if not result.fetchone():
            db.execute(text(
                "ALTER TABLE conversations ADD COLUMN seller_id INTEGER REFERENCES sellers(id)"
            ))
            db.commit()
            print("conversations.seller_id 컬럼 추가 완료")

        # 3. 기본 판매자 생성
        existing = db.query(Seller).filter(Seller.nickname == "초기-판매자-0").first()
        if existing:
            default_seller = existing
            print(f"기본 판매자 이미 존재: id={default_seller.id}")
        else:
            default_seller = Seller(nickname="초기-판매자-0")
            db.add(default_seller)
            db.commit()
            db.refresh(default_seller)
            print(f"기본 판매자 생성: id={default_seller.id}")

        # 4. seller_id가 없는 기존 conversation에 기본 판매자 할당
        updated = db.execute(
            text("UPDATE conversations SET seller_id = :sid WHERE seller_id IS NULL"),
            {"sid": default_seller.id},
        )
        db.commit()
        print(f"기존 conversation {updated.rowcount}개에 기본 판매자 할당 완료")

    finally:
        db.close()


if __name__ == "__main__":
    migrate()
