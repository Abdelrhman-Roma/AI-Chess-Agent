from game.rules import get_valid_moves
# بنستورد الفانكشن اللي بترجع الحركات المتاحة لأي قطعة

from game.move import Move
# بنستورد كلاس Move علشان نمثل الحركة

def handle_mouse_click(board_obj,selected_square,row,col):
    # دي الفانكشن اللي بتتعامل مع كل ضغطة ماوس
    
    board = board_obj.board
    # بنجيب البورد (المصفوفة)

    if not( 0 <= row < 8 and 0 <= col < 8):
        # لو الضغطه كانت بره البورد
        
        return selected_square
        # متغيرش أي حاجة

    if selected_square is None:
        # لو مفيش مربع متحدد قبل كده
        
        if board[row][col] != "":
            # ولو ضغطت على مربع فيه قطعة
            
            return(row ,col)
            # نختار المربع ده (يبقى selected)

    else:
        # لو كان في مربع متحدد قبل كده
        
        old_row , old_col = selected_square
        # ده مكان القطعة اللي اخترتها

        if (row,col) == selected_square:
            # لو ضغطت على نفس المربع تاني
            
            return None
            # نلغي الاختيار (deselect)

        valid_move = get_valid_moves(board,old_row,old_col)
        # نجيب الحركات المتاحة للقطعة

        if (row, col) in valid_move:
            # لو المكان اللي ضغطت عليه موجود ضمن الحركات الصح
            
            move = Move((old_row,old_col),(row , col))
            # نعمل object يمثل الحركة
            
            board_obj.move_piece(move)
            # ننفذ الحركة على البورد

        return None
        # بعد الحركة (أو حتى لو مش valid) نلغي الاختيار

    return selected_square
    # لو محصلش حاجة، نرجع نفس الاختيار زي ما هو