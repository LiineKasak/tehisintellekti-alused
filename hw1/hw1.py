from queue import Queue
import copy


class Graph:

    # every coordinate is made of x, y
    # y is the index of row in map and x is it's position from the left side of the map

    def __init__(self, map: list):
        """Class constructor."""
        self.width = len(map[0])
        self.height = len(map)
        self.map = [list(row) for row in map]
        self.visited_map = copy.deepcopy(self.map)

    def get_start_coords(self) -> tuple:
        for y, row in enumerate(self.map):
            if "s" in row:
                return row.index("s"), y

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

    def in_range(self, coords: tuple) -> bool:
        """Check if coordinate is in range of the map."""
        return 0 <= coords[0] < self.width and 0 <= coords[1] < self.height

    def is_not_lava(self, coords: tuple) -> bool:
        """Check if the coordinate is safe to visit - it's not lava."""
        return self.map[coords[1]][coords[0]] != "*"

    def get_current(self, coords: tuple) -> str:
        """Get string value of coordinate."""
        return str(self.map[coords[1]][coords[0]])

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


def bfs(graph: Graph, start: tuple):
    """Do breath first to find the Diamond (D) and print visited coordinates as a map."""
    if start is None:
        return

    frontier = Queue()
    frontier.put(start)
    came_from = {start: None}
    current = None

    while not frontier.empty():
        current = frontier.get()

        if graph.get_current(current) == "D":
            break

        graph.display_visited(current)

        for next in graph.neighbors(current):
            if next not in came_from:
                frontier.put(next)
                came_from[next] = current

    path = []
    while current != start:
        next = came_from[current]
        path.append(next)
        current = next
    return path


def find_and_display_path(map: list):
    """Do BFS and display the path."""
    graph = Graph(map)
    start = graph.get_start_coords()
    path = bfs(graph, start)
    graph.display_path(path)


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

find_and_display_path(lava_map2)

