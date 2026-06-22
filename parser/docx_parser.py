from docx import Document as DocxDocument

from parser.base_parser import BaseParser
from schema.document import Document, Page


class DOCXParser(BaseParser):

    def parse(self, document: Document) -> Document:
        """
        解析 DOCX 文件
        """
        print(f"234")

        doc = DocxDocument(document.file_path)

        full_text = ""

        for para in doc.paragraphs:

            text = para.text.strip()

            if not text:
                continue

            full_text += text + "\n"

        document.raw_text = full_text

        # 整个DOCX作为一个逻辑Pag
        document.pages = [
            Page(
                page_num=1,
                text=full_text
            )
        ]

        document.first_page_layout = {}

        document.metadata.common["page_count"] = 1

        document.metadata.common["parser"] = (
            "python-docx"
        )

        document.audit_trail.append(
            {
                "action": "docx_parse"
            }
        )

        document.processing_snapshots["raw"] = (
            document.raw_text
        )

        return document