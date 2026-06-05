from abc import ABC, abstractmethod
from schema.document import Document

class BaseLoader(ABC):
    @abstractmethod
    def load(self, file_path: str) -> Document:
        """
        加载文件并返回 Document 对象
        """
        pass