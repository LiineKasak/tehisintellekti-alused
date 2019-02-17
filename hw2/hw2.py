from queue import PriorityQueue
import copy
import time
import os


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
        """Get start coordinates marked by 's'."""
        for y, row in enumerate(self.map):
            if "s" in row:
                return row.index("s"), y

    def get_goal_coords(self) -> tuple:
        """Get goal coordinates marked by 'D'."""
        for y, row in enumerate(self.map):
            if "D" in row:
                return row.index("D"), y

    def neighbors(self, coords: tuple, is_diagonal: False) -> list:
        """Get all okay to visit neighboring coordinates."""
        x = coords[0]
        y = coords[1]
        neighbors = []
        for y_shift in [-1, 0, 1]:
            for x_shift in [-1, 0, 1]:
                if abs(y_shift) + abs(x_shift) != 0 and is_diagonal or \
                        abs(y_shift) + abs(x_shift) == 1 and not is_diagonal:
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

    def heuristic(self, coords: tuple, h1=True) -> int:
        """Get heuristic value for coordinate."""
        if h1:
            return abs(coords[0] - self.goal[0]) + abs(coords[1] - self.goal[1])
        return max(abs(coords[0] - self.goal[0]), abs(coords[1] - self.goal[1]))

    def display_path(self, path: list) -> None:
        """Print map with displayed path."""
        for coord in path[:-1]:
            self.map[coord[1]][coord[0]] = "."
        print(Graph.map_to_str(self.map))

    def display_visited(self, current: tuple) -> None:
        """Print map with all visited coordinates."""
        self.visited_map[current[1]][current[0]] = "."
        print(Graph.map_to_str(self.visited_map))
        print("-" * self.width)

    @staticmethod
    def map_to_str(map: list) -> str:
        """Map map to printable string."""
        return "\n".join(["".join(row) for row in map])


def path_finding(graph: Graph, is_astar: bool, is_diagonal: bool, h1: bool = True) -> list:
    """Use path finding algorithms to find the path to the Diamond (D)."""
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
        # graph.display_visited(current)

        for next_vertex in graph.neighbors(current, is_diagonal):

            if is_astar:
                new_cost = cost_so_far[current] + 1
                if next_vertex not in cost_so_far or new_cost < cost_so_far[next_vertex]:
                    cost_so_far[next_vertex] = new_cost
                    priority = new_cost + (graph.heuristic(next_vertex, h1=h1))  # g(n) + h(n)
                    frontier.put((priority, next_vertex))
                    came_from[next_vertex] = current

            if not is_astar and next_vertex not in came_from:
                priority = graph.heuristic(next_vertex, h1=h1)
                frontier.put((priority, next_vertex))
                came_from[next_vertex] = current

    path = []
    while current != graph.start:
        next_vertex = came_from[current]
        path.append(next_vertex)
        current = next_vertex
    return path


def find_path_lengths_and_time(files: list):
    """Find paths with different algorithms and display their time and resulting path length."""
    print(f"h1: manhattan heuristic; h2: biggest coordinate diff\n")
    len1 = 22
    len2 = 5
    for file in files:
        if not os.path.exists(file):
            print(f"{file} file not found!\n")
            continue
        title = f"Map: {file}"
        print(title)
        print("-" * len(title))
        with open(file) as f:
            map_data = [l.strip() for l in f.readlines() if len(l) > 1]
            graph = Graph(map_data)

            # Greedy variants

            start = time.time()
            path = path_finding(graph, is_astar=False, is_diagonal=False, h1=True)
            end = time.time()
            print(f"\r{'Greedy not-diag [h1]:': <{len1}} {len(path) : <{len2}} time:  {round(end - start, 4)} s")

            start = time.time()
            path = path_finding(graph, is_astar=False, is_diagonal=False, h1=False)
            end = time.time()
            print(f"\r{'Greedy not-diag [h2]:': <{len1}} {len(path) : <{len2}} time:  {round(end - start, 4)} s")

            start = time.time()
            path = path_finding(graph, is_astar=False, is_diagonal=True, h1=True)
            end = time.time()
            print(f"\r{'Greedy diag [h1]:': <{len1}} {len(path) : <{len2}} time:  {round(end - start, 4)} s")

            start = time.time()
            path = path_finding(graph, is_astar=False, is_diagonal=True, h1=False)
            end = time.time()
            print(f"\r{'Greedy diag [h2]:': <{len1}} {len(path) : <{len2}} time:  {round(end - start, 4)} s")

            # A* variants

            start = time.time()
            path = path_finding(graph, is_astar=True, is_diagonal=False, h1=True)
            end = time.time()
            print(f"\r{'A* not-diag [h1]:': <{len1}} {len(path) : <{len2}} time:  {round(end - start, 4)} s")

            start = time.time()
            path = path_finding(graph, is_astar=True, is_diagonal=False, h1=False)
            end = time.time()
            print(f"\r{'A* not-diag [h2]:': <{len1}} {len(path) : <{len2}} time:  {round(end - start, 4)} s")

            start = time.time()
            path = path_finding(graph, is_astar=True, is_diagonal=True, h1=True)
            end = time.time()
            print(f"\r{'A* diag [h1]:': <{len1}} {len(path) : <{len2}} time:  {round(end - start, 4)} s")

            start = time.time()
            path = path_finding(graph, is_astar=True, is_diagonal=True, h1=False)
            end = time.time()
            print(f"\r{'A* diag [h2]:': <{len1}} {len(path) : <{len2}} time:  {round(end - start, 4)} s")

            print()


find_path_lengths_and_time(["cave300x300", "cave600x600", "cave900x900"])

# example of output:

# h1: manhattan heuristic; h2: biggest coordinate diff
# Map: cave300x300
# ----------------
# Greedy not-diag [h1]:  830   time:  0.0345 s
# Greedy not-diag [h2]:  746   time:  0.037 s
# Greedy diag [h1]:      558   time:  0.028 s
# Greedy diag [h2]:      547   time:  0.029 s
# A* not-diag [h1]:      554   time:  0.099 s
# A* not-diag [h2]:      554   time:  0.376 s
# A* diag [h1]:          458   time:  0.0725 s
# A* diag [h2]:          374   time:  0.2086 s
#
# Map: cave600x600
# ----------------
# Greedy not-diag [h1]:  2355  time:  0.127 s
# Greedy not-diag [h2]:  1763  time:  0.1125 s
# Greedy diag [h1]:      1319  time:  0.069 s
# Greedy diag [h2]:      1327  time:  0.124 s
# A* not-diag [h1]:      1247  time:  0.7621 s
# A* not-diag [h2]:      1247  time:  2.0692 s
# A* diag [h1]:          891   time:  0.132 s
# A* diag [h2]:          856   time:  1.4197 s
#
# Map: cave900x900
# ----------------
# Greedy not-diag [h1]:  3087  time:  0.161 s
# Greedy not-diag [h2]:  2539  time:  0.1321 s
# Greedy diag [h1]:      1983  time:  0.1861 s
# Greedy diag [h2]:      1716  time:  0.1455 s
# A* not-diag [h1]:      1843  time:  1.2397 s
# A* not-diag [h2]:      1843  time:  4.9112 s
# A* diag [h1]:          1355  time:  0.161 s
# A* diag [h2]:          1223  time:  2.6558 s
