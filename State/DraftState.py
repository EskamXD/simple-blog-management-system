from State.ArticleState import ArticleState


class DraftState(ArticleState):
    @staticmethod
    def get_status():
        return "draft"
