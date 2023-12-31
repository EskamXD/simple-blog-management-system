from State.ArticleState import ArticleState


class PublishedState(ArticleState):
    @staticmethod
    def get_status():
        return "published"
