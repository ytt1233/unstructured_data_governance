import re

from cleaners.base_cleaner import BaseCleaner
from schema.document import Document


class OCRNoiseCleaner(BaseCleaner):

    NOISE_PATTERN = re.compile(
        r"[■□◆◇▲△▼▽★☆●○�]"
    )

    def clean(self, document: Document) -> Document:

        total_removed = 0

        for page in document.pages:

            matches = self.NOISE_PATTERN.findall(
                page.text
            )

            total_removed += len(matches)

            page.text = self.NOISE_PATTERN.sub(
                "",
                page.text
            )

        document.cleaned_text = "\n".join(
            page.text
            for page in document.pages
        )

        document.audit_trail.append(
            {
                "action": "ocr_noise_clean",
                "removed_noise_chars": total_removed
            }
        )
        
        document.processing_snapshots["after_ocr_noise"] = document.cleaned_text

        return document