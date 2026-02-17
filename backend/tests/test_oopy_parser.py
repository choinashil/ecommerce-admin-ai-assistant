from unittest.mock import MagicMock, patch

from app.shared.crawling.parsers.base import ContentFormat
from app.shared.crawling.parsers.oopy import OopyParser


def _make_html(body_content: str) -> str:
    return f"<html><body>{body_content}</body></html>"


def _make_oopy_html(
    breadcrumb_parts: list[str],
    title: str,
    toc: list[str],
    body_lines: list[str],
) -> str:
    """OOPY 페이지 구조의 HTML을 생성한다."""
    parts = []

    # breadcrumb: 각 조각 사이에 '/' 삽입
    for i, part in enumerate(breadcrumb_parts):
        parts.append(f"<span>{part}</span>")
        if i < len(breadcrumb_parts) - 1:
            parts.append("<span>/</span>")
    parts.append("<span>Search</span>")

    # 제목 (h1)
    parts.append(f"<h1>{title}</h1>")

    # TOC (notion-table_of_contents-block)
    if toc:
        toc_items = "".join(f"<div>{item}</div>" for item in toc)
        parts.append(f'<div class="notion-table_of_contents-block">{toc_items}</div>')

    # 본문
    for line in body_lines:
        parts.append(f"<div>{line}</div>")

    return _make_html("\n".join(parts))


class TestOopyParserTitle:
    def test_extracts_h1(self):
        parser = OopyParser()
        result = parser.parse(_make_html("<h1>등급 관리</h1><p>본문</p>"))
        assert result.title == "등급 관리"

    def test_fallback_to_title_tag(self):
        html = "<html><head><title>페이지 제목</title></head><body><p>본문</p></body></html>"
        parser = OopyParser()
        result = parser.parse(html)
        assert result.title == "페이지 제목"

    def test_no_title(self):
        parser = OopyParser()
        result = parser.parse(_make_html("<p>본문만 있음</p>"))
        assert result.title == "제목 없음"


class TestOopyParserBreadcrumb:
    def test_extracts_breadcrumb(self):
        html = _make_oopy_html(
            breadcrumb_parts=["가이드", "고객", "등급"],
            title="등급 관리",
            toc=[],
            body_lines=["본문 내용"],
        )
        parser = OopyParser()
        result = parser.parse(html)
        assert result.breadcrumb == "가이드 > 고객 > 등급"

    def test_no_breadcrumb_when_single_part(self):
        html = _make_html("<span>홈</span><span>Search</span><h1>제목</h1><p>본문</p>")
        parser = OopyParser()
        result = parser.parse(html)
        assert result.breadcrumb is None


class TestOopyParserContent:
    def test_removes_breadcrumb_from_content(self):
        html = _make_oopy_html(
            breadcrumb_parts=["가이드", "고객"],
            title="등급 관리",
            toc=[],
            body_lines=["본문 첫 줄"],
        )
        parser = OopyParser()
        result = parser.parse(html)
        assert "고객" not in result.content.split("\n")[0]

    def test_removes_title_duplicate(self):
        html = _make_oopy_html(
            breadcrumb_parts=["가이드", "고객"],
            title="등급 관리",
            toc=[],
            body_lines=["본문"],
        )
        parser = OopyParser()
        result = parser.parse(html)
        assert not result.content.startswith("등급 관리")

    def test_removes_toc(self):
        html = _make_oopy_html(
            breadcrumb_parts=["가이드"],
            title="등급 관리",
            toc=["등급 추가", "등급 삭제"],
            body_lines=["설명 텍스트", "등급 추가", "추가 방법", "등급 삭제", "삭제 방법"],
        )
        parser = OopyParser()
        result = parser.parse(html)
        assert result.content.startswith("설명 텍스트")

    def test_removes_noise_text(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            "<div>본문</div><div>로 돌아가기</div>"
        )
        parser = OopyParser()
        result = parser.parse(html)
        assert "로 돌아가기" not in result.content

    def test_removes_slash_separators(self):
        html = _make_oopy_html(
            breadcrumb_parts=["가이드", "고객"],
            title="등급",
            toc=[],
            body_lines=["본문"],
        )
        parser = OopyParser()
        result = parser.parse(html)
        lines = result.content.split("\n")
        assert "/" not in lines

    def test_empty_body(self):
        parser = OopyParser()
        result = parser.parse("<html></html>")
        assert result.content == ""


class TestOopyParserMarkdown:
    """마크다운 출력 형식을 테스트한다."""

    def test_preserves_h2_headings(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            "<h2>섹션 A</h2><p>내용 A</p>"
            "<h2>섹션 B</h2><p>내용 B</p>"
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "## 섹션 A" in result.content
        assert "## 섹션 B" in result.content

    def test_preserves_h3_headings(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            "<h2>옵션</h2><h3>세부 설정</h3><p>설명</p>"
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "## 옵션" in result.content
        assert "### 세부 설정" in result.content

    def test_removes_h1_title_duplicate(self):
        html = _make_html(
            "<span>Search</span><h1>등급 관리</h1>"
            "<h2>등급 추가</h2><p>본문</p>"
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "# 등급 관리" not in result.content
        assert "## 등급 추가" in result.content

    def test_preserves_list_items(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            "<ul><li>항목 1</li><li>항목 2</li></ul>"
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "항목 1" in result.content
        assert "항목 2" in result.content

    def test_removes_breadcrumb_in_markdown(self):
        html = _make_oopy_html(
            breadcrumb_parts=["가이드", "고객"],
            title="등급 관리",
            toc=[],
            body_lines=["<h2>등급 추가</h2>", "추가 방법"],
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "가이드" not in result.content

    def test_text_format_unchanged(self):
        """기존 텍스트 모드가 변경되지 않았는지 확인한다."""
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            "<h2>섹션</h2><p>본문</p>"
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.TEXT)
        assert "##" not in result.content
        assert "섹션" in result.content


class TestOopyParserImageCleanup:
    """OOPY 이미지 노이즈 제거를 테스트한다."""

    def test_removes_oopy_cdn_images(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            '<img src="https://cdn.lazyrockets.com/_next/static/media/dark-mode.png">'
            '<img src="https://oopy.lazyrockets.com/api/v2/notion/image?src=test">'
            "<p>본문</p>"
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "lazyrockets" not in result.content
        assert "본문" in result.content

    def test_removes_data_image_spacers(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            '<img src="data:image/gif;base64,R0lGODlhAQABAIAAAP///wAAACH5BAEAAAAALAAAAAABAAEAAAICRAEAOw==">'
            "<p>본문</p>"
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "data:image" not in result.content
        assert "본문" in result.content

    def test_removes_broken_images(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            '<img src=""><img><p>본문</p>'
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "![" not in result.content
        assert "본문" in result.content

    def test_preserves_valid_images(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            '<img src="https://example.com/guide-screenshot.png">'
            "<p>본문</p>"
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "guide-screenshot" in result.content


class TestOopyParserTocMarkdown:
    """마크다운 모드에서 TOC 제거를 테스트한다."""

    def test_toc_removal_with_markdown_headings(self):
        """TOC 항목이 본문의 ## 헤딩과 매칭되어 제거된다."""
        html = _make_oopy_html(
            breadcrumb_parts=["가이드"],
            title="상품 관리",
            toc=["옵션 설정", "재고 관리"],
            body_lines=[
                "<h2>옵션 설정</h2>", "옵션 설명",
                "<h2>재고 관리</h2>", "재고 설명",
            ],
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        lines = result.content.split("\n")
        assert lines[0].startswith("## 옵션 설정") or lines[0] == "## 옵션 설정"


class TestOopyParserFooter:
    """Footer "로 돌아가기" 제거를 테스트한다."""

    def test_removes_footer_link_in_markdown(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            "<p>본문</p>"
            '<a href="/">식스샵 프로 가이드로 돌아가기</a>'
        )
        parser = OopyParser()
        result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
        assert "돌아가기" not in result.content
        assert "본문" in result.content

    def test_removes_plain_footer(self):
        html = _make_html(
            "<span>Search</span><h1>제목</h1>"
            "<p>본문</p>"
            "<div>로 돌아가기</div>"
        )
        parser = OopyParser()
        result = parser.parse(html)
        assert "돌아가기" not in result.content


class TestFetchHtml:
    """fetch_html의 토글 감지 / meta-refresh 재시도 분기를 테스트한다."""

    _URL = "https://example.com/page"
    _STATIC_HTML = "<html><body><p>정적 페이지</p></body></html>"
    _TOGGLE_HTML = '<html><body><div class="notion-toggle-block">토글</div></body></html>'
    _EXPANDED_HTML = "<html><body><div>토글 펼쳐진 내용</div></body></html>"
    _META_REFRESH_HTML = '<html><head><meta http-equiv="refresh" content="2"></head><body></body></html>'

    @patch.object(OopyParser, "_expand_toggles")
    @patch("app.shared.crawling.parsers.base.httpx.get")
    def test_skips_playwright_when_no_toggle(self, mock_get, mock_expand):
        mock_get.return_value.text = self._STATIC_HTML
        mock_get.return_value.url = self._URL
        mock_get.return_value.raise_for_status = lambda: None

        parser = OopyParser()
        html, resolved_url = parser.fetch_html(self._URL)

        assert html == self._STATIC_HTML
        assert resolved_url == self._URL
        mock_expand.assert_not_called()

    @patch.object(OopyParser, "_expand_toggles")
    @patch("app.shared.crawling.parsers.base.httpx.get")
    def test_calls_playwright_when_toggle_exists(self, mock_get, mock_expand):
        mock_get.return_value.text = self._TOGGLE_HTML
        mock_get.return_value.url = self._URL
        mock_get.return_value.raise_for_status = lambda: None
        mock_expand.return_value = self._EXPANDED_HTML

        parser = OopyParser()
        html, resolved_url = parser.fetch_html(self._URL)

        assert html == self._EXPANDED_HTML
        mock_expand.assert_called_once_with(self._URL)

    @patch("app.shared.crawling.parsers.oopy.time.sleep")
    @patch.object(OopyParser, "_expand_toggles")
    @patch("app.shared.crawling.parsers.base.httpx.get")
    def test_retries_on_meta_refresh(self, mock_get, mock_expand, mock_sleep):
        """OOPY 로딩 페이지(meta refresh)를 감지하면 대기 후 재요청한다."""
        mock_get.return_value.url = self._URL
        mock_get.return_value.raise_for_status = lambda: None
        mock_get.return_value.text = self._META_REFRESH_HTML

        # 두 번째 호출에서 실제 콘텐츠 반환
        second_response = MagicMock()
        second_response.text = self._STATIC_HTML
        second_response.url = self._URL
        second_response.raise_for_status = lambda: None
        mock_get.side_effect = [mock_get.return_value, second_response]

        parser = OopyParser()
        html, _ = parser.fetch_html(self._URL)

        assert html == self._STATIC_HTML
        mock_sleep.assert_called_once()
        assert mock_get.call_count == 2


