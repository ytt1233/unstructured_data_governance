from schema.document import Document


class MetadataValidator:

    REQUIRED_FIELDS = [
        "title",
        "category"
    ]

    def validate(self, document: Document) -> Document:

        metadata = document.metadata.domain or {}

        missing_fields = []
        warnings = []
        # =========================
        # 必填字段检查
        # =========================

        for field in self.REQUIRED_FIELDS:

            value = metadata.get(field)
            if value is None:
                missing_fields.append(field)
                continue

            if isinstance(value, str) and not value.strip():
                missing_fields.append(field)

        # =========================
        # Warning检查
        # =========================

        title = metadata.get("title", "")
        category = metadata.get("category", "")

        # 标题过短
        if title and len(title.strip()) < 5:
            warnings.append(
                "Title is unusually short"
            )

        # 分类未识别
        if category == "未知":
            warnings.append(
                "Category could not be determined"
            )
        # =========================
        # 状态判断
        # =========================

        status = "PASS"

        if missing_fields:
            status = "FAIL"
        
        # =========================
        # 保存结果
        # =========================

        document.validation_results["metadata"] = {
            "rule": "metadata_completeness",
            "status": status,
            "missing_fields": missing_fields,
            "warnings": warnings,
        }

        return document