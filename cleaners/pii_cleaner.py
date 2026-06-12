import re
from .base_cleaner import BaseCleaner
from schema.document import Document

PHONE_PATTERN = re.compile(r'1[3-9]\d{9}')
EMAIL_PATTERN = re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}')
ID_CARD_PATTERN = re.compile(r'\b\d{17}[\dXx]\b')


class PiiCleaner(BaseCleaner):

    def clean(self, document: Document) -> Document:
        """
        PII 脱敏

        以 document.pages 为治理主数据源
        最终重新生成 document.cleaned_text
        """

        if not document.pages:
            return document

        if not hasattr(document, "sample_records"):
            document.sample_records = []#记录脱敏前后信息

        phone_set = set()
        email_set = set()
        id_set = set()

        # =========================
        # Page级治理
        # =========================

        for page in document.pages:

            text = page.text

            if not text:
                continue

            text = self._mask_text(
                text,
                phone_set,
                email_set,
                id_set,
                document
            )

            page.text = text

        # =========================
        # 重建 cleaned_text
        # =========================

        document.cleaned_text = "\n".join(
            page.text
            for page in document.pages
        )

        # =========================
        # Audit Trail
        # =========================

        document.audit_trail.append(
            {
                "action": "pii_clean",
                "phone_count": len(phone_set),
                "email_count": len(email_set),
                "id_card_count": len(id_set),
            }
        )

        document.processing_snapshots["after_pii"] = document.cleaned_text

        return document
    # ==================================
    # 核心脱敏逻辑
    # ==================================

    def _mask_text(
        self,
        text,
        phone_set,
        email_set,
        id_set,
        document
    ):

        # ===== Phone =====

        phones = PHONE_PATTERN.findall(text)

        for phone in set(phones):

            masked_phone = self._mask_phone(phone)

            text = text.replace(
                phone,
                masked_phone
            )

            phone_set.add(phone)

            document.sample_records.append(
                {
                    "type": "pii_phone",
                    "before": phone,
                    "after": masked_phone,
                }
            )

        # ===== Email =====

        emails = EMAIL_PATTERN.findall(text)

        for email in set(emails):

            masked_email = self._mask_email(email)

            text = text.replace(
                email,
                masked_email
            )

            email_set.add(email)

            document.sample_records.append(
                {
                    "type": "pii_email",
                    "before": email,
                    "after": masked_email,
                }
            )

        # ===== ID Card =====

        ids = ID_CARD_PATTERN.findall(text)

        for id_num in set(ids):

            masked_id = self._mask_id(id_num)

            text = text.replace(
                id_num,
                masked_id
            )

            id_set.add(id_num)

            document.sample_records.append(
                {
                    "type": "pii_id_card",
                    "before": id_num,
                    "after": masked_id,
                }
            )

        return text

    # ==================================
    # Mask Rules
    # ==================================

    def _mask_phone(self, phone: str) -> str:
        return phone[:3] + "****" + phone[-4:]

    def _mask_email(self, email: str) -> str:

        name, domain = email.split("@")

        return name[0] + "***@" + domain

    def _mask_id(self, id_num: str) -> str:

        return (
            id_num[:4]
            + "**********"
            + id_num[-4:]
        )