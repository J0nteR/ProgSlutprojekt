import pygame
import random
import sys
import time

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)

# Define constants
SIZE = 12
NUM_X = 20
CELL_SIZE = 40
MARGIN = 5
HEADER_HEIGHT = 50
WIDTH = SIZE * (CELL_SIZE + MARGIN) + MARGIN
HEIGHT = SIZE * (CELL_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
BUTTON_CENTRE = (WIDTH/2, HEADER_HEIGHT-30)
BUTTON_RADIUS = 20

# Define difficulty levels
DIFFICULTIES = {
    "easy": {"size": 8, "num_mines": 10},
    "medium": {"size": 12, "num_mines": 20},
    "hard": {"size": 16, "num_mines": 40}
}

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Main menu variables
menu_font = pygame.font.Font(None, 36)
input_font = pygame.font.Font(None, 24)
player_name = ""

def draw_main_menu():
    screen.fill(WHITE)
    menu_text = menu_font.render("Minesweeper", True, BLACK)
    menu_rect = menu_text.get_rect(center=(WIDTH/2, HEADER_HEIGHT/2))
    screen.blit(menu_text, menu_rect)

    # Draw difficulty selection buttons
    easy_button = pygame.Rect(100, 150, 200, 50)
    medium_button = pygame.Rect(100, 210, 200, 50)
    hard_button = pygame.Rect(100, 270, 200, 50)
    pygame.draw.rect(screen, BLACK, easy_button)
    pygame.draw.rect(screen, BLACK, medium_button)
    pygame.draw.rect(screen, BLACK, hard_button)

    easy_text = menu_font.render("Easy", True, WHITE)
    medium_text = menu_font.render("Medium", True, WHITE)
    hard_text = menu_font.render("Hard", True, WHITE)
    screen.blit(easy_text, (150, 165))
    screen.blit(medium_text, (140, 225))
    screen.blit(hard_text, (150, 285))

    # Player name input
    input_text = input_font.render("Enter your name:", True, BLACK)
    input_rect = input_text.get_rect(topleft=(50, 100))
    screen.blit(input_text, input_rect)

    name_text = input_font.render(player_name, True, BLACK)
    name_rect = name_text.get_rect(topleft=(50, 130))
    pygame.draw.rect(screen, BLACK, name_rect, 2)
    screen.blit(name_text, name_rect)

    pygame.display.flip()

def main_menu():
    global player_name
    draw_main_menu()

    # Define buttons here
    easy_button = pygame.Rect(100, 150, 200, 50)
    medium_button = pygame.Rect(100, 210, 200, 50)
    hard_button = pygame.Rect(100, 270, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if easy_button.collidepoint(pos):
                    start_game("easy")
                elif medium_button.collidepoint(pos):
                    start_game("medium")
                elif hard_button.collidepoint(pos):
                    start_game("hard")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                elif event.key == pygame.K_RETURN:
                    start_game("medium")  # Default to medium difficulty if no button clicked
                else:
                    player_name += event.unicode
                draw_main_menu()
        draw_main_menu()  # Added to update the menu continuously

def start_game(difficulty):
    global player_name
    size = DIFFICULTIES[difficulty]["size"]
    num_mines = DIFFICULTIES[difficulty]["num_mines"]

    # Your game initialization code here
    print(f"Starting game with difficulty: {difficulty}, grid size: {size}, mines: {num_mines}, and player name: {player_name}")

if __name__ == "__main__":
    main_menu()
