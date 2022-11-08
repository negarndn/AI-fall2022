from base import BaseAgent, Action
from pathfinding import FindPath, Node
from gem import Gem, GEM_SCORES
from operator import attrgetter
from math import sqrt
from coloring import Coloring

GEM_SEQUENCE_SCORE = [
    [50,   0,   0, 0],
    [50, 200, 100, 0],
    [100, 50, 200, 100],
    [50, 100, 50,  200],
    [250, 50, 100, 50]
]


class Agent(BaseAgent):

    def __init__(self):
        super(Agent, self).__init__()
        self.actions = []
        self.last_gem = 0
        self.agent = None
        self.last_goal = Node(0, 0)
        self.gems_list = []
        self.finished = False
        self.walls_count = 0
        self.coloring = None

    def convert_path_to_action(self, final_path):
        for i in range(len(final_path) - 1):
            x = final_path[i][1] - final_path[i + 1][1]
            y = final_path[i][0] - final_path[i + 1][0]
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

    def evaluate_gems(self, remaining_gems) -> list:
        evaluated_gems = []
        for gem in remaining_gems:
            if self.coloring.contains(gem):
                euclidean_distance = sqrt((self.agent.x - gem.x) ** 2 + (self.agent.y - gem.y) ** 2)
                gem_seq_score = GEM_SEQUENCE_SCORE[self.last_gem][int(gem.type)-1]
                if self.walls_count > 0:
                    gem.evaluation_result = gem_seq_score - (self.walls_count * euclidean_distance)
                else:
                    gem.evaluation_result = gem_seq_score - euclidean_distance
                # gem.evaluation_result = gem.score + gem_seq_score - euclidean_distance
                evaluated_gems.append(gem)
        return evaluated_gems

    def choose_goal(self) -> list:
        evaluated_gems = self.evaluate_gems(self.gems_list)
        evaluated_gems.sort(key=attrgetter("evaluation_result"), reverse=True)
        for gem in evaluated_gems:
            manhattan_distance = abs(self.agent.x - gem.x) + abs(self.agent.y - gem.y)
            if self.max_turn_count - self.turn_count + 1 <= manhattan_distance:
                evaluated_gems.pop(evaluated_gems.index(gem))
                continue
        if not len(evaluated_gems) == 0:
            return evaluated_gems
        return []

    def find_gems(self) -> list:
        gems_list = []
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                if self.grid[x][y] in ['1', '2', '3', '4']:
                    gem = Gem(x, y)
                    gem.type = self.grid[x][y]
                    # gem.score = GEM_SCORES[self.grid[x][y]]
                    gems_list.append(gem)
        return gems_list

    def wall_count(self):
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                if self.grid[x][y] == "W":
                    self.walls_count += 1

    def generate_actions(self):
        self.gems_list = self.find_gems()
        self.agent = self.last_goal
        print(f"las goal -> {self.last_goal.x, self.last_goal.y}")
        if not self.last_goal.type == '':
            self.last_gem = int(self.last_goal.type)
            print(f"last gem: {self.last_gem}")
        f = FindPath(self.grid, self.grid_height, self.grid_width)
        goals_list = self.choose_goal()
        for goal in goals_list:
            print(f"x: {goal.x} y: {goal.y} type: {goal.type}")
        agent_location = (self.agent.x, self.agent.y)
        for goal in goals_list:
            goal_location = (goal.x, goal.y)
            print("------------------------------------------")
            print(f"goal location: {goal_location}")
            print(f"evaluation result -> {goal.evaluation_result}")
            final_path = f.find_path(agent_location, goal_location)
            print(f"final -> {final_path}")
            print(f"agent location: {agent_location}")
            if len(final_path) - 1 <= self.max_turn_count - self.turn_count + 1 and not len(final_path) == 0:
                print(f"self.max_turn_count - self.turn_count, len(final_path) - 1 -> {self.max_turn_count - self.turn_count, len(final_path) - 1}")
                self.convert_path_to_action(final_path)
                self.last_goal = goal
                print("------------------------------------------")
                return
        self.finished = True

    def do_turn(self) -> Action:
        if self.turn_count == 1:
            self.wall_count()

            self.coloring = Coloring(self.grid, self.grid_height, self.grid_width)
            self.coloring.bfs(0, 0)
            for node in self.coloring.available_cells:
                print(node.x, node.y, node.type)
        print(f"turn count: {self.turn_count}")

        if not self.finished:
            print(f"self.finished is: {self.finished}")
            if len(self.actions) == 0:
                print(f"generate actions call, turn: {self.turn_count}")
                self.generate_actions()
            if not self.finished:
                print(f"action pop: {self.actions[0]}")
                return self.actions.pop(0)
            else:
                print("no op called in else aval")
                return Action.NOOP
        else:
            print("no op called in else dovom")
            return Action.NOOP


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
