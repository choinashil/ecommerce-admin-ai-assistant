from unittest.mock import MagicMock, patch

from app.shared.crawling.parsers.base import ParseResult
from app.shared.crawling.crawler import CrawlResult
from app.faq.model import FaqDocument
from app.faq.service import crawl_faq_site, search_faq

_HTML = "<html><body><h1>제목</h1><p>본문</p></body></html>"


def _make_parse_result(title: str = "제목", content: str = "본문") -> ParseResult:
    return ParseResult(title=title, content=content, breadcrumb=None)


class TestCrawlFaqSite:
    """crawl_faq_site의 FAQ 도메인 로직(new/updated 추적)을 테스트한다."""

    @patch("app.faq.service.crawl_site")
    @patch("app.faq.service.embed_text", return_value=[0.0] * 1536)
    @patch("app.faq.service.get_parser")
    def test_tracks_new_pages(
        self, mock_get_parser, mock_embed, mock_crawl_site, db
    ):
        mock_parser = MagicMock()
        mock_parser.parse.return_value = _make_parse_result()
        mock_get_parser.return_value = mock_parser

        def fake_crawl(root_url, *, on_page, **kwargs):
            on_page("https://example.com/page1", _HTML)
            return CrawlResult(total_pages=1)

        mock_crawl_site.side_effect = fake_crawl

        result = crawl_faq_site(db, "https://example.com/docs", delay=0)

        assert result.total_pages == 1
        assert result.new_pages == 1
        assert result.updated_pages == 0

    @patch("app.faq.service.crawl_site")
    @patch("app.faq.service.embed_text", return_value=[0.0] * 1536)
    @patch("app.faq.service.get_parser")
    def test_tracks_updated_pages(
        self, mock_get_parser, mock_embed, mock_crawl_site, db
    ):
        mock_parser = MagicMock()
        mock_parser.parse.return_value = _make_parse_result()
        mock_get_parser.return_value = mock_parser

        def fake_crawl(root_url, *, on_page, **kwargs):
            on_page("https://example.com/page1", _HTML)
            return CrawlResult(total_pages=1)

        # 첫 번째: 신규 저장
        mock_crawl_site.side_effect = fake_crawl
        crawl_faq_site(db, "https://example.com/docs", delay=0)

        # 두 번째: 업데이트
        mock_crawl_site.side_effect = fake_crawl
        result = crawl_faq_site(db, "https://example.com/docs", delay=0)

        assert result.updated_pages == 1
        assert result.new_pages == 0

    @patch("app.faq.service.crawl_site")
    @patch("app.faq.service.embed_text", return_value=[0.0] * 1536)
    @patch("app.faq.service.get_parser")
    def test_propagates_failed_urls(
        self, mock_get_parser, mock_embed, mock_crawl_site, db
    ):
        mock_get_parser.return_value = MagicMock()

        def fake_crawl(root_url, *, on_page, **kwargs):
            return CrawlResult(
                total_pages=0, failed_urls=["https://example.com/fail"]
            )

        mock_crawl_site.side_effect = fake_crawl

        result = crawl_faq_site(db, "https://example.com/docs", delay=0)

        assert result.total_pages == 0
        assert result.failed_urls == ["https://example.com/fail"]


def _make_embedding(index: int) -> list[float]:
    """1536차원 단위 벡터를 생성한다. index 위치만 1.0, 나머지 0.0."""
    vec = [0.0] * 1536
    vec[index] = 1.0
    return vec


class TestSearchFaq:
    """search_faq의 유사도 검색 동작을 테스트한다."""

    def _insert_doc(self, db, *, url: str, title: str, content: str, embedding: list[float]):
        doc = FaqDocument(
            url=url, title=title, content=content, embedding=embedding,
        )
        db.add(doc)
        db.flush()
        return doc

    @patch("app.faq.service.embed_text")
    def test_returns_documents_ordered_by_similarity(self, mock_embed, db):
        self._insert_doc(db, url="https://ex.com/a", title="A", content="내용A", embedding=_make_embedding(0))
        self._insert_doc(db, url="https://ex.com/b", title="B", content="내용B", embedding=_make_embedding(1))

        mock_embed.return_value = _make_embedding(0)

        results = search_faq(db, "질문")

        assert len(results) == 2
        assert results[0]["title"] == "A"
        assert results[0]["similarity"] > results[1]["similarity"]

    @patch("app.faq.service.embed_text")
    def test_respects_top_k(self, mock_embed, db):
        for i in range(3):
            self._insert_doc(
                db, url=f"https://ex.com/{i}", title=f"Doc{i}",
                content=f"내용{i}", embedding=_make_embedding(i),
            )

        mock_embed.return_value = _make_embedding(0)

        results = search_faq(db, "질문", top_k=1)

        assert len(results) == 1

    @patch("app.faq.service.embed_text")
    def test_returns_correct_format(self, mock_embed, db):
        self._insert_doc(
            db, url="https://ex.com/page", title="FAQ 제목",
            content="FAQ 내용", embedding=_make_embedding(0),
        )

        mock_embed.return_value = _make_embedding(0)

        results = search_faq(db, "질문")

        assert len(results) == 1
        doc = results[0]
        assert doc["id"].startswith("FAQ-")
        assert doc["title"] == "FAQ 제목"
        assert doc["content"] == "FAQ 내용"
        assert doc["url"] == "https://ex.com/page"
        assert doc["similarity"] == 1.0
