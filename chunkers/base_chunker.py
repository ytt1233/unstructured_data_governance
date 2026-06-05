from abc import ABC, abstractmethod
from schema.document import Document
class BaseChunker(ABC):

    @abstractmethod
    def chunk(self, document: Document) -> Document:
        """
        对 document 进行 chunk 切分
        """
        pass