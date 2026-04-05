import math
import copy


import math
import copy

def minimax_alpha_beta(board, depth, alpha, beta, is_ai_turn, get_legal_moves, evaluate, is_game_over):

    
    if depth == 0 or is_game_over(board):
        return evaluate(board), None

    best_move = None

    
    if is_ai_turn:
        max_eval = -math.inf

        for move in get_legal_moves(board, "b"):
            new_board = copy.deepcopy(board)
            new_board.move_piece(move)

            eval_score, _ = minimax_alpha_beta(
                new_board, depth - 1, alpha, beta, False,
                get_legal_moves, evaluate, is_game_over
            )

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, eval_score)

            if beta <= alpha:
                break  
        return max_eval, best_move

    
    else:
        min_eval = math.inf

        for move in get_legal_moves(board, "w"):
            new_board = copy.deepcopy(board)
            new_board.move_piece(move)

            eval_score, _ = minimax_alpha_beta(
                new_board, depth - 1, alpha, beta, True,
                get_legal_moves, evaluate, is_game_over
            )

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, eval_score)

            if beta <= alpha:
                break  

        return min_eval, best_move


def get_ai_move(board, get_legal_moves, evaluate, is_game_over, depth=3):

    _, best_move = minimax_alpha_beta(
        board,
        depth,
        -math.inf,
        math.inf,
        True,
        get_legal_moves,
        evaluate,
        is_game_over
    )

    return best_move