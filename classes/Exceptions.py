
class InvalidMove(Exception):
    def __init__(self):
        self.message = "Invalid move"
        super().__init__(self.message)