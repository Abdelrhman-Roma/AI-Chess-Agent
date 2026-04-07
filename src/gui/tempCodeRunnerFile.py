import pygame
from ai.minimax import get_ai_move
from ai.heuristics import heuristics_1, heuristics_2, heuristics_3

from gui.input_handler import handle_mouse_click
from gui.assests import load_images
from game.board import Board

from game.rules import (
    get_legal_moves,
    is_checkmate,
    is_stalemate,
    is_in_check
)

pygame.init()

# -------- إعدادات --------
width, height = 1000, 800
board_width = 800

rows, cols = 8, 8
square_size = board_width // cols

white = (238, 238, 210)
brown = (118, 150, 86)

board_obj = Board()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess AI")

clock = pygame.time.Clock()
images = load_images(square_size)

current_turn = "w"
game_over = False
winner_text = ""
valid_moves = []

difficulty = None
game_started = False

# ⏱️ Timer (10 minutes)
white_time = 600
black_time = 600
last_time = pygame.time.get_ticks()


# ================= MENU =================
def draw_menu():
    screen.fill((20, 20, 20))
    font = pygame.font.SysFont(None, 50)

    title = font.render("Choose Difficulty", True, (255, 255, 255))
    screen.blit(title, (230, 150))

    screen.blit(font.render("1 - Easy", True, (0, 255, 0)), (300, 300))
    screen.blit(font.render("2 - Medium", True, (255, 255, 0)), (300, 380))
    screen.blit(font.render("3 - Hard", True, (0, 255, 255)), (300, 460))


# ================= BOARD =================
def draw_board():
    for row in range(rows):
        for col in range(cols):
            color = white if (row + col) % 2 == 0 else brown
            pygame.draw.rect(screen, color,
                             (col * square_size, row * square_size, square_size, square_size))

            piece = board_obj.board[row][col]
            if piece:
                screen.blit(images[piece],
                            (col * square_size, row * square_size))


# ================= HIGHLIGHTS =================
def highlight_moves(moves):
    for row, col in moves:
        center = (
            col * square_size + square_size // 2,
            row * square_size + square_size // 2
        )
        pygame.draw.circle(screen, (0, 255, 0), center, 10)


def highlight_hover():
    x, y = pygame.mouse.get_pos()
    if x < board_width:
        row = y // square_size
        col = x // square_size

        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (col * square_size, row * square_size, square_size, square_size),
            2
        )


def highlight_last_move():
    if board_obj.move_log:
        move = board_obj.move_log[-1][0]
        r, c = move.end

        pygame.draw.rect(
            screen,
            (255, 255, 0),
            (c * square_size, r * square_size, square_size, square_size),
            4
        )


# ================= TIMER FORMAT =================
def format_time(seconds):
    minutes = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{minutes:02}:{secs:02}"


# ================= SIDE PANEL =================
def draw_side_panel():
    panel_x = 820

    pygame.draw.rect(screen, (30, 30, 30), (800, 0, 200, 800))

    font = pygame.font.SysFont(None, 32)

    mode_text = f"Mode: {difficulty.upper()}"
    screen.blit(font.render(mode_text, True, (255, 255, 255)), (panel_x, 50))

    white_text = f"White: {format_time(white_time)}"
    black_text = f"Black: {format_time(black_time)}"

    screen.blit(font.render(white_text, True, (200, 200, 200)), (panel_x, 150))
    screen.blit(font.render(black_text, True, (200, 200, 200)), (panel_x, 200))


# ================= UI =================
def draw_text(text):
    font = pygame.font.SysFont(None, 60)
    render = font.render(text, True, (255, 0, 0))
    rect = render.get_rect(center=(400, height // 2))
    screen.blit(render, rect)


# ================= MOUSE =================
def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    return y // square_size, x // square_size


# ================= MAIN =================
def main():
    global current_turn, game_over, winner_text
    global valid_moves, difficulty, game_started
    global white_time, black_time, last_time

    run = True
    selected_square = None

    while run:
        clock.tick(60)

        # -------- MENU --------
        if not game_started:
            draw_menu()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        difficulty = "easy"
                        game_started = True
                    elif event.key == pygame.K_2:
                        difficulty = "medium"
                        game_started = True
                    elif event.key == pygame.K_3:
                        difficulty = "hard"
                        game_started = True
            continue

        # ⏱️ تحديث الوقت
        current_time = pygame.time.get_ticks()
        delta = (current_time - last_time) / 1000
        last_time = current_time

        if not game_over:
            if current_turn == "w":
                white_time -= delta
            else:
                black_time -= delta

        if white_time <= 0:
            winner_text = "Black Wins (Time)!"
            game_over = True
        elif black_time <= 0:
            winner_text = "White Wins (Time)!"
            game_over = True

        # -------- DRAW --------
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

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False

            # ===== PLAYER =====
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

                        if is_checkmate(board_obj, "b"):
                            winner_text = "White Wins!"
                            game_over = True
                        elif is_stalemate(board_obj, "b"):
                            winner_text = "Draw!"
                            game_over = True

        # ===== AI =====
        if current_turn == "b" and not game_over:

            if difficulty == "easy":
                evaluation_function = heuristics_1
                max_time = 0.2
            elif difficulty == "medium":
                evaluation_function = heuristics_2
                max_time = 0.5
            else:
                evaluation_function = heuristics_3
                max_time = 1.2

            ai_move = get_ai_move(
                board_obj,
                get_legal_moves,
                evaluation_function,
                lambda b: False,
                max_time=max_time
            )

            if ai_move:
                board_obj.make_move(ai_move)

            current_turn = "w"
            valid_moves = []  # 👈 مهم يمسح الدوائر بعد حركة AI

            if is_checkmate(board_obj, "w"):
                winner_text = "Black Wins!"
                game_over = True
            elif is_stalemate(board_obj, "w"):
                winner_text = "Draw!"
                game_over = True

    pygame.quit()


main()