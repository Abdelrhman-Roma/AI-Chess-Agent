# from game.piece import pawn_moves , rook_moves ,knight_moves , bishop_moves ,queen_moves
from game.piece import *
from game.move import Move
# بنستورد فانكشن حركات البيدق من ملف تاني

def get_valid_moves(board,row,col):
    # دي فانكشن بترجع الحركات المتاحة لأي قطعة حسب مكانها

    piece = board[row][col]
    # بنجيب القطعة الموجودة في المكان ده

    if piece =="":
        # لو مفيش قطعة في المكان
        
        return []
        # مفيش حركات طبعًا

    #-------pawn---------

    if piece in ["wp" ,"bp"]:
        # لو القطعة بيدق (أبيض أو أسود)
        
        return pawn_moves(board ,row ,col)
        # ننادي فانكشن البيدق ونرجع الحركات بتاعته
    
    #---------rook-----------------
    elif piece in ["wr" ,"br"]:
        return rook_moves(board,row,col)    
    #---------knight--------------------
    elif piece in ["wn" , "bn"]:
        return knight_moves(board,row ,col)
    #-------------bishop-------------------
    elif piece in ["wb" ,"bb"]:
        return bishop_moves(board,row ,col)
    elif piece in ["wq" ,"bq"]:
        return queen_moves(board,row,col)
    elif piece in ["wk" ,"bk"]:
        return king_moves(board,row,col)
    return []
    # باقي القطع (rook / knight / bishop / queen / king)
  
def get_legal_moves(board_obj, color):
    # دي بترجع كل الحركات الممكنة لكل قطع لون معين

    board = board_obj.board
    moves = []

    for r in range(8):
        for c in range(8):
            piece = board[r][c]

            if piece != "" and piece[0] == color:
                # لو القطعة من نفس اللون

                valid = get_valid_moves(board, r, c)

                for (r2, c2) in valid:
                    moves.append(Move((r, c), (r2, c2)))

    return moves