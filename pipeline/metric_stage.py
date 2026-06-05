
from typing import List
from schema.document import Document
from .base_stage import BaseStage


class MetricStage(BaseStage):

    def __init__(self, metrics: List):
        self.metrics = metrics

    def process(self, document: Document) -> Document:

        for metric in self.metrics:
            document = metric.calculate(document)

        return document