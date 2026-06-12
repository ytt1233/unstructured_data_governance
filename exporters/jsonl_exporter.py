import json
from pathlib import Path

from schema.document import Document
from exporters.base_exporter import BaseExporter


class JsonlExporter(BaseExporter):

    def __init__(self, output_dir="output/governed_docs"):
        self.output_dir = Path(output_dir)

        self.output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

    def export(self, document: Document):

        file_name = (
            f"{document.doc_id}.jsonl"
        )

        output_file = (
            self.output_dir / file_name
        )

        with open(
            output_file,
            "w",
            encoding="utf-8"
        ) as f:

            for chunk in document.chunks:

                record = {

                    "doc_id":
                        document.doc_id,

                    "chunk_id":
                        chunk.chunk_id,

                    "text":
                        chunk.text,

                    "page_num":
                        chunk.page_num,

                    "metadata": {

                        "common":
                            document.metadata.common,

                        "domain":
                            document.metadata.domain
                    }
                }

                f.write(
                    json.dumps(
                        record,
                        ensure_ascii=False
                    )
                    + "\n"
                )

        print(
            f"\n📄 清洗后JSONL文件: "
            f"{output_file}"
        )