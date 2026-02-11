# Backend

FastAPI 기반 백엔드 API

## 설치

```bash
# 1. 가상환경 생성
python -m venv venv

# 2. 가상환경 활성화
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt
```

## 실행

```bash
# 가상환경 활성화
source venv/bin/activate

# 서버 실행
uvicorn app.main:app --reload --port 8000
```
