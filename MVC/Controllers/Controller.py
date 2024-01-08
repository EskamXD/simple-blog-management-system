from abc import ABC, abstractmethod

class Controller(ABC):
    @abstractmethod
    def __init__(self, root, view = None):
        self.root = root
        # self.model = model
        self.view = view

    @abstractmethod
    def place(self):
        pass

    @abstractmethod
    def set_view(self, view):
        pass