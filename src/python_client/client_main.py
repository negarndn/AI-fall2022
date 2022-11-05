import random
from base import BaseAgent, Action
from pathfinding import FindPath

from pathfinding import FindPath, Node
from gem import Gem, GEM_SCORES
from operator import attrgetter
from math import sqrt


GEM_SEQUENCE_SCORE = [
    [50,   0,   0, 0],
    [50, 200, 100, 0],
    [100, 50, 200, 100],
    [50, 100, 50,  200],
    [250, 50, 100, 50]
]

# TODO: Convert grid cells into nodes like path finding module

class Agent(BaseAgent):
    def __init__(self):
        super(Agent, self).__init__()
        self.actions = []
        self.last_gem = 0
        self.gems_list = []
        self.agent = Node(0, 0)
        self.find_gems()


    def convert_path_to_action(self, final_path):

        for i in range(len(final_path) - 1):
            x = final_path[i][1] - final_path[i+1][1]
            y = final_path[i][0] - final_path[i+1][0]
            if x == 0:
                if y == 1:
                    self.actions.append(Action.DOWN)
                elif y == -1:
                    self.actions.append(Action.UP)
            if x == 1:
                if y == 0:
                    self.actions.append(Action.RIGHT)
                elif y == 1:
                    self.actions.append(Action.DOWN_RIGHT)
                elif y == -1:
                    self.actions.append(Action.UP_RIGHT)
            if x == -1:
                if y == 0:
                    self.actions.append(Action.LEFT)
                elif y == 1:
                    self.actions.append(Action.DOWN_LEFT)
                elif y == -1:
                    self.actions.append(Action.UP_LEFT)
        self.actions.reverse()
        print(self.actions)

    def evaluate_gems(self, remaining_gems) -> list:
        evaluated_gems = []
        for gem in remaining_gems:
            euclidean_distance = sqrt((self.agent.x - gem.x) ** 2 + (self.agent.y - gem.y) ** 2)
            gem_seq_score = GEM_SEQUENCE_SCORE[self.last_gem][gem.type]
            gem.evaluation_result = gem.score + gem_seq_score - euclidean_distance
            evaluated_gems.append(gem)

        return evaluated_gems

    def choose_goal(self, remaining_gems) -> Gem:
        evaluated_gems = self.evaluate_gems(remaining_gems)
        for _ in range(len(evaluated_gems)):
            most_valuable_gem = max(evaluated_gems, key=attrgetter('evaluation_result'))
            manhattan_distance = abs(self.agent.x - most_valuable_gem.x) + abs(self.agent.y - most_valuable_gem.y)
            if self.max_turn_count - self.turn_count < manhattan_distance:
                evaluated_gems.remove(most_valuable_gem)
                continue
            else:
                return most_valuable_gem
        # TODO: Return Agent location as node if it does not find any valid goal

    def find_gems(self):
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                pass
                # print( self.grid)
                # if self.grid[x][y] in ['1', '2', '3', '4']:
                #     gem = Gem(x, y)
                #     gem.type = self.grid[x][y]
                #     gem.score = GEM_SCORES[self.grid[x][y]]
                #     self.gems_list.append(gem)

    def generate_actions(self):
        path = FindPath(self.grid, self.grid_height, self.grid_width)
        # goal = self.choose_goal(self.gems_list)
        # self.gems_list.remove(goal)
        # goal_location = (goal.x, goal.y)
        # agent_location = (self.agent.x, self.agent.y)
        final_path = path.find_path((0, 0), (6, 19))
        print(final_path)
        self.convert_path_to_action(final_path)

    def do_turn(self) -> Action:
        if len(self.actions) == 0:
            self.generate_actions()
        if len(self.actions) > self.max_turn_count - self.turn_count:
            self.actions = []
            self.generate_actions()
            # for _ in self.actions:
            #     self.actions.append(Action.NOOP)
        else:
            return self.actions.pop(0)

        # return random.choice(
        #     [Action.UP, Action.DOWN, Action.LEFT, Action.RIGHT, Action.DOWN_RIGHT, Action.DOWN_LEFT, Action.UP_LEFT,
        #      Action.UP_RIGHT, Action.NOOP])


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
