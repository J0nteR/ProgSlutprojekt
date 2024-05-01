import pygame
import random
import sys

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)

# Define constants
SIZE = 8
NUM_X = 10
CELL_SIZE = 40
MARGIN = 5
WIDTH = SIZE * (CELL_SIZE + MARGIN) + MARGIN
HEIGHT = SIZE * (CELL_SIZE + MARGIN) + MARGIN

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Minesweeper")

# Backend functions
def createMap(size, num_x):
    grid = [[0 for _ in range(size)] for _ in range(size)]
    coordinates = [(i, j) for i in range(size) for j in range(size)]
    random.shuffle(coordinates)
    for i in range(num_x):
        x, y = coordinates[i]
        grid[x][y] = 'x'
    return grid

def add_numbers(grid):
    mine = "x"
    row_length = len(grid)
    column_length = len(grid[0])

    row = 0
    while row < row_length:
        cell = 0
        while cell < column_length:
            mine_num = 0
            if grid[row][cell] != mine:
                if cell != 0 and grid[row][cell-1] == mine:
                    mine_num += 1
                if cell != column_length-1 and grid[row][cell+1] == mine:
                    mine_num += 1

                if row != 0 and cell != 0 and grid[row-1][cell-1] == mine:
                    mine_num += 1
                if row != 0 and grid[row-1][cell] == mine:
                    mine_num += 1
                if row != 0 and cell != column_length-1 and grid[row-1][cell+1] == mine:
                    mine_num += 1

                if row != row_length-1 and cell != 0 and grid[row+1][cell-1] == mine:
                    mine_num += 1
                if row != row_length-1 and grid[row+1][cell] == mine:
                    mine_num += 1
                if row != row_length-1 and cell != column_length-1 and grid[row+1][cell+1] == mine:
                    mine_num += 1

                grid[row][cell] = mine_num
            cell += 1
        row += 1
    
    return grid


def is_bomb(grid, user_input_x, user_input_y):
    if user_input_x > len(grid[0])-1:
        message = f"user_input_x cannot exceed the length of the array rows. user_input_x = {user_input_x}, length of array rows = {len(grid[0])-1}"
        raise IndexError(message)
    elif user_input_y > len(grid)-1:
        message = f"user_input_y cannot exceed the length of the array. user_input_y = {user_input_x}, length of array = {len(grid[0])-1}"
        raise IndexError(message)

    if grid[user_input_y][user_input_x] == "x":
        return True
    else:
        grid[user_input_y][user_input_x] = str(grid[user_input_y][user_input_x])
        grid[user_input_y][user_input_x] += "c"
        return False

def clear_around(grid, pos_x, pos_y):
    y = pos_y-1
    if y < 0:
        y = 0
        
    while y <= pos_y+1:
        x = pos_x-1
        if x < 0:
            x = 0
         
        while x <= pos_x+1:
            grid[y][x] = str(grid[y][x])
            if "c" not in grid[y][x]:
                grid[y][x] += "c"
            
            x += 1
            if x > len(grid[0])-1:
                break
            
        y += 1
        if y > len(grid)-1:
            break
        
    if "d" not in grid[pos_y][pos_x]:
        grid[pos_y][pos_x] += "d"

def clear(grid, pos_x, pos_y):
    if grid[pos_y][pos_x] == 0 or grid[pos_y][pos_x] == "0c" or grid[pos_y][pos_x] == "0cd":
        clear_around(grid, pos_x, pos_y)
    
    y = pos_y-1
    if y < 0:
        y = 0
        
    while y <= pos_y+1:
        x = pos_x-1
        if x < 0:
            x = 0
            
        while x <= pos_x+1:
            if grid[y][x] == "0c":
                clear_around(grid, x, y)
                clear(grid, x, y)
                
            x += 1
            if x > len(grid[0])-1:
                break
            
        y += 1
        if y > len(grid)-1:
            break  

def remove_d(grid):
    for row in grid:
        cell = 0
        while cell < len(row):
            if isinstance(row[cell], str) and 'd' in row[cell]:
                row[cell] = row[cell].replace('d', '')
            cell += 1

def flag(grid, pos_x, pos_y):
    grid[pos_y][pos_x] = str(grid[pos_y][pos_x])
    
    if "f" in grid[pos_y][pos_x]:
        grid[pos_y][pos_x] = grid[pos_y][pos_x][0]
    
    elif "c" not in grid[pos_y][pos_x]:
        grid[pos_y][pos_x] += "f"

def create_visible_grid(grid):
    visible_grid = []
    for row in grid:
        visible_row = []
        for cell in row:
            if 'c' in str(cell):
                visible_row.append(str(cell).replace('c', ''))
            elif "f" in str(cell):
                visible_row.append("f")
            elif isinstance(cell, int):
                visible_row.append('.')
            else:
                visible_row.append('.')
        visible_grid.append(visible_row)
    return visible_grid

# Frontend functions
def draw_grid(grid):
    for row in range(SIZE):
        for column in range(SIZE):
            color = WHITE
            if "c" not in str(grid[row][column]) and "f" not in str(grid[row][column]):
                pygame.draw.rect(screen, color, [(MARGIN + CELL_SIZE) * column + MARGIN,
                                                (MARGIN + CELL_SIZE) * row + MARGIN,
                                                CELL_SIZE, CELL_SIZE])
            elif "c" in grid[row][column]:
                font = pygame.font.Font(None, 36)
                text = font.render(str(grid[row][column][0]), True, BLACK)  # Access grid[row][column] directly
                text_rect = text.get_rect(center=((MARGIN + CELL_SIZE) * column + MARGIN + CELL_SIZE / 2,
                                                  (MARGIN + CELL_SIZE) * row + MARGIN + CELL_SIZE / 2))
                screen.blit(text, text_rect)
            elif "f" in grid[row][column]:
                print("hej")
                font = pygame.font.Font(None, 36)
                text = font.render("f", True, BLACK)  # Access grid[row][column] directly
                text_rect = text.get_rect(center=((MARGIN + CELL_SIZE) * column + MARGIN + CELL_SIZE / 2,
                                                  (MARGIN + CELL_SIZE) * row + MARGIN + CELL_SIZE / 2))
                screen.blit(text, text_rect)



def main():
    # Create backend grid
    backend_grid = createMap(SIZE, NUM_X)
    add_numbers(backend_grid)
    
    for row in backend_grid:
            print(row)
            
    # Draw grid
    screen.fill(BLACK)
    draw_grid(backend_grid)
    pygame.display.flip()

    # Game loop
    while True:
    
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                column = pos[0] // (CELL_SIZE + MARGIN)
                row = pos[1] // (CELL_SIZE + MARGIN)
                if event.button == 1:
                    if is_bomb(backend_grid, column, row):
                        pygame.quit()
                    else:
                        clear(backend_grid, column, row)
                        remove_d(backend_grid)
                elif event.button == 3:
                    flag(backend_grid, column, row)
                print("")
                for row in backend_grid:
                    print(row)
                draw_grid(backend_grid)
                pygame.display.flip()
   


if __name__ == "__main__":
    main()
