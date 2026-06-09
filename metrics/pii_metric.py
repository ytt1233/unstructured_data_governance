from metrics.base_metric import BaseMetric
from schema.document import Document


class PiiMetric(BaseMetric):

    def calculate(
        self,
        document: Document
    ) -> Document:

        phone_count = 0
        email_count = 0
        id_card_count = 0

        for item in document.audit_trail:

            if (
                item.get("action")
                == "pii_clean"
            ):

                phone_count = item.get(
                    "phone_count",
                    0
                )

                email_count = item.get(
                    "email_count",
                    0
                )

                id_card_count = item.get(
                    "id_card_count",
                    0
                )

                break

        total_pii = (
            phone_count
            + email_count
            + id_card_count
        )

        document.metrics["pii"] = {

            "phone_count":
                phone_count,

            "email_count":
                email_count,

            "id_card_count":
                id_card_count,

            "total_pii":
                total_pii
        }

        return document