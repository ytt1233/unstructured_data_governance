import os


class DatasetReportGenerator:

    def __init__(
        self,
        output_dir: str = "output/reports"
    ):
        self.output_dir = output_dir

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    def generate(
        self,
        report: dict,
        file_name: str = "dataset_report.md"
    ):

        output_path = os.path.join(
            self.output_dir,
            file_name
        )

        lines = []

        lines.append("# DATASET GOVERNANCE REPORT\n")

        # =========================
        # Dataset Summary
        # =========================

        lines.append("## Dataset Summary\n")

        for k, v in report[
            "dataset_summary"
        ].items():

            lines.append(
                f"- **{k}**: {v}"
            )

        # =========================
        # Corpus Summary
        # =========================

        lines.append(
            "\n## Corpus Summary\n"
        )

        for k, v in report[
            "corpus_summary"
        ].items():

            lines.append(
                f"- **{k}**: {v}"
            )

        # =========================
        # Validation Summary
        # =========================

        lines.append("\n## Validation Summary\n")

        for validator, stats in report[
            "validation_summary"
        ].items():

            passed = stats.get(
                "PASS",
                0
            )

            failed = stats.get(
                "FAIL",
                0
            )

            total = passed + failed

            status = (
                "PASS"
                if failed == 0
                else "FAIL"
            )

            lines.append(
                f"- **{validator}**: "
                f"{status} "
                f"({passed}/{total})"
            )

        # =========================
        # Governance Effectiveness
        # =========================

        lines.append(
            "\n## Governance Effectiveness\n"
        )

        for k, v in report[
            "governance_effectiveness"
        ].items():

            lines.append(
                f"- **{k}**: {v}"
            )

        # =========================
        # Dataset Insights
        # =========================

        lines.append(
            "\n## Dataset Insights\n"
        )

        for k, v in report[
            "dataset_insights"
        ].items():

            lines.append(
                f"- **{k}**: {v}"
            )

        # =========================
        # Recommendations
        # =========================

        lines.append(
            "\n## Recommendations\n"
        )

        for item in report[
            "recommendations"
        ]:

            lines.append(
                f"- {item}"
            )

        with open(
            output_path,
            "w",
            encoding="utf-8"
        ) as f:

            f.write(
                "\n".join(lines)
            )

        print(
            f"[Dataset Report Saved] {output_path}"
        )