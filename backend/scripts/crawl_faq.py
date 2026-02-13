"""
FAQ 문서 크롤링 스크립트.

Usage:
    cd backend
    python -m scripts.crawl_faq <URL>

Example:
    python -m scripts.crawl_faq https://help.pro.sixshop.com/customers/grade
"""

import sys

from app.database import SessionLocal
from app.display_id import to_display_id
from app.services.faq_service import crawl_and_ingest


def main():
    if len(sys.argv) < 2:
        print("Usage: python -m scripts.crawl_faq <URL>")
        sys.exit(1)

    url = sys.argv[1]
    print(f"크롤링 시작: {url}")

    db = SessionLocal()
    try:
        doc = crawl_and_ingest(db, url)
        display_id = to_display_id("faq_documents", doc.id)
        print(f"완료: {display_id}")
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
