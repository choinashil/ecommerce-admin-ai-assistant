from openai import OpenAI

from app.shared.config import settings

client = OpenAI(api_key=settings.openai_api_key)


def embed_text(text: str) -> list[float]:
    """텍스트를 임베딩 벡터로 변환한다."""
    response = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=text,
    )
    return response.data[0].embedding


def embed_texts(texts: list[str]) -> list[list[float]]:
    """여러 텍스트를 배치로 임베딩한다."""
    response = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=texts,
    )
    return [item.embedding for item in response.data]
