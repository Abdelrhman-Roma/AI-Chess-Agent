import pygame  # بنستورد مكتبة pygame علشان نعمل الجرافيك

from ai.minimax import get_ai_move  # دي الفنكشن اللي بتخلي الـ AI يختار الحركة
from ai.evaluate import evaluate    # دي heuristic سهلة (Easy)
from ai.heuristics import heuristics_2  # دي heuristic أصعب شوية (Medium)

from gui.input_handler import handle_mouse_click  # دي بتتعامل مع ضغطات الماوس
from gui.assests import load_images  # دي بتحميل صور القطع
from game.board import Board  # ده كلاس البورد

from game.rules import (
    get_legal_moves,  # دي بترجع الحركات القانونية بس
    is_checkmate,     # هل في checkmate
    is_stalemate,     # هل في تعادل
    is_in_check       # هل الملك في خطر
)

pygame.init()  # بنشغل pygame

# -------- إعدادات الشاشة --------
width, height = 800, 800  # حجم الشاشة
rows, cols = 8, 8         # عدد الصفوف والأعمدة
square_size = width // cols  # حجم كل مربع

# -------- ألوان --------
white = (240, 217, 181)  # لون فاتح
brown = (181, 136, 99)   # لون غامق

# -------- إنشاء البورد --------
board_obj = Board()  # بنعمل بورد جديد

# -------- شاشة اللعبة --------
screen = pygame.display.set_mode((width, height))  # بنعمل الشاشة
pygame.display.set_caption("Chess Game")  # اسم اللعبة

clock = pygame.time.Clock()  # علشان نتحكم في السرعة
images = load_images(square_size)  # بنحمل صور القطع

# -------- حالة اللعبة --------
current_turn = "w"  # الأبيض يبدأ
game_over = False  # هل اللعبة خلصت
winner_text = ""   # النص اللي هيظهر لما حد يكسب
valid_moves = []   # الحركات الممكنة

# -------- الصعوبة --------
difficulty = None   # مستوى الصعوبة
game_started = False  # هل اللعبة بدأت ولا لسه

# ================== MENU ==================
def draw_menu():
    screen.fill((20, 20, 20))  # نخلي الخلفية سودا

    font = pygame.font.SysFont(None, 50)  # نوع الخط

    title = font.render("Choose Difficulty", True, (255, 255, 255))  # عنوان
    screen.blit(title, (230, 150))  # نحطه في الشاشة

    easy = font.render("1 - Easy", True, (0, 255, 0))  # اختيار سهل
    medium = font.render("2 - Medium", True, (255, 255, 0))  # متوسط
    hard = font.render("3 - Hard (Locked)", True, (255, 0, 0))  # صعب مقفول

    screen.blit(easy, (300, 300))    # نعرض easy
    screen.blit(medium, (300, 380))  # نعرض medium
    screen.blit(hard, (300, 460))    # نعرض hard

# ================== رسم البورد ==================
def draw_board():
    for row in range(rows):  # نلف على الصفوف
        for col in range(cols):  # نلف على الأعمدة
            color = white if (row + col) % 2 == 0 else brown  # نحدد اللون
            pygame.draw.rect(screen, color,
                             (col * square_size, row * square_size, square_size, square_size))  # نرسم المربع

            piece = board_obj.board[row][col]  # نجيب القطعة
            if piece != "":  # لو في قطعة
                screen.blit(images[piece],
                            (col * square_size, row * square_size))  # نرسمها

# ================== رسم النص ==================
def draw_text(text):
    font = pygame.font.SysFont(None, 60)  # حجم الخط
    render = font.render(text, True, (255, 0, 0))  # نحول النص لصورة
    rect = render.get_rect(center=(width // 2, height // 2))  # مكانه في النص
    screen.blit(render, rect)  # نعرضه

# ================== عرض الصعوبة ==================
def draw_difficulty():
    font = pygame.font.SysFont(None, 30)  # خط صغير

    if difficulty == "easy":  # لو easy
        text = "Mode: Easy"
    elif difficulty == "medium":  # لو medium
        text = "Mode: Medium"
    else:
        text = ""  # غير كده مفيش حاجة

    render = font.render(text, True, (0, 0, 0))  # نحول النص
    screen.blit(render, (10, 10))  # نعرضه فوق

# ================== الماوس ==================
def get_mouse_pos():
    x, y = pygame.mouse.get_pos()  # نجيب مكان الماوس
    return y // square_size, x // square_size  # نحوله لإحداثيات بورد

# ================== Highlight ==================
def highlight_square(row, col):
    pygame.draw.rect(screen, (0, 0, 255),
                     (col * square_size, row * square_size, square_size, square_size), 4)  # نحدد المربع

def highlight_moves(moves):
    for row, col in moves:  # لكل حركة
        pygame.draw.circle(
            screen,
            (0, 255, 0),  # لون أخضر
            (col * square_size + square_size // 2,
             row * square_size + square_size // 2),  # مركز الدائرة
            15  # حجمها
        )

def highlight_check():
    if is_in_check(board_obj, "w"):  # لو الأبيض في خطر
        draw_king("w")
    if is_in_check(board_obj, "b"):  # لو الأسود في خطر
        draw_king("b")

def draw_king(color):
    for r in range(8):  # نلف على الصفوف
        for c in range(8):  # نلف على الأعمدة
            if board_obj.board[r][c] == color + "k":  # لو ده الملك
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),  # لون أحمر
                    (c * square_size, r * square_size, square_size, square_size),
                    5  # سمك الإطار
                )

# ================== MAIN ==================
def main():
    global current_turn, game_over, winner_text  # متغيرات عامة
    global valid_moves, difficulty, game_started

    run = True  # تشغيل اللعبة
    selected_square = None  # المربع المختار

    while run:  # لوب اللعبة
        clock.tick(60)  # سرعة 60 فريم

        # -------- MENU --------
        if not game_started:  # لو اللعبة لسه مبدأتش
            draw_menu()  # ارسم المينيو
            pygame.display.update()  # حدث الشاشة

            for event in pygame.event.get():  # الأحداث
                if event.type == pygame.QUIT:
                    run = False  # خروج

                if event.type == pygame.KEYDOWN:  # لو ضغط زر
                    if event.key == pygame.K_1:
                        difficulty = "easy"  # easy
                        game_started = True  # نبدأ اللعبة

                    elif event.key == pygame.K_2:
                        difficulty = "medium"  # medium
                        game_started = True

                    elif event.key == pygame.K_3:
                        print("Hard Locked")  # مقفولة

            continue  # يرجع لأول اللوب

        # -------- GAME --------
        draw_board()  # رسم البورد
        highlight_moves(valid_moves)  # الحركات
        highlight_check()  # check
        draw_difficulty()  # عرض الصعوبة

        if selected_square:
            highlight_square(*selected_square)  # تحديد القطعة

        if game_over:
            draw_text(winner_text)  # عرض النتيجة

        pygame.display.update()  # تحديث الشاشة

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False  # خروج

            # اللاعب
            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if current_turn == "w":  # دور الأبيض
                    row, col = get_mouse_pos()  # مكان الكليك

                    old_board = [r[:] for r in board_obj.board]  # نسخة من البورد

                    selected_square = handle_mouse_click(
                        board_obj, selected_square, row, col
                    )

                    if selected_square:
                        r, c = selected_square

                        legal_moves = get_legal_moves(board_obj, current_turn)  # نجيب الحركات القانونية

                        valid_moves = []
                        for move in legal_moves:
                            if move.start == (r, c):
                                valid_moves.append(move.end)  # نضيف الحركات الخاصة بالقطعة

                    else:
                        valid_moves = []

                    if old_board != board_obj.board:  # لو حصلت حركة
                        valid_moves = []
                        current_turn = "b"  # دور AI

                        if is_checkmate(board_obj, "b"):
                            winner_text = "White Wins!"
                            game_over = True

                        elif is_stalemate(board_obj, "b"):
                            winner_text = "Draw!"
                            game_over = True

        # AI
        if current_turn == "b" and not game_over:

            if difficulty == "easy":
                evaluation_function = evaluate  # easy
            elif difficulty == "medium":
                evaluation_function = heuristics_2  # medium
            else:
                evaluation_function = evaluate

            ai_move = get_ai_move(
                board_obj,
                get_legal_moves,
                evaluation_function,
                lambda b: False,
                depth=2
            )

            if ai_move is not None:
                board_obj.move_piece(ai_move)  # ينفذ الحركة

            current_turn = "w"  # يرجع الدور

            if is_checkmate(board_obj, "w"):
                winner_text = "Black Wins!"
                game_over = True

            elif is_stalemate(board_obj, "w"):
                winner_text = "Draw!"
                game_over = True

    pygame.quit()  # قفل اللعبة

main()  # تشغيل