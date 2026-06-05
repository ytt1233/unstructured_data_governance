from abc import ABC, abstractmethod
from schema.document import Document
class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, document: Document) -> Document:
        """
        从 Document 中提取元数据
        """
        pass