from math import sqrt


class Node:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.type = ''

        # neighbors = []
        self.previous = None
        # self.obstacle = False


class FindPath:
    def __init__(self, initial_grid, height, width):
        self.start = None
        self.end = None
        self.height = height
        self.width = width
        self.grid = self.create_grid(initial_grid)
        self.open_set = []
        self.closed_set = []
        self.current_node = None
        self.final_path = []
        self.keys = []
        self.doors = []
        self.door_allowed = False
    def find_path(self, start, end):
        self.open_set = []
        self.closed_set = []
        self.current_node = None
        self.final_path = []
        self.keys = []
        self.start = self.grid[start[0]][start[1]]
        self.end = self.grid[end[0]][end[1]]
        self.open_set.append(self.start)
        while len(self.open_set) > 0:
            self.a_star()
            if len(self.final_path) > 0:
                break

        return self.final_path

    def a_star(self):
        best_way = 0
        for i in range(len(self.open_set)):
            if self.open_set[i].f < self.open_set[best_way].f:
                best_way = i

        self.current_node = self.open_set[best_way]
        self.find_keys(self.current_node)

        self.open_set.pop(best_way)
        self.final_path = []
        if self.current_node == self.end:
            self.create_final_path(self.current_node, self.start)

        if len(self.final_path) == 0:
            if not self.door_allowed:
                self.door_allowed = True
                self.find_path(self.start, self.end)
                if len(self.final_path) != 0:
                    pass


        # open_set = self.clean_open_set(self.open_set, self.current_node)
        # self.closed_set.append(self.current_node)

        neighbors = self.find_neighbors(self.current_node)
        for i, neighbor in enumerate(neighbors):
            if self.can_go(neighbor):
                temp_g = self.current_node.g + self.g_score(neighbor)

                if neighbor in self.open_set:
                    if temp_g < neighbor.g:
                        self.update_node(neighbor, temp_g)
                else:
                    self.update_node(neighbor, temp_g)
                    self.open_set.append(neighbor)

                self.closed_set.append(self.current_node)

    def update_node(self, node, temp_g):
        node.g = temp_g
        node.h = self.h_score(node)
        node.f = node.g + node.h
        node.previous = self.current_node

    def h_score(self, node):
        distance = sqrt(abs(node.x - self.end.x)**2 + abs(node.y - self.end.y)**2)
        return distance

    def can_go(self, node, door_allowed):
        if node.x == self.end.x and node.y == self.end.y:
            return True
        # elif (node in self.closed_set) or (node.type in ['W', '1', '2', '3', '4']):
        #     return False

        if (node in self.closed_set) or (node.type == 'W'):
            return False

        elif node.type in ['R', 'Y', 'G']:
            if node.type.lower() in self.keys:
                return True
            else:
                if door_allowed:
                    return True
                else:
                    return False
        else:
            return True

    def find_neighbors(self, node):
        x = node.x
        y = node.y
        neighbors = []
        if x < self.height - 1:
            neighbors.append(self.grid[x + 1][y])
        if x > 0:
            neighbors.append(self.grid[x - 1][y])
        if y < self.width - 1:
            neighbors.append(self.grid[x][y + 1])
        if y > 0:
            neighbors.append(self.grid[x][y - 1])
        # diagonals
        if x > 0 and y > 0:
            neighbors.append(self.grid[x - 1][y - 1])
        if x < self.height - 1 and y > 0:
            neighbors.append(self.grid[x + 1][y - 1])
        if x > 0 and y < self.width - 1:
            neighbors.append(self.grid[x - 1][y + 1])
        if x < self.height - 1 and y < self.width - 1:
            neighbors.append(self.grid[x + 1][y + 1])
        return neighbors

    def create_grid(self, initial_grid):
        grid = []
        for i in range(self.height):
            grid.append([])
            for j in range(self.width):
                grid[-1].append(0)
                grid[i][j] = Node(i, j)
                grid[i][j].type = initial_grid[i][j]

        return grid

    def return_node(self, x, y):
        node = self.grid[x][y]
        print(f"type: {node.type}"
              f"f: {node.f}")

    def show_grid(self):
        for i in range(self.height):
            print()
            for j in range(self.width):
                print(f"{self.grid[i][j].type}, ", end='')
        print()

    def g_score(self, node):
        if node.type == "*":
            return 20
        elif abs(node.x - self.current_node.x) == 1 and abs(node.y - self.current_node.y) == 1:
            return 2
        else:
            return 1

    def check_door(self, node):
        print(self.keys)
        if node.type == "R":
            if "r" in self.keys:
                return True
            else:
                return False
        elif node.type == "Y":
            if "y" in self.keys:
                return True
            else:
                return False
        elif node.type == "G":
            if "g" in self.keys:
                return True
            else:
                return False
        else:
            return False

    def find_keys(self, current_node):
        self.keys = []
        temp = current_node
        while temp.previous:
            if temp.type in ['r', 'g', 'y']:
                self.keys.append(temp.type)
            temp = temp.previous

    def create_final_path(self, node, start):
        temp = node
        while temp.previous:
            if self.door_allowed:
                if temp.type in ['R', 'Y', 'G']:
                    self.doors.append(temp.type)
            self.final_path.append((temp.x, temp.y))
            temp = temp.previous
        self.final_path.append((start.x, start.y))

# if __name__ == '__main__':
#     grid = [
#         ['EA', '1', 'W', 'E', 'E', 'E', 'E', 'E', '*', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
#         ['1', '*', 'W', 'y', 'G', 'E', 'E', 'E', 'E', 'E', '2', 'r', 'E', 'E', 'E', 'R', 'E', 'E', 'E', 'E'],
#         ['W', 'W', 'W', 'E', 'E', 'E', 'G', 'G', 'E', 'E', '1', 'E', 'g', 'E', 'E', 'G', 'R', 'Y', 'E', 'E'],
#         ['E', 'E', 'E', 'E', 'r', 'E', 'E', 'E', 'E', 'R', 'R', 'E', 'E', 'E', 'E', 'E', 'E', '*', 'E', 'E'],
#         ['E', 'E', 'E', 'E', '3', 'E', 'E', 'Y', 'Y', 'E', 'E', '2', 'E', 'y', 'E', 'E', 'E', 'E', 'E', 'E'],
#         ['E', 'E', 'E', '*', 'E', 'E', '2', 'E', '1', '1', '1', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
#         ['E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'g', 'r', 'y', 'E', 'E', 'E', 'E', 'E', 'E']
#     ]
#     height = 7
#     width = 20
#     # grid = [
#     #     ['E', 'E', 'E', 'E'],
#     #     ['E', 'W', 'W', 'W'],
#     #     ['E', 'E', 'E', 'E']
#     # ]
#     # height = 3
#     # width = 4
#
#     f = FindPath(grid, height, width)
#     # f.show_grid()
#     f.find_path((0, 0), (0, 1))

