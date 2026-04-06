import pygame
from ai.minimax import get_ai_move
from ai.evaluate import evaluate
from ai.heuristics import heuristics_2

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
width, height = 800, 800
rows, cols = 8, 8
square_size = width // cols

white = (240, 217, 181)
brown = (181, 136, 99)

board_obj = Board()

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Chess Game")

clock = pygame.time.Clock()
images = load_images(square_size)

current_turn = "w"
game_over = False
winner_text = ""
valid_moves = []

difficulty = None
game_started = False

# ================= MENU =================
def draw_menu():
    screen.fill((20, 20, 20))
    font = pygame.font.SysFont(None, 50)

    title = font.render("Choose Difficulty", True, (255, 255, 255))
    screen.blit(title, (230, 150))

    easy = font.render("1 - Easy", True, (0, 255, 0))
    medium = font.render("2 - Medium", True, (255, 255, 0))
    hard = font.render("3 - Hard (Locked)", True, (255, 0, 0))

    screen.blit(easy, (300, 300))
    screen.blit(medium, (300, 380))
    screen.blit(hard, (300, 460))

# ================= BOARD =================
def draw_board():
    for row in range(rows):
        for col in range(cols):
            color = white if (row + col) % 2 == 0 else brown
            pygame.draw.rect(screen, color,
                             (col * square_size, row * square_size, square_size, square_size))

            piece = board_obj.board[row][col]
            if piece != "":
                screen.blit(images[piece],
                            (col * square_size, row * square_size))

# ================= TEXT =================
def draw_text(text):
    font = pygame.font.SysFont(None, 60)
    render = font.render(text, True, (255, 0, 0))
    rect = render.get_rect(center=(width // 2, height // 2))
    screen.blit(render, rect)

# ================= DIFFICULTY =================
def draw_difficulty():
    font = pygame.font.SysFont(None, 30)

    if difficulty == "easy":
        text = "Mode: Easy"
    elif difficulty == "medium":
        text = "Mode: Medium"
    else:
        text = ""

    render = font.render(text, True, (0, 0, 0))
    screen.blit(render, (10, 10))

# ================= MOUSE =================
def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    return y // square_size, x // square_size

# ================= HIGHLIGHT =================
def highlight_square(row, col):
    pygame.draw.rect(screen, (0, 0, 255),
                     (col * square_size, row * square_size, square_size, square_size), 4)

def highlight_moves(moves):
    for row, col in moves:
        pygame.draw.circle(
            screen,
            (0, 255, 0),
            (col * square_size + square_size // 2,
             row * square_size + square_size // 2),
            15
        )

def highlight_check():
    if is_in_check(board_obj, "w"):
        draw_king("w")
    if is_in_check(board_obj, "b"):
        draw_king("b")

def draw_king(color):
    for r in range(8):
        for c in range(8):
            if board_obj.board[r][c] == color + "k":
                pygame.draw.rect(
                    screen,
                    (255, 0, 0),
                    (c * square_size, r * square_size, square_size, square_size),
                    5
                )

# ================= MAIN =================
def main():
    global current_turn, game_over, winner_text
    global valid_moves, difficulty, game_started

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
                        print("Hard Locked")

            continue

        # -------- GAME --------
        draw_board()
        highlight_moves(valid_moves)
        highlight_check()
        draw_difficulty()

        if selected_square:
            highlight_square(*selected_square)

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
                        board_obj, selected_square, row, col
                    )

                    if selected_square:
                        r, c = selected_square
                        legal_moves = get_legal_moves(board_obj, current_turn)

                        valid_moves = []
                        for move in legal_moves:
                            if move.start == (r, c):
                                valid_moves.append(move.end)
                    else:
                        valid_moves = []

                    # لو حصلت حركة
                    if old_board != board_obj.board:
                        valid_moves = []
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
                evaluation_function = evaluate
            elif difficulty == "medium":
                evaluation_function = heuristics_2
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
                board_obj.make_move(ai_move)  # 🔥 أهم تعديل

            current_turn = "w"

            if is_checkmate(board_obj, "w"):
                winner_text = "Black Wins!"
                game_over = True
            elif is_stalemate(board_obj, "w"):
                winner_text = "Draw!"
                game_over = True

    pygame.quit()

main()