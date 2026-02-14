import logging
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Callable

import httpx

from app.parsers import get_parser, normalize_url

logger = logging.getLogger(__name__)


def _resolve_url(url: str) -> str:
    """리다이렉트를 따라가서 최종 URL을 반환한다."""
    response = httpx.head(url, timeout=30.0, follow_redirects=True)
    return normalize_url(str(response.url))


@dataclass
class CrawlResult:
    """사이트 크롤링 결과 요약."""

    total_pages: int = 0
    failed_urls: list[str] = field(default_factory=list)


def crawl_site(
    root_url: str,
    *,
    on_page: Callable[[str, str], None],
    max_pages: int = 50,
    max_depth: int = 3,
    delay: float = 1.0,
) -> CrawlResult:
    """루트 URL에서 BFS로 하위 페이지를 재귀 크롤링한다.

    같은 도메인 내의 페이지만 크롤링한다 (extract_links가 도메인 필터링 담당).
    각 페이지 크롤링 시 on_page(url, html) 콜백을 호출한다.
    """
    root_normalized = normalize_url(root_url)

    queue: deque[tuple[str, int]] = deque([(root_normalized, 0)])
    visited: set[str] = set()
    result = CrawlResult()
    parser = get_parser(root_url)

    while queue and result.total_pages < max_pages:
        url, depth = queue.popleft()

        if url in visited:
            continue
        visited.add(url)

        logger.info(f"크롤링 [{result.total_pages + 1}] (depth={depth}): {url}")

        try:
            # 리다이렉트를 따라가서 최종 URL로 치환
            resolved_url = _resolve_url(url)
            if resolved_url != url:
                if resolved_url in visited:
                    continue
                visited.add(resolved_url)
                url = resolved_url

            html = parser.fetch_html(url)

            # max_depth 미달 시에만 링크 추출
            if depth < max_depth:
                links = parser.extract_links(html, url)
                for link in links:
                    if link not in visited:
                        queue.append((link, depth + 1))

            on_page(url, html)
            result.total_pages += 1

            logger.info(f"  완료")

        except Exception as e:
            logger.error(f"  실패: {e}")
            result.failed_urls.append(url)

        if queue:
            time.sleep(delay)

    return result
