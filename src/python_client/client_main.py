from base import BaseAgent, Action
from pathfinding import FindPath, Node
from gem import Gem
from operator import attrgetter
from coloring import Coloring
from itertools import permutations
from permutation import Permutation

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
        self.wall_density = 0
        self.gems_count = 0
        self.gem_density = 0
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

    def evaluate_permutation(self, perms) -> list:
        evaluated_permutations = []
        for seq in perms:
            permutation = Permutation()
            permutation.sequence_tuple = seq
            evaluation_result = 0
            current_agent_loc = self.agent
            last_goal_type = self.last_gem
            manhattan_distance = 0
            is_reachable = True
            for gem in seq:
                diagonal_distance = abs(current_agent_loc.x - gem.x) + abs(current_agent_loc.y - gem.y)
                manhattan_distance += abs(current_agent_loc.x - gem.x) + abs(current_agent_loc.y - gem.y)
                if self.max_turn_count - self.turn_count + 1 < manhattan_distance:
                    is_reachable = False
                    break
                gem_seq_score = GEM_SEQUENCE_SCORE[last_goal_type][int(gem.type)-1]
                evaluation_result += gem_seq_score - (diagonal_distance * ((self.grid_height * self.grid_width) / self.max_turn_count))
                current_agent_loc = gem
                last_goal_type = int(gem.type)
            if is_reachable:
                permutation.evaluation_result = evaluation_result
                evaluated_permutations.append(permutation)

        return evaluated_permutations

    def choose_goals_sequence(self, perms) -> list:
        evaluated_permutations = self.evaluate_permutation(perms)
        evaluated_permutations.sort(key=attrgetter("evaluation_result"), reverse=True)
        return evaluated_permutations

    def find_gems(self) -> list:
        gems_list = []
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                if self.grid[x][y] in ['1', '2', '3', '4']:
                    gem = Gem(x, y)
                    gem.type = self.grid[x][y]
                    gems_list.append(gem)
        self.gem_density = len(gems_list)
        return gems_list

    def count_wall_density(self):
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                if self.grid[x][y] == "W":
                    self.walls_count += 1
        self.wall_density = self.walls_count / (self.grid_width * self.grid_height)

    def find_permutations(self):
        if len(self.gems_list) >= 2:
            return permutations(self.gems_list, 2)
        else:
            return permutations(self.gems_list, len(self.gems_list))

    def generate_actions(self):
        # f = FindPath(self.grid, self.grid_height, self.grid_width)
        self.gems_list = self.find_gems()
        temp_gems_list = []
        for gem in self.gems_list:
            if self.coloring.contains(gem):
                temp_gems_list.append(gem)

        self.gems_list = temp_gems_list

        perms = list(self.find_permutations())
        print(len(perms))
        if len(perms[0]) == 0:
            self.finished = True
            return

        self.agent = self.last_goal

        if not self.last_goal.type == '':
            self.last_gem = int(self.last_goal.type)
        permutations_list = self.choose_goals_sequence(perms)

        for perm in permutations_list:
            agent_location = (self.agent.x, self.agent.y)
            final_path = []
            is_reachable = True
            for goal in perm.sequence_tuple:
                f = FindPath(self.grid, self.grid_height, self.grid_width)
                goal_location = (goal.x, goal.y)
                print(f"goal_location {goal_location}")
                print(f"agent location {agent_location}")
                path = f.find_path(agent_location, goal_location)
                print(f"path: {path}")
                if not len(path) == 0:
                    path.reverse()
                    if not len(final_path) == 0:
                        final_path.pop()
                    for tup in path:
                        final_path.append(tup)
                    print(f"final_path: {final_path}")
                    if len(final_path) - 1 > self.max_turn_count - self.turn_count + 1:
                        print("is reachable false")
                        is_reachable = False
                        break
                    agent_location = (goal.x, goal.y)
                else:
                    is_reachable = False
            if is_reachable:
                final_path.reverse()
                self.convert_path_to_action(final_path)
                self.last_goal = perm.sequence_tuple[-1]
                return

        self.finished = True

    def do_turn(self) -> Action:
        if self.turn_count == 1:
            self.count_wall_density()

            self.coloring = Coloring(self.grid, self.grid_height, self.grid_width)
            self.coloring.bfs(0, 0)

        if not self.finished:
            if len(self.actions) == 0:
                self.generate_actions()
            if not self.finished:
                return self.actions.pop(0)
            else:
                return Action.NOOP
        else:
            return Action.NOOP


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)
