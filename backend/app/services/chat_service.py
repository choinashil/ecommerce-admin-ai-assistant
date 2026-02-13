import json
import time
from collections.abc import AsyncGenerator

from openai import OpenAI
from sqlalchemy.orm import Session

from app.config import settings
from app.display_id import parse_pk, to_display_id
from app.models.conversation import Conversation
from app.models.message import Message, MessageRole
from app.tools.definitions import TOOL_DEFINITIONS
from app.tools.executor import execute_tool

client = OpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """당신은 이커머스 판매자를 돕는 AI 어시스턴트입니다. 한국어로 친근하게 답변하세요.

## 도구 사용 규칙
- 당신은 제공된 도구만 사용할 수 있습니다. 그 외 기능은 수행할 수 없습니다.
- 요청에 답하기 위해 도구가 도움이 된다면 적극적으로 활용하세요.
- 할 수 없는 작업은 솔직하게 안내하세요. 자연스러운 표현으로, 매번 다르게.
- 할 수 없는 작업을 우회 방법으로 제안하지 마세요.
- 도구를 호출하지 않았는데 작업을 수행한 것처럼 답변하지 마세요."""


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

    full_response = ""
    usage = None
    first_usage = None
    tool_calls_metadata = None
    start_time = time.time()

    try:
        # --- 1차 LLM 호출 (tools 포함) ---
        stream = client.chat.completions.create(
            model=settings.openai_model,
            messages=openai_messages,
            tools=TOOL_DEFINITIONS,
            stream=True,
            stream_options={"include_usage": True},
        )

        tool_calls_chunks = {}

        for chunk in stream:
            if chunk.usage:
                usage = chunk.usage

            if not chunk.choices:
                continue

            delta = chunk.choices[0].delta

            # Case A: 일반 content 스트리밍
            if delta.content:
                full_response += delta.content
                yield _sse_event("content", delta.content)

            # Case B: tool_call chunk 누적
            if delta.tool_calls:
                for tc in delta.tool_calls:
                    idx = tc.index
                    if idx not in tool_calls_chunks:
                        tool_calls_chunks[idx] = {"id": "", "name": "", "arguments": ""}
                    if tc.id:
                        tool_calls_chunks[idx]["id"] = tc.id
                    if tc.function and tc.function.name:
                        tool_calls_chunks[idx]["name"] += tc.function.name
                    if tc.function and tc.function.arguments:
                        tool_calls_chunks[idx]["arguments"] += tc.function.arguments

        # --- tool call이 있으면 실행 후 2차 LLM 호출 ---
        if tool_calls_chunks:
            tool_results = []
            tool_calls_metadata = []
            assistant_tool_calls = []

            for idx in sorted(tool_calls_chunks.keys()):
                tc_data = tool_calls_chunks[idx]
                arguments = json.loads(tc_data["arguments"])
                result = execute_tool(db, tc_data["name"], arguments)

                tool_results.append({
                    "tool_call_id": tc_data["id"],
                    "role": "tool",
                    "content": json.dumps(result, ensure_ascii=False),
                })

                assistant_tool_calls.append({
                    "id": tc_data["id"],
                    "type": "function",
                    "function": {
                        "name": tc_data["name"],
                        "arguments": tc_data["arguments"],
                    },
                })

                tool_calls_metadata.append({
                    "name": tc_data["name"],
                    "arguments": arguments,
                    "result": result,
                })

            for tc_meta in tool_calls_metadata:
                yield _sse_event("tool_result", tc_meta["name"])

            # 2차 요청 메시지 구성
            second_messages = openai_messages + [
                {"role": "assistant", "tool_calls": assistant_tool_calls},
                *tool_results,
            ]

            # 2차 LLM 호출 (tools 제외 — 재귀 방지)
            first_usage = usage
            usage = None
            second_stream = client.chat.completions.create(
                model=settings.openai_model,
                messages=second_messages,
                stream=True,
                stream_options={"include_usage": True},
            )

            for chunk in second_stream:
                if chunk.usage:
                    usage = chunk.usage
                if chunk.choices and chunk.choices[0].delta.content:
                    full_response += chunk.choices[0].delta.content
                    yield _sse_event("content", chunk.choices[0].delta.content)

        # 토큰 합산 (tool call 시 1차 + 2차)
        input_tokens = (usage.prompt_tokens if usage else 0) + (first_usage.prompt_tokens if first_usage else 0) if (usage or first_usage) else None
        output_tokens = (usage.completion_tokens if usage else 0) + (first_usage.completion_tokens if first_usage else 0) if (usage or first_usage) else None

        elapsed_ms = int((time.time() - start_time) * 1000)
        metadata = {
            "model": settings.openai_model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "response_time_ms": elapsed_ms,
            "system_prompt": SYSTEM_PROMPT,
            "error": None,
            "tool_calls": tool_calls_metadata,
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
            "tool_calls": tool_calls_metadata,
        }
        yield _sse_event("error", str(e))

    save_message(db, conversation.id, MessageRole.ASSISTANT, full_response, metadata)
    yield _sse_event("done", "")
