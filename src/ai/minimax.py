import math
import time

from game.rules import is_checkmate, is_stalemate

MATE_SCORE = 100000


# ============================================
# Terminal evaluation
# ============================================
def get_terminal_score(board, depth, evaluate):
    # White checkmated -> Black wins -> very good for AI (Black)
    if is_checkmate(board, "w"):
        return -MATE_SCORE + depth

    # Black checkmated -> White wins -> very bad for AI (Black)
    if is_checkmate(board, "b"):
        return MATE_SCORE - depth

    # Draw
    if is_stalemate(board, "w") or is_stalemate(board, "b"):
        return 0

    return evaluate(board)


# ============================================
# Minimax + Alpha-Beta
# ============================================
def minimax_alpha_beta(
    board,
    depth,
    alpha,
    beta,
    is_ai_turn,
    get_legal_moves,
    evaluate,
    is_game_over,
    start_time,
    time_limit,
):
    if time.time() - start_time > time_limit:
        return evaluate(board), None, True

    if depth == 0 or is_game_over(board):
        return get_terminal_score(board, depth, evaluate), None, False

    current_color = "b" if is_ai_turn else "w"
    moves = get_legal_moves(board, current_color)

    if not moves:
        return get_terminal_score(board, depth, evaluate), None, False

    def score_move(move):
        score = 0

        if getattr(move, "promotion", False):
            score += 200

        if getattr(move, "is_capture", False):
            score += 100

        if getattr(move, "is_castling", False):
            score += 50

        return score

    moves = sorted(moves, key=score_move, reverse=True)
    best_move = None

    # AI is Black, and evaluation is White-positive / Black-negative
    # so Black should minimize the score.
    if is_ai_turn:
        best_eval = math.inf

        for move in moves:
            board.make_move(move)
            try:
                eval_score, _, timed_out = minimax_alpha_beta(
                    board,
                    depth - 1,
                    alpha,
                    beta,
                    False,
                    get_legal_moves,
                    evaluate,
                    is_game_over,
                    start_time,
                    time_limit,
                )
            finally:
                board.undo_move()

            if timed_out:
                return best_eval, best_move, True

            if getattr(move, "is_capture", False):
                eval_score -= 30

            if eval_score < best_eval:
                best_eval = eval_score
                best_move = move

            beta = min(beta, best_eval)

            if beta <= alpha:
                break

        return best_eval, best_move, False

    # White should maximize the score.
    best_eval = -math.inf

    for move in moves:
        board.make_move(move)
        try:
            eval_score, _, timed_out = minimax_alpha_beta(
                board,
                depth - 1,
                alpha,
                beta,
                True,
                get_legal_moves,
                evaluate,
                is_game_over,
                start_time,
                time_limit,
            )
        finally:
            board.undo_move()

        if timed_out:
            return best_eval, best_move, True

        if getattr(move, "is_capture", False):
            eval_score += 30

        if eval_score > best_eval:
            best_eval = eval_score
            best_move = move

        alpha = max(alpha, best_eval)

        if beta <= alpha:
            break

    return best_eval, best_move, False


# ============================================
# Iterative deepening
# ============================================
def get_ai_move(board, get_legal_moves, evaluate, is_game_over, max_time=1.0):
    start_time = time.time()
    best_move = None
    depth = 1

    while True:
        if time.time() - start_time > max_time:
            break

        _, move, timed_out = minimax_alpha_beta(
            board,
            depth,
            -math.inf,
            math.inf,
            True,
            get_legal_moves,
            evaluate,
            is_game_over,
            start_time,
            max_time,
        )

        if timed_out:
            break

        if move is not None:
            best_move = move

        depth += 1

    return best_move
