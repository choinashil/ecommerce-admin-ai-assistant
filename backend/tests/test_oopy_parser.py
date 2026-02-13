from app.parsers import get_parser
from app.parsers.oopy_parser import OopyParser


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

    # TOC
    for item in toc:
        parts.append(f"<div>{item}</div>")

    # 본문
    for line in body_lines:
        parts.append(f"<div>{line}</div>")

    # footer 잔재
    parts.append("<div>식스샵 프로 가이드</div>")

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
        assert "가이드" not in result.content
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
        # TOC의 "등급 추가", "등급 삭제"는 제거되고, 본문의 것은 남아야 함
        assert result.content.startswith("설명 텍스트")

    def test_removes_footer_site_name(self):
        html = _make_oopy_html(
            breadcrumb_parts=["가이드", "고객"],
            title="등급 관리",
            toc=[],
            body_lines=["본문"],
        )
        parser = OopyParser()
        result = parser.parse(html)
        assert not result.content.endswith("식스샵 프로 가이드")

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


class TestGetParser:
    def test_returns_oopy_parser(self):
        parser = get_parser("https://help.pro.sixshop.com/customers/grade")
        assert isinstance(parser, OopyParser)

    def test_returns_same_instance(self):
        p1 = get_parser("https://example.com/a")
        p2 = get_parser("https://example.com/b")
        assert p1 is p2
