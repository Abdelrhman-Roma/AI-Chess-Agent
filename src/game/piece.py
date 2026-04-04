def pawn_moves(board,row,col):
    # دي فانكشن بترجع كل الحركات الممكنة للبيدق حسب مكانه

    piece = board[row][col]  # بنجيب القطعة اللي في المكان ده
    moves =[]                # ليستة فاضية هنحط فيها الحركات

    #-------white pawn----------

    if piece == "wp":
        # لو القطعة بيدق أبيض

        if row -1 >= 0 and board[row - 1][col] == "":
            # يتحرك خطوة لقدام (لفوق) لو المكان فاضي
            
            moves.append((row-1 , col))  # نضيف الحركة

            if row == 6 and board[row  - 2][col] == "":
                # لو أول حركة ليه (في الصف 6)
                # يقدر يتحرك خطوتين لو الطريق فاضي
                
                moves.append((row -2 ,col))

        if row - 1 >= 0 and col - 1 >= 0:
            # نتاكد إننا جوه البورد (مش بره)
            
            if board[row -1][col -1] != "" and board[row -1][col -1][0] == "b":
                # لو في قطعة قدامه شمال وهي سوداء
                
                moves.append(( row-1 , col-1))  # ياكلها

        if row - 1 >=0 and col + 1 < 8:
            # نفس الكلام بس يمين
            
            if board[row -1][col + 1] != "" and board[row-1][col + 1][0] =="b":
                # لو في قطعة سوداء
                
                moves.append((row -1 , col +1))  # ياكلها

    #-----------black pawn            
    elif piece == "bp":
        # لو بيدق أسود

        # move forward 1
        if row + 1 < 8 and board[row + 1][col] == "":
            # يتحرك خطوة لقدام (لتحت)
            
            moves.append((row + 1, col))

            # move forward 2 (first move)
            if row == 1 and board[row + 2][col] == "":
                # لو أول حركة (في الصف 1)
                
                moves.append((row + 2, col))

        # capture left
        if row + 1 < 8 and col - 1 >= 0:
            # يتأكد إنه جوه البورد
            
            if board[row + 1][col - 1] != "" and board[row + 1][col - 1][0] == "w":
                # لو في قطعة بيضا
                
                moves.append((row + 1, col - 1))  # ياكلها

        # capture right
        if row + 1 < 8 and col + 1 < 8:
            # نفس الكلام يمين
            
            if board[row + 1][col + 1] != "" and board[row + 1][col + 1][0] == "w":
                # لو في قطعة بيضا
                
                moves.append((row + 1, col + 1))  # ياكلها

    return moves  # يرجع كل الحركات الممكنة