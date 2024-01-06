from State.ArticleStatusContext import ArticleStatusContext
from State.DraftState import DraftState
from State.ReadyToPublishState import ReadyToPublishState
from State.PublishedState import PublishedState
from Strategy.ValidationStrategy import ValidationStrategy


class ArticleStatusChanger(ValidationStrategy):
    def validate(self, new_status):
        article_status_context = ArticleStatusContext()
        article_status_dict = {
            "D": DraftState(),
            "DRAFT": DraftState(),
            "R": ReadyToPublishState(),
            "READY TO PUBLISH": ReadyToPublishState(),
            "P": PublishedState(),
            "PUBLISHED": PublishedState(),
        }
        new_status = new_status.strip().upper()

        if new_status in article_status_dict.keys():
            article_status_state = article_status_dict[new_status]
            article_status_context.set_state(article_status_state)
        else:
            article_status_context.set_state(DraftState())

        return article_status_context.get_status()
    
    @staticmethod
    def get_status_dict():
        return {
            "D": "Draft",
            "DRAFT": "Draft",
            "R": "Ready to publish",
            "READY TO PUBLISH": "Ready to publish",
            "P": "Published",
            "PUBLISHED": "Published",}
