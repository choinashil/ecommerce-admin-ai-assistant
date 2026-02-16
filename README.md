# E-commerce Admin AI Assistant

판매자 어드민을 위한 AI 어시스턴트 챗봇

## 주요 기능

- **가이드 자동 응답**: RAG 기반으로 CS 가이드 문서 검색 및 답변
- **업무 자동화**: Function Calling으로 상품 등록, 주문 조회 등 실행
- **AI 파이프라인 모니터**: 대화별 검색 결과, 토큰 사용량, 응답 시간 시각화

## 기술 스택

### Backend

- FastAPI (Python)
- PostgreSQL
- Pinecone
- OpenAI API

### Frontend

- React + Vite
- TypeScript
- SSE (Server-Sent Events)
