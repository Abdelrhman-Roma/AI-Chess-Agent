import math
from game.rules import get_legal_moves


def evaluate(board):
    piece_values = {
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
            if piece:
                value = piece_values.get(piece[1], 0)
                if piece[0] == "b":
                    score += value
                else:
                    score -= value

    return score


def alphabeta(board, depth, alpha, beta, is_maximizing):
    valid_moves = get_legal_moves(board, "b" if is_maximizing else "w")

    if depth == 0 or not valid_moves:
        return evaluate(board), None

    best_move = None

    if is_maximizing:
        best_score = -math.inf

        for move in valid_moves:
            try:
                board.make_move(move)
                score, _ = alphabeta(board, depth - 1, alpha, beta, False)
            finally:
                board.undo_move()

            if score > best_score:
                best_score = score
                best_move = move

            alpha = max(alpha, best_score)
            if beta <= alpha:
                break

        return best_score, best_move

    else:
        best_score = math.inf

        for move in valid_moves:
            try:
                board.make_move(move)
                score, _ = alphabeta(board, depth - 1, alpha, beta, True)
            finally:
                board.undo_move()

            if score < best_score:
                best_score = score
                best_move = move

            beta = min(beta, best_score)
            if beta <= alpha:
                break

        return best_score, best_move


def get_ai_move_alphabeta(board, depth=4):
    _, move = alphabeta(board, depth, -math.inf, math.inf, True)
    return move
