from schema.document import Document
from metrics.base_metric import BaseMetric


class TextQualityMetric(BaseMetric):

    def calculate(self, document: Document) -> Document:

        raw_text = (
            document.processing_snapshots.get(
                "raw",
                ""
            )
        )

        cleaned_text = (
            document.processing_snapshots.get(
                "after_text_clean",
                ""
            )
        )

        chars_before = len(raw_text)

        chars_after = len(cleaned_text)

        removed_chars = (
            chars_before - chars_after
        )

        char_reduction_rate = str(
            round(
                removed_chars / chars_before * 100,
                2
            )
            if chars_before > 0
            else 0.0
        ) + '%'

        blank_lines_before = (
            self._count_blank_lines(raw_text)
        )

        blank_lines_after = (
            self._count_blank_lines(cleaned_text)
        )

        blank_lines_removed = (
            blank_lines_before - blank_lines_after
        )

        document.metrics["text_quality"] = {

            "chars_before": chars_before,

            "chars_after": chars_after,

            "removed_chars": removed_chars,

            "char_reduction_rate": char_reduction_rate,

            "blank_lines_before":
                blank_lines_before,

            "blank_lines_after":
                blank_lines_after,

            "blank_lines_removed":
                blank_lines_removed
        }

        return document

    def _count_blank_lines(
        self,
        text: str
    ) -> int:

        if not text:
            return 0

        count = 0

        for line in text.splitlines():

            if not line.strip():
                count += 1

        return count