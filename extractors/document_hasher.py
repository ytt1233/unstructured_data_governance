# extractors/document_hasher.py

import hashlib

class DocumentHashExtractor:

    def extract(self, document):

        # =========================
        # Exact Hash
        # =========================
        text_for_hash = (
            document.cleaned_text
            .strip()
            .replace("\r\n", "\n")
            .replace("\r", "\n")
        )

        document_hash = hashlib.sha256(
            text_for_hash.encode("utf-8")
        ).hexdigest()

        # =========================
        # Metadata
        # =========================
        document.metadata.common[
            "document_hash"
        ] = document_hash


        document.audit_trail.append(
            {
                "action": "document_hash",
                "document_hash": document_hash,
            }
        )

        return document
