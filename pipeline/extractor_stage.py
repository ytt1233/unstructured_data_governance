from typing import List
from schema.document import Document
from .base_stage import BaseStage
class ExtractorStage(BaseStage):
    def __init__(self, extractors: List):
        self.extractors = extractors
    def process(self, document: Document) -> Document:
        for extractor in self.extractors:
            document = extractor.extract(document)

        return document