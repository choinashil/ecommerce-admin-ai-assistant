"""
가이드 문서를 JSON으로 추출하는 스크립트.

Usage:
    cd backend
    python -m scripts.export_guide
    python -m scripts.export_guide --format markdown --output guide_documents_md.json
"""

import argparse
import json
import logging
import time

from sqlalchemy import select

from app.guide.model import GuideDocument
from app.guide.service import _remove_noise, _SITE_NOISE
from app.shared.crawling import ContentFormat, get_parser
from app.shared.database import SessionLocal

logger = logging.getLogger(__name__)


def _export_from_db(output: str) -> None:
    """DB에 저장된 텍스트 콘텐츠를 그대로 JSON으로 추출한다."""
    db = SessionLocal()
    try:
        docs = db.execute(select(GuideDocument)).scalars().all()

        data = [
            {
                "url": doc.url,
                "title": doc.title,
                "content": doc.content,
                "breadcrumb": doc.breadcrumb,
                "content_length": len(doc.content),
            }
            for doc in docs
        ]

        with open(output, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        print(f"{len(data)}개 문서 추출 완료 → {output}")
    finally:
        db.close()


def _export_as_markdown(output: str, delay: float) -> None:
    """DB의 URL 목록을 기반으로 각 페이지를 re-fetch하여 마크다운으로 추출한다."""
    db = SessionLocal()
    try:
        docs = db.execute(select(GuideDocument)).scalars().all()
        urls = [(doc.url, doc.breadcrumb) for doc in docs]
    finally:
        db.close()

    data = []
    for i, (url, breadcrumb) in enumerate(urls):
        print(f"[{i + 1}/{len(urls)}] {url}")
        try:
            parser = get_parser(url)
            html = parser.fetch_html(url)
            result = parser.parse(html, content_format=ContentFormat.MARKDOWN)
            content = _remove_noise(result.content, _SITE_NOISE)

            data.append(
                {
                    "url": url,
                    "title": result.title,
                    "content": content,
                    "breadcrumb": breadcrumb or result.breadcrumb,
                    "content_length": len(content),
                }
            )
        except Exception as e:
            print(f"  실패: {e}")

        if i < len(urls) - 1:
            time.sleep(delay)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"{len(data)}개 문서 마크다운 추출 완료 → {output}")


def main():
    parser = argparse.ArgumentParser(description="가이드 문서 JSON 추출")
    parser.add_argument(
        "--output",
        default="guide_documents.json",
        help="출력 파일 경로 (기본: guide_documents.json)",
    )
    parser.add_argument(
        "--format",
        choices=["text", "markdown"],
        default="text",
        dest="content_format",
        help="콘텐츠 출력 형식 (기본: text)",
    )
    parser.add_argument(
        "--delay",
        type=float,
        default=1.0,
        help="마크다운 모드에서 페이지 간 딜레이 초 (기본: 1.0)",
    )
    args = parser.parse_args()

    if args.content_format == "markdown":
        _export_as_markdown(args.output, args.delay)
    else:
        _export_from_db(args.output)


if __name__ == "__main__":
    main()
