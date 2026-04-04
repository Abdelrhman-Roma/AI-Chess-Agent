from game.piece import pawn_moves
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
    

    return []
    # باقي القطع (rook / knight / bishop / queen / king)
    # لسه مش متطبقة، فبيرجع ليستة فاضية