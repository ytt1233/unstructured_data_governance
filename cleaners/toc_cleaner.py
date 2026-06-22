import re

from cleaners.base_cleaner import BaseCleaner
from schema.document import Document


class TOCCleaner(BaseCleaner):

    TOC_PATTERN = re.compile(
        r".*[\.\·…]{3,}\s*\d+\s*$"
    )

    def clean(self, document: Document) -> Document:

        removed_lines = 0

        for page in document.pages:

            lines = page.text.split("\n")

            cleaned_lines = []

            for line in lines:

                stripped = line.strip()

                # 目录标题
                if stripped.lower() in [
                    "目录",
                    "contents"
                ]:
                    removed_lines += 1
                    continue

                # 目录项
                if self.TOC_PATTERN.match(
                    stripped
                ):
                    removed_lines += 1
                    continue

                cleaned_lines.append(line)

            page.text = "\n".join(
                cleaned_lines
            )

        # 重建 cleaned_text
        document.cleaned_text = "\n".join(
            page.text
            for page in document.pages
        )

        # Metrics
        document.metrics["toc"] = {
            "removed_toc_lines": removed_lines
        }

        # Audit
        document.audit_trail.append(
            {
                "action": "toc_clean",
                "removed_toc_lines": removed_lines
            }
        )

        document.processing_snapshots[
            "after_toc_clean"
        ] = document.cleaned_text

        return document