from abc import ABC, abstractmethod


class BlogManagement(ABC):
    @abstractmethod
    def add_article(self) -> None:
        pass

    @abstractmethod
    def show_categories(self) -> None:
        pass

    @abstractmethod
    def update_status(self) -> None:
        pass