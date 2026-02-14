from app.shared.crawling import get_parser
from app.shared.crawling.parsers.base import normalize_url
from app.shared.crawling.parsers.oopy import OopyParser


def _make_html(body_content: str) -> str:
    return f"<html><body>{body_content}</body></html>"


class TestNormalizeUrl:
    def test_removes_fragment(self):
        assert normalize_url("https://example.com/page#section") == "https://example.com/page"

    def test_removes_query(self):
        assert normalize_url("https://example.com/page?ref=nav") == "https://example.com/page"

    def test_removes_trailing_slash(self):
        assert normalize_url("https://example.com/page/") == "https://example.com/page"


class TestExtractLinks:
    """BaseParser.extract_links의 공통 동작을 테스트한다."""

    _BASE_URL = "https://help.pro.sixshop.com/customers"

    def test_extracts_internal_links(self):
        html = _make_html(
            '<a href="/customers/grade">등급</a>'
            '<a href="/products/settings">상품</a>'
        )
        parser = OopyParser()
        links = parser.extract_links(html, self._BASE_URL)
        assert "https://help.pro.sixshop.com/customers/grade" in links
        assert "https://help.pro.sixshop.com/products/settings" in links

    def test_excludes_external_links(self):
        html = _make_html(
            '<a href="/page1">내부</a>'
            '<a href="https://google.com/search">외부</a>'
        )
        parser = OopyParser()
        links = parser.extract_links(html, self._BASE_URL)
        assert len(links) == 1
        assert "google.com" not in links[0]

    def test_removes_fragment_and_query(self):
        html = _make_html(
            '<a href="/page#section">링크1</a>'
            '<a href="/page?ref=nav">링크2</a>'
        )
        parser = OopyParser()
        links = parser.extract_links(html, self._BASE_URL)
        assert links == ["https://help.pro.sixshop.com/page"]

    def test_deduplicates_links(self):
        html = _make_html(
            '<a href="/page">링크1</a>'
            '<a href="/page/">링크2</a>'
        )
        parser = OopyParser()
        links = parser.extract_links(html, self._BASE_URL)
        assert len(links) == 1

    def test_resolves_relative_links(self):
        html = _make_html('<a href="grade">등급</a>')
        parser = OopyParser()
        links = parser.extract_links(html, self._BASE_URL + "/")
        assert "https://help.pro.sixshop.com/customers/grade" in links

    def test_empty_html(self):
        parser = OopyParser()
        links = parser.extract_links("<html></html>", self._BASE_URL)
        assert links == []


class TestGetParser:
    def test_returns_oopy_parser(self):
        parser = get_parser("https://help.pro.sixshop.com/customers/grade")
        assert isinstance(parser, OopyParser)

    def test_returns_same_instance(self):
        p1 = get_parser("https://example.com/a")
        p2 = get_parser("https://example.com/b")
        assert p1 is p2
