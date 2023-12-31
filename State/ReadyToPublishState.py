from State.ArticleState import ArticleState


class ReadyToPublishState(ArticleState):
    @staticmethod
    def get_status():
        return "ready to publish"
