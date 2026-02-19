from sqlalchemy.orm import Session

from app.shared.display_id import to_display_id
from app.chat.model import Conversation, Message, MessageRole
from app.chat.schema import ConversationSummary, MessageDetail, MessageMetadata


def get_conversations(db: Session) -> list[ConversationSummary]:
    conversations = (
        db.query(Conversation).order_by(Conversation.created_at.desc()).all()
    )

    results = []
    for conv in conversations:
        messages = (
            db.query(Message)
            .filter(Message.conversation_id == conv.id)
            .order_by(Message.created_at)
            .all()
        )

        first_user_message = next(
            (m for m in messages if m.role == MessageRole.USER), None
        )
        first_message = first_user_message.content[:50] if first_user_message else ""

        total_tokens = 0
        for m in messages:
            if m.metadata_ and m.role == MessageRole.ASSISTANT:
                input_t = m.metadata_.get("input_tokens") or 0
                output_t = m.metadata_.get("output_tokens") or 0
                total_tokens += input_t + output_t

        results.append(
            ConversationSummary(
                id=to_display_id("conversations", conv.id),
                first_message=first_message,
                message_count=len(messages),
                total_tokens=total_tokens,
                created_at=conv.created_at,
            )
        )

    return results


def get_messages(db: Session, conversation_id: int) -> list[MessageDetail]:
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )

    results = []
    for m in messages:
        metadata = None
        if m.metadata_ and m.role == MessageRole.ASSISTANT:
            metadata = MessageMetadata(**m.metadata_)

        results.append(
            MessageDetail(
                id=to_display_id("messages", m.id),
                role=m.role.value,
                content=m.content,
                created_at=m.created_at,
                metadata=metadata,
            )
        )

    return results
