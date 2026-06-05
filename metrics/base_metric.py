# metrics/base_metric.py

from abc import ABC, abstractmethod


class BaseMetric(ABC):

    @abstractmethod
    def calculate(self, document):
        pass