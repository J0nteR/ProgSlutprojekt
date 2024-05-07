import pygame
import sys
sys.path.append(jonathan\createMap.py)
                import createMap
                
pygame.init()
size = 4
num_x = 10
screen_width = 1000
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Minesweeper')

WIDTH, HEIGHT = 800, 600
GRID_SIZE = 10
TILE_SIZE = WIDTH // GRID_SIZE

# Colors
WHITE = (255, 255, 255)
GRAY = (200, 200, 200)
RED = (255, 0, 0)

def createMap(size, num_x):
    grid = [[0 for _ in range(size)] for _ in range(size)] 
    coordinates = [(i, j) for i in range(size) for j in range(size)]
    random.shuffle(coordinates)
    for i in range(num_x):
        x, y = coordinates[i]
        grid[x][y] = 'x'  
    return grid


def draw_board(board):
    for row in(GRID_SIZE):
        for col in range(GRID_SIZE):
            tile = board[row][col]
            color = white if tile == 0 else gray
            pygame.draw.rect(screen, color, (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE))
            if tile == "x":  # Mine
                pygame.draw.circle(screen, RED, (col * TILE_SIZE + TILE_SIZE // 2, row * TILE_SIZE + TILE_SIZE // 2), TILE_SIZE // 4)


def main():
    board = create_board()
    place_mines(board, num_x)
    running = True
    
    while running:
    
        for event in pygame.event.get():
        
            if event.type == pygame.QUIT:
                pygame.quit()
            quit()
    #draw_board
    draw_board(board)

    #update display
    pygame.dispay.flip()
    

    pygame.display.update()