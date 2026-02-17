from unittest.mock import MagicMock, patch

from app.shared.crawling.crawler import crawl_site


def _make_html_with_links(links: list[str]) -> str:
    """테스트용 HTML을 생성한다. 링크 목록을 a 태그로 삽입."""
    anchors = "".join(f'<a href="{link}">link</a>' for link in links)
    return f"<html><body><h1>제목</h1><p>본문</p>{anchors}</body></html>"


_HTML = _make_html_with_links([])


class TestCrawlSite:
    """crawl_site의 BFS 오케스트레이션을 테스트한다."""

    @patch("app.shared.crawling.crawler.get_parser")
    def test_crawls_root_page(self, mock_get_parser):
        mock_parser = MagicMock()
        mock_parser.fetch_html.side_effect = lambda url: (_HTML, url)
        mock_parser.extract_links.return_value = []
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        result = crawl_site(
            "https://example.com/docs", on_page=on_page, delay=0
        )

        assert result.total_pages == 1
        on_page.assert_called_once()

    @patch("app.shared.crawling.crawler.get_parser")
    def test_follows_internal_links(self, mock_get_parser):
        mock_parser = MagicMock()
        mock_parser.fetch_html.side_effect = lambda url: (_HTML, url)
        mock_parser.extract_links.side_effect = [
            [
                "https://example.com/docs/page1",
                "https://example.com/docs/page2",
            ],
            [],
            [],
        ]
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        result = crawl_site(
            "https://example.com/docs", on_page=on_page, delay=0
        )

        assert result.total_pages == 3
        assert on_page.call_count == 3

    @patch("app.shared.crawling.crawler.get_parser")
    def test_respects_max_pages(self, mock_get_parser):
        mock_parser = MagicMock()
        mock_parser.fetch_html.side_effect = lambda url: (_HTML, url)
        mock_parser.extract_links.side_effect = [
            ["https://example.com/docs/p1", "https://example.com/docs/p2"],
            ["https://example.com/docs/p3", "https://example.com/docs/p4"],
            [],
        ]
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        result = crawl_site(
            "https://example.com/docs", on_page=on_page, max_pages=3, delay=0
        )

        assert result.total_pages == 3

    @patch("app.shared.crawling.crawler.get_parser")
    def test_respects_max_depth(self, mock_get_parser):
        mock_parser = MagicMock()
        mock_parser.fetch_html.side_effect = lambda url: (_HTML, url)
        mock_parser.extract_links.side_effect = [
            ["https://example.com/docs/d1"],
            ["https://example.com/docs/d2"],
            [],
        ]
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        result = crawl_site(
            "https://example.com/docs", on_page=on_page, max_depth=1, delay=0
        )

        assert result.total_pages == 2

    @patch("app.shared.crawling.crawler.get_parser")
    def test_skips_visited_urls(self, mock_get_parser):
        mock_parser = MagicMock()
        mock_parser.fetch_html.side_effect = lambda url: (_HTML, url)
        mock_parser.extract_links.side_effect = [
            ["https://example.com/docs/page1"],
            ["https://example.com/docs"],
            [],
        ]
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        result = crawl_site(
            "https://example.com/docs", on_page=on_page, delay=0
        )

        assert result.total_pages == 2

    @patch("app.shared.crawling.crawler.get_parser")
    def test_follows_all_same_domain_links(self, mock_get_parser):
        mock_parser = MagicMock()
        mock_parser.fetch_html.side_effect = lambda url: (_HTML, url)
        mock_parser.extract_links.side_effect = [
            [
                "https://example.com/docs/page1",
                "https://example.com/other/page",
            ],
            [],
            [],
        ]
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        result = crawl_site(
            "https://example.com/docs", on_page=on_page, delay=0
        )

        assert result.total_pages == 3

    @patch("app.shared.crawling.crawler.get_parser")
    def test_records_failed_urls(self, mock_get_parser):
        mock_parser = MagicMock()
        mock_parser.fetch_html.side_effect = Exception("네트워크 오류")
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        result = crawl_site(
            "https://example.com/docs", on_page=on_page, delay=0
        )

        assert result.total_pages == 0
        assert len(result.failed_urls) == 1
        on_page.assert_not_called()

    @patch("app.shared.crawling.crawler.get_parser")
    def test_url_filter_excludes_urls(self, mock_get_parser):
        """url_filter가 False를 반환하는 URL은 큐에 추가되지 않는다."""
        mock_parser = MagicMock()
        mock_parser.fetch_html.side_effect = lambda url: (_HTML, url)
        mock_parser.extract_links.side_effect = [
            [
                "https://example.com/docs/page1",
                "https://example.com/docs/excluded",
            ],
            [],
        ]
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        result = crawl_site(
            "https://example.com/docs",
            on_page=on_page,
            url_filter=lambda url: "excluded" not in url,
            delay=0,
        )

        assert result.total_pages == 2
        visited_urls = [call.args[0] for call in on_page.call_args_list]
        assert not any("excluded" in url for url in visited_urls)

    @patch("app.shared.crawling.crawler.get_parser")
    def test_url_filter_none_allows_all(self, mock_get_parser):
        """url_filter=None이면 모든 URL을 허용한다."""
        mock_parser = MagicMock()
        mock_parser.fetch_html.side_effect = lambda url: (_HTML, url)
        mock_parser.extract_links.side_effect = [
            ["https://example.com/docs/page1"],
            [],
        ]
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        result = crawl_site(
            "https://example.com/docs",
            on_page=on_page,
            url_filter=None,
            delay=0,
        )

        assert result.total_pages == 2

    @patch("app.shared.crawling.crawler.get_parser")
    def test_url_filter_applies_after_redirect(self, mock_get_parser):
        """UUID URL이 제외 대상으로 리다이렉트되면 크롤링하지 않는다."""
        mock_parser = MagicMock()
        mock_parser.extract_links.side_effect = [
            ["https://example.com/uuid-123"],
            [],
        ]
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        def fake_fetch(url):
            if "uuid" in url:
                return (_HTML, "https://example.com/excluded")
            return (_HTML, url)

        mock_parser.fetch_html.side_effect = fake_fetch

        result = crawl_site(
            "https://example.com/docs",
            on_page=on_page,
            url_filter=lambda url: "excluded" not in url,
            delay=0,
        )

        assert result.total_pages == 1
        visited_urls = [call.args[0] for call in on_page.call_args_list]
        assert not any("excluded" in url for url in visited_urls)

    @patch("app.shared.crawling.crawler.get_parser")
    def test_deduplicates_redirected_urls(self, mock_get_parser):
        """UUID URL이 이미 방문한 slug URL로 리다이렉트되면 건너뛴다."""
        mock_parser = MagicMock()
        mock_parser.extract_links.side_effect = [
            ["https://example.com/uuid-123"],
            [],
        ]
        mock_get_parser.return_value = mock_parser
        on_page = MagicMock()

        def fake_fetch(url):
            if "uuid" in url:
                return (_HTML, "https://example.com/docs")
            return (_HTML, url)

        mock_parser.fetch_html.side_effect = fake_fetch

        result = crawl_site(
            "https://example.com/docs", on_page=on_page, delay=0
        )

        assert result.total_pages == 1
