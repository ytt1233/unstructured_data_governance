import os
import fitz  # pip install PyMuPDF
from schema.document import Document, Page
from parser.base_parser import BaseParser

class PDFParser(BaseParser):

    def parse(self, document: Document) -> Document:
        """
        解析 PDF 文件，将文本填充到 Document.raw_text 和 Document.pages
        """
        if not os.path.exists(document.file_path):
            raise FileNotFoundError(f"{document.file_path} not found")
        
        # 打开 PDF
        pdf = fitz.open(document.file_path)
        full_text = ""
        pages_list = []

        for i, page in enumerate(pdf):
            text = page.get_text()
            full_text += text + "\n"
            pages_list.append(Page(page_num=i+1, text=text))

            # 只保存第一页版面信息
            if i == 0:
                first_page_layout = page.get_text("dict")

        document.raw_text = full_text
        document.pages = pages_list
        document.first_page_layout = first_page_layout

        document.metadata.common["page_count"] = pdf.page_count
        document.metadata.common["parser"] = "PyMuPDF"
        
        document.audit_trail.append(
            {
                "action": "pdf_parse"
            }
        )
        
        document.processing_snapshots['raw'] = (
            document.raw_text
        )

        pdf.close()
        return document