from app.shared.crawling.parsers import (
    BaseParser,
    ContentFormat,
    ParseResult,
    normalize_url,
    OopyParser,
)

_OOPY_PARSER = OopyParser()


def get_parser(url: str) -> BaseParser:
    """URL 패턴에 따라 적절한 파서를 반환한다."""
    # 현재는 OOPY 파서만 지원. 추후 URL 패턴에 따라 분기.
    return _OOPY_PARSER


__all__ = ["BaseParser", "ContentFormat", "ParseResult", "get_parser", "normalize_url"]
