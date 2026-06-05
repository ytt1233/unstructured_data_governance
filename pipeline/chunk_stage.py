from typing import List
from schema.document import Document
from .base_stage import BaseStage

class ChunkStage(BaseStage):

    def __init__(self, chunkers: List):
        self.chunkers = chunkers

    def process(self, document: Document) -> Document:

        for chunker in self.chunkers:
            document = chunker.chunk(document)

        return document