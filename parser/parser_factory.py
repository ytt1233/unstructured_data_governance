from parser.pdf_parser import PDFParser
from parser.docx_parser import DOCXParser
from parser.txt_parser import TXTParser 


class ParserFactory:

    @staticmethod
    def get_parser(file_type: str):

        file_type = file_type.lower()

        if file_type == ".pdf":
            return PDFParser()

        elif file_type == ".docx":
            return DOCXParser()

        elif file_type == ".txt":
            return TXTParser()

        else:
            raise ValueError(
                f"Unsupported file type: {file_type}"
            )