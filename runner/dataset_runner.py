import os
from typing import List
from pathlib import Path

from pipeline.pipeline_manager import PipelineManager
from schema.document import Document
from report.dataset_report_generator import DatasetReportGenerator


class DatasetRunner:

    def __init__(self):

        self.pipeline = PipelineManager()

        # dataset级统计
        self.results: List[Document] = []
        self.failed_files: List[str] = []

        self.dataset_reporter = DatasetReportGenerator()

    # =========================
    # 批处理入口
    # =========================
    def run(self, folder_path: str):

        files = self._collect_files(folder_path)

        print(f"[DatasetRunner] Found {len(files)} files")

        for idx, file_path in enumerate(files):

            try:
                print(f"\n[{idx+1}/{len(files)}] Processing: {Path(file_path)}")

                document = self.pipeline.run(file_path)

                self.results.append(document)

            except Exception as e:

                print(f"[ERROR] Failed: {file_path} -> {e}")

                self.failed_files.append(file_path)

        # =========================
        # dataset summary
        # =========================
        report = self._generate_dataset_report()

        self.dataset_reporter.generate(
            report
        )
        return report

    # =========================
    # 文件收集
    # =========================
    def _collect_files(self, folder_path: str) -> List[str]:

        files = []

        for root, _, filenames in os.walk(folder_path):

            for f in filenames:

                if f.lower().endswith(".pdf"):

                    files.append(os.path.join(root, f))

        return files

    # =========================
    # dataset report
    # =========================
    def _generate_dataset_report(self):

        total = len(self.results)
        failed = len(self.failed_files)

        report = {
            "dataset_summary": {
                "total_files": total,
                "failed_files": failed,
                "success_rate": round(
                    total / (total + failed),
                    4
                ) if (total + failed) else 0
            },

            "validation_summary":
                self._build_validation_summary(),

            "governance_effectiveness":
                self._build_governance_effectiveness(),

            "dataset_insights":
                self._build_dataset_insights(),

             "recommendations":
                self._build_recommendations()
        }

        self._print_report(report)

        return report
    # =========================
    # dataset report 中的validators summary
    # =========================
    def _build_validation_summary(self):

        validation_stats = {}

        for doc in self.results:

            for k, v in doc.validation_results.items():

                if k not in validation_stats:

                    validation_stats[k] = {
                        "PASS": 0,
                        "FAIL": 0
                    }

                status = v.get("status", "UNKNOWN")

                if status in validation_stats[k]:
                    validation_stats[k][status] += 1

        return validation_stats

    # =========================
    # dataset report 中的metrics summary
    # ========================= 

    
    def _build_metrics_summary(self):

        chunk_sizes = []

        total_pii = 0
        total_noise = 0

        for doc in self.results:

            metrics = doc.metrics

            # chunk
            if "chunk" in metrics:

                chunk_sizes.append(
                    metrics["chunk"].get(
                        "avg_chunk_size",
                        0
                    )
                )

            # pii
            if "pii" in metrics:

                total_pii += metrics["pii"].get(
                    "total_pii",
                    0
                )

            # ocr
            if "ocr_noise" in metrics:

                total_noise += metrics[
                    "ocr_noise"
                ].get(
                    "removed_noise_chars",
                    0
                )

        return {

            "avg_chunk_size":
                round(
                    sum(chunk_sizes) / len(chunk_sizes),
                    2
                ) if chunk_sizes else 0,

            "total_pii_removed":
                total_pii,

            "total_noise_removed":
                total_noise
        }

    # =========================
    # 治理效果
    # ========================= 
    def _build_governance_effectiveness(self):

        chars_removed = 0
        blank_lines_removed = 0

        headers_removed = 0
        footers_removed = 0

        pii_removed = 0

        ocr_noise_removed = 0

        chunks_generated = 0

        avg_chunk_sizes = []

        for doc in self.results:

            metrics = doc.metrics

            # text quality
            text_metric = metrics.get(
                "text_quality",
                {}
            )

            chars_removed += text_metric.get(
                "removed_chars",
                0
            )

            blank_lines_removed += text_metric.get(
                "blank_lines_removed",
                0
            )
            # ==========================
            # header footer
            # ==========================
            hf_metric = metrics.get(
                "header_footer",
                {}
            )

            headers_removed += hf_metric.get(
                "removed_headers",
                0
            )

            footers_removed += hf_metric.get(
                "removed_footers",
                0
            )
            # ==========================
            # pii
            # ==========================
            pii_metric = metrics.get(
                "pii",
                {}
            )

            pii_removed += pii_metric.get(
                "total_pii",
                0
            )
            # ==========================
            # ocr
            # ==========================
            ocr_metric = metrics.get(
                "ocr_noise",
                {}
            )

            ocr_noise_removed += ocr_metric.get(
                "removed_noise_chars",
                0
            )
            # ==========================
            # chunk
            # ==========================
            chunk_metric = metrics.get(
                "chunk",
                {}
            )

            chunks_generated += chunk_metric.get(
                "chunk_count",
                0
            )

            avg_chunk_sizes.append(
                chunk_metric.get(
                    "avg_chunk_size",
                    0
                )
            )

        return {

            "characters_removed":
                chars_removed,

            "blank_lines_removed":
                blank_lines_removed,

            "headers_removed":
                headers_removed,

            "footers_removed":
                footers_removed,

            "pii_removed":
                pii_removed,

            "ocr_noise_removed":
                ocr_noise_removed,

            "chunks_generated":
                chunks_generated,

            "avg_chunk_size":
                round(
                    sum(avg_chunk_sizes)
                    / len(avg_chunk_sizes),
                    2
                )
                if avg_chunk_sizes
                else 0
        }
    
    # =========================
    # 生成洞察
    # =========================
    def _build_dataset_insights(self):

        total_docs = len(self.results)

        if total_docs == 0:

            return {
                "quality_level": "UNKNOWN",
                "risk_level": "UNKNOWN",
                "kb_readiness": "UNKNOWN"
            }
        #========================
        # validation pass rate
        #========================

        pass_count = 0
        total_checks = 0

        for doc in self.results:

            for result in doc.validation_results.values():

                total_checks += 1

                if result.get("status") == "PASS":
                    pass_count += 1

        pass_rate = (
            pass_count / total_checks
            if total_checks
            else 0
        )

        # =========================
        # quality level
        # =========================
        if pass_rate >= 0.95:
            quality_level = "GOOD"

        elif pass_rate >= 0.80:
            quality_level = "FAIR"

        else:
            quality_level = "POOR"
        # =========================
        # risk level
        # =========================
        remaining_pii = False

        for doc in self.results:

            pii_result = doc.validation_results.get(
                "pii",
                {}
            )

            if pii_result.get("status") == "FAIL":

                remaining_pii = True

                break

        risk_level = (
            "HIGH"
            if remaining_pii
            else "LOW"
        )
        # =========================
        # kb readiness
        # =========================
        kb_readiness = (
            "READY"
            if quality_level == "GOOD"
            and risk_level == "LOW"
            else "PARTIALLY_READY"
        )#质量好且风险等级低返回knowledge base准备就绪                 

        return {

            "quality_level": quality_level,

            "risk_level": risk_level,

            "kb_readiness": kb_readiness,

            "validation_pass_rate": round(pass_rate * 100, 2)
        }


    # =========================
    # 生成推荐
    # =========================
    def _build_recommendations(self):

        recommendations = []

        all_pass = True

        for doc in self.results:

            for result in doc.validation_results.values():

                if result.get("status") == "FAIL":

                    all_pass = False

                    break

        if all_pass:

            recommendations.extend(
                [
                    "Ready for vector database indexing",
                    "Ready for enterprise knowledge base ingestion"
                ]
            )

        else:

            recommendations.append(
                "Review failed validation items before ingestion"
            )

        return recommendations


    # =========================
    # 打印报告
    # =========================
    def _print_report(self, report):

        print("\n" + "=" * 60)
        print("DATASET REPORT")
        print("=" * 60)

        print("\n[Dataset Summary]")
        for k, v in report["dataset_summary"].items():
            print(f"  {k}: {v}")

        print("\n[Validation Summary]")
        for validator, stats in report["validation_summary"].items():
            passed = stats.get("PASS",0)
            failed = stats.get("FAIL",0)
            total = passed + failed
            status = ("PASS" if failed == 0 else "FAIL")
            print(
                f"  {validator:<20}"
                f"{status:<6}"
                f"({passed}/{total})"
            )
        total_pass = 0
        total_fail = 0

        for stats in report["validation_summary"].values():
            total_pass += stats.get("PASS",0)
            total_fail += stats.get("FAIL",0)
        overall = ("PASS" if total_fail == 0 else "FAIL")
        print(
            f"\n  Overall Status: "
            f"{overall}"
        )

        print("\n[Governance Effectiveness]")
        for k, v in report["governance_effectiveness"].items():
            print(f"  {k}: {v}")

        print("\n[Dataset Insights]")
        for k, v in report["dataset_insights"].items():
            print(f"  {k}: {v}")

        print("\n[Recommendations]")
        for item in report["recommendations"]:
            print(f"  - {item}")