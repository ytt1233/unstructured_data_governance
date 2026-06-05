
from schema.document import Document
from metrics.definitions import METRIC_DEFINITIONS


class ReportGenerator:


    def generate(self, document: Document):

        print("\n" + "=" * 60)
        print("DOCUMENT GOVERNANCE REPORT")
        print("=" * 60)

        self._print_document_info(document)

        self._print_metadata(document)

        self._print_metrics(document)

        self._print_validation(document)

        self._print_audit_trail(document)

        self._print_sample_records(document)

        print("\n" + "=" * 60)

    # ==================================
    # Document Info
    # ==================================
    def _print_document_info(self, document: Document):

        print("\n[Document Info]")

        print(f"  Doc ID      : {document.doc_id}")
        print(f"  File Name   : {document.file_name}")
        print(f"  File Type   : {document.file_type}")
        print(f"  Pages       : {len(document.pages)}")
        print(f"  Raw Chars   : {len(document.raw_text)}")
        print(f"  Clean Chars : {len(document.cleaned_text)}")

    # ==================================
    # Metadata
    # ==================================
    def _print_metadata(self, document: Document):

        print("\n[Metadata]")

        print("\nCommon Metadata:")

        for k, v in document.metadata.common.items():
            print(f"  {k}: {v}")

        print("\nDomain Metadata:")

        for k, v in document.metadata.domain.items():
            print(f"  {k}: {v}")

    # ==================================
    # Metrics
    # ==================================
    def _print_metrics(self, document: Document):

        print("\n[Metrics]")

        if not document.metrics:
            print("  No metrics")
            return

        for metric_name, metric_data in document.metrics.items():

            print(f"\n{metric_name}")

            if isinstance(metric_data, dict):

                for k, v in metric_data.items():
                    print(f"  {k}: {v}")

            else:
                print(f"  {metric_data}")

        print("\n[Metric Definitions]")

        for k, v in METRIC_DEFINITIONS.items():
            print(f'  {k}:')
            for i, j in v.items():
                if i != "interpretation": #内容太长，暂不打印
                    print(f"    {i}: {j}")


    # ==================================
    # Validation
    # ==================================
    def _print_validation(self, document: Document):

        print("\n[Validation Summary]")

        pass_count = 0
        fail_count = 0

        for result in document.validation_results.values():

            if result.get("status") == "PASS":
                pass_count += 1
            else:
                fail_count += 1

        print(f"  PASS: {pass_count}")
        print(f"  FAIL: {fail_count}")

        overall_status = (
            "PASS"
            if fail_count == 0
            else "FAIL"
        )
        print(f"\n  Overall Status: {overall_status}")
        print()

        for validator_name, result in document.validation_results.items():

            status = result.get("status", "UNKNOWN")

            print(
                f"  {validator_name:<20} {status}"
            )

        # ==========================
        # Validation Details
        # ==========================
        print("\n[Validation Details]")

        for validator_name, result in document.validation_results.items():

            print(f"\n-  {validator_name}")

            for k, v in result.items():

                if k == "status":
                    continue

                print(f"  {k}: {v}")

    # ==================================
    # Audit Trail
    # ==================================
    def _print_audit_trail(self, document: Document):

        print("\n[Audit Trail]")

        if not document.audit_trail:
            print("  No audit trail")
            return

        for item in document.audit_trail:

            action = item.get("action", "unknown")

            print(f"\n- {action}")

            for k, v in item.items():

                if k == "action":
                    continue

                print(f"    {k}: {v}")

    # ==================================
    # Sample_Records
    # ==================================
    def _print_sample_records(self, document: Document):
    
        print("\n[Cleaning Samples]")

        if not document.sample_records:
            print("  No sample_records")
            return
        for record in document.sample_records:
            for k, v in record.items():
                if k == "type":
                    print(f"- {v}")
                else:
                    print(f"  {k}: {v}")