from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def operation(self) -> None:
        pass

    @abstractmethod
    def to_dict(self) -> dict:
        pass

    @abstractmethod
    def from_dict(cls, data: dict) -> "Component":
        pass
