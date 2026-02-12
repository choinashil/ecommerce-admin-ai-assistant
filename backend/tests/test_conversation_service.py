from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.services.conversation_service import get_conversations, get_messages


def _create_conversation_with_messages(db, metadata=None):
    """테스트용 대화 + 메시지 생성 헬퍼."""
    conv = Conversation()
    db.add(conv)
    db.flush()

    user_msg = Message(
        conversation_id=conv.id,
        role=MessageRole.USER,
        content="재고 관리 방법 알려줘",
    )
    db.add(user_msg)

    assistant_msg = Message(
        conversation_id=conv.id,
        role=MessageRole.ASSISTANT,
        content="재고 관리는 크게 세 가지 방법이 있습니다.",
        metadata_=metadata,
    )
    db.add(assistant_msg)
    db.flush()

    return conv


class TestGetConversations:
    def test_returns_conversations(self, db):
        _create_conversation_with_messages(db)

        result = get_conversations(db)

        assert len(result) == 1
        assert result[0].id.startswith("CON-")
        assert result[0].message_count == 2

    def test_first_message_from_user(self, db):
        _create_conversation_with_messages(db)

        result = get_conversations(db)

        assert result[0].first_message == "재고 관리 방법 알려줘"

    def test_total_tokens_from_metadata(self, db):
        metadata = {
            "model": "gpt-4o-mini",
            "input_tokens": 100,
            "output_tokens": 200,
            "response_time_ms": 1500,
            "system_prompt": "test",
            "error": None,
        }
        _create_conversation_with_messages(db, metadata=metadata)

        result = get_conversations(db)

        assert result[0].total_tokens == 300

    def test_total_tokens_zero_without_metadata(self, db):
        _create_conversation_with_messages(db, metadata=None)

        result = get_conversations(db)

        assert result[0].total_tokens == 0

    def test_ordered_by_latest_first(self, db):
        _create_conversation_with_messages(db)
        _create_conversation_with_messages(db)

        result = get_conversations(db)

        assert len(result) == 2
        assert result[0].created_at >= result[1].created_at

    def test_empty_list(self, db):
        result = get_conversations(db)

        assert result == []


class TestGetMessages:
    def test_returns_messages(self, db):
        conv = _create_conversation_with_messages(db)

        result = get_messages(db, conv.id)

        assert len(result) == 2
        assert result[0].role == "user"
        assert result[1].role == "assistant"

    def test_message_ids_have_prefix(self, db):
        conv = _create_conversation_with_messages(db)

        result = get_messages(db, conv.id)

        assert all(m.id.startswith("MSG-") for m in result)

    def test_assistant_message_has_metadata(self, db):
        metadata = {
            "model": "gpt-4o-mini",
            "input_tokens": 50,
            "output_tokens": 150,
            "response_time_ms": 800,
            "system_prompt": "테스트 프롬프트",
            "error": None,
        }
        conv = _create_conversation_with_messages(db, metadata=metadata)

        result = get_messages(db, conv.id)
        assistant = result[1]

        assert assistant.metadata is not None
        assert assistant.metadata.model == "gpt-4o-mini"
        assert assistant.metadata.input_tokens == 50
        assert assistant.metadata.output_tokens == 150
        assert assistant.metadata.response_time_ms == 800

    def test_user_message_has_no_metadata(self, db):
        conv = _create_conversation_with_messages(db)

        result = get_messages(db, conv.id)
        user_msg = result[0]

        assert user_msg.metadata is None

    def test_ordered_by_created_at(self, db):
        conv = _create_conversation_with_messages(db)

        result = get_messages(db, conv.id)

        assert result[0].created_at <= result[1].created_at
