import math
import time

from game.rules import is_checkmate, is_stalemate

MATE_SCORE = 100000


# ==========================================================
# Helper Part: Terminal Evaluation
# ==========================================================
# الجزء ده مساعد للخوارزمية كلها
# بيحدد تقييم الوضع لو اللعبة انتهت:
# checkmate / stalemate / normal evaluation
# ==========================================================

def get_terminal_score(board, depth, evaluate):
    # لو الأبيض اتعمله checkmate
    # يبقى الأسود كسب
    if is_checkmate(board, "w"):
        return -MATE_SCORE + depth

    # لو الأسود اتعمله checkmate
    # يبقى الأبيض كسب
    if is_checkmate(board, "b"):
        return MATE_SCORE - depth

    # لو حصل تعادل
    if is_stalemate(board, "w") or is_stalemate(board, "b"):
        return 0

    # لو اللعبة لسه مستمرة
    return evaluate(board)


# ==========================================================
# =================== GAME TREE PART =======================
# ==========================================================
# مسؤول عن:
# 1. تحديد اللاعب الحالي
# 2. جلب الحركات القانونية
# 3. ترتيب الحركات
# 4. تجربة الحركة على البورد
# 5. الرجوع خطوة للخلف undo_move
# ==========================================================

def get_current_color(is_ai_turn):
    # AI هو الأسود
    # اللاعب الآخر هو الأبيض
    return "b" if is_ai_turn else "w"


def score_move(move):
    # بنستخدم الدالة دي لترتيب الحركات
    # عشان نجرب الحركات المهمة الأول
    score = 0

    if getattr(move, "promotion", False):
        score += 200

    if getattr(move, "is_capture", False):
        score += 100

    if getattr(move, "is_castling", False):
        score += 50

    return score


def get_ordered_moves(board, is_ai_turn, get_legal_moves):
    current_color = get_current_color(is_ai_turn)

    # كل حركة هنا تعتبر فرع في Game Tree
    moves = get_legal_moves(board, current_color)

    # ترتيب الحركات عشان البحث يكون أسرع
    moves = sorted(moves, key=score_move, reverse=True)

    return moves


# ==========================================================
# ==================== MINIMAX PART ========================
# ==========================================================
# مسؤول عن:
# 1. معرفة هل الدور Min ولا Max
# 2. اختيار أفضل evaluation
# 3. اختيار أفضل move
#
# في المشروع:
# Positive score = كويس للأبيض
# Negative score = كويس للأسود
#
# إذن:
# Black AI = Min Player
# White = Max Player
# ==========================================================

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
    # ======================================================
    # Helper Part: Time Limit
    # ======================================================

    if time.time() - start_time > time_limit:
        return evaluate(board), None, True

    # ======================================================
    # Helper Part: Stop Condition
    # ======================================================

    if depth == 0 or is_game_over(board):
        return get_terminal_score(board, depth, evaluate), None, False

    # ======================================================
    # GAME TREE PART
    # ======================================================
    # هنا بنجيب كل الحركات القانونية
    # كل move منهم يمثل فرع في شجرة الاحتمالات
    # ======================================================

    moves = get_ordered_moves(board, is_ai_turn, get_legal_moves)

    if not moves:
        return get_terminal_score(board, depth, evaluate), None, False

    best_move = None

    # ======================================================
    # MINIMAX PART: MIN PLAYER
    # ======================================================
    # لو الدور على الأسود AI
    # الأسود بيحاول يقلل score
    # ======================================================

    if is_ai_turn:
        best_eval = math.inf

        for move in moves:
            # ==================================================
            # GAME TREE PART
            # ==================================================
            # نجرب الحركة وننزل مستوى أعمق في الشجرة
            # ==================================================

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
                # GAME TREE PART
                # نرجع الحركة عشان نجرب فرع تاني
                board.undo_move()

            if timed_out:
                return best_eval, best_move, True

            # Bonus بسيط للحركات اللي فيها capture
            # لأن الأسود Min، بنقلل التقييم
            if getattr(move, "is_capture", False):
                eval_score -= 30

            # ==================================================
            # MINIMAX PART
            # ==================================================
            # الأسود يختار أقل evaluation
            # ==================================================

            if eval_score < best_eval:
                best_eval = eval_score
                best_move = move

            # ==================================================
            # ALPHA-BETA PART
            # ==================================================
            # في دور Min بنحدث beta
            # beta = أفضل أقل قيمة وصل لها Min
            # ==================================================

            beta = min(beta, best_eval)

            # ==================================================
            # ALPHA-BETA PRUNING
            # ==================================================
            # لو beta <= alpha
            # يبقى باقي الفروع مش هتغير القرار
            # ==================================================

            if beta <= alpha:
                break

        return best_eval, best_move, False

    # ======================================================
    # MINIMAX PART: MAX PLAYER
    # ======================================================
    # لو الدور على الأبيض
    # الأبيض بيحاول يكبر score
    # ======================================================

    best_eval = -math.inf

    for move in moves:
        # ======================================================
        # GAME TREE PART
        # ======================================================
        # نجرب حركة الأبيض وننزل مستوى أعمق
        # ======================================================

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
            # GAME TREE PART
            # نرجع الحركة عشان نجرب حركة تانية
            board.undo_move()

        if timed_out:
            return best_eval, best_move, True

        # Bonus بسيط للحركات اللي فيها capture
        # لأن الأبيض Max، بنزود التقييم
        if getattr(move, "is_capture", False):
            eval_score += 30

        # ======================================================
        # MINIMAX PART
        # ======================================================
        # الأبيض يختار أكبر evaluation
        # ======================================================

        if eval_score > best_eval:
            best_eval = eval_score
            best_move = move

        # ======================================================
        # ALPHA-BETA PART
        # ======================================================
        # في دور Max بنحدث alpha
        # alpha = أفضل أعلى قيمة وصل لها Max
        # ======================================================

        alpha = max(alpha, best_eval)

        # ======================================================
        # ALPHA-BETA PRUNING
        # ======================================================
        # لو beta <= alpha
        # يبقى مفيش داعي نكمل باقي الفروع
        # ======================================================

        if beta <= alpha:
            break

    return best_eval, best_move, False


# ==========================================================
# Helper Part: Iterative Deepening
# ==========================================================
# ده جزء مساعد مش من التقسيمة الأساسية
# بيشغل البحث بعمق 1 ثم 2 ثم 3...
# لحد ما الوقت يخلص
# ==========================================================

def get_ai_move(board, get_legal_moves, evaluate, is_game_over, max_time=1.0):
    start_time = time.time()

    best_move = None
    depth = 1

    while True:
        if time.time() - start_time > max_time:
            break

        # ======================================================
        # ALPHA-BETA START VALUES
        # ======================================================
        # alpha = -infinity
        # beta = +infinity
        # البداية من دور الأسود AI
        # ======================================================

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