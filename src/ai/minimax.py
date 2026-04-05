import math
def minimax_alpha_beta(board, depth, alpha, beta, is_ai_turn,
                       get_legal_moves, evaluate, is_game_over):
    if depth == 0 or is_game_over(board):
        return evaluate(board), None

    best_move = None
    moves = get_legal_moves(board, "b" if is_ai_turn else "w")

    # 🔥 تحسين 1: ترتيب الحركات (الأهم الأول)
    def score_move(move):
        return getattr(move, "is_capture", False)
    moves.sort(key=score_move, reverse=True)

    if is_ai_turn:
        max_eval = -math.inf

        for move in moves:
            try:
                board.make_move(move)
                eval_score, _ = minimax_alpha_beta(
                    board, depth - 1, alpha, beta, False,
                    get_legal_moves, evaluate, is_game_over
                )
            finally:
                board.undo_move()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, max_eval)
            # 🔥 تحسين 2: pruning أسرع
            if beta <= alpha:
                break

        return max_eval, best_move

    else:
        min_eval = math.inf

        for move in moves:
            try:
                board.make_move(move)
                eval_score, _ = minimax_alpha_beta(
                    board, depth - 1, alpha, beta, True,
                    get_legal_moves, evaluate, is_game_over
                )
            finally:
                board.undo_move()

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, min_eval)
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
