from abc import ABC, abstractmethod
from schema.document import Document
class BaseParser(ABC):
    @abstractmethod
    def parse(self, document: Document) -> Document:
        """
        填充 Document 的内容，如 raw_text、pages
        """
        pass    