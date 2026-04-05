#----------Pawn Function---------------------------------
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
#----------------------------------------------------------------------------------------------
def rook_moves(board, row, col):
    # دي فانكشن بترجع كل الحركات الممكنة للـ rook

    piece = board[row][col]   # بنجيب القطعة
    moves = []                # ليستة الحركات

    directions = [
        (-1, 0),  # لفوق
        (1, 0),   # لتحت
        (0, -1),  # شمال
        (0, 1)    # يمين
    ]

    for dr, dc in directions:
        # بنلف على كل اتجاه

        r, c = row + dr, col + dc
        # أول خطوة في الاتجاه

        while 0 <= r < 8 and 0 <= c < 8:
            # طول ما احنا جوه البورد

            if board[r][c] == "":
                # لو المربع فاضي
                
                moves.append((r, c))  # نضيفه

            else:
                # لو في قطعة
                
                if board[r][c][0] != piece[0]:
                    # لو لونها مختلف (عدو)
                    
                    moves.append((r, c))  # نقدر ناكلها
                
                break
                # لازم نقف هنا (مش نعدي القطعة)

            r += dr
            c += dc
            # نكمل في نفس الاتجاه

    return moves
#------------------------------------------------------------------------------------------------------
def knight_moves(board, row, col):
    # دي فانكشن بترجع حركات الحصان

    piece = board[row][col]  # نجيب القطعة
    moves = []               # ليستة الحركات

    directions = [
        (-2, -1), (-2, 1),
        (-1, -2), (-1, 2),
        (1, -2), (1, 2),
        (2, -1), (2, 1)
    ]
    # كل الحركات الممكنة للحصان (L shape)

    for dr, dc in directions:
        r = row + dr
        c = col + dc
        # نحسب المكان الجديد

        if 0 <= r < 8 and 0 <= c < 8:
            # نتأكد جوه البورد

            if board[r][c] == "":
                # لو فاضي
                
                moves.append((r, c))

            elif board[r][c][0] != piece[0]:
                # لو قطعة عدو
                
                moves.append((r, c))

    return moves

#-------------------------------------------------------------------------------------------------------------
def bishop_moves(board, row, col):
    # دي فانكشن بترجع حركات الفيل

    piece = board[row][col]  # نجيب القطعة
    moves = []               # ليستة الحركات

    directions = [
        (-1, -1),  # فوق شمال
        (-1, 1),   # فوق يمين
        (1, -1),   # تحت شمال
        (1, 1)     # تحت يمين
    ]

    for dr, dc in directions:
        # نمشي في كل اتجاه قطري

        r, c = row + dr, col + dc

        while 0 <= r < 8 and 0 <= c < 8:
            # طول ما احنا جوه البورد

            if board[r][c] == "":
                # لو فاضي
                
                moves.append((r, c))

            else:
                # لو في قطعة
                
                if board[r][c][0] != piece[0]:
                    # لو عدو
                    
                    moves.append((r, c))
                
                break
                # نقف (مينفعش نعدي القطع)

            r += dr
            c += dc
            # نكمل في نفس الاتجاه

    return moves

#------------------------------------------------------------------------------------------------------------------------------
def queen_moves(board, row, col):
    # دي فانكشن حركات الوزير

    # الوزير = rook + bishop
    rook_part = rook_moves(board, row, col)
    bishop_part = bishop_moves(board, row, col)

    return rook_part + bishop_part
#------------------------------------------------------------------------------------------------------------------------------
def king_moves(board, row, col):
    # دي فانكشن حركات الملك

    piece = board[row][col]  # نجيب القطعة
    moves = []               # ليستة الحركات

    directions = [
        (-1, 0),  # فوق
        (1, 0),   # تحت
        (0, -1),  # شمال
        (0, 1),   # يمين
        (-1, -1), # فوق شمال
        (-1, 1),  # فوق يمين
        (1, -1),  # تحت شمال
        (1, 1)    # تحت يمين
    ]

    for dr, dc in directions:
        r = row + dr
        c = col + dc
        # نحسب المكان الجديد

        if 0 <= r < 8 and 0 <= c < 8:
            # نتأكد جوه البورد

            if board[r][c] == "":
                # لو فاضي
                
                moves.append((r, c))

            elif board[r][c][0] != piece[0]:
                # لو قطعة عدو
                
                moves.append((r, c))

    return moves