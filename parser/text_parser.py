import os
import fitz  # pip install PyMuPDF
from schema.document import Document, Page
from parser.base_parser import BaseParser

class TextParser(BaseParser):

    def parse(self, document: Document) -> Document:
        """
        解析 txt/md 文件
        """
        with open(document.file_path, "r", encoding="utf-8") as f:
            text = f.read()

        document.raw_text = text
        # txt 默认作为单页
        page = Page(
            page_num=1,
            text=text
        )

        document.pages = [page]
        return document