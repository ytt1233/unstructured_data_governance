import os
from typing import List

from pipeline.pipeline_manager import PipelineManager
from schema.document import Document


class DatasetRunner:

    def __init__(self):

        self.pipeline = PipelineManager()

        # dataset级统计
        self.results: List[Document] = []
        self.failed_files: List[str] = []

    # =========================
    # 批处理入口
    # =========================
    def run(self, folder_path: str):

        files = self._collect_files(folder_path)

        print(f"[DatasetRunner] Found {len(files)} files")

        for idx, file_path in enumerate(files):

            try:
                print(f"\n[{idx+1}/{len(files)}] Processing: {file_path}")

                document = self.pipeline.run(file_path)

                self.results.append(document)

            except Exception as e:

                print(f"[ERROR] Failed: {file_path} -> {e}")

                self.failed_files.append(file_path)

        # =========================
        # dataset summary
        # =========================
        return self._generate_dataset_report()

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

        # =========================
        # validation 汇总
        # =========================
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

        # =========================
        # metric 汇总
        # =========================
        avg_chunk_size = 0
        chunk_counts = 0

        for doc in self.results:

            metrics = doc.metrics

            if "chunk" in metrics:

                avg_chunk_size += metrics["chunk"].get("avg_chunk_size", 0)
                chunk_counts += 1

        avg_chunk_size = avg_chunk_size / chunk_counts if chunk_counts else 0

        # =========================
        # report 输出
        # =========================
        report = {
            "dataset_summary": {
                "total_files": total,
                "failed_files": failed,
                "success_rate": round(total / (total + failed), 4) if (total + failed) else 0
            },

            "validation_summary": validation_stats,

            "metrics_summary": {
                "avg_chunk_size": round(avg_chunk_size, 2)
            }
        }

        self._print_report(report)

        return report

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
        for k, v in report["validation_summary"].items():
            print(f"  {k}: {v}")

        print("\n[Metrics Summary]")
        for k, v in report["metrics_summary"].items():
            print(f"  {k}: {v}")