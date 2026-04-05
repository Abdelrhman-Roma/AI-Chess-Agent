import math
import copy


def minimax(board, depth, is_ai_turn, get_legal_moves, is_game_over):
    # Base case
    if depth == 0 or is_game_over(board):
        return evaluate(board), None

    best_move = None

    # دور الـ AI (الأسود) - Maximizer
    if is_ai_turn:
        max_eval = -math.inf

        for move in get_legal_moves(board, "b"):
            new_board = copy.deepcopy(board)
            new_board.move_piece(move)

            evalscore,  = minimax(new_board, depth - 1, False, get_legal_moves, is_game_over)

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

        return max_eval, best_move

    # دور اليوزر (الأبيض) - Minimizer
    else:
        min_eval = math.inf

        for move in get_legal_moves(board, "w"):
            new_board = copy.deepcopy(board)
            new_board.move_piece(move)

            evalscore,  = minimax(new_board, depth - 1, True, get_legal_moves, is_game_over)

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

        return min_eval, best_move


def get_ai_move(board, get_legal_moves, is_gameover, depth=4):
    , best_move = minimax(
        board,
        depth,
        True,
        get_legal_moves,
        is_game_over
    )
    return best_move