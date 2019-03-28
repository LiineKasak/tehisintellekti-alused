import heapq


class MyHeap(object):

    def __init__(self, initial=None, key=lambda x: x):
        self.key = key
        if initial:
            self.data = [(key(item), tuple(sorted(item))) for item in initial]
            heapq.heapify(self.data)
        else:
            self.data = []

    def push(self, item):
        key = self.key(item)
        heapq.heappush(self.data, (key, item))

    def pop(self):
        return heapq.heappop(self.data)[1]

    def is_empty(self):
        return len(self.data) == 0


class MineSweeperKb:

    def __init__(self, minesweeper_map: list):
        self.m_map = minesweeper_map
        self.kb = []
        for row_i, row in enumerate(self.m_map):
            for col_i, col in enumerate(row):
                if col.isdigit() and col != 0:
                    self.kb += self.generate_kb_for_spot(row_i, col_i)

    def generate_kb_for_spot(self, row_i: int, col_i: int) -> list:
        neighbors = self.get_unknown_indices(row_i, col_i)
        mines_nr = int(self.m_map[row_i][col_i])

        n = len(neighbors)
        cnf = []
        for i in range(2 ** n):
            binform = "{:0{n}b}".format(i, n=n)
            ones = 0
            clause = []
            for j in range(n):
                if binform[j] == "1":
                    ones += 1
                    clause.append(-neighbors[j])
                else:
                    clause.append(neighbors[j])
            if ones != mines_nr:
                cnf.append(tuple(clause))
        return cnf

    def get_unknown_indices(self, row_i: int, col_i: int) -> list:
        unknowns = []
        map_height = len(self.m_map)
        map_width = len(self.m_map[0])
        shift = [-1, 0, 1]
        for row_shift in shift:
            for col_shift in shift:
                if abs(col_shift) + abs(row_shift) == 0:
                    continue
                new_row = row_i + row_shift
                new_col = col_i + col_shift
                if not (0 <= new_row < map_height and 0 <= new_col < map_width):
                    continue
                if not self.m_map[new_row][new_col].isdigit():
                    unknowns.append(1 + new_col + new_row * map_width)
        return unknowns


class ResolutionMethod:

    def __init__(self, kb):
        self.kb = kb

    def resolution(self, alpha: int, debug: bool):
        # alpha - literaal, mida tahame kontrollida. for example 9 or -9
        processed = set()
        candidates = MyHeap(set(self.kb.copy() + [tuple([alpha])]), key=len)

        i = 0
        while not candidates.is_empty():
            candidate = candidates.pop()
            if debug:
                print(f"\nCurrent: {candidate} Candidates: {candidates.data}\nProcessed: {processed}")
            subsumed = False
            for p in processed:
                if self.subsumes(candidate, p, debug):
                    subsumed = True
                    break
            if subsumed:
                continue
            for p in processed:
                resolvents = self.resolve(candidate, p, debug)
                for r in resolvents:
                    if len(r) == 0:
                        return True
                    candidates.push(tuple(sorted(r)))
            processed.add(candidate)

            i += 1
            if i > 200:
                return False  # to stop endless loop in case of no contradiction found
        return False

    @staticmethod
    def subsumes(clause: tuple, subset: tuple, debug: bool):
        for i in clause:
            if i not in subset:
                return False
        if debug:
            print(f"{clause} subsumes {subset}")
        return True

    @staticmethod
    def resolve(clause1: tuple, clause2: tuple, debug: bool):
        if debug:
            print(f"Resolving {clause1} and {clause2}.. ", end="")
        resolvents = set()
        resolved = set()
        for p in clause1:
            if -p in clause2:
                if p in resolved or -p in resolved:
                    continue
                resolved.add(p)
                temp = list(clause1 + clause2)
                while p in temp:
                    temp.remove(p)
                while -p in temp:
                    temp.remove(-p)
                resolvents.add(tuple(set(temp)))
        temp = sorted(set(clause1 + clause2))
        if len(resolvents) == 0 and temp != sorted(clause1) and temp != sorted(clause2):
            resolvents.add(tuple(temp))
        if debug:
            print(f"Resolvents: {resolvents}")
        return resolvents

    @staticmethod
    def is_tautology(clause: set):
        for i in clause:
            if -i in clause:
                return True
        return False


def check_minesweeper_index(minesweeper_map: list, alpha: int, debug: bool = False):
    print(f"Index: {alpha}, Map: {minesweeper_map}")
    minesweeper = MineSweeperKb(minesweeper_map)
    knowledge_base = minesweeper.kb
    print(f"kb: {knowledge_base}")
    resolution_method = ResolutionMethod(knowledge_base)

    is_mine = resolution_method.resolution(-alpha, debug)
    print(f"is mine: {is_mine}")
    if is_mine:
        print("Mine exists\n")
    else:
        is_not_mine = resolution_method.resolution(alpha, debug)
        print(f"is not mine: {is_not_mine}")

        if not is_mine and not is_not_mine:
            print("Not sure... Unable to resolve\n")
        else:
            print("No mine\n")


def check_all_cases():
    l1 = ["2.", ".."]
    check_minesweeper_index(l1, 2, True)  # not sure

    l2 = ["110",
          ".1.",
          "110"]
    check_minesweeper_index(l2, 4)  # yes
    check_minesweeper_index(l2, 6)  # no

    l3 = ["000.",
          "1211",
          "...."]
    check_minesweeper_index(l3, 9)  # yes

    l4 = ["....0",
          ".421.",
          ".100."]
    check_minesweeper_index(l4, 1)  # yes


if __name__ == '__main__':
    # check_all_cases()
    l3 = ["000.",
          "1211",
          "...."]
    check_minesweeper_index(l3, 11, True)  # yes
