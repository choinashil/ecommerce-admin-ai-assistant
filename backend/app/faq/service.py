import logging
from dataclasses import dataclass, field

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.shared.display_id import to_display_id
from app.faq.model import FaqDocument
from app.shared.crawling import get_parser
from app.shared.crawling.crawler import crawl_site
from app.shared.embedding import embed_text

logger = logging.getLogger(__name__)

_SITE_NOISE = {"식스샵 프로 가이드", "(클릭) "}


def _remove_noise(content: str, noise: set[str]) -> str:
    """파싱된 콘텐츠에서 사이트 고유의 불필요한 텍스트를 제거한다."""
    lines = content.split("\n")
    for n in noise:
        lines = [line.replace(n, "") for line in lines]
    return "\n".join(line for line in lines if line.strip())


def crawl_and_ingest(
    db: Session, url: str, *, html: str | None = None
) -> FaqDocument:
    """URL에서 FAQ 문서를 크롤링하여 DB에 저장한다. 이미 존재하면 업데이트한다."""
    parser = get_parser(url)
    if html is None:
        html = parser.fetch_html(url)
    result = parser.parse(html)
    content = _remove_noise(result.content, _SITE_NOISE)

    embedding_text = f"{result.title}\n\n{content}"
    embedding_vector = embed_text(embedding_text)

    existing = db.execute(
        select(FaqDocument).where(FaqDocument.url == url)
    ).scalar_one_or_none()

    if existing:
        existing.title = result.title
        existing.content = content
        existing.breadcrumb = result.breadcrumb
        existing.embedding = embedding_vector
        db.commit()
        db.refresh(existing)
        return existing

    doc = FaqDocument(
        url=url,
        title=result.title,
        content=content,
        breadcrumb=result.breadcrumb,
        embedding=embedding_vector,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    return doc


@dataclass
class FaqCrawlResult:
    """FAQ 사이트 크롤링 결과 요약."""

    total_pages: int = 0
    new_pages: int = 0
    updated_pages: int = 0
    failed_urls: list[str] = field(default_factory=list)


def crawl_faq_site(
    db: Session,
    root_url: str,
    *,
    max_pages: int = 50,
    max_depth: int = 3,
    delay: float = 1.0,
) -> FaqCrawlResult:
    """루트 URL에서 FAQ 페이지를 재귀 크롤링하여 DB에 저장한다."""
    faq_result = FaqCrawlResult()

    def on_page(url: str, html: str):
        is_existing = db.execute(
            select(FaqDocument).where(FaqDocument.url == url)
        ).scalar_one_or_none()
        crawl_and_ingest(db, url, html=html)
        if is_existing:
            faq_result.updated_pages += 1
        else:
            faq_result.new_pages += 1

    crawl_result = crawl_site(
        root_url,
        on_page=on_page,
        max_pages=max_pages,
        max_depth=max_depth,
        delay=delay,
    )
    faq_result.total_pages = crawl_result.total_pages
    faq_result.failed_urls = crawl_result.failed_urls
    return faq_result


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
