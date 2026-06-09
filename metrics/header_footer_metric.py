from metrics.base_metric import BaseMetric
from schema.document import Document


class HeaderFooterMetric(BaseMetric):

    def calculate(
        self,
        document: Document
    ) -> Document:

        removed_headers = 0
        removed_footers = 0
        total_pages = 0

        for item in document.audit_trail:

            if (
                item.get("action")
                == "header_footer_clean"
            ):

                removed_headers = item.get(
                    "removed_headers",
                    0
                )

                removed_footers = item.get(
                    "removed_footers",
                    0
                )

                total_pages = item.get(
                    "total_pages",
                    0
                )

                break

        document.metrics["header_footer"] = {

            "removed_headers":
                removed_headers,

            "removed_footers":
                removed_footers,

            "total_pages":
                total_pages
        }

        return document