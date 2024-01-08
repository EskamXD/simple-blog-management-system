from abc import ABC, abstractmethod

class Subject(ABC):
    @abstractmethod
    def add_observer(self, observer):
        self._observers.append(observer)

    @abstractmethod
    def remove_observer(self, observer):
        self._observers.remove(observer)

    @abstractmethod
    def notify_observers(self):
        for observer in self._observers:
            observer.update()
