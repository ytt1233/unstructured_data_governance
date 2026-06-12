from validators.base_validator import BaseValidator
from schema.document import Document
import re

PHONE_PATTERN = re.compile(r'1[3-9]\d{9}')
EMAIL_PATTERN = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
ID_CARD_PATTERN = re.compile(r'\b\d{17}[\dXx]\b')


class PiiValidator(BaseValidator):

    
    def validate(self, document: Document) -> Document:

        text = document.cleaned_text or ""

        # =========================
        # 检测残留PII
        # =========================

        remaining_phones = PHONE_PATTERN.findall(text)
        remaining_emails = EMAIL_PATTERN.findall(text)
        remaining_ids = ID_CARD_PATTERN.findall(text)

        status = "PASS"
        warnings = []

        # =========================
        # FAIL判断
        # =========================

        if remaining_phones or remaining_emails or remaining_ids:
            status = "FAIL"

        # =========================
        # WARNINGS（辅助解释）
        # =========================

        if remaining_phones:
            warnings.append(f"Remaining phones detected: {len(remaining_phones)}")

        if remaining_emails:
            warnings.append(f"Remaining emails detected: {len(remaining_emails)}")

        if remaining_ids:
            warnings.append(f"Remaining ID cards detected: {len(remaining_ids)}")

        # =========================
        # 写回结果
        # =========================

        document.validation_results["pii"] = {
            "rule": "pii_masking_validation",
            "status": status,
            "remaining_phone_count": len(remaining_phones),
            "remaining_email_count": len(remaining_emails),
            "remaining_id_card_count": len(remaining_ids),
            "warnings": warnings
        }
        return document