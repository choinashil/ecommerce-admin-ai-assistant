import json
import time
from collections.abc import AsyncGenerator

from openai import OpenAI
from sqlalchemy.orm import Session

from app.config import settings
from app.display_id import parse_pk, to_display_id
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


def save_message(
    db: Session,
    conversation_id: int,
    role: MessageRole,
    content: str,
    metadata: dict | None = None,
) -> Message:
    message = Message(
        conversation_id=conversation_id,
        role=role,
        content=content,
        metadata_=metadata,
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


async def stream_chat(db: Session, message: str, conversation_display_id: str | None) -> AsyncGenerator[str, None]:
    pk = parse_pk(conversation_display_id, "conversations") if conversation_display_id else None
    conversation = create_or_get_conversation(db, pk)
    save_message(db, conversation.id, MessageRole.USER, message)

    yield _sse_event("conversation_id", to_display_id("conversations", conversation.id))

    history = get_conversation_history(db, conversation.id)
    openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    stream = client.chat.completions.create(
        model=settings.openai_model,
        messages=openai_messages,
        stream=True,
        stream_options={"include_usage": True},
    )

    full_response = ""
    usage = None
    start_time = time.time()

    try:
        for chunk in stream:
            if chunk.usage:
                usage = chunk.usage
            if chunk.choices and chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
                yield _sse_event("content", chunk.choices[0].delta.content)

        elapsed_ms = int((time.time() - start_time) * 1000)
        metadata = {
            "model": settings.openai_model,
            "input_tokens": usage.prompt_tokens if usage else None,
            "output_tokens": usage.completion_tokens if usage else None,
            "response_time_ms": elapsed_ms,
            "system_prompt": SYSTEM_PROMPT,
            "error": None,
        }
    except Exception as e:
        elapsed_ms = int((time.time() - start_time) * 1000)
        metadata = {
            "model": settings.openai_model,
            "input_tokens": None,
            "output_tokens": None,
            "response_time_ms": elapsed_ms,
            "system_prompt": SYSTEM_PROMPT,
            "error": str(e),
        }
        yield _sse_event("error", str(e))

    save_message(db, conversation.id, MessageRole.ASSISTANT, full_response, metadata)
    yield _sse_event("done", "")
