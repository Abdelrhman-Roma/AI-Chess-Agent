from game.rules import get_valid_moves
from game.move import Move
def evaluate(board):
    values = {
        "p": 1,
        "n": 3,
        "b": 3,
        "r": 5,
        "q": 9,
        "k": 0
    }

    score = 0

    for row in board.board:
        for piece in row:
            if piece != "":
                val = values[piece[1]]

                if piece[0] == "b":
                    score += val
                else:
                    score -= val

    return score