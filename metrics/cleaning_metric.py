from schema.document import Document
from metrics.base_metric import BaseMetric


class CleaningMetric(BaseMetric):

    def calculate(self, document: Document) -> Document:
        
        raw_length = len(document.raw_text)

        cleaned_length = len(document.cleaned_text)

        removed_chars = raw_length - cleaned_length

        removed_ratio = (
            round(removed_chars / raw_length * 100, 2)
            if raw_length > 0
            else 0.0
        )

        document.metrics["cleaning"] = {
            "raw_length": raw_length,
            "cleaned_length": cleaned_length,
            "removed_chars": removed_chars,
            "removed_ratio": removed_ratio
        }
        

        return document