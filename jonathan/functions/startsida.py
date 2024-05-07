import pygame 
import sys

# Initialize pygame
pygame.init()

# Top 5
with open("highscores.txt", "r") as f:
    LEADERS = [line.strip() for line in f.readlines()[:5]]
f.close

# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Leaderboard")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont(None, 30)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.center = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.fill(WHITE)
        draw_text('Leaderboard', font, BLACK, screen, WIDTH // 2, 100)

        #Main menu
        menu_rect = pygame.Rect(WIDTH // 6 - 50, 75, 100, 50)
        pygame.draw.rect(screen, BLACK, menu_rect)
        draw_text('Menu', font, WHITE, screen, WIDTH // 6, 100)

        #Leaders
        title_y = 100
        available_height = HEIGHT - 2 * 100
        box_height = 50
        space_between_boxes = (available_height - 5 * box_height) / 4  # Distribute space evenly between the boxes
 
        # Display top 5 high scores
        for i, leader in enumerate(LEADERS):
            # Calculate the y-position for each high score box
            y_pos = title_y + (i + 0.5) * (space_between_boxes + box_height)
            
            
            # Create a rectangle for each high score box
            highscore_rect = pygame.Rect(WIDTH // 2 - 100, y_pos, 200, box_height)
            
            # Draw the rectangle and the text
            pygame.draw.rect(screen, BLACK, highscore_rect)
            draw_text(leader, font, WHITE, screen, WIDTH // 2, y_pos + box_height / 2)
          
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if menu_rect.collidepoint(mouse_pos):
                    # Return to main menu
                    #Lägg till så man går till menyn
                    print("Starting game...")               

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
    
"""
        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 4 - 50, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text("User 1", font, WHITE, screen, WIDTH // 2, HEIGHT // 4)
        
                
        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text("User 2", font, WHITE, screen, WIDTH // 2, HEIGHT // 2)
        
        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text("User 3", font, WHITE, screen, WIDTH // 2, HEIGHT // 3)
        
        









        # Start Game button
        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 4 - 50, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('Start Game', font, WHITE, screen, WIDTH // 2, HEIGHT // 5)
        
        # Leaderboard button
        leaderboard_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, BLACK, leaderboard_rect)
        draw_text('Leaderboard', font, WHITE, screen, WIDTH // 2 , HEIGHT // 2 + 65)
        
        # Quit button
        quit_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
        pygame.draw.rect(screen, BLACK, quit_rect)
        draw_text('Quit', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 170)

        start_rect = pygame.Rect(WIDTH // 2 - 325 , HEIGHT // 3 - 20 , 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('easy mode', font, WHITE, screen, WIDTH // 3 -100, HEIGHT // 3)

        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 - 20, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('medium mode', font, WHITE, screen, WIDTH // 2, HEIGHT // 3)

        start_rect = pygame.Rect(WIDTH // 2 + 150, HEIGHT // 3 -20, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('hard morde', font, WHITE, screen, WIDTH // 2 + 250, HEIGHT // 3 )

        start_rect = pygame.Rect(WIDTH // 2 - 325 , HEIGHT // 3 - 20 , 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('small', font, WHITE, screen, WIDTH // 3 -100, HEIGHT // 3)

        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 3 - 20, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('medium', font, WHITE, screen, WIDTH // 2, HEIGHT // 3)

        start_rect = pygame.Rect(WIDTH // 2 + 150, HEIGHT // 3 -20, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('big', font, WHITE, screen, WIDTH // 2 + 250, HEIGHT // 3 )

"""