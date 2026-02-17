import logging
import time
from collections import deque
from dataclasses import dataclass, field
from typing import Callable

from app.shared.crawling import get_parser, normalize_url

logger = logging.getLogger(__name__)


@dataclass
class CrawlResult:
    """사이트 크롤링 결과 요약."""

    total_pages: int = 0
    failed_urls: list[str] = field(default_factory=list)


def crawl_site(
    root_url: str,
    *,
    on_page: Callable[[str, str], None],
    url_filter: Callable[[str], bool] | None = None,
    max_pages: int = 50,
    max_depth: int = 3,
    delay: float = 1.0,
) -> CrawlResult:
    """루트 URL에서 BFS로 하위 페이지를 재귀 크롤링한다.

    같은 도메인 내의 페이지만 크롤링한다 (extract_links가 도메인 필터링 담당).
    url_filter가 주어지면, False를 반환하는 URL은 큐에 추가하지 않는다.
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
            # GET 한 번으로 HTML + 리다이렉트 해소를 동시에 처리
            html, resolved_url = parser.fetch_html(url)
            if resolved_url != url:
                if resolved_url in visited:
                    continue
                visited.add(resolved_url)
                url = resolved_url

            if url_filter and not url_filter(url):
                continue

            # max_depth 미달 시에만 링크 추출
            if depth < max_depth:
                links = parser.extract_links(html, url)
                for link in links:
                    if link not in visited:
                        if url_filter and not url_filter(link):
                            continue
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
