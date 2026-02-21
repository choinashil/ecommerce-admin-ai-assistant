# [SixPro AI Assistant](https://sixpro-ai-assistant.vercel.app)

자연어로 상품을 관리하고 가이드를 검색하는 이커머스 어드민 AI 어시스턴트

## 주요 기능

- **가이드 검색 답변**: [식스샵 프로 가이드 문서](https://help.pro.sixshop.com/)를 RAG로 검색해 질문에 답변
- **자연어 업무 처리**: Function Calling으로 상품 관리 (CRUD)
- **실시간 스트리밍**: SSE 기반으로 LLM 응답을 스트리밍
- **AI 파이프라인 로그**: 대화별 tool 호출 내역, 검색 결과 시각화

## 기술 스택

### Backend

- **FastAPI** (Python)
- **PostgreSQL + pgvector** (RAG)
- **OpenAI API**
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
사용자 입력
    │
    ▼
FastAPI (SSE 스트리밍)
    │
    ▼
OpenAI Function Calling
    │
    ├── search_guide  →  pgvector 유사도 검색  →  컨텍스트로 주입
    ├── create_product
    └── list_products
```

## 로컬 실행

### 사전 준비

- Python 3.11+
- Node.js 18+ / pnpm
- Docker

### 1. DB 실행

```bash
docker-compose up -d
```

### 2. Backend

```bash
cd backend

python -m venv venv
source venv/bin/activate

pip install -r requirements-dev.txt

cp .env.example .env
# .env에 환경변수 입력

uvicorn app.main:app --reload --port 8000
```

### 3. Frontend

```bash
cd frontend

pnpm install

cp .env.example .env
# .env에 환경변수 입력

pnpm dev
```
