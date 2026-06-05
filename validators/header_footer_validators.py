from collections import Counter

from validators.base_validator import BaseValidator
from schema.document import Document


class HeaderFooterValidator(BaseValidator):

    def __init__(self, repeat_threshold: int = 3):
        """
        V1:
        仅检测重复行

        注意：
        重复行 != 页眉页脚残留

        因此当前版本仅给出 Warning，
        不直接判定 FAIL。
        """
        self.repeat_threshold = repeat_threshold

    def validate(self, document: Document) -> Document:

        text = document.cleaned_text or ""
        

        lines = [
            line.strip()
            for line in text.splitlines()
            if line.strip()
        ]

        counter = Counter(lines)

        suspicious_lines = []

        for line, count in counter.items():

            # 忽略过短文本
            if len(line) < 5:
                continue

            if count >= self.repeat_threshold:

                suspicious_lines.append(
                    {
                        "text": line[:100],
                        "count": count
                    }
                )

        # =========================
        # 状态判断
        # =========================
        status = "PASS"
        warnings = []

        if suspicious_lines:

            warnings.append(
                f"{len(suspicious_lines)} repeated lines detected"
            )

        # =========================
        # 保存结果
        # =========================

        document.validation_results["header_footer"] = {
            "rule": "repeated_line_detection",
            "status": status,
            "suspicious_count": len(suspicious_lines),
            "suspicious_lines": suspicious_lines[:10],
            "warnings": warnings
        }

        return document