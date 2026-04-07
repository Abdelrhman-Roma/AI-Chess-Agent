import pygame  # استدعاء مكتبة pygame للرسم والتحكم
from ai.minimax import get_ai_move  # دالة الذكاء الصناعي
from ai.heuristics import heuristics_1, heuristics_2, heuristics_3  # دوال التقييم

from gui.input_handler import handle_mouse_click  # التعامل مع ضغط الماوس
from gui.assests import load_images  # تحميل صور القطع
from game.board import Board  # كلاس البورد

from game.rules import (
    get_legal_moves,  # الحركات القانونية
    is_checkmate,     # هل في مات
    is_stalemate,     # هل في تعادل
    is_in_check       # هل الملك في كش
)

pygame.init()  # تشغيل pygame

# -------- إعدادات الشاشة --------
width, height = 1000, 800  # حجم الشاشة
board_width = 800  # عرض البورد فقط

rows, cols = 8, 8  # عدد الصفوف والأعمدة
square_size = board_width // cols  # حجم كل مربع

white = (238, 238, 210)  # لون مربع أبيض
brown = (118, 150, 86)   # لون مربع بني

board_obj = Board()  # إنشاء البورد

screen = pygame.display.set_mode((width, height))  # إنشاء الشاشة
pygame.display.set_caption("Chess AI")  # اسم النافذة

clock = pygame.time.Clock()  # التحكم في الفريمات
images = load_images(square_size)  # تحميل صور القطع

current_turn = "w"  # الدور الحالي
game_over = False  # هل اللعبة انتهت
winner_text = ""  # نص الفائز
valid_moves = []  # الحركات المتاحة

difficulty = None  # مستوى اللعبة
game_started = False  # هل اللعبة بدأت

# -------- التايمر --------
white_time = 600  # وقت الأبيض 10 دقايق
black_time = 600  # وقت الأسود
last_time = pygame.time.get_ticks()  # آخر وقت


# -------- رسم المينيو (أزرار) --------
def draw_menu():
    screen.fill((20, 20, 20))  # خلفية سوداء

    title_font = pygame.font.SysFont(None, 60)  # خط كبير
    font = pygame.font.SysFont(None, 40)  # خط عادي

    # العنوان
    title = title_font.render("Choose Difficulty", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(width // 2, 180)))

    mouse_pos = pygame.mouse.get_pos()  # مكان الماوس

    buttons = [
        ("Easy", (0, 255, 0), 320),     # زر easy
        ("Medium", (255, 255, 0), 400), # زر medium
        ("Hard", (255, 0, 0), 480)      # زر hard
    ]

    button_rects = []

    for text, color, y in buttons:
        rect = pygame.Rect(0, 0, 250, 60)  # مستطيل الزر
        rect.center = (width // 2, y)

        # تأثير hover
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, (70, 70, 70), rect, border_radius=10)
        else:
            pygame.draw.rect(screen, (40, 40, 40), rect, border_radius=10)

        label = font.render(text, True, color)  # نص الزر
        screen.blit(label, label.get_rect(center=rect.center))

        button_rects.append((rect, text.lower()))  # حفظ الزر

    return button_rects


# -------- رسم البورد --------
def draw_board():
    for row in range(rows):
        for col in range(cols):
            color = white if (row + col) % 2 == 0 else brown  # تحديد اللون
            pygame.draw.rect(screen, color,
                             (col * square_size, row * square_size, square_size, square_size))

            piece = board_obj.board[row][col]  # القطعة
            if piece:
                screen.blit(images[piece],
                            (col * square_size, row * square_size))


# -------- highlight moves --------
def highlight_moves(moves):
    for row, col in moves:
        center = (
            col * square_size + square_size // 2,
            row * square_size + square_size // 2
        )
        pygame.draw.circle(screen, (0, 255, 0), center, 10)  # دايرة خضرا


# -------- hover effect --------
def highlight_hover():
    x, y = pygame.mouse.get_pos()
    if x < board_width:
        row = y // square_size
        col = x // square_size

        pygame.draw.rect(screen, (255, 255, 0),
                         (col * square_size, row * square_size, square_size, square_size), 2)


# -------- آخر حركة --------
def highlight_last_move():
    if board_obj.move_log:
        move = board_obj.move_log[-1][0]
        r, c = move.end

        pygame.draw.rect(screen, (255, 255, 0),
                         (c * square_size, r * square_size, square_size, square_size), 4)


# -------- تحويل الوقت mm:ss --------
def format_time(seconds):
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes:02}:{secs:02}"


# -------- side panel --------
def draw_side_panel():
    pygame.draw.rect(screen, (30, 30, 30), (800, 0, 200, 800))

    font = pygame.font.SysFont(None, 32)

    screen.blit(font.render(f"Mode: {difficulty.upper()}", True, (255, 255, 255)), (820, 50))

    screen.blit(font.render(f"White: {format_time(white_time)}", True, (200, 200, 200)), (820, 150))
    screen.blit(font.render(f"Black: {format_time(black_time)}", True, (200, 200, 200)), (820, 200))


# -------- رسم نص الفوز --------
def draw_text(text):
    font = pygame.font.SysFont(None, 60)
    render = font.render(text, True, (255, 0, 0))
    screen.blit(render, render.get_rect(center=(400, height // 2)))


# -------- مكان الماوس --------
def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    return y // square_size, x // square_size


# -------- main loop --------
def main():
    global current_turn, game_over, winner_text
    global valid_moves, difficulty, game_started
    global white_time, black_time, last_time

    run = True
    selected_square = None

    while run:
        clock.tick(60)

        # -------- المينيو --------
        if not game_started:
            button_rects = draw_menu()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()

                    for rect, level in button_rects:
                        if rect.collidepoint(mouse_pos):
                            difficulty = level
                            game_started = True
            continue

        # -------- تحديث الوقت --------
        current_time = pygame.time.get_ticks()
        delta = (current_time - last_time) / 1000
        last_time = current_time

        if not game_over:
            if current_turn == "w":
                white_time -= delta
            else:
                black_time -= delta

        # -------- انتهاء الوقت --------
        if white_time <= 0:
            winner_text = "Black Wins (Time)!"
            game_over = True
        elif black_time <= 0:
            winner_text = "White Wins (Time)!"
            game_over = True

        # -------- الرسم --------
        draw_board()
        highlight_moves(valid_moves)
        highlight_last_move()
        highlight_hover()
        draw_side_panel()

        if selected_square:
            pygame.draw.rect(screen, (0, 0, 255),
                             (selected_square[1] * square_size, selected_square[0] * square_size, square_size, square_size), 4)

        if game_over:
            draw_text(winner_text)

        pygame.display.update()

        # -------- events --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if current_turn == "w":
                    row, col = get_mouse_pos()

                    old_board = [r[:] for r in board_obj.board]

                    selected_square = handle_mouse_click(
                        board_obj, selected_square, row, col, current_turn
                    )

                    if selected_square:
                        r, c = selected_square
                        legal_moves = get_legal_moves(board_obj, current_turn)
                        valid_moves = [m.end for m in legal_moves if m.start == (r, c)]
                    else:
                        valid_moves = []

                    if old_board != board_obj.board:
                        current_turn = "b"

        # -------- AI --------
        if current_turn == "b" and not game_over:

            if difficulty == "easy":
                eval_func = heuristics_1
                max_time = 0.2
            elif difficulty == "medium":
                eval_func = heuristics_2
                max_time = 0.5
            else:
                eval_func = heuristics_3
                max_time = 1.2

            move = get_ai_move(board_obj, get_legal_moves, eval_func, lambda b: False, max_time)

            if move:
                board_obj.make_move(move)

            current_turn = "w"
            valid_moves = []

    pygame.quit()


main()