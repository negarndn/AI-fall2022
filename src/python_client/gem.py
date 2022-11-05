from pathfinding import Node

GEMS_SCORES = {"1": 50, "2": 100, "3": 200, "4": 300}


class Gem(Node):
    def __init__(self):
        self.score = None
        self.color = None
        self.evaluation_result = None