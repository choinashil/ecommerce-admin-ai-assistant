from sqlalchemy import select
from sqlalchemy.orm import Session

from app.display_id import to_display_id
from app.models.faq_document import FaqDocument
from app.parsers import get_parser
from app.services.embedding_service import embed_text


def crawl_and_ingest(db: Session, url: str) -> FaqDocument:
    """URL에서 FAQ 문서를 크롤링하여 DB에 저장한다. 이미 존재하면 업데이트한다."""
    parser = get_parser(url)
    html = parser.fetch_html(url)
    result = parser.parse(html)

    embedding_text = f"{result.title}\n\n{result.content}"
    embedding_vector = embed_text(embedding_text)

    existing = db.execute(
        select(FaqDocument).where(FaqDocument.url == url)
    ).scalar_one_or_none()

    if existing:
        existing.title = result.title
        existing.content = result.content
        existing.breadcrumb = result.breadcrumb
        existing.embedding = embedding_vector
        db.commit()
        db.refresh(existing)
        return existing

    doc = FaqDocument(
        url=url,
        title=result.title,
        content=result.content,
        breadcrumb=result.breadcrumb,
        embedding=embedding_vector,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


def search_faq(db: Session, query: str, top_k: int = 3) -> list[dict]:
    """사용자 질문과 유사한 FAQ 문서를 검색한다."""
    query_vector = embed_text(query)

    results = db.execute(
        select(
            FaqDocument,
            FaqDocument.embedding.cosine_distance(query_vector).label("distance"),
        )
        .order_by("distance")
        .limit(top_k)
    ).all()

    return [
        {
            "id": to_display_id("faq_documents", doc.id),
            "title": doc.title,
            "content": doc.content,
            "url": doc.url,
            "breadcrumb": doc.breadcrumb,
            "similarity": round(1 - distance, 4),
        }
        for doc, distance in results
    ]
