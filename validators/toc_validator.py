import re

from validators.base_validator import BaseValidator


class TOCValidator(BaseValidator):

    TOC_PATTERN = re.compile(
        r".*[\.\·…]{3,}\s*\d+\s*$"
    )

    def validate(self, document):

        text = document.cleaned_text or ""

        remaining = []

        for line in text.splitlines():

            if self.TOC_PATTERN.match(
                line.strip()
            ):
                remaining.append(line)

        document.validation_results[
            "toc"
        ] = {

            "status":
                "PASS"
                if len(remaining) == 0
                else "FAIL",

            "remaining_toc_lines":
                len(remaining)
        }

        return document