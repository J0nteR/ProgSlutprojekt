import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

# Button dimensions
BUTTON_WIDTH = 200
BUTTON_HEIGHT = 50

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Main Menu")

# Function to create buttons
def draw_button(screen, color, x, y, width, height, text):
    pygame.draw.rect(screen, color, (x, y, width, height))
    
    font = pygame.font.Font(None, 36)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
    screen.blit(text_surface, text_rect)

# Main menu loop
def main_menu():
    size = "Medium"
    difficulty = "Medium"
    while True:
        screen.fill(WHITE)
        
        # Draw title and creator credits
        title_font = pygame.font.Font(None, 48)
        title_text = title_font.render("Minesweeper", True, BLACK)
        title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 50))
        screen.blit(title_text, title_text_rect)

        creator_font = pygame.font.Font(None, 24)
        creator_text = creator_font.render("Created by Jamal, Truls, & Jonathan", True, BLACK)
        creator_text_rect = creator_text.get_rect(center=(SCREEN_WIDTH / 2, 90))
        screen.blit(creator_text, creator_text_rect)
        
        # Draw buttons for size selection
        draw_button(screen, RED if size == "Small" else GRAY, SCREEN_WIDTH / 2 - 350, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "Small")
        draw_button(screen, RED if size == "Medium" else GRAY, SCREEN_WIDTH / 2 - 100, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "Medium")
        draw_button(screen, RED if size == "Big" else GRAY, SCREEN_WIDTH / 2 + 150, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "Big")

        # Draw buttons for difficulty selection
        draw_button(screen, RED if difficulty == "Easy" else GRAY, SCREEN_WIDTH / 2 - 350, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "Easy")
        draw_button(screen, RED if difficulty == "Medium" else GRAY, SCREEN_WIDTH / 2 - 100, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "Medium")
        draw_button(screen, RED if difficulty == "Hard" else GRAY, SCREEN_WIDTH / 2 + 150, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "Hard")

        # Draw button to start game
        draw_button(screen, GRAY, SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT, "Start Game")

        # Draw button for leaderboard
        draw_button(screen, GRAY, SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 450, BUTTON_WIDTH, BUTTON_HEIGHT, "Leaderboard")

        # Draw button to quit
        draw_button(screen, GRAY, SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 550, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Check if size button clicked
                size_buttons = [pygame.Rect(SCREEN_WIDTH / 2 - 350, 150, BUTTON_WIDTH, BUTTON_HEIGHT),
                                pygame.Rect(SCREEN_WIDTH / 2 - 100, 150, BUTTON_WIDTH, BUTTON_HEIGHT),
                                pygame.Rect(SCREEN_WIDTH / 2 + 150, 150, BUTTON_WIDTH, BUTTON_HEIGHT)]
                for i, button in enumerate(size_buttons):
                    if button.collidepoint(mouse_pos):
                        if i == 0:
                            size = "Small"
                        elif i == 1:
                            size = "Medium"
                        elif i == 2:
                            size = "Big"
                # Check if difficulty button clicked
                difficulty_buttons = [pygame.Rect(SCREEN_WIDTH / 2 - 350, 250, BUTTON_WIDTH, BUTTON_HEIGHT),
                                       pygame.Rect(SCREEN_WIDTH / 2 - 100, 250, BUTTON_WIDTH, BUTTON_HEIGHT),
                                       pygame.Rect(SCREEN_WIDTH / 2 + 150, 250, BUTTON_WIDTH, BUTTON_HEIGHT)]
                for i, button in enumerate(difficulty_buttons):
                    if button.collidepoint(mouse_pos):
                        if i == 0:
                            difficulty = "Easy"
                        elif i == 1:
                            difficulty = "Medium"
                        elif i == 2:
                            difficulty = "Hard"
                # Check if start game button clicked
                start_game_button = pygame.Rect(SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT)
                if start_game_button.collidepoint(mouse_pos):
                    if size is not None and difficulty is not None:
                        print("Starting game with size:", size, "and difficulty:", difficulty)
                        # Call your game start function here with size and difficulty as parameters
                # Check if leaderboard button clicked
                leaderboard_button = pygame.Rect(SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 450, BUTTON_WIDTH, BUTTON_HEIGHT)
                if leaderboard_button.collidepoint(mouse_pos):
                    print("Showing leaderboard")
                    # Call function to display leaderboard
                # Check if quit button clicked
                quit_button = pygame.Rect(SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 550, BUTTON_WIDTH, BUTTON_HEIGHT)
                if quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()
        
        pygame.display.flip()

# Run the main menu loop
if __name__ == "__main__":
    main_menu()
