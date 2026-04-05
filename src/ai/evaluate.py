def evaluate(board):
    # دي الفانكشن اللي بتقيم البورد

    values = {
        "p": 1,  # البيدق = 1
        "n": 3,  # الحصان = 3
        "b": 3,  # الفيل = 3
        "r": 5,  # القلعة = 5
        "q": 9,  # الوزير = 9
        "k": 0   # الملك = 0 (مش بيتحسب)
    }

    score = 0  # مجموع النقاط

    for row in board.board:  # نلف على كل صف
        for piece in row:    # نلف على كل قطعة

            if piece != "":  # لو في قطعة
                val = values[piece[1]]  # نجيب قيمتها

                if piece[0] == "b":
                    score += val  # نزود للأسود
                else:
                    score -= val  # نقلل للأبيض

    return score  # نرجع الفرق