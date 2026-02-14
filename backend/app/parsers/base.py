from abc import ABC, abstractmethod
from dataclasses import dataclass
from urllib.parse import urljoin, urlparse

import httpx
from bs4 import BeautifulSoup


def normalize_url(url: str) -> str:
    """URL을 정규화한다. fragment, query 제거, 끝 슬래시 통일."""
    parsed = urlparse(url)
    return parsed._replace(fragment="", query="").geturl().rstrip("/")


@dataclass
class ParseResult:
    """파서가 HTML에서 추출한 결과."""

    title: str
    content: str
    breadcrumb: str | None = None


class BaseParser(ABC):
    """HTML 파서의 기본 인터페이스."""

    def fetch_html(self, url: str) -> str:
        """URL에서 HTML을 가져온다."""
        response = httpx.get(url, timeout=30.0, follow_redirects=True)
        response.raise_for_status()
        return response.text

    @abstractmethod
    def parse(self, html: str) -> ParseResult:
        """HTML 문자열을 파싱하여 구조화된 결과를 반환한다."""
        ...

    def extract_links(self, html: str, base_url: str) -> list[str]:
        """HTML에서 같은 도메인의 내부 링크를 추출한다."""
        soup = BeautifulSoup(html, "lxml")
        base_domain = urlparse(base_url).netloc

        links = []
        for a_tag in soup.find_all("a", href=True):
            absolute = urljoin(base_url, a_tag["href"])
            if urlparse(absolute).netloc == base_domain:
                links.append(normalize_url(absolute))

        return list(dict.fromkeys(links))  # 순서 유지 중복 제거
