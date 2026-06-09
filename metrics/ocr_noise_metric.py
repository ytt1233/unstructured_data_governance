from metrics.base_metric import BaseMetric
from schema.document import Document


class OCRNoiseMetric(BaseMetric):

    def calculate(self, document: Document) -> Document:

        removed_noise_chars = 0

        for item in document.audit_trail:

            if item.get("action") == "ocr_noise_clean":

                removed_noise_chars = item.get(
                    "removed_noise_chars",
                    0
                )

                break

        before = document.processing_snapshots.get(
            "after_header_footer",
            ""
        )

        before = len(before)

        after = document.processing_snapshots.get(
            "after_ocr_noise",
            ""
        )

        after = len(after)

        noise_ratio = str(
            round(removed_noise_chars / before * 100,2)
                if before > 0
                else 0.0
        ) + "%"

        document.metrics["ocr_noise"] = {

            "text_length_before": before,

            "text_length_after": after,

            "removed_noise_chars": removed_noise_chars,

            "noise_ratio": noise_ratio,
        }

        return document