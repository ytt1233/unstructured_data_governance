from schema.document import Document


class ContentLengthValidator:

    def __init__(self, min_length: int = 100):
        self.min_length = min_length

    def validate(self, document: Document) -> Document:

        text = document.cleaned_text.strip()

        length = len(text)

        warnings = []

        status = "PASS"

        if length < self.min_length:
            status = "FAIL"

        document.validation_results["content_length"] = {
            "rule": "minimum_content_length",
            "status": status,
            "length": length,
            "min_length": self.min_length,
            "warnings": warnings
        }

        if status == "FAIL":
            document.validation_results["content_length"]["message"] = (
                "Document content is too short."
            )

        return document