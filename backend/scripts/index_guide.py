"""
JSON 파일에서 가이드 문서를 읽어 청킹 + 임베딩 후 DB에 저장하는 스크립트.

Usage:
    cd backend
    python -m scripts.index_guide
    python -m scripts.index_guide --input crawl_preview_v2.json
    python -m scripts.index_guide --batch-size 50
"""

import argparse
import json
import logging
import sys

from langchain_text_splitters import RecursiveCharacterTextSplitter
from sqlalchemy import text

from app.guide.model import GuideChunk, GuideDocument
from app.shared.database import SessionLocal
from app.shared.embedding import embed_texts

logger = logging.getLogger(__name__)

_text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100,
)


def main():
    parser = argparse.ArgumentParser(description="가이드 문서 인덱싱")
    parser.add_argument(
        "--input",
        default="crawl_preview_v2.json",
        help="입력 JSON 파일 경로 (기본: crawl_preview_v2.json)",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=100,
        help="임베딩 배치 크기 (기본: 100)",
    )
    args = parser.parse_args()

    logging.basicConfig(level=logging.INFO, format="%(message)s")

    with open(args.input, encoding="utf-8") as f:
        data = json.load(f)

    pages = data["pages"] if isinstance(data, dict) else data
    print(f"JSON 로드 완료: {len(pages)}개 문서")

    db = SessionLocal()
    try:
        db.execute(text("DELETE FROM guide_chunks"))
        db.execute(text("DELETE FROM guide_documents"))
        db.commit()
        print("기존 데이터 삭제 완료")

        all_chunks = []
        doc_map = {}

        for page in pages:
            doc = GuideDocument(
                url=page["url"],
                title=page["title"],
                content=page["content"],
                breadcrumb=page.get("breadcrumb"),
            )
            db.add(doc)
            db.flush()

            chunks = _text_splitter.split_text(page["content"])
            for i, chunk_text in enumerate(chunks):
                all_chunks.append({
                    "document_id": doc.id,
                    "content": chunk_text,
                    "chunk_index": i,
                    "embedding_input": f"{page['title']}\n\n{chunk_text}",
                })
            doc_map[doc.id] = page["title"]

        print(f"문서 저장 완료: {len(doc_map)}개")
        print(f"청크 생성 완료: {len(all_chunks)}개 (문서당 평균 {len(all_chunks) / len(doc_map):.1f}개)")

        print(f"임베딩 시작 (배치 크기: {args.batch_size})...")
        for batch_start in range(0, len(all_chunks), args.batch_size):
            batch = all_chunks[batch_start:batch_start + args.batch_size]
            embedding_inputs = [c["embedding_input"] for c in batch]
            embeddings = embed_texts(embedding_inputs)

            for chunk_data, embedding in zip(batch, embeddings):
                db.add(GuideChunk(
                    document_id=chunk_data["document_id"],
                    content=chunk_data["content"],
                    embedding=embedding,
                    chunk_index=chunk_data["chunk_index"],
                ))

            progress = min(batch_start + args.batch_size, len(all_chunks))
            print(f"  {progress}/{len(all_chunks)} 청크 임베딩 완료")

        db.commit()
        print(f"\n인덱싱 완료: {len(doc_map)}개 문서 → {len(all_chunks)}개 청크")

    except Exception as e:
        db.rollback()
        print(f"에러: {e}")
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
