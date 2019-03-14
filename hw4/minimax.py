import random

PLAYER_1 = -1
PLAYER_2 = 1

ROLL = 0
PASS = 1


def pig_game(player1_func, player2_func) -> int:
    rolled = 0
    turn = PLAYER_2
    player1_points = player2_points = 0

    while player1_points < 100 and player2_points < 100:
        # print("Player 1 points:", player1_points, "Player 2 points:", player2_points, "holding", rolled)

        if turn == PLAYER_1:
            decision = player1_func(turn, rolled, player1_points, player2_points)
            if decision == PASS:
                # print("-- Player 1 decides to pass.")
                rolled = 0
                turn = PLAYER_2
            else:
                dieroll = random.randint(1, 6)
                # print("-- Player 1 rolled...", dieroll)
                if dieroll == 1:
                    player1_points -= rolled  # lose all points again
                    rolled = 0
                    turn = PLAYER_2
                else:
                    rolled += dieroll
                    player1_points += dieroll
        else:
            decision = player2_func(turn, rolled, player2_points, player1_points)
            if decision == PASS:
                # print("-- Player 2 decides to pass.")
                rolled = 0
                turn = PLAYER_1
            else:
                dieroll = random.randint(1, 6)
                # print("-- Player 2 rolled...", dieroll)
                if dieroll == 1:
                    player2_points -= rolled  # lose all points again
                    rolled = 0
                    turn = PLAYER_1
                else:
                    rolled += dieroll
                    player2_points += dieroll

    if player1_points >= 100:
        return PLAYER_1
    elif player2_points >= 100:
        return PLAYER_2


def dummy_ai(turn, rolled, my_points, opp_points):
    if rolled < 21:
        return ROLL
    else:
        return PASS


def minimax_ai(turn: int, rolled: int, my_points: int, opp_points: int) -> int:
    # this is the top level of search
    # we search all possible moves
    # (PASS and ROLL in case of the Pig game)
    # and pick the one that returns the highest minimax estimate
    pass_value = exp_minimax(-turn, False, 0, my_points, opp_points)
    roll_value = exp_minimax(turn, True, rolled, my_points, opp_points)
    # print(f"MINIMAX_AI------- pass value: {pass_value} roll_value: {roll_value}")
    return PASS if pass_value >= roll_value else ROLL


def exp_minimax(turn: int, chance: bool, rolled: int, my_points: int, opp_points: int, depth: int = 5) -> float:
    # update remaining depth as we go deeper in the search tree
    depth -= 1

    # case 1a: somebody won, stop searching
    # return a high value if AI wins, low if it loses.
    if my_points >= 100 > opp_points:
        return 2000
    elif opp_points >= 100 > my_points:
        return -2000

    # case 1b: out of depth, stop searching
    # return game state eval (should be between win and loss)
    elif depth == 0:
        return my_points - opp_points * 0.7

    # case 2: AI's turn (and NOT a chance node):
    # return max value of possible moves (recursively) - roll or pass
    if turn == PLAYER_1 and not chance:
        return max(exp_minimax(turn, True, rolled, my_points, opp_points, depth),  # ROLL
                   exp_minimax(-turn, False, 0, my_points, opp_points, depth))  # PASS

    # case 3: player's turn:
    # return min value (assume optimal action from player)
    if turn == PLAYER_2 and not chance:
        return min(exp_minimax(turn, True, rolled, my_points, opp_points, depth),  # ROLL
                   exp_minimax(-turn, False, 0, my_points, opp_points, depth))  # PASS

    # case 4: chance node:
    # return average of all dice rolls
    if chance:

        results = []

        if turn == PLAYER_1:
            results.append(exp_minimax(-turn, False, 0, my_points - rolled, opp_points, depth))
            for roll in [2, 3, 4, 5, 6]:
                results.append(exp_minimax(turn, True, rolled + roll, my_points + roll, opp_points, depth))
            return sum(results) / 6

        if turn == PLAYER_2:
            results.append(exp_minimax(-turn, False, 0, my_points, opp_points - rolled, depth))
            for roll in [2, 3, 4, 5, 6]:
                results.append(exp_minimax(turn, True, rolled + roll, my_points, opp_points + roll, depth))
            return sum(results) / 6


if __name__ == '__main__':
    player1_wins = player2_wins = 0
    nr_of_games = 200
    for i in range(nr_of_games):
        # print(f"Game {i + 1}: ", end='')
        result = pig_game(minimax_ai, dummy_ai)
        if result == PLAYER_1:
            # print("won")
            player1_wins += 1
    print(f"Minimax won {int(player1_wins * 100 / nr_of_games)}%")
