import math

def alpha_beta(board, depth, alpha, beta, maximizing_player,
               evaluate, get_moves, make_move):

    if depth == 0 or is_terminal(board):
        return evaluate(board)

    if maximizing_player:
        max_eval = -math.inf

        for move in get_moves(board):
            new_board = make_move(board, move)

            eval = alpha_beta(new_board, depth - 1, alpha, beta, False,
                              evaluate, get_moves, make_move)

            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)

            if beta <= alpha:
                break  # pruning

        return max_eval

    else:
        min_eval = math.inf

        for move in get_moves(board):
            new_board = make_move(board, move)

            eval = alpha_beta(new_board, depth - 1, alpha, beta, True,
                              evaluate, get_moves, make_move)

            min_eval = min(min_eval, eval)
            beta = min(beta, eval)

            if beta <= alpha:
                break  # pruning

        return min_eval


def is_terminal(board):
    return False