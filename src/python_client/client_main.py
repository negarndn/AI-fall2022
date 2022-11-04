import random
from base import BaseAgent, Action
from pathfinding import FindPath

class Agent(BaseAgent):

    def __init__(self):
        super(Agent, self).__init__()
        self.actions = []
    

    def convert_path_to_action(self, final_path):

        for i in range(len(final_path) - 1):
            y = final_path[i][1] - final_path[i+1][1]
            x = final_path[i][0] - final_path[i+1][0]
            # print(x)
            # print(y)
            if x == 0:
                if y == 1:
                    self.actions.append(Action.RIGHT)
                elif y == -1:
                    self.actions.append(Action.LEFT)
            if x == 1:
                if y == 0:
                    self.actions.append(Action.DOWN)
                elif y == 1:
                    self.actions.append(Action.DOWN_RIGHT)
                elif y == -1:
                    self.actions.append(Action.DOWN_LEFT)
            if x == -1:
                if y == 0:
                    self.actions.append(Action.UP)
                elif y == 1:
                    self.actions.append(Action.UP_RIGHT)
                elif y == -1:
                    self.actions.append(Action.UP_LEFT)
            # print(self.actions)

    def generate_actions(self):
        f = FindPath(self.grid, self.grid_height, self.grid_width)
        final_path = f.find_path((0, 0), (6, 19))
        print(final_path)
        self.convert_path_to_action(final_path)
        # print(self.actions)
    def do_turn(self) -> Action:

        if len(self.actions) == 0:
            self.generate_actions()
        # print(self.actions[0])
        if len(self.actions) > self.max_turn_count:
            self.actions = []
            for _ in self.actions:
                self.actions.append(Action.NOOP)

        else:
            # print(random.choice(self.actions))
            return self.actions.pop(0)

        # print(random.choice(
        #     [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT, Action.DOWN_RIGHT, Action.DOWN_LEFT, Action.UP_LEFT,
        #      Action.UP_RIGHT, Action.NOOP]))
        # return random.choice(
        #     [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT, Action.DOWN_RIGHT, Action.DOWN_LEFT, Action.UP_LEFT,
        #      Action.UP_RIGHT, Action.NOOP])


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
