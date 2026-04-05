# from game.piece import pawn_moves , rook_moves ,knight_moves , bishop_moves ,queen_moves
from game.piece import *
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
    # لسه مش متطبقة، فبيرجع ليستة فاضية