from metrics.base_metric import BaseMetric
from schema.document import Document


class TOCMetric(BaseMetric):

    def calculate(
        self,
        document: Document
    ) -> Document:

        removed_toc_lines = 0

        for item in document.audit_trail:

            if item.get("action") == "toc_clean":

                removed_toc_lines = item.get(
                    "removed_toc_lines",
                    0
                )

                break

        before = document.processing_snapshots.get(
            "after_header_footer",
            ""
        )

        before_lines = len(
            before.splitlines()
        )

        after = document.processing_snapshots.get(
            "after_toc_clean",
            ""
        )

        after_lines = len(
            after.splitlines()
        )

        toc_ratio = str(
            round(
                removed_toc_lines /
                before_lines * 100,
                2
            )
            if before_lines > 0
            else 0.0
        ) + "%"

        document.metrics["toc"] = {

            "lines_before":
                before_lines,

            "lines_after":
                after_lines,

            "removed_toc_lines":
                removed_toc_lines,

            "toc_removal_ratio":
                toc_ratio
        }

        return document