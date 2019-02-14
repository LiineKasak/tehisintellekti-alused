from queue import Queue, PriorityQueue
import copy
import time


class Graph:

    # every coordinate is made of x, y
    # y is the index of row in map and x is it's position from the left side of the map

    def __init__(self, map: list):
        """Class constructor."""
        self.width = len(map[0])
        self.height = len(map)

        self.map = [list(row) for row in map]
        self.visited_map = copy.deepcopy(self.map)

        self.start = self.get_start_coords()
        self.goal = self.get_goal_coords()

    def get_start_coords(self) -> tuple:
        for y, row in enumerate(self.map):
            if "s" in row:
                return row.index("s"), y

    def get_goal_coords(self) -> tuple:
        for y, row in enumerate(self.map):
            if "D" in row:
                return row.index("D"), y

    def neighbors(self, coords: tuple) -> list:
        """Get all okay to visit neighboring coordinates."""
        x = coords[0]
        y = coords[1]
        neighbors = []
        for y_shift in [-1, 0, 1]:
            for x_shift in [-1, 0, 1]:
                if abs(y_shift) + abs(x_shift) == 1:
                    neighbor = (x + x_shift, y + y_shift)
                    if self.in_range(neighbor) and self.is_not_lava(neighbor):
                        neighbors.append(neighbor)
        return neighbors

    def neighbors_diagonal(self, coords: tuple) -> list:
        """Get all okay to visit neighboring coordinates."""
        x = coords[0]
        y = coords[1]
        neighbors = []
        for y_shift in [-1, 0, 1]:
            for x_shift in [-1, 0, 1]:
                if abs(y_shift) + abs(x_shift) != 0:
                    neighbor = (x + x_shift, y + y_shift)
                    if self.in_range(neighbor) and self.is_not_lava(neighbor):
                        neighbors.append(neighbor)
        return neighbors

    def in_range(self, coords: tuple) -> bool:
        """Check if coordinate is in range of the map."""
        return 0 <= coords[0] < self.width and 0 <= coords[1] < self.height

    def is_not_lava(self, coords: tuple) -> bool:
        """Check if the coordinate is safe to visit - it's not lava."""
        return self.map[coords[1]][coords[0]] != "*"

    def get_current(self, coords: tuple) -> str:
        """Get string value of coordinate."""
        return str(self.map[coords[1]][coords[0]])

    def calculate_priority(self, coords: tuple) -> int:
        return abs(coords[0] - self.goal[0]) + abs(coords[1] - self.goal[1])

    def calculate_priority_diagonal(self, coords: tuple) -> int:
        return max(abs(coords[0] - self.goal[0]), abs(coords[1] - self.goal[1]))

    def display_path(self, path):
        """Print map with displayed path."""
        for coord in path[:-1]:
            self.map[coord[1]][coord[0]] = "."
        print(Graph.map_to_str(self.map))

    def display_visited(self, current):
        """Print map with all visited coordinates."""
        self.visited_map[current[1]][current[0]] = "."
        print(Graph.map_to_str(self.visited_map))
        print("-" * self.width)

    @staticmethod
    def map_to_str(map):
        """Map map to printable string."""
        return "\n".join(["".join(row) for row in map])


def greedy(graph: Graph) -> list:
    """Do breath first to find the Diamond (D) and print visited coordinates as a map."""
    if graph.start is None:
        return

    frontier = PriorityQueue()
    frontier.put((0, graph.start))

    current = None

    came_from = {graph.start: None}

    while not frontier.empty():
        _, current = frontier.get()

        if graph.get_current(current) == "D":
            break

        # graph.display_visited(current)

        for next_vertex in graph.neighbors(current):
            if next_vertex not in came_from:
                priority = graph.calculate_priority(next_vertex)
                frontier.put((priority, next_vertex))
                came_from[next_vertex] = current

    path = []
    while current != graph.start:
        next_vertex = came_from[current]
        path.append(next_vertex)
        current = next_vertex
    return path


def a_star(graph: Graph) -> list:
    """Do breath first to find the Diamond (D) and print visited coordinates as a map."""
    if graph.start is None:
        return

    frontier = PriorityQueue()
    frontier.put((0, graph.start))

    current = None

    came_from = {graph.start: None}

    cost_so_far = {graph.start: 0}

    while not frontier.empty():
        # print(frontier.__dict__)
        _, current = frontier.get()

        if graph.get_current(current) == "D":
            break

        # graph.display_visited(current)

        for next_vertex in graph.neighbors(current):
            new_cost = cost_so_far[current] + 1
            if next_vertex not in cost_so_far or new_cost < cost_so_far[next_vertex]:
                cost_so_far[next_vertex] = new_cost
                priority = new_cost + graph.calculate_priority(next_vertex)  # g(n) + h(n)
                frontier.put((priority, next_vertex))
                came_from[next_vertex] = current

    path = []
    while current != graph.start:
        next_vertex = came_from[current]
        path.append(next_vertex)
        current = next_vertex
    return path


def a_star_diagonal(graph: Graph) -> list:
    """Do breath first to find the Diamond (D) and print visited coordinates as a map."""
    if graph.start is None:
        return

    frontier = PriorityQueue()
    frontier.put((0, graph.start))

    current = None

    came_from = {graph.start: None}

    cost_so_far = {graph.start: 0}

    while not frontier.empty():
        _, current = frontier.get()

        if graph.get_current(current) == "D":
            break

        for next_vertex in graph.neighbors_diagonal(current):
            new_cost = cost_so_far[current] + 1
            if next_vertex not in cost_so_far or new_cost < cost_so_far[next_vertex]:
                cost_so_far[next_vertex] = new_cost
                priority = new_cost + graph.calculate_priority_diagonal(next_vertex)  # g(n) + h(n)
                frontier.put((priority, next_vertex))
                came_from[next_vertex] = current

    path = []
    while current != graph.start:
        next_vertex = came_from[current]
        path.append(next_vertex)
        current = next_vertex
    return path


def find_path_lengths_and_time(files: list):
    """Do BFS and display the path."""
    for file in files:
        print(f"Map: {file}")
        with open(file) as f:
            map_data = [l.strip() for l in f.readlines() if len(l) > 1]
            graph = Graph(map_data)

            start = time.time()
            path = greedy(graph)
            end = time.time()
            print(f"Greedy path length: {len(path)}, time: {round(end - start, 4)}s")

            start = time.time()
            path = a_star(graph)
            end = time.time()
            print(f"A* path length: {len(path)}, time: {round(end - start, 4)}s")

            start = time.time()
            path = a_star_diagonal(graph)
            end = time.time()
            print(f"A* diagonal path length: {len(path)}, time: {round(end - start, 4)}s")

            print()


lava_map1 = [
    "      **               **      ",
    "     ***     D        ***      ",
    "     ***                       ",
    "                      *****    ",
    "           ****      ********  ",
    "           ***          *******",
    " **                      ******",
    "*****             ****     *** ",
    "*****              **          ",
    "***                            ",
    "              **         ******",
    "**            ***       *******",
    "***                      ***** ",
    "                               ",
    "                s              ",
]

lava_map2 = [
    "     **********************    ",
    "   *******   D    **********   ",
    "   *******                     ",
    " ****************    **********",
    "***********          ********  ",
    "            *******************",
    " ********    ******************",
    "********                   ****",
    "*****       ************       ",
    "***               *********    ",
    "*      ******      ************",
    "*****************       *******",
    "***      ****            ***** ",
    "                               ",
    "                s              ",
]

find_path_lengths_and_time(["cave300x300", "cave600x600", "cave900x900"])
