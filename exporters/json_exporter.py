import json
from pathlib import Path

from schema.document import Document
from exporters.base_exporter import BaseExporter



class JsonExporter(BaseExporter):

    def __init__(self, output_dir="example_docs/governed_docs"):
        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(parents=True, exist_ok=True)

    def export(self, document: Document):

        data = {
            "doc_id": document.doc_id,

            "file_name": document.file_name,

            "file_type": document.file_type,

            "metadata": {
                "common": document.metadata.common,
                "domain": document.metadata.domain
            },

            "metrics": document.metrics,

            "validation_results": document.validation_results,

            "audit_trail": document.audit_trail,

            "chunks": []
        }
        # =========================
        # 转换自定义chunk类型转换为python标准类型
        # =========================
        for chunk in document.chunks:
            data["chunks"].append(
                {
                    "chunk_id": chunk.chunk_id,

                    "text": chunk.text,

                    "page_num": chunk.page_num,

                    "metadata": chunk.metadata
                }
            )
        # =========================
        # 写文件
        # =========================
        file_name = (f"{document.doc_id}.json")
        output_file = (self.output_dir / file_name)
        print(f'\n📄 清洗后文件: {output_file}')

        with open(output_file,"w",encoding="utf-8") as f:

            json.dump(data, f, ensure_ascii=False, indent=2)