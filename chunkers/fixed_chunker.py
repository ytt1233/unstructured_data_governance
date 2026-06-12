from .base_chunker import BaseChunker
from typing import List
from schema.chunk import Chunk
import uuid
class FixedChunker(BaseChunker):
    def __init__(self, chunk_size: int=500, overlap=50):
        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, document):
        chunks = []
        step = (self.chunk_size- self.overlap)
        for page in document.pages:
            text = page.text
            if not text:
                continue
            for i in range(0, len(text), step):
                chunk_text = text[i:i+self.chunk_size]
                chunks.append(
                    Chunk(
                        chunk_id=str(uuid.uuid4()),
                        text=chunk_text,
                        source_doc_id=document.doc_id,
                        page_num=page.page_num,
                        metadata={
                            "chunk_index": len(chunks),
                            "chunk_size": len(chunk_text)
                        }
                    )
                )
            
        
        document.chunks = chunks

        # =========================
        # Chunk Metrics
        # =========================

        chunk_count = len(chunks)

        if chunks:

            chunk_sizes = [
                len(chunk.text)
                for chunk in chunks
            ]

            avg_chunk_size = round(
                sum(chunk_sizes) / chunk_count,
                2
            )

            min_chunk_size = min(chunk_sizes)

            max_chunk_size = max(chunk_sizes)

        else:

            avg_chunk_size = 0
            min_chunk_size = 0
            max_chunk_size = 0

        document.metrics["chunk"] = {
            "chunk_count": chunk_count,
            "avg_chunk_size": avg_chunk_size,
            "min_chunk_size": min_chunk_size,
            "max_chunk_size": max_chunk_size,
        }

        document.audit_trail.append(
            {
                "action": "fixed_chunk",
                "strategy": "fixed",
                "configured_chunk_size": self.chunk_size,
                "overlap": self.overlap,
                "chunk_count": chunk_count
            }
        )

        return document