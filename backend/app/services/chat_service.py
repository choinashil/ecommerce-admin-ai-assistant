import json
from collections.abc import AsyncGenerator

from openai import OpenAI
from sqlalchemy.orm import Session

from app.config import settings
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = "당신은 이커머스 판매자를 돕는 AI 어시스턴트입니다. 한국어로 답변하세요."


def create_or_get_conversation(db: Session, conversation_id: int | None) -> Conversation:
    if conversation_id:
        conversation = db.get(Conversation, conversation_id)
        if conversation:
            return conversation

    conversation = Conversation()
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation


def save_message(db: Session, conversation_id: int, role: MessageRole, content: str) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
    )
    db.add(message)
    db.commit()
    return message


def get_conversation_history(db: Session, conversation_id: int) -> list[dict]:
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )
    return [{"role": m.role.value, "content": m.content} for m in messages]


def _sse_event(event_type: str, data: str) -> str:
    payload = json.dumps({"type": event_type, "data": data}, ensure_ascii=False)
    return f"data: {payload}\n\n"


async def stream_chat(db: Session, message: str, conversation_id: int | None) -> AsyncGenerator[str, None]:
    conversation = create_or_get_conversation(db, conversation_id)
    save_message(db, conversation.id, MessageRole.USER, message)

    yield _sse_event("conversation_id", str(conversation.id))

    history = get_conversation_history(db, conversation.id)
    openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    stream = client.chat.completions.create(
        model=settings.openai_model,
        messages=openai_messages,
        stream=True,
    )

    full_response = ""
    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta.content:
            full_response += delta.content
            yield _sse_event("content", delta.content)

    save_message(db, conversation.id, MessageRole.ASSISTANT, full_response)
    yield _sse_event("done", "")
