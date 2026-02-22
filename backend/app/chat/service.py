import json
import time
from collections.abc import AsyncGenerator

from openai import AsyncOpenAI
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.shared.config import settings
from app.shared.display_id import parse_pk, to_display_id
from app.chat.model import Conversation, Message, MessageRole
from app.chat.tools.definitions import TOOL_DEFINITIONS
from app.chat.tools.executor import ToolContext, execute_tool

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = """당신의 이름은 '식식이'이고, '식스샵 프로' 쇼핑몰 솔루션의 판매자를 돕는 AI 어시스턴트입니다.

## 말투
- 해요체를 기본으로 사용하세요. (ex. "~이에요", "~할 수 있어요", "~해보세요")
- 합니다체도 자연스러우면 섞어 사용해도 돼요. (ex. "~입니다", "~드릴게요")
- 반말 금지. (ex. "~야", "~해", "~줄게", "~물어봐" 금지)

## 답변 범위

**답변 가능:**
- 식스샵 프로의 기능 사용법, 설정, 운영 방법
- 상품 관리, 주문 관리, 고객 관리, 디자인 편집
- 통계/리포트, 마케팅, 연동 서비스 설정
- 식스샵 프로 기능 구현을 위한 CSS/HTML/JS 커스터마이징
- 외부 서비스(구글, 카카오, 네이버 등)의 식스샵 프로 연동·설정

**답변 불가:**
- 식스샵 프로와 무관한 순수 일반 상식·코딩(알고리즘, 프로그래밍 학습 등)
- 세금·회계·사업자등록 등 정부 서비스 영역
- 일반 택배사 추천·계약 조건 등 플랫폼과 무관한 물류 조언

범위 밖 질문에는 대화 흐름에 맞게 짧고 자연스럽게 거절하세요. 같은 말을 반복하지 마세요.

## 도구 사용
- 제공된 도구만 사용할 수 있어요. 도구로 할 수 없는 작업은 솔직하게 안내하세요. (자연스러운 표현으로, 매번 다르게)
- 도구를 호출하지 않은 작업을 수행한 것처럼 답변하지 마세요.
- 할 수 없는 작업의 우회 방법을 제안하지 마세요.
- 상품명으로 해석될 수 있는 질문은 거절하지 말고, list_products로 먼저 조회하세요.

**search_guide:**
- 쇼핑몰 기능, 설정, 용어 관련 질문은 search_guide로 먼저 검색하세요. 확실히 범위 밖이 아니라면 검색 결과가 없을 때만 거절하세요.
- 검색 결과에 포함된 내용만으로 답변하고, 출처 URL을 함께 안내하세요.
- 검색 결과에 없는 내용은 절대 추측하거나 지어내지 마세요. "보통", "일반적으로" 같은 표현으로 다른 정보를 덧붙이지 마세요.
- 답변할 수 없으면 식스샵 프로 가이드(https://help.pro.sixshop.com/)나 채널톡으로 문의하라고 안내하세요."""


def create_or_get_conversation(
    db: Session, conversation_id: int | None, seller_id: int | None = None
) -> Conversation:
    if conversation_id:
        conversation = db.get(Conversation, conversation_id)
        if conversation:
            return conversation

    conversation = Conversation(seller_id=seller_id)
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

    conversation = db.get(Conversation, conversation_id)
    if conversation:
        conversation.updated_at = func.now()

    db.commit()
    return message


def get_conversation_history(db: Session, conversation_id: int) -> list[dict]:
    messages = (
        db.query(Message)
        .filter(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
        .all()
    )
    return [
        {"role": m.role.value, "content": m.content}
        for m in messages
        if not (m.metadata_ and m.metadata_.get("aborted"))
    ]


def _sse_event(event_type: str, data: str) -> str:
    payload = json.dumps({"type": event_type, "data": data}, ensure_ascii=False)
    return f"data: {payload}\n\n"


async def stream_chat(
    db: Session, message: str, conversation_display_id: str | None, seller_id: int | None = None
) -> AsyncGenerator[str, None]:
    pk = parse_pk(conversation_display_id, "conversations") if conversation_display_id else None
    conversation = create_or_get_conversation(db, pk, seller_id=seller_id)
    save_message(db, conversation.id, MessageRole.USER, message)

    yield _sse_event("conversation_id", to_display_id("conversations", conversation.id))

    history = get_conversation_history(db, conversation.id)
    openai_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    full_response = ""
    usage = None
    first_usage = None
    tool_calls_metadata = None
    start_time = time.time()
    is_done = False

    try:
        # --- 1차 LLM 호출 (tools 포함) ---
        stream = await client.chat.completions.create(
            model=settings.openai_model,
            messages=openai_messages,
            tools=TOOL_DEFINITIONS,
            stream=True,
            stream_options={"include_usage": True},
        )

        tool_calls_chunks = {}

        async for chunk in stream:
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

                yield _sse_event("tool_call", tc_data["name"])
                ctx = ToolContext(db=db, seller_id=seller_id)
                result = execute_tool(ctx, tc_data["name"], arguments)
                yield _sse_event("tool_result", tc_data["name"])

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

            # 2차 요청 메시지 구성
            second_messages = openai_messages + [
                {"role": "assistant", "tool_calls": assistant_tool_calls},
                *tool_results,
            ]

            # 2차 LLM 호출 (tools 제외 — 재귀 방지)
            first_usage = usage
            usage = None
            second_stream = await client.chat.completions.create(
                model=settings.openai_model,
                messages=second_messages,
                stream=True,
                stream_options={"include_usage": True},
            )

            async for chunk in second_stream:
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
        save_message(db, conversation.id, MessageRole.ASSISTANT, full_response, metadata)
        is_done = True
        yield _sse_event("done", "")
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
        save_message(db, conversation.id, MessageRole.ASSISTANT, full_response, metadata)
        is_done = True
        yield _sse_event("error", str(e))
    finally:
        if not is_done:
            elapsed_ms = int((time.time() - start_time) * 1000)
            metadata = {
                "model": settings.openai_model,
                "input_tokens": None,
                "output_tokens": None,
                "response_time_ms": elapsed_ms,
                "system_prompt": SYSTEM_PROMPT,
                "error": None,
                "aborted": True,
                "tool_calls": tool_calls_metadata,
            }
            save_message(db, conversation.id, MessageRole.ASSISTANT, full_response, metadata)
