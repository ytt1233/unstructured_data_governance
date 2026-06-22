from parser.pdf_parser import PDFParser
from parser.docx_parser import DOCXParser
from parser.txt_parser import TXTParser 


class ParserFactory:

    @staticmethod
    def get_parser(file_type: str):

        file_type = file_type.lower()
        print(f"123:{file_type}")

        if file_type == ".pdf":
            print("111")
            return PDFParser()

        elif file_type == ".docx":
            print("222")
            return DOCXParser()

        elif file_type == ".txt":
            return TXTParser()

        else:
            raise ValueError(
                f"Unsupported file type: {file_type}"
            )