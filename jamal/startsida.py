import pygame 
import pygame
import sys

# Initialize pygame
pygame.init()

# svårhetsgrad


# Set up display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game Main Menu")

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
        draw_text('Main Menu', font, BLACK, screen, WIDTH // 2, HEIGHT // 8)
        
        # Start Game button
        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('Start Game', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + -30)
        
        # Leaderboard button
        leaderboard_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 50, 200, 50)
        pygame.draw.rect(screen, BLACK, leaderboard_rect)
        draw_text('Leaderboard', font, WHITE, screen, WIDTH // 2 , HEIGHT // 2 + 65)
        
        # Quit button
        quit_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 + 150, 200, 50)
        pygame.draw.rect(screen, BLACK, quit_rect)
        draw_text('Quit', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + 170)

        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('easy mode', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + -30)

        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('medium mode', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + -30)

        start_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2 - 50, 200, 50)
        pygame.draw.rect(screen, BLACK, start_rect)
        draw_text('hard morde', font, WHITE, screen, WIDTH // 2, HEIGHT // 2 + -30)


        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if start_rect.collidepoint(mouse_pos):
                    # Start game
                    # Add your code to start the game here
                    print("Starting game...")
                elif leaderboard_rect.collidepoint(mouse_pos):
                    # Leaderboard
                    # Add your code to show leaderboard here
                    print("Showing leaderboard...")
                elif quit_rect.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
