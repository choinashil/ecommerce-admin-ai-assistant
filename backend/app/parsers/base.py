from abc import ABC, abstractmethod
from dataclasses import dataclass

import httpx


@dataclass
class ParseResult:
    """파서가 HTML에서 추출한 결과."""

    title: str
    content: str
    breadcrumb: str | None = None


class BaseParser(ABC):
    """HTML 파서의 기본 인터페이스."""

    def fetch_html(self, url: str) -> str:
        """URL에서 HTML을 가져온다.."""
        response = httpx.get(url, timeout=30.0)
        response.raise_for_status()
        return response.text

    @abstractmethod
    def parse(self, html: str) -> ParseResult:
        """HTML 문자열을 파싱하여 구조화된 결과를 반환한다."""
        ...
