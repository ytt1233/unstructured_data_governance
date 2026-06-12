
from schema.document import Document
from metrics.definitions import METRIC_DEFINITIONS
from pathlib import Path
import os 
import json



class ReportGenerator:

    def __init__(self, output_dir="output/reports"):
        self.output_dir = Path(output_dir)
        os.makedirs(self.output_dir, exist_ok=True)
    def generate(self, document: Document):
        # =========================
        # 1. 组装报告数据（核心）
        # =========================
        report_data = self._build_report_data(document)

        # =========================
        # 2. 输出 Markdown
        # =========================
        md_path = self._write_markdown(document, report_data)

        # =========================
        # 3. 输出 JSON
        # =========================
        json_path = self._write_json(document, report_data)

        # =========================
        # 4. 仍然保留控制台输出（可选）
        # =========================
        self._print_console(report_data)

        print(f"\n[Report Generated]")
        print(f"  Markdown: {md_path}")
        print(f"  JSON    : {json_path}")

        return report_data
    
    # =========================
    # 构建统一报告结构
    # =========================
    def _build_report_data(self, document: Document):

        return {
            "document_info": {
                "doc_id": document.doc_id,
                "file_name": document.file_name,
                "file_type": document.file_type,
                "pages": len(document.pages),
                "raw_chars": len(document.raw_text),
                "clean_chars": len(document.cleaned_text),
            },

            "metadata": {
                "common": document.metadata.common,
                "domain": document.metadata.domain,
            },

            "metrics": document.metrics,

            "validation": {
                "summary": self._build_validation_summary(document),
                "details": document.validation_results,
            },

            "audit_trail": document.audit_trail,

            "sample_records": document.sample_records,
        }
    
    # =========================
    # validation 汇总
    # =========================
    def _build_validation_summary(self, document: Document):

        pass_count = 0
        fail_count = 0

        for result in document.validation_results.values():
            if result.get("status") == "PASS":
                pass_count += 1
            else:
                fail_count += 1

        total = pass_count + fail_count

        return {
            "pass": pass_count,
            "fail": fail_count,
            "total": total,
            "pass_rate": round(pass_count / total, 4) if total else 0,
            "overall_status": "PASS" if fail_count == 0 else "FAIL"
        }
    # =========================
    # Markdown 输出
    # =========================
    def _write_markdown(self, document: Document, report):

        path = os.path.join(
            self.output_dir,
            f"{document.doc_id}_report.md"
        )

        lines = []

        lines.append("# Document Governance Report\n")

        # -------- Document Info --------
        info = report["document_info"]
        lines.append("## 1. Document Info")
        for k, v in info.items():
            lines.append(f"- {k}: {v}")
        lines.append("")
        # -------- Metadata --------
        metadata = report["metadata"]["domain"]

        lines.append("## 2. Metadata")

        for field in ['title', 'category']:

            lines.append(
                f"- {field}: "
                f"{metadata.get(field, 'N/A')}"
            )
        lines.append("")
        # -------- Metrics --------
        lines.append("## 3. Metrics")
        for metric_name, metric_data in report["metrics"].items():
            lines.append(f"\n### {metric_name}")
            if isinstance(metric_data, dict):
                for k, v in metric_data.items():
                    lines.append(f"- {k}: {v}")
            else:
                lines.append(str(metric_data))

        lines.append("")

        # -------- Validation --------
        lines.append("## 4. Validation Summary")
        v = report["validation"]["summary"]
        for k, val in v.items():
            lines.append(f"- {k}: {val}")

        lines.append("")

        # -------- Audit (简化输出) --------
        lines.append("## 5. Audit Trail (Top 10)")
        for item in report["audit_trail"][:10]:
            lines.append(f"- {item.get('action')} | {item}")

        # 写文件
        with open(path, "w", encoding="utf-8") as f:
            f.write("\n".join(lines))

        return path
    
    # =========================
    # JSON 输出
    # =========================
    def _write_json(self, document: Document, report):

        path = os.path.join(
            self.output_dir,
            f"{document.doc_id}_report.json"
        )

        with open(path, "w", encoding="utf-8") as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        return path
    
    # =========================
    # 控制台输出
    # =========================
    def _print_console(self, report):

        print("\n" + "=" * 60)
        print("DOCUMENT GOVERNANCE REPORT (CONSOLE VIEW)")
        print("=" * 60)

        print("\n[Document Info]")
        for k, v in report["document_info"].items():
            print(f"  {k}: {v}")

        print("\n[Metadata]")

        metadata = report["metadata"]["domain"]

        for field in ['title', 'category']:

            print(
                f"  {field}: "
                f"{metadata.get(field, 'N/A')}"
            )
        print("\n[Metrics]")
        for k, v in report["metrics"].items():
            print(f"\n{k}")
            if isinstance(v, dict):
                for kk, vv in v.items():
                    print(f"  {kk}: {vv}")
            else:
                print(v)

        print("\n[Validation]")
        for k, v in report["validation"]["summary"].items():
            print(f"  {k}: {v}")    
