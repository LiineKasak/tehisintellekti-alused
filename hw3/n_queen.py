import random


class NQPosition:

    def __init__(self, n):
        self.n = n
        self.queens_with_rows = [random.randrange(self.n) for _ in range(self.n)]
        # every queen has it's own column, int in array is row position

    def value(self) -> int:
        # calculate number of conflicts (pairs of queens that can capture each other)
        value = 0
        for i, q in enumerate(self.queens_with_rows):
            for i2 in range(i + 1, self.n):
                q2 = self.queens_with_rows[i2]
                # captures horizontally (same row) or captures diagonally
                if q == q2 or abs(q - q2) == abs(i - i2):
                    value += 1
                    break
        return value

    def make_move(self, queen_to_move: int, move: int) -> None:
        self.queens_with_rows[queen_to_move] = move

    def best_move(self) -> tuple:
        # find the best move and the value function after making that move
        queen_to_move = 0
        best_move = 0
        value = self.value()

        for i, q in enumerate(self.queens_with_rows):
            for move in range(self.n):
                if move != q:  # new position not the same
                    self.make_move(i, move)
                    new_value = self.value()
                    if new_value < value:  # if better value, remember the move and queen
                        queen_to_move = i
                        best_move = move
                        value = new_value
                    self.make_move(i, q)  # restore position before move
        return queen_to_move, best_move, value

    def print_board(self) -> None:
        board = []
        for row in range(self.n):
            board_row = []
            for q in self.queens_with_rows:
                board_row.append('Q' if q == row else '.')
            board.append(board_row)

        print('\n'.join([''.join(row) for row in board]))
        print()


def hill_climbing(pos: NQPosition):
    curr_value = pos.value()
    while True:
        queen_to_move, move, new_value = pos.best_move()
        if new_value >= curr_value:
            # no improvement, give up
            return pos, curr_value
        else:
            # position improves, keep searching
            curr_value = new_value
            pos.make_move(queen_to_move, move)


def n_queen_problem(n: int):
    best_value = n
    try_nr = 1
    while best_value != 0:  # random restart
        print(f"Try {try_nr}:\n------")
        pos = NQPosition(n)
        print(f"Initial value {pos.value()}")
        best_pos, best_value = hill_climbing(pos)
        print(f"Final value {best_value}\n")
        if best_value == 0:
            pos.print_board()
        try_nr += 1
        if try_nr > 200:
            print(f"No solution for N={n} or unable to solve!")
            break


if __name__ == '__main__':
    n_queen_problem(8)
