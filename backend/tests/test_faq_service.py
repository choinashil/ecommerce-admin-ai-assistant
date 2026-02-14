from unittest.mock import MagicMock, patch

from app.parsers.base import ParseResult
from app.services.crawler import CrawlResult
from app.services.faq_service import crawl_faq_site

_HTML = "<html><body><h1>제목</h1><p>본문</p></body></html>"


def _make_parse_result(title: str = "제목", content: str = "본문") -> ParseResult:
    return ParseResult(title=title, content=content, breadcrumb=None)


class TestCrawlFaqSite:
    """crawl_faq_site의 FAQ 도메인 로직(new/updated 추적)을 테스트한다."""

    @patch("app.services.faq_service.crawl_site")
    @patch("app.services.faq_service.embed_text", return_value=[0.0] * 1536)
    @patch("app.services.faq_service.get_parser")
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

    @patch("app.services.faq_service.crawl_site")
    @patch("app.services.faq_service.embed_text", return_value=[0.0] * 1536)
    @patch("app.services.faq_service.get_parser")
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

    @patch("app.services.faq_service.crawl_site")
    @patch("app.services.faq_service.embed_text", return_value=[0.0] * 1536)
    @patch("app.services.faq_service.get_parser")
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
