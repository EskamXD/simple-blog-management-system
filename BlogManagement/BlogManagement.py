from abc import ABC, abstractmethod


class BlogManagement(ABC):
    @abstractmethod
    def save_and_exit(self) -> None:
        pass

    @abstractmethod
    def add_article(self) -> None:
        pass

    @abstractmethod
    def show_articles(self) -> None:
        pass

    @abstractmethod
    def update_status(self) -> None:
        pass

    @abstractmethod
    def show_categories(self) -> None:
        pass

    @abstractmethod
    def show_titles(self) -> None:
        pass

    @abstractmethod
    def print_composite(self) -> None:
        pass
