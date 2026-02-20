import random

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.chat.model import Conversation, Message, MessageRole
from app.seller.model import Seller
from app.shared.display_id import to_display_id

ADJECTIVES = [
    "행복한", "용감한", "빠른", "조용한", "밝은",
    "귀여운", "씩씩한", "따뜻한", "재빠른", "똑똑한",
    "활발한", "상냥한", "신나는", "든든한", "멋진",
    "산뜻한", "부지런한", "느긋한", "다정한", "유쾌한",
]

ANIMALS = [
    "고양이", "강아지", "토끼", "여우", "판다",
    "코알라", "펭귄", "돌고래", "다람쥐", "수달",
    "부엉이", "햄스터", "거북이", "앵무새", "사슴",
    "해달", "레서판다", "미어캣", "알파카", "카피바라",
]


def generate_nickname() -> str:
    adj = random.choice(ADJECTIVES)
    animal = random.choice(ANIMALS)
    num = random.randint(1, 99)
    return f"{adj}-{animal}-{num}"


MAX_NICKNAME_RETRIES = 5


def _generate_unique_nickname(db: Session) -> str:
    for _ in range(MAX_NICKNAME_RETRIES):
        nickname = generate_nickname()
        exists = db.query(Seller).filter(Seller.nickname == nickname).first()
        if not exists:
            return nickname
    raise RuntimeError("닉네임 생성에 실패했습니다. 재시도 횟수를 초과했습니다.")


def create_seller(db: Session) -> Seller:
    nickname = _generate_unique_nickname(db)
    seller = Seller(nickname=nickname)
    db.add(seller)
    db.commit()
    db.refresh(seller)
    return seller


def get_seller_by_token(db: Session, token: str) -> Seller | None:
    return db.query(Seller).filter(Seller.token == token).first()


def get_seller_detail(db: Session, seller_pk: int) -> dict | None:
    seller = db.get(Seller, seller_pk)
    if not seller:
        return None

    stats = (
        db.query(
            func.count(func.distinct(Conversation.id)).label("total_conversations"),
            func.count(Message.id).label("total_messages"),
            func.max(Conversation.updated_at).label("last_active_at"),
        )
        .select_from(Conversation)
        .outerjoin(Message, Message.conversation_id == Conversation.id)
        .filter(Conversation.seller_id == seller_pk)
        .one()
    )

    token_rows = (
        db.query(Message.metadata_)
        .join(Conversation, Message.conversation_id == Conversation.id)
        .filter(
            Conversation.seller_id == seller_pk,
            Message.role == MessageRole.ASSISTANT,
            Message.metadata_.isnot(None),
        )
        .all()
    )
    total_tokens = 0
    for (metadata,) in token_rows:
        if metadata:
            total_tokens += (metadata.get("input_tokens") or 0) + (
                metadata.get("output_tokens") or 0
            )

    return {
        "id": to_display_id("sellers", seller.id),
        "nickname": seller.nickname,
        "created_at": seller.created_at,
        "last_active_at": stats.last_active_at,
        "total_conversations": stats.total_conversations,
        "total_messages": stats.total_messages,
        "total_tokens": total_tokens,
    }
