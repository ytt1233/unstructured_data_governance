# validators/base_validator.py

from abc import ABC, abstractmethod

class BaseValidator(ABC):

    @abstractmethod
    def validate(self, document):
        pass