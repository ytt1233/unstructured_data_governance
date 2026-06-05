
from abc import ABC, abstractmethod
from schema.document import Document


class BaseStage(ABC):

    @abstractmethod
    def process(self, document: Document) -> Document:
        """
        所有 stage 必须实现 process 方法
        """
        pass