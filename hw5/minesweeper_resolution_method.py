class MineSweeperKb:

    def __init__(self, minesweeper_map: list):
        self.m_map = minesweeper_map
        self.kb = []
        for row_i, row in enumerate(self.m_map):
            for col_i, col in enumerate(row):
                if col.isdigit() and col != 0:
                    self.kb += self.generate_kb_for_spot(row_i, col_i)

    def generate_kb_for_spot(self, row_i: int, col_i: int) -> list:
        unknowns = self.get_unknown_indices(row_i, col_i)
        binary_combinations = self.get_all_binary_combinations(unknowns)

        mines_nr = int(self.m_map[row_i][col_i])
        if mines_nr == 0:
            return []
        binary_combinations = self.fix_combinations(binary_combinations, mines_nr)
        return binary_combinations

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

    @staticmethod
    def get_all_binary_combinations(unknowns) -> list:
        combinations = []
        for ind in range(2 ** len(unknowns)):
            binary_num = '{:0{}b}'.format(ind, len(unknowns))
            num = [x if binary_num[i - 1] == '0' else -x for i, x in enumerate(unknowns)]
            combinations.append(tuple(num))
        return combinations

    @staticmethod
    def fix_combinations(combinations: list, mines_nr: int) -> list:
        return [comb for comb in combinations if len([x for x in comb if x < 0]) != mines_nr]


class ResolutionMethod:

    def __init__(self, kb):
        self.kb = kb

    def resolution(self, alpha: int):
        # alpha - literaal, mida tahame kontrollida. for example 9 or -9
        candidates = set(self.kb + [tuple([alpha])])
        processed = set()

        i = 0
        while len(candidates) != 0:
            candidate = candidates.pop()
            for p in processed:
                if self.subsumes(p, candidate):
                    continue
            for p in processed:
                resolvents = self.resolve(candidate, p)
                for r in resolvents:
                    if len(r) == 0:
                        return True
                    candidates.add(r)
            processed.add(candidate)

            i += 1
            if i > 300:
                return False  # to stop endless loop in case of no contradiction found
        return False

    @staticmethod
    def subsumes(p: tuple, sub: tuple):
        for i in sub:
            if i not in p:
                return False
        #  print(f"{sub} subsumes {p}")
        return True

    @staticmethod
    def resolve(clause1: tuple, clause2: tuple):
        #  print(f"Resolving {clause1} and {clause2}.. ", end="")
        resolvents = set()
        resolvents.add(tuple(set(clause1 + clause2)))
        for p in clause1:
            if -p in clause2:
                temp = list(clause1 + clause2)
                temp.remove(p)
                temp.remove(-p)
                resolvents.add(tuple(temp))

        #  print(f"Resolvents: {resolvents}")
        return resolvents


if __name__ == '__main__':
    l1 = ["2.", ".."]
    l2 = ["110",
          ".1.",
          "110"]
    l3 = ["000.",
          "1211",
          "...."]
    l4 = ["....0",
          ".421.",
          ".100."]
    l5 = [".21",
          "11.",
          "01."]
    minesweeper = MineSweeperKb(l5)
    knowledge_base = minesweeper.kb
    print(f"Whole kb: {knowledge_base}")
    resolution_method = ResolutionMethod(knowledge_base)
    print(f"Resolution: {resolution_method.resolution(0)}")
