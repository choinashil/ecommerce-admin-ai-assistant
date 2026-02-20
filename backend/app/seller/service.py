import random

from sqlalchemy.orm import Session

from app.seller.model import Seller

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
