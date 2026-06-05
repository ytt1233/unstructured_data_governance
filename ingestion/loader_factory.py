from typing import Dict, Type
from ingestion.base_load import BaseLoader
from ingestion.pdf_loader import PDFLoader
from ingestion.text_loader import TextLoader
class LoaderFactory:
    """
    loader 工厂类
    根据 文件类型 创建对应的 loader 实例
    """
    @classmethod
    def get_loader(cls,file_type: str) -> BaseLoader:
        loaders = {
            ".pdf": PDFLoader(),#返回实例
            ".txt": TextLoader()
        }

        if file_type not in loaders:
            raise ValueError(f"Unsupported file type: {file_type}")
        return loaders[file_type]
    