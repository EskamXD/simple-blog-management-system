from abc import abstractmethod


class ArticleState:
    @abstractmethod
    def get_status(self):
        pass
