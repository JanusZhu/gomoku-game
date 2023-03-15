
import pygame
import numpy as np
import sys

BOARD_SIZE = 15
WIN_COUNT = 5
CELL_SIZE = 40
SCREEN_SIZE = (BOARD_SIZE * CELL_SIZE, BOARD_SIZE * CELL_SIZE + 60)  # Adjust the screen size
LINE_COLOR = (0, 0, 0)
BG_COLOR = (255, 255, 255)
PLAYER1_COLOR = (0, 0, 0)
PLAYER2_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 0, 0)
BUTTON_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)

class Button:
    def __init__(self, x, y, width, height, text, font_size):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font_size = font_size

    def draw(self, screen):
        pygame.draw.rect(screen, BUTTON_COLOR, self.rect)
        font = pygame.font.Font(None, self.font_size)
        text_surface = font.render(self.text, True, BUTTON_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

def draw_board(screen):
    board_pixel_size = BOARD_SIZE * CELL_SIZE

    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, board_pixel_size), 1)
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (board_pixel_size, i * CELL_SIZE), 1)

def draw_stones(screen, board):
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == 1:
                pygame.draw.circle(screen, PLAYER1_COLOR, (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)
            elif board[x][y] == 2:
                pygame.draw.circle(screen, PLAYER2_COLOR, (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 2 - 5)

def draw_winner(screen, winner):
    font = pygame.font.Font(None, 36)
    text = font.render(f"Player {winner} wins!", True, TEXT_COLOR)
    text_rect = text.get_rect(center=(SCREEN_SIZE[0] // 2, SCREEN_SIZE[1] // 2 - 20))
    screen.blit(text, text_rect)


def check_win(board, x, y, player):
    directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

    for dx, dy in directions:
        count = 1
        for i in range(1, WIN_COUNT):
            if (0 <= x + i * dx < BOARD_SIZE and 0 <= y + i * dy < BOARD_SIZE
                    and board[x + i * dx][y + i * dy] == player):
                count += 1
            else:
                break

        for i in range(1, WIN_COUNT):
            if (0 <= x - i * dx < BOARD_SIZE and 0 <= y - i * dy < BOARD_SIZE
                    and board[x - i * dx][y - i * dy] == player):
                count += 1
            else:
                break

        if count >= WIN_COUNT:
            return True

    return False



def play_gomoku():
    pygame.init()
    screen = pygame.display.set_mode(SCREEN_SIZE)  # Adjust the screen size
    pygame.display.set_caption("Gomoku")
    board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
    player = 1
    game_over = False
    winner = None
    history = []

    revert_button = Button(SCREEN_SIZE[0] // 2 - 110, SCREEN_SIZE[1] - 50, 100, 40, "Revert", 24)
    restart_button = Button(SCREEN_SIZE[0] // 2 + 10, SCREEN_SIZE[1] - 50, 100, 40, "Restart", 24)

    def reset_game():
        nonlocal board, player, winner, history
        board = np.zeros((BOARD_SIZE, BOARD_SIZE), dtype=int)
        player = 1
        winner = None
        history = []

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
                break

            if event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos

                if revert_button.is_clicked(event.pos) and len(history) > 0:
                    row, col = history.pop()
                    board[row][col] = 0
                    winner = None
                    player = 3 - player

                elif winner is None:
                    row, col = y // CELL_SIZE, x // CELL_SIZE

                    if board[row][col] == 0:
                        board[row][col] = player
                        history.append((row, col))

                        if check_win(board, row, col, player):
                            print(f"Player {player} wins!")
                            winner = player

                        player = 3 - player

                elif restart_button.is_clicked(event.pos):
                    reset_game()

        screen.fill(BG_COLOR)
        draw_board(screen)
        draw_stones(screen, board)
        if winner:
            draw_winner(screen, winner)
            restart_button.draw(screen)
        revert_button.draw(screen)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    play_gomoku()
