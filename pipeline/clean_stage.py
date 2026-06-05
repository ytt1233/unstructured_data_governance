from .base_stage import BaseStage
from schema.document import Document
from typing import List
class CleanStage(BaseStage):
    def __init__(self, cleaners:List) -> None:
        self.cleaners = cleaners

    def process(self, document: Document) -> Document:
        for cleaner in self.cleaners:
            document = cleaner.clean(document)
        return document