import uuid
from unittest.mock import patch

import pytest

from app.chat.model import Conversation, Message, MessageRole
from app.seller.model import Seller
from app.seller.service import create_seller, get_seller_by_token, get_seller_detail, generate_nickname


class TestGenerateNickname:
    def test_format(self):
        nickname = generate_nickname()
        parts = nickname.split("-")
        assert len(parts) == 3
        assert parts[2].isdigit()

    def test_randomness(self):
        nicknames = {generate_nickname() for _ in range(10)}
        assert len(nicknames) > 1


class TestCreateSeller:
    def test_creates_with_token_and_nickname(self, db):
        seller = create_seller(db)
        assert seller.id is not None
        assert isinstance(seller.token, uuid.UUID)
        assert len(seller.nickname) > 0

    def test_unique_tokens(self, db):
        s1 = create_seller(db)
        s2 = create_seller(db)
        assert s1.token != s2.token

    def test_unique_nicknames(self, db):
        s1 = create_seller(db)
        s2 = create_seller(db)
        assert s1.nickname != s2.nickname

    def test_retries_on_duplicate_nickname(self, db):
        existing = create_seller(db)
        with patch(
            "app.seller.service.generate_nickname",
            side_effect=[existing.nickname, "새로운-닉네임-42"],
        ):
            seller = create_seller(db)
        assert seller.nickname == "새로운-닉네임-42"

    def test_raises_when_retries_exhausted(self, db):
        existing = create_seller(db)
        with patch(
            "app.seller.service.generate_nickname",
            return_value=existing.nickname,
        ):
            with pytest.raises(RuntimeError, match="닉네임 생성에 실패"):
                create_seller(db)


class TestGetSellerByToken:
    def test_found(self, db):
        seller = create_seller(db)
        found = get_seller_by_token(db, str(seller.token))
        assert found is not None
        assert found.id == seller.id

    def test_not_found(self, db):
        result = get_seller_by_token(db, str(uuid.uuid4()))
        assert result is None


def _create_conversation_with_messages(db, seller, metadata=None):
    """seller에 연결된 대화 + 메시지 생성 헬퍼."""
    conv = Conversation(seller_id=seller.id)
    db.add(conv)
    db.flush()

    user_msg = Message(
        conversation_id=conv.id,
        role=MessageRole.USER,
        content="테스트 질문",
    )
    db.add(user_msg)

    assistant_msg = Message(
        conversation_id=conv.id,
        role=MessageRole.ASSISTANT,
        content="테스트 답변",
        metadata_=metadata,
    )
    db.add(assistant_msg)
    db.flush()

    return conv


class TestGetSellerDetail:
    def test_returns_none_for_nonexistent_seller(self, db):
        result = get_seller_detail(db, 99999)
        assert result is None

    def test_returns_zero_stats_for_new_seller(self, db):
        seller = create_seller(db)
        result = get_seller_detail(db, seller.id)

        assert result["id"] == f"SLR-{seller.id}"
        assert result["nickname"] == seller.nickname
        assert result["total_conversations"] == 0
        assert result["total_messages"] == 0
        assert result["total_tokens"] == 0
        assert result["last_active_at"] is None

    def test_returns_detail_with_stats(self, db):
        seller = create_seller(db)
        metadata = {
            "model": "gpt-4o-mini",
            "input_tokens": 100,
            "output_tokens": 200,
            "response_time_ms": 1000,
            "system_prompt": "test",
            "error": None,
        }
        _create_conversation_with_messages(db, seller, metadata=metadata)
        _create_conversation_with_messages(db, seller, metadata=metadata)

        result = get_seller_detail(db, seller.id)

        assert result["total_conversations"] == 2
        assert result["total_messages"] == 4
        assert result["total_tokens"] == 600
        assert result["last_active_at"] is not None

    def test_last_active_at_is_latest_conversation(self, db):
        seller = create_seller(db)
        _create_conversation_with_messages(db, seller)
        conv2 = _create_conversation_with_messages(db, seller)

        result = get_seller_detail(db, seller.id)

        assert result["last_active_at"] == conv2.updated_at
