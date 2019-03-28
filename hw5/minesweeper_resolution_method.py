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
        map_size = len(self.m_map)
        shift = [-1, 0, 1]
        for row_shift in shift:
            for col_shift in shift:
                if abs(col_shift) + abs(row_shift) == 0:
                    continue
                new_row = row_i + row_shift
                new_col = col_i + col_shift
                if not (0 <= new_row < map_size and 0 <= new_col < map_size):
                    continue
                if not self.m_map[new_row][new_col].isdigit():
                    unknowns.append(new_col + new_row * map_size)
        return unknowns


class ResolutionMethod:

    def __init__(self, kb):
        self.kb = kb

    def resolution(self, alpha: int, debug: bool):
        # alpha - literaal, mida tahame kontrollida. for example 9 or -9
        candidates = set(self.kb.copy() + [tuple([alpha])])
        processed = set()

        i = 0
        while len(candidates) != 0:
            if debug:
                print(f"Candidates: {candidates}")
            candidate = candidates.pop()
            for p in processed:
                if self.subsumes(candidate, p, debug):
                    continue
            for p in processed:
                resolvents = self.resolve(set(candidate), set(p), debug)
                for r in resolvents:
                    if len(r) == 0:
                        return True
                    candidates.add(r)
            processed.add(candidate)

            i += 1
            if i > 200:
                return False  # to stop endless loop in case of no contradiction found
        return False

    @staticmethod
    def subsumes(clause: tuple, subset: tuple, debug: bool):
        for i in subset:
            if i not in clause:
                return False
        if debug:
            print(f"{subset} subsumes {clause}")
        return True

    @staticmethod
    def resolve(clause1: set, clause2: set, debug: bool):
        if debug:
            print(f"Resolving {clause1} and {clause2}.. ", end="")
        resolvents = set()
        for p in clause1:
            if -p in clause2:
                temp1, temp2 = clause1.copy(), clause2.copy()
                temp1.remove(p)
                temp2.remove(-p)
                resolvents.add(tuple(temp1) + tuple(temp2))
        if len(resolvents) == 0:
            temp = set(tuple(clause1) + tuple(clause2))
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


if __name__ == '__main__':
    l1 = ["2.", ".."]
    check_minesweeper_index(l1, 1)  # not sure

    l2 = ["110",
          ".1.",
          "110"]
    check_minesweeper_index(l2, 3)  # yes
    check_minesweeper_index(l2, 5)  # no

    l3 = ["000.",
          "1211",
          "...."]
    check_minesweeper_index(l3, 8)  # yes

    l4 = ["....0",
          ".421.",
          ".100."]
    check_minesweeper_index(l4, 1)  # yes
