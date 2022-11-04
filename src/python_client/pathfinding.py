from math import sqrt

def gem_sequence():
    pass


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






    def find_path(self, start, end):
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
        self.open_set.pop(best_way)
        self.final_path = []
        if self.current_node == self.end:
            temp = self.current_node
            while temp.previous:
                self.final_path.append((temp.x, temp.y))
                temp = temp.previous
            self.final_path.append((self.start.x, self.start.y))


        # open_set = self.clean_open_set(self.open_set, self.current_node)
        # self.closed_set.append(self.current_node)

        neighbors = self.find_neighbors(self.current_node)
        for i, neighbor in enumerate(neighbors):
            if self.can_go(neighbor):
                # for diagonals neighbors
                if self.is_diagonals(neighbor):
                    temp_g = self.current_node.g + 2
                else:
                    temp_g = self.current_node.g + 1
                control_flag = 0
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

    def can_go(self, node):
        if (node in self.closed_set) or (node.type == 'W'):
            return False
        # elif node.type == 'DOOR':
        #     pass
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

    def is_diagonals(self, node):
        if abs(node.x - self.current_node.x) == 1 and abs(node.y - self.current_node.y) == 1:
            return True



# if __name__ == '__main__':
#     grid = [
#         ['EA', 'E', 'E', 'E', 'E', 'E', 'E', 'E', '*', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E'],
#         ['E', '1', '2', 'y', 'G', 'E', 'E', 'E', 'E', 'E', '2', 'r', 'E', 'E', 'E', 'R', 'E', 'E', 'E', 'E'],
#         ['E', 'E', '3', 'E', 'E', 'E', 'G', 'G', 'E', 'E', '1', 'E', 'g', 'E', 'E', 'G', 'R', 'Y', 'E', 'E'],
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
#     f.find_path((0, 0), (2, 3))

