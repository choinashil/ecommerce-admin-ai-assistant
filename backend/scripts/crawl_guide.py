"""
가이드 문서 크롤링 스크립트.

Usage:
    cd backend
    python -m scripts.crawl_guide <URL>
    python -m scripts.crawl_guide <URL> --recursive
    python -m scripts.crawl_guide <URL> --recursive --max-pages 100 --max-depth 5

Example:
    python -m scripts.crawl_guide https://help.pro.sixshop.com/customers/grade
    python -m scripts.crawl_guide https://help.pro.sixshop.com --recursive
"""

import argparse
import logging
import sys

from app.shared.database import SessionLocal
from app.guide.service import crawl_and_ingest, crawl_guide_site


def main():
    parser = argparse.ArgumentParser(description="가이드 문서 크롤링")
    parser.add_argument("url", help="크롤링할 URL")
    parser.add_argument(
        "--recursive", action="store_true", help="하위 페이지 재귀 크롤링"
    )
    parser.add_argument(
        "--max-pages", type=int, default=200, help="최대 크롤링 페이지 수 (기본: 200)"
    )
    parser.add_argument(
        "--max-depth", type=int, default=5, help="최대 크롤링 깊이 (기본: 5)"
    )
    parser.add_argument(
        "--delay", type=float, default=1.0, help="요청 간 딜레이 초 (기본: 1.0)"
    )

    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    db = SessionLocal()
    try:
        if args.recursive:
            result = crawl_guide_site(
                db,
                args.url,
                max_pages=args.max_pages,
                max_depth=args.max_depth,
                delay=args.delay,
            )
            print(f"\n크롤링 완료:")
            print(
                f"  총 {result.total_pages}페이지"
                f" (신규: {result.new_pages}, 업데이트: {result.updated_pages},"
                f" 건너뜀: {result.skipped_pages})"
            )
            if result.failed_urls:
                print(f"  실패: {len(result.failed_urls)}건")
                for url in result.failed_urls:
                    print(f"    - {url}")
        else:
            doc = crawl_and_ingest(db, args.url)
            print(f"완료: {doc.id}")
            print(f"  제목: {doc.title}")
            print(f"  내용 길이: {len(doc.content)} 문자")
            print(f"  Breadcrumb: {doc.breadcrumb or '(없음)'}")
    except Exception as e:
        print(f"에러: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
