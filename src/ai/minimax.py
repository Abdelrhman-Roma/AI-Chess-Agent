import math
import time


# ============================================
# Minimax
# ============================================
def minimax_alpha_beta(board, depth, alpha, beta, is_ai_turn,
                       get_legal_moves, evaluate, is_game_over,
                       start_time, time_limit):

    # ⏱️ وقف لو الوقت خلص
    if time.time() - start_time > time_limit:
        return evaluate(board), None

    if depth == 0 or is_game_over(board):
        return evaluate(board), None

    moves = get_legal_moves(board, "b" if is_ai_turn else "w")

    if not moves:
        return evaluate(board), None

    best_move = moves[0]

    # ============================================
    # 🔥 Move Ordering (مهم جدًا)
    # ============================================
    def score_move(move):
        score = 0

        if getattr(move, "is_capture", False):
            score += 100

        if getattr(move, "promotion", False):
            score += 200

        return score

    moves.sort(key=score_move, reverse=True)

    # ============================================
    # MAX
    # ============================================
    if is_ai_turn:
        max_eval = -math.inf

        for move in moves:
            try:
                board.make_move(move)

                eval_score, _ = minimax_alpha_beta(
                    board, depth - 1, alpha, beta, False,
                    get_legal_moves, evaluate, is_game_over,
                    start_time, time_limit
                )

                if getattr(move, "is_capture", False):
                    eval_score += 30

            finally:
                board.undo_move()

            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move

            alpha = max(alpha, max_eval)

            if beta <= alpha:
                break

        return max_eval, best_move

    # ============================================
    # MIN
    # ============================================
    else:
        min_eval = math.inf

        for move in moves:
            try:
                board.make_move(move)

                eval_score, _ = minimax_alpha_beta(
                    board, depth - 1, alpha, beta, True,
                    get_legal_moves, evaluate, is_game_over,
                    start_time, time_limit
                )

                if getattr(move, "is_capture", False):
                    eval_score -= 30

            finally:
                board.undo_move()

            if eval_score < min_eval:
                min_eval = eval_score
                best_move = move

            beta = min(beta, min_eval)

            if beta <= alpha:
                break

        return min_eval, best_move


# ============================================
# 🎮 Iterative Deepening (🔥 السر الحقيقي)
# ============================================
def get_ai_move(board, get_legal_moves, evaluate, is_game_over, max_time=1.0):

    start_time = time.time()
    best_move = None
    depth = 1

    while True:
        # ⏱️ وقف لو الوقت خلص
        if time.time() - start_time > max_time:
            break

        score, move = minimax_alpha_beta(
            board,
            depth,
            -math.inf,
            math.inf,
            True,
            get_legal_moves,
            evaluate,
            is_game_over,
            start_time,
            max_time
        )

        # لو لقينا move نحفظه
        if move is not None:
            best_move = move

        depth += 1  # 🔥 نزود العمق تدريجي

    return best_move