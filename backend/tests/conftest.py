import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base


@pytest.fixture()
def db():
    """테스트용 DB 세션. 각 테스트 후 롤백하여 격리."""
    engine = create_engine(settings.database_url)
    Base.metadata.create_all(bind=engine)

    connection = engine.connect()
    transaction = connection.begin()
    session = sessionmaker(bind=connection)()

    # 기존 데이터 삭제 (트랜잭션 내부이므로 테스트 후 rollback으로 원복)
    session.execute(text("DELETE FROM messages"))
    session.execute(text("DELETE FROM orders"))
    session.execute(text("DELETE FROM products"))
    session.execute(text("DELETE FROM conversations"))
    session.flush()

    yield session

    session.close()
    transaction.rollback()

    # PostgreSQL 시퀀스는 트랜잭션과 독립적이므로, 롤백 후 시퀀스를 max(id) 기준으로 리셋
    with engine.connect() as reset_conn:
        for table in ("conversations", "messages", "orders", "products"):
            reset_conn.execute(
                text(
                    f"SELECT setval(pg_get_serial_sequence('{table}', 'id'), "
                    f"COALESCE((SELECT MAX(id) FROM {table}), 0) + 1, false)"
                )
            )
        reset_conn.commit()

    connection.close()
