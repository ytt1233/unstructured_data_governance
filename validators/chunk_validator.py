from schema.document import Document
from validators.base_validator import BaseValidator


class ChunkValidator(BaseValidator):
    # =========================
    # 对chunk的数量和内容进行校验
    # =========================

    def validate(self, document: Document) -> Document:

        chunks = document.chunks or []

        chunk_count = len(chunks)

        empty_chunk_count = 0

        for chunk in chunks:

            text = chunk.text or ""

            if not text.strip():
                empty_chunk_count += 1

        # =========================
        # 状态判断
        # =========================

        status = "PASS"

        if chunk_count == 0:
            status = "FAIL"

        elif empty_chunk_count > 0:
            status = "FAIL"
        # =========================
        # 读取 Metrics
        # =========================

        chunk_metrics = document.metrics.get("chunk", {})

        min_chunk_size = chunk_metrics.get("min_chunk_size", 0)

        warnings = []

        # 最小Chunk过小提醒
        if min_chunk_size > 0 and min_chunk_size < 50:
            warnings.append(
                f"Small chunk detected: {min_chunk_size} chars"
            )

        # =========================
        # 保存结果
        # =========================

        document.validation_results["chunk"] = {
            "rule": "chunk_integrity",
            "status": status,
            "chunk_count": chunk_count,
            "empty_chunk_count": empty_chunk_count,
            "warnings": warnings,
        }

        return document