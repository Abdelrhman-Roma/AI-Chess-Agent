def heuristics_2(board_obj):
    white_position_score=0#قيمه الابيض الاوليه 
    black_position_score=0#قيمه الاسود الاوليه 
    matrix = board_obj.board# هنا بستدعي البورد
#دي القيم بتاعت اماكن كل قطعه 
    PAWN_TABLE = [
        [ 0,  0,  0,  0,  0,  0,  0,  0],
        [50, 50, 50, 50, 50, 50, 50, 50],
        [10, 10, 20, 30, 30, 20, 10, 10],
        [ 5,  5, 10, 25, 25, 10,  5,  5],
        [ 0,  0,  0, 20, 20,  0,  0,  0],
        [ 5, -5,-10,  0,  0,-10, -5,  5],
        [ 5, 10, 10,-20,-20, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ]
    KNIGHT_TABLE = [
        [-50,-40,-30,-30,-30,-30,-40,-50],
        [-40,-20,  0,  0,  0,  0,-20,-40],
        [-30,  0, 10, 15, 15, 10,  0,-30],
        [-30,  5, 15, 20, 20, 15,  5,-30],
        [-30,  0, 15, 20, 20, 15,  0,-30],
        [-30,  5, 10, 15, 15, 10,  5,-30],
        [-40,-20,  0,  5,  5,  0,-20,-40],
        [-50,-40,-30,-30,-30,-30,-40,-50]
    ]
    ROOK_TABLE = [
        [ 0,  0,  0,  5,  5,  0,  0,  0],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [-5,  0,  0,  0,  0,  0,  0, -5],
        [ 5, 10, 10, 10, 10, 10, 10,  5],
        [ 0,  0,  0,  0,  0,  0,  0,  0]
    ]
    BISHOP_TABLE = [
        [-20,-10,-10,-10,-10,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5, 10, 10,  5,  0,-10],
        [-10,  5,  5, 10, 10,  5,  5,-10],
        [-10,  0, 10, 10, 10, 10,  0,-10],
        [-10, 10, 10, 10, 10, 10, 10,-10],
        [-10,  5,  0,  0,  0,  0,  5,-10],
        [-20,-10,-10,-10,-10,-10,-10,-20]
    ]
    QUEEN_TABLE = [
        [-20,-10,-10, -5, -5,-10,-10,-20],
        [-10,  0,  0,  0,  0,  0,  0,-10],
        [-10,  0,  5,  5,  5,  5,  0,-10],
        [ -5,  0,  5,  5,  5,  5,  0, -5],
        [  0,  0,  5,  5,  5,  5,  0, -5],
        [-10,  5,  5,  5,  5,  5,  0,-10],
        [-10,  0,  5,  0,  0,  0,  0,-10],
        [-20,-10,-10, -5, -5,-10,-10,-20]
    ]
    KING_TABLE = [
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-30,-40,-40,-50,-50,-40,-40,-30],
        [-20,-30,-30,-40,-40,-30,-30,-20],
        [-10,-20,-20,-20,-20,-20,-20,-10],
        [ 20, 20,  0,  0,  0,  0, 20, 20],
        [ 20, 30, 10,  0,  0, 10, 30, 20]
    ]
# ده قاموس عشان اربط بالقيم و القطع الي على البورد 
    tables = {
        'p': PAWN_TABLE,
        'n': KNIGHT_TABLE,
        'b': BISHOP_TABLE,
        'r': ROOK_TABLE,
        'q': QUEEN_TABLE,
        'k': KING_TABLE
    }
#فور لوب بحسب بيها قيم الابيض و الاسود 
    for r in range(8):
        for c in range(8):
            piece = matrix[r][c]
            if piece == "":
                continue
                
            color = piece[0]  
            ptype = piece[1]  
            if color == 'w':
                white_position_score += tables[ptype][r][c]
            else:
                black_position_score += tables[ptype][7 - r][c]

   #القيمه النهاءيه لو موجب يبقا الابيض كسبان لو سالب الاسود كسبان 
    return white_position_score - black_position_score


from game.rules import get_valid_moves

# ============================================
# Heuristic 3: Advanced Evaluation Function
# ============================================

def heuristics_3(board_obj):
    board = board_obj.board

    # =========================
    # 1. PIECE VALUES (centipawns)
    # =========================
    values = {
        'p': 100,
        'n': 320,
        'b': 330,
        'r': 500,
        'q': 900,
        'k': 0
    }

    # =========================
    # 2. CENTER SQUARES
    # =========================
    center_squares = [(3,3), (3,4), (4,3), (4,4)]

    # =========================
    # 3. TRACKING VARIABLES
    # =========================
    material_score = 0
    center_score = 0
    pawn_structure_score = 0
    bishop_count = {'w': 0, 'b': 0}
    king_pos = {'w': None, 'b': None}
    pawns = {'w': [], 'b': []}

    # =========================
    # 4. BOARD SCAN
    # =========================
    for r in range(8):
        for c in range(8):
            piece = board[r][c]
            if piece == "":
                continue

            color = piece[0]
            ptype = piece[1]
            val = values[ptype]

            # Material
            if color == 'w':
                material_score += val
            else:
                material_score -= val

            # Center control
            if (r, c) in center_squares:
                if color == 'w':
                    center_score += 10
                else:
                    center_score -= 10

            # Pawn tracking
            if ptype == 'p':
                pawns[color].append((r, c))

            # Bishop tracking
            if ptype == 'b':
                bishop_count[color] += 1

            # King position
            if ptype == 'k':
                king_pos[color] = (r, c)

    # =========================
    # 5. MOBILITY
    # =========================
    # NOTE: depends on your engine turn handling
    current_turn_moves = len(get_valid_moves(board_obj))

    # Flip turn to estimate opponent mobility
    board_obj.white_to_move = not board_obj.white_to_move
    opponent_moves = len(get_valid_moves(board_obj))
    board_obj.white_to_move = not board_obj.white_to_move

    mobility_score = 5 * (current_turn_moves - opponent_moves)

    # =========================
    # 6. PAWN STRUCTURE
    # =========================
    def evaluate_pawns(pawn_list):
        score = 0
        files = {}

        for r, c in pawn_list:
            # Count pawns per file
            files[c] = files.get(c, 0) + 1

        for r, c in pawn_list:
            # Doubled pawn
            if files[c] > 1:
                score -= 15

            # Isolated pawn
            if (c-1 not in files) and (c+1 not in files):
                score -= 10

        return score

    pawn_structure_score += evaluate_pawns(pawns['w'])
    pawn_structure_score -= evaluate_pawns(pawns['b'])

    # =========================
    # 7. BISHOP PAIR BONUS
    # =========================
    bishop_bonus = 0
    if bishop_count['w'] >= 2:
        bishop_bonus += 30
    if bishop_count['b'] >= 2:
        bishop_bonus -= 30

    # =========================
    # 8. KING SAFETY (simple version)
    # =========================
    def king_safety(king_position, color):
        if king_position is None:
            return 0

        r, c = king_position
        safety = 0

        # Check pawn shield (3 squares in front of king)
        direction = -1 if color == 'w' else 1

        for dc in [-1, 0, 1]:
            nr = r + direction
            nc = c + dc

            if 0 <= nr < 8 and 0 <= nc < 8:
                piece = board[nr][nc]
                if piece != "" and piece[0] == color and piece[1] == 'p':
                    safety += 10
                else:
                    safety -= 10

        return safety

    king_safety_score = king_safety(king_pos['w'], 'w') - king_safety(king_pos['b'], 'b')

    # =========================
    # 9. FINAL SCORE
    # =========================
    final_score = (
        material_score
        + center_score
        + mobility_score
        + pawn_structure_score
        + bishop_bonus
        + king_safety_score
    )

    return final_score