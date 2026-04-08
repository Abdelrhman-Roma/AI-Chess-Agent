import pygame

from ai.minimax import get_ai_move
from ai.heuristics import heuristics_1, heuristics_2, heuristics_3
from game.board import Board
from game.rules import get_legal_moves, is_checkmate, is_stalemate, is_in_check
from gui.assests import load_images
from gui.input_handler import handle_mouse_click

pygame.init()

# -------- SETTINGS --------
WIDTH, HEIGHT = 1000, 800
BOARD_WIDTH = 800
ROWS, COLS = 8, 8
SQUARE_SIZE = BOARD_WIDTH // COLS

WHITE_SQUARE = (238, 238, 210)
GREEN_SQUARE = (118, 150, 86)
SIDE_PANEL_COLOR = (30, 30, 30)
MENU_BG = (20, 20, 20)
HOVER_COLOR = (255, 255, 0)
CHECK_COLOR = (255, 0, 0)
MOVE_HINT_COLOR = (0, 255, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Chess AI")

clock = pygame.time.Clock()
images = load_images(SQUARE_SIZE)


def create_game_state():
    return {
        "board_obj": Board(),
        "current_turn": "w",
        "game_over": False,
        "winner_text": "",
        "valid_moves": [],
        "selected_square": None,
        "difficulty": None,
        "game_started": False,
        "white_time": 600.0,
        "black_time": 600.0,
        "last_time": pygame.time.get_ticks(),
    }


state = create_game_state()


# -------- MENU --------
def draw_menu():
    screen.fill(MENU_BG)

    title_font = pygame.font.SysFont(None, 60)
    font = pygame.font.SysFont(None, 40)

    title = title_font.render("Choose Difficulty", True, (255, 255, 255))
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 180)))

    mouse_pos = pygame.mouse.get_pos()
    buttons = [
        ("Easy", (0, 255, 0), 320),
        ("Medium", (255, 255, 0), 400),
        ("Hard", (255, 0, 0), 480),
    ]

    rects = []
    for text, color, y in buttons:
        rect = pygame.Rect(0, 0, 250, 60)
        rect.center = (WIDTH // 2, y)

        fill_color = (70, 70, 70) if rect.collidepoint(mouse_pos) else (40, 40, 40)
        pygame.draw.rect(screen, fill_color, rect, border_radius=10)

        label = font.render(text, True, color)
        screen.blit(label, label.get_rect(center=rect.center))

        rects.append((rect, text.lower()))

    return rects


# -------- DRAW BOARD --------
def draw_board(board_obj):
    for r in range(ROWS):
        for c in range(COLS):
            color = WHITE_SQUARE if (r + c) % 2 == 0 else GREEN_SQUARE
            pygame.draw.rect(
                screen,
                color,
                (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            )

            piece = board_obj.board[r][c]
            if piece:
                image = images.get(piece)
                if image is not None:
                    screen.blit(image, (c * SQUARE_SIZE, r * SQUARE_SIZE))


# -------- HIGHLIGHTS --------
def highlight_moves(moves):
    for r, c in moves:
        pygame.draw.circle(
            screen,
            MOVE_HINT_COLOR,
            (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2),
            10,
        )


def highlight_check(board_obj, current_turn):
    if is_in_check(board_obj, current_turn):
        for r in range(8):
            for c in range(8):
                if board_obj.board[r][c] == current_turn + "k":
                    pygame.draw.rect(
                        screen,
                        CHECK_COLOR,
                        (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                        4,
                    )


def highlight_hover():
    x, y = pygame.mouse.get_pos()
    if 0 <= x < BOARD_WIDTH and 0 <= y < HEIGHT:
        r = y // SQUARE_SIZE
        c = x // SQUARE_SIZE
        pygame.draw.rect(
            screen,
            HOVER_COLOR,
            (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
            2,
        )


def highlight_last_move(board_obj):
    if board_obj.move_log:
        move = board_obj.move_log[-1][0]

        for r, c in (move.start, move.end):
            pygame.draw.rect(
                screen,
                HOVER_COLOR,
                (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE),
                4,
            )


# -------- TIME --------
def format_time(seconds):
    clamped = max(0, int(seconds))
    return f"{clamped // 60:02}:{clamped % 60:02}"


# -------- SIDE PANEL --------
def draw_side_panel(difficulty, white_time, black_time):
    pygame.draw.rect(screen, SIDE_PANEL_COLOR, (800, 0, 200, 800))

    font = pygame.font.SysFont(None, 32)

    mode = difficulty.upper() if difficulty else "SELECT"
    screen.blit(font.render(f"Mode: {mode}", True, (255, 255, 255)), (820, 50))
    screen.blit(
        font.render(f"White: {format_time(white_time)}", True, (200, 200, 200)),
        (820, 150),
    )
    screen.blit(
        font.render(f"Black: {format_time(black_time)}", True, (200, 200, 200)),
        (820, 200),
    )


# -------- TEXT --------
def draw_text(text):
    font = pygame.font.SysFont(None, 70)

    bg = pygame.Surface((600, 120))
    bg.set_alpha(200)
    bg.fill((0, 0, 0))

    rect = bg.get_rect(center=(BOARD_WIDTH // 2, HEIGHT // 2))
    screen.blit(bg, rect)

    render = font.render(text, True, CHECK_COLOR)
    screen.blit(render, render.get_rect(center=(BOARD_WIDTH // 2, HEIGHT // 2)))


def get_mouse_pos():
    x, y = pygame.mouse.get_pos()
    return y // SQUARE_SIZE, x // SQUARE_SIZE


def get_ai_settings(difficulty):
    if difficulty == "easy":
        return heuristics_1, 0.2
    if difficulty == "medium":
        return heuristics_2, 0.5
    return heuristics_3, 1.0


def is_terminal_state(board_obj):
    return (
        is_checkmate(board_obj, "w")
        or is_checkmate(board_obj, "b")
        or is_stalemate(board_obj, "w")
        or is_stalemate(board_obj, "b")
    )


def update_game_over_status(board_obj, current_turn):
    if is_checkmate(board_obj, current_turn):
        if current_turn == "w":
            return True, "BLACK WINS (CHECKMATE)"
        return True, "WHITE WINS (CHECKMATE)"

    if is_stalemate(board_obj, current_turn):
        return True, "DRAW (STALEMATE)"

    return False, ""


# -------- MAIN --------
def main():
    global state

    run = True

    while run:
        clock.tick(60)

        # -------- MENU --------
        if not state["game_started"]:
            rects = draw_menu()
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    for rect, level in rects:
                        if rect.collidepoint(event.pos):
                            state = create_game_state()
                            state["difficulty"] = level
                            state["game_started"] = True
                            state["last_time"] = pygame.time.get_ticks()
                            break

            continue

        # -------- TIMER --------
        now = pygame.time.get_ticks()
        delta = (now - state["last_time"]) / 1000.0
        state["last_time"] = now

        if not state["game_over"]:
            if state["current_turn"] == "w":
                state["white_time"] -= delta
            else:
                state["black_time"] -= delta

        # -------- TIME END --------
        if state["white_time"] <= 0:
            state["white_time"] = 0
            state["winner_text"] = "BLACK WINS (TIME)"
            state["game_over"] = True
        elif state["black_time"] <= 0:
            state["black_time"] = 0
            state["winner_text"] = "WHITE WINS (TIME)"
            state["game_over"] = True

        # -------- CHECK GAME END --------
        if not state["game_over"]:
            state["game_over"], state["winner_text"] = update_game_over_status(
                state["board_obj"],
                state["current_turn"],
            )

        # -------- DRAW --------
        draw_board(state["board_obj"])
        highlight_moves(state["valid_moves"])
        highlight_last_move(state["board_obj"])
        highlight_hover()
        highlight_check(state["board_obj"], state["current_turn"])
        draw_side_panel(
            state["difficulty"],
            state["white_time"],
            state["black_time"],
        )

        if state["game_over"]:
            draw_text(state["winner_text"])

        pygame.display.flip()

        # -------- EVENTS --------
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            elif event.type == pygame.MOUSEBUTTONDOWN and not state["game_over"]:
                if state["current_turn"] == "w":
                    r, c = get_mouse_pos()
                    old_board = [row[:] for row in state["board_obj"].board]

                    state["selected_square"] = handle_mouse_click(
                        state["board_obj"],
                        state["selected_square"],
                        r,
                        c,
                        state["current_turn"],
                    )

                    if state["selected_square"]:
                        sr, sc = state["selected_square"]
                        legal_moves = get_legal_moves(state["board_obj"], state["current_turn"])
                        state["valid_moves"] = [
                            move.end for move in legal_moves if move.start == (sr, sc)
                        ]
                    else:
                        state["valid_moves"] = []

                    if old_board != state["board_obj"].board:
                        state["current_turn"] = "b"
                        state["selected_square"] = None
                        state["valid_moves"] = []

                        state["game_over"], state["winner_text"] = update_game_over_status(
                            state["board_obj"],
                            state["current_turn"],
                        )

        # -------- AI --------
        if state["current_turn"] == "b" and not state["game_over"]:
            eval_func, max_time = get_ai_settings(state["difficulty"])

            move = get_ai_move(
                state["board_obj"],
                get_legal_moves,
                eval_func,
                is_terminal_state,
                max_time,
            )

            if move is not None:
                state["board_obj"].make_move(move)

            state["current_turn"] = "w"
            state["selected_square"] = None
            state["valid_moves"] = []

            state["game_over"], state["winner_text"] = update_game_over_status(
                state["board_obj"],
                state["current_turn"],
            )

        if state["game_over"]:
            state["valid_moves"] = []
            state["selected_square"] = None

    pygame.quit()


if __name__ == "__main__":
    main()
