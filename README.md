# SixPro AI Assistant

[Demo](https://sixpro-ai-assistant.vercel.app) | [Blog](https://nashu.vercel.app/posts/sixpro-ai-assistant/)

[식스샵 프로](https://www.sixshop.com/)를 기반으로 만든 이커머스 어드민 AI 어시스턴트입니다. <br/>
Function Calling, RAG, SSE 스트리밍을 활용하여 채팅으로 상품 관리와 CS 응대를 할 수 있습니다.

https://github.com/user-attachments/assets/demo.mp4

## 주요 기능

### Function Calling 기반 상품 관리

Agent Loop(최대 5회)으로 상품 CRUD와 멀티쿼리를 처리합니다.

### RAG 파이프라인

가이드 문서 231페이지를 크롤링 → 임베딩하여 pgvector에 저장하고, LLM이 필요시 검색합니다.

### SSE 스트리밍

LLM 응답과 Function Calling 진행 상태를 실시간으로 스트리밍합니다.

### 채팅 UX

React Virtuoso 가상화, 질문 상단 고정, AI 채팅에 맞는 스크롤 패턴을 적용했습니다.

### LLM 로그

대화별 시스템 프롬프트, 토큰 사용량, 툴 호출 내역을 확인할 수 있는 관리자 페이지입니다.

### 온보딩 가이드 / 추천 프롬프트

순차적 툴팁으로 핵심 기능을 안내하고, 추천 프롬프트로 진입 허들을 낮췄습니다.

## 기술 스택

### Backend

- **FastAPI** (Python)
- **PostgreSQL + pgvector**
- **OpenAI API** (gpt-4o-mini, text-embedding-3-small)
- **SQLAlchemy**

### Frontend

- **React + TypeScript + Vite**
- **TanStack Query**
- **shadcn/ui + Tailwind CSS**
- **FSD (Feature-Sliced Design)**

### 인프라

- **Railway** (BE)
- **Vercel** (FE)

## 아키텍처

```
React (FE)
    │
    │  SSE
    ▼
FastAPI (BE)
    │
    ▼
OpenAI API ──── Agent Loop (최대 5회)
    │
    ├── search_guide    → RAG 검색
    ├── create_product
    ├── list_products
    ├── update_product
    └── delete_product
```

## 로컬 실행

### 사전 준비

- Python 3.11+
- Node.js 18+ / pnpm
- Docker

### 1. DB

```bash
docker-compose up -d
```

### 2. BE

```bash
cd backend

python -m venv venv
source venv/bin/activate

pip install -r requirements-dev.txt

cp .env.example .env
# .env에 환경변수 입력

uvicorn app.main:app --reload --port 8000
```

### 3. FE

```bash
cd frontend

pnpm install

cp .env.example .env
# .env에 환경변수 입력

pnpm dev
```
