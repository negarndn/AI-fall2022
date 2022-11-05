from base import BaseAgent, Action
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


class Agent(BaseAgent):

    def __init__(self):
        super(Agent, self).__init__()
        self.actions = []
        self.last_gem = 0
        self.agent = None
        self.last_goal = Node(0, 0)
        self.current_goal = Node(0, 0)
        self.visited_goals = []
        self.gems_list = []

    def convert_path_to_action(self, final_path):
        for i in range(len(final_path) - 1):
            x = final_path[i][1] - final_path[i + 1][1]
            y = final_path[i][0] - final_path[i + 1][0]
            if x == 0:
                if y == 1:
                    self.actions.append(Action.UP)
                elif y == -1:
                    self.actions.append(Action.DOWN)
            if x == 1:
                if y == 0:
                    self.actions.append(Action.LEFT)
                elif y == 1:
                    self.actions.append(Action.UP_LEFT)
                elif y == -1:
                    self.actions.append(Action.DOWN_LEFT)
            if x == -1:
                if y == 0:
                    self.actions.append(Action.RIGHT)
                elif y == 1:
                    self.actions.append(Action.UP_RIGHT)
                elif y == -1:
                    self.actions.append(Action.DOWN_RIGHT)
        # self.actions.reverse()

    def evaluate_gems(self, remaining_gems) -> list:
        evaluated_gems = []
        for gem in remaining_gems:
            euclidean_distance = sqrt((self.agent.x - gem.x) ** 2 + (self.agent.y - gem.y) ** 2)
            gem_seq_score = GEM_SEQUENCE_SCORE[self.last_gem][int(gem.type)-1]
            gem.evaluation_result = gem.score + gem_seq_score - euclidean_distance
            evaluated_gems.append(gem)
        return evaluated_gems

    def choose_goal(self, remaining_gems) -> Gem:
        # remaining_gems = self.find_gems()
        evaluated_gems = self.evaluate_gems(remaining_gems)
        for _ in range(len(evaluated_gems)):
            most_valuable_gem = max(evaluated_gems, key=attrgetter('evaluation_result'))
            manhattan_distance = abs(self.agent.x - most_valuable_gem.x) + abs(self.agent.y - most_valuable_gem.y)
            if self.max_turn_count - self.turn_count < manhattan_distance:
                for i, o in enumerate(evaluated_gems):
                    if o.x == most_valuable_gem.x and o.y == most_valuable_gem.y:
                        del evaluated_gems[i]
                        break
                continue
            else:
                self.current_goal = most_valuable_gem
                return most_valuable_gem
        # TODO: Return Agent location as node if it does not find any valid goal
        return self.agent

    def find_gems(self) -> list:
        gems_list = []
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                if self.grid[x][y] in ['1', '2', '3', '4']:
                    gem = Gem(x, y)
                    gem.type = self.grid[x][y]
                    gem.score = GEM_SCORES[self.grid[x][y]]
                    gems_list.append(gem)
        return gems_list

    def get_current_location_of_agent(self):
        for x in range(self.grid_height):
            for y in range(self.grid_width):
                if self.grid[x][y].find("A") == -1:
                    location = (x, y)
                    return location

    def generate_actions(self, current_location, remaining_gems):
        self.agent = current_location
        if not current_location.type == '':
            self.last_gem = int(current_location.type)
        f = FindPath(self.grid, self.grid_height, self.grid_width)
        goal = self.choose_goal(remaining_gems)
        print(goal.x, goal.y, goal.type, goal.evaluation_result)
        goal_location = (goal.x, goal.y)
        agent_location = (self.agent.x, self.agent.y)
        final_path = f.find_path(agent_location, goal_location)
        print(final_path[::-1])
        self.convert_path_to_action(final_path[::-1])
        print(self.actions)

    def __eq__(self, other):
        return self.title == other.title

    def do_turn(self) -> Action:
        if self.turn_count == 1:
            self.gems_list = self.find_gems()

        if len(self.actions) == 0:
            remaining_gems = self.find_gems()
            self.generate_actions(self.current_goal, remaining_gems)

        if len(self.actions) > self.max_turn_count - self.turn_count:
            print("in shart: " + str(self.max_turn_count - self.turn_count), str(len(self.actions)))
            self.actions.clear()
            remaining_gems = self.find_gems()
            print(self.current_goal.x, self.current_goal.y, self.current_goal.type, self.current_goal.evaluation_result)
            print(remaining_gems)
            for i, o in enumerate(remaining_gems):
                if o.x == self.current_goal.x and o.y == self.current_goal.y:
                    del remaining_gems[i]
                    break
            self.generate_actions(self.last_goal, remaining_gems)
            # for _ in self.actions:
            #     self.actions.append(Action.NOOP)

        else:
            self.last_goal = self.current_goal
            print("last goal")
            print(self.last_goal.x, self.last_goal.y)
            remaining_gems = self.find_gems()
            agent_location = self.get_current_location_of_agent()
            for gem in self.gems_list:
                print("agent loc")
                print(agent_location)
                if agent_location[0] == gem.x and agent_location[1] == gem.y:
                    self.visited_goals.append(gem)
                    print("len visited goals")
                    print(len(self.visited_goals))
            for i, o in enumerate(remaining_gems):
                if o.x == self.last_goal.x and o.y == self.last_goal.y:
                    del remaining_gems[i]
                for visited_goal in self.visited_goals:
                    print("visited goal")
                    print(visited_goal.x, visited_goal.y)
                    if o.x == visited_goal.x and o.y == visited_goal.y:
                        del remaining_gems[i]

            self.generate_actions(self.last_goal, remaining_gems)
            return self.actions.pop(0)


if __name__ == '__main__':
    data = Agent().play()
    print("FINISH : ", data)