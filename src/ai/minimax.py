import math  # مكتبة فيها قيم زي اللانهاية
import copy  # علشان نعمل نسخة من البورد منغير ما نبوظ الأصل

def minimax_alpha_beta(board, depth, alpha, beta, is_ai_turn, get_legal_moves, evaluate, is_game_over):
    # دي الفانكشن الأساسية بتاعة الذكاء الاصطناعي (Minimax + Alpha Beta)

    if depth == 0 or is_game_over(board):
        # لو وصلنا لأقصى عمق أو اللعبة خلصت
        return evaluate(board), None  # نرجع تقييم البورد بس

    best_move = None  # هنخزن هنا أفضل حركة

    if is_ai_turn:
        # لو الدور بتاع الـ AI (الأسود)
        max_eval = -math.inf  # بنبدأ بأقل قيمة ممكنة

        for move in get_legal_moves(board, "b"):
            # نلف على كل الحركات الممكنة للأسود

            new_board = copy.deepcopy(board)  
            # نعمل نسخة من البورد علشان نجرب عليها

            new_board.move_piece(move)  
            # ننفذ الحركة

            eval_score, _ = minimax_alpha_beta(
                new_board, depth - 1, alpha, beta, False,
                get_legal_moves, evaluate, is_game_over
            )
            # ننزل مستوى أعمق في الشجرة

            if eval_score > max_eval:
                # لو لقينا تقييم أحسن
                max_eval = eval_score  
                best_move = move  

            alpha = max(alpha, eval_score)  
            # نحدث alpha

            if beta <= alpha:
                # لو حصل قطع (pruning)
                break  

        return max_eval, best_move  # نرجع أفضل نتيجة

    else:
        # دور اللاعب (الأبيض)
        min_eval = math.inf  # نبدأ بأكبر قيمة

        for move in get_legal_moves(board, "w"):
            # كل حركات الأبيض

            new_board = copy.deepcopy(board)  
            # ننسخ البورد

            new_board.move_piece(move)  
            # ننفذ الحركة

            eval_score, _ = minimax_alpha_beta(
                new_board, depth - 1, alpha, beta, True,
                get_legal_moves, evaluate, is_game_over
            )

            if eval_score < min_eval:
                # لو لقيت تقييم أقل (أسوأ للـ AI)
                min_eval = eval_score  
                best_move = move  

            beta = min(beta, eval_score)  
            # نحدث beta

            if beta <= alpha:
                # pruning
                break  

        return min_eval, best_move  


def get_ai_move(board, get_legal_moves, evaluate, is_game_over, depth=3):
    # دي الفانكشن اللي بنناديها علشان نجيب حركة الـ AI

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

    return best_move  # نرجع أفضل حركة