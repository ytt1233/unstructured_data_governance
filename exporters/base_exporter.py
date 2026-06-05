from abc import ABC, abstractmethod
from schema.document import Document


class BaseExporter(ABC):

    @abstractmethod
    def export(
        self,
        document: Document
    ):
        pass