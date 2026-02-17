"""
크롤링 결과를 DB에 저장하지 않고 JSON 파일로 내보내는 스크립트.

실제 crawl_and_ingest와 동일한 파싱/필터링을 적용하되,
임베딩과 DB 저장을 건너뛰어 결과물을 눈으로 검증할 수 있다.

Usage:
    cd backend
    python -m scripts.preview_crawl https://help.pro.sixshop.com
    python -m scripts.preview_crawl https://help.pro.sixshop.com --max-pages 10
    python -m scripts.preview_crawl https://help.pro.sixshop.com -o result.json
"""

import argparse
import json
import logging
from datetime import datetime

from app.guide.service import (
    _SITE_NOISE,
    _is_guide_content,
    _remove_noise,
)
from app.shared.crawling import ContentFormat, get_parser
from app.shared.crawling.crawler import crawl_site

logger = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description="크롤링 결과 미리보기 (JSON 출력)")
    parser.add_argument("url", help="크롤링할 루트 URL")
    parser.add_argument("--max-pages", type=int, default=200)
    parser.add_argument("--max-depth", type=int, default=5)
    parser.add_argument("--delay", type=float, default=1.0)
    parser.add_argument("-o", "--output", default="crawl_preview.json")

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    pages = []
    skipped = []

    def on_page(url: str, html: str):
        page_parser = get_parser(url)
        result = page_parser.parse(html, content_format=ContentFormat.MARKDOWN)
        content = _remove_noise(result.content, _SITE_NOISE)

        entry = {
            "url": url,
            "title": result.title,
            "breadcrumb": result.breadcrumb,
            "content_length": len(content),
            "content": content,
        }

        if not _is_guide_content(result.breadcrumb):
            entry["skip_reason"] = f"비가이드 (breadcrumb: {result.breadcrumb})"
            skipped.append(entry)
            logger.info(f"  건너뜀 (비가이드): {url}")
        else:
            pages.append(entry)
            logger.info(f"  저장 ({len(content)}자): {url}")

    crawl_result = crawl_site(
        args.url,
        on_page=on_page,
        max_pages=args.max_pages,
        max_depth=args.max_depth,
        delay=args.delay,
    )

    output = {
        "crawled_at": datetime.now().isoformat(),
        "root_url": args.url,
        "summary": {
            "total_visited": crawl_result.total_pages,
            "saved": len(pages),
            "skipped": len(skipped),
            "failed": len(crawl_result.failed_urls),
        },
        "pages": sorted(pages, key=lambda p: p["url"]),
        "skipped": skipped,
        "failed_urls": crawl_result.failed_urls,
    }

    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f"\n크롤링 완료:")
    print(f"  방문: {crawl_result.total_pages}페이지")
    print(f"  저장 대상: {len(pages)}개")
    print(f"  건너뜀: {len(skipped)}개")
    print(f"  실패: {len(crawl_result.failed_urls)}개")
    print(f"  출력: {args.output}")


if __name__ == "__main__":
    main()
