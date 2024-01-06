from abc import ABC, abstractmethod

class View(ABC):
    @abstractmethod
    def __init__(self, root, tab):
        self.root = root
        self.tab = tab

    @abstractmethod
    def place(self):
        pass
