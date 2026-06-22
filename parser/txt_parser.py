from parser.base_parser import BaseParser
from schema.document import Document, Page


class TXTParser(BaseParser):

    def parse(self, document: Document) -> Document:
        """
        解析 TXT 文件
        """

        with open(
            document.file_path,
            "r",
            encoding="utf-8"
        ) as f:

            full_text = f.read()

        document.raw_text = full_text

        # 整个TXT作为一个逻辑Page
        document.pages = [
            Page(
                page_num=1,
                text=full_text
            )
        ]

        document.first_page_layout = {}

        document.metadata.common["page_count"] = 1

        document.metadata.common["parser"] = (
            "txt"
        )

        document.audit_trail.append(
            {
                "action": "txt_parse"
            }
        )

        document.processing_snapshots["raw"] = (
            document.raw_text
        )

        return document