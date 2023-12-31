from abc import ABC, abstractmethod


class ValidationStrategy(ABC):
    @abstractmethod
    def validate(self, data):
        pass
