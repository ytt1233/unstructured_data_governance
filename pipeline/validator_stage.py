from typing import List
from schema.document import Document
from .base_stage import BaseStage


class ValidatorStage(BaseStage):

    def __init__(self, validators: List):
        self.validators = validators

    def process(self, document: Document) -> Document:

        for validator in self.validators:
            document = validator.validate(document)

        return document