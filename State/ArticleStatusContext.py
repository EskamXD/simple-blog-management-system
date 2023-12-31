from State.DraftState import DraftState


class ArticleStatusContext:
    def __init__(self):
        self.state = DraftState().get_status()

    def set_state(self, state):
        self.state = state.get_status()

    def get_status(self):
        return self.state
