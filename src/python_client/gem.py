from pathfinding import Node

GEM_SCORES = {"1": 50, "2": 100, "3": 200, "4": 300}


class Gem(Node):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.score = None
        self.color = None
        self.evaluation_result = None