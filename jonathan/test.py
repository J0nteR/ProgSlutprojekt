import pygame
import sys

# Initialize pygame
pygame.init()

# Load the top 5 high scores
with open("highscores.txt", "r") as f:
    LEADERS = [line.strip() for line in f.readlines()[:5]]

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Leaderboard")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 30)

# Define the margin from the top and bottom of the window
MARGIN = 100  # Adjust this value to increase or decrease the margin

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.fill(WHITE)
        
        # Display title
        title_y = MARGIN  # Y-position for the title is at the margin from the top
        draw_text('Leaderboard', font, BLACK, screen, WIDTH // 2, title_y)
        
        # Display menu button on the same y-level as the leaderboard title
        menu_rect = pygame.Rect(WIDTH // 6 - 50, title_y - 25, 100, 50)
        pygame.draw.rect(screen, BLACK, menu_rect)
        draw_text('Menu', font, WHITE, screen, WIDTH // 6, title_y)
        
        # Calculate the available height between the title and the bottom margin
        available_height = HEIGHT - 2 * MARGIN  # The total height minus margins at the top and bottom
        
        # Calculate the spacing between the boxes and their heights
        box_height = 50  # Fixed height for each box
        space_between_boxes = (available_height - 5 * box_height) / 4  # Distribute space evenly between the boxes
        
        # Display top 5 high scores
        for i, leader in enumerate(LEADERS):
            # Calculate the y-position for each high score box
            y_pos = title_y + (i + 1) * (space_between_boxes + box_height)
            
            # Create a rectangle for each high score box
            highscore_rect = pygame.Rect(WIDTH // 2 - 100, y_pos, 200, box_height)
            
            # Draw the rectangle and the text
            pygame.draw.rect(screen, BLACK, highscore_rect)
            draw_text(leader, font, WHITE, screen, WIDTH // 2, y_pos + box_height / 2)
        
        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                # Check if the menu button was clicked
                if menu_rect.collidepoint(mouse_pos):
                    print("Menu button clicked.")
        
        pygame.display.update()

if __name__ == "__main__":
    main_menu()
