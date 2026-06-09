import re

from cleaners.base_cleaner import BaseCleaner
from schema.document import Document


class OCRNoiseCleaner(BaseCleaner):

    NOISE_PATTERN = re.compile(
        r"[■□◆◇▲△▼▽★☆●○�]"
    )

    def clean(self, document: Document) -> Document:

        text = document.cleaned_text

        if not text:
            return document

        matches = self.NOISE_PATTERN.findall(text)

        cleaned_text = self.NOISE_PATTERN.sub(
            "",
            text
        )

        document.cleaned_text = cleaned_text

        document.audit_trail.append(
            {
                "action": "ocr_noise_clean",
                "removed_noise_chars": len(matches)
            }
        )
        
        document.processing_snapshots["after_ocr_noise"] = cleaned_text

        return document