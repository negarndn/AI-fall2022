import random
from base import BaseAgent, Action
from pathfinding import FindPath

class Agent(BaseAgent):

    def do_turn(self) -> Action:
        # f = FindPath(self.grid, self.grid_height, self.grid_width)
        # f.show_grid()
        # f.find_path((0, 0), (2, 5))



        return random.choice(
            [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT, Action.DOWN_RIGHT, Action.DOWN_LEFT, Action.UP_LEFT,
             Action.UP_RIGHT, Action.NOOP])


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
