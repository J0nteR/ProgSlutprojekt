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
        if "f" not in str(grid[user_input_y][user_input_x]):
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
                grid[y][x] = grid[y][x][0]+"c"
            
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

def flag(grid, pos_x, pos_y, flags_left):
    grid[pos_y][pos_x] = str(grid[pos_y][pos_x])
    
    if "f" in grid[pos_y][pos_x]:
        grid[pos_y][pos_x] = grid[pos_y][pos_x][0]
        flags_left += 1
    
    elif "c" not in grid[pos_y][pos_x]:
        grid[pos_y][pos_x] += "f"
        flags_left -= 1
    return flags_left

def won(grid):
    flagged = True
    cleared = True
    for row in grid:
        for cell in row:
            if cell == "x":
                flagged = False
            elif "x" not in str(cell) and "c" not in str(cell):
                cleared = False
    return flagged and cleared

# Frontend functions
def draw_square(color, column, row):
    pygame.draw.rect(screen, color, [(MARGIN + CELL_SIZE) * column + MARGIN,
                                    (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT,
                                    CELL_SIZE, CELL_SIZE])

def draw_num(grid, column, row):
    font = pygame.font.Font(None, 36)
    if str(grid[row][column][0]) == "1":
        text = font.render("1", True, BLUE)
    elif str(grid[row][column][0]) == "2":
        text = font.render("2", True, GREEN)
    elif str(grid[row][column][0]) == "3":
        text = font.render("3", True, RED)
    elif str(grid[row][column][0]) == "x":
        text = font.render("x", True, BLACK)
    else:
        text = font.render(str(grid[row][column][0]), True, PURPLE)
        
    text_rect = text.get_rect(center=((MARGIN + CELL_SIZE) * column + MARGIN + CELL_SIZE / 2,
                                        (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT + CELL_SIZE / 2))
    screen.blit(text, text_rect)

def draw_grid(grid):
    for row in range(SIZE):
        for column in range(SIZE):
            if "c" not in str(grid[row][column]) and "f" not in str(grid[row][column]):
                draw_square(WHITE, column, row)
            elif "c" in grid[row][column]:
                if "0" in grid[row][column]:
                    draw_square(GRAY, column, row)
                else:
                    draw_num(grid, column, row)
            elif "f" in grid[row][column]:
                font = pygame.font.Font(None, 36)
                text = font.render("f", True, BLACK)  # Access grid[row][column] directly
                text_rect = text.get_rect(center=((MARGIN + CELL_SIZE) * column + MARGIN + CELL_SIZE / 2,
                                                  (MARGIN + CELL_SIZE) * row + HEADER_HEIGHT + MARGIN + CELL_SIZE / 2))
                screen.blit(text, text_rect)
    pygame.display.flip()

def draw_header(elapsed_time, flags_left):
    screen.fill((255,255,255), pygame.Rect(0, 0, WIDTH, HEADER_HEIGHT))
    pygame.draw.circle(screen, (255,0,0), BUTTON_CENTRE, BUTTON_RADIUS)
    
    if SIZE < 5:
            font_size = 15
            margin = 10
    else:
            font_size = 25
            margin = 20
    font = pygame.font.Font(None, font_size)
    
    flags_text = font.render(f"Mines: {flags_left}", True, BLACK)
    time_text = font.render(f"Time: {elapsed_time:.2f}", True, BLACK)

    screen.blit(flags_text, (MARGIN, HEADER_HEIGHT-margin))
    screen.blit(time_text, (WIDTH-(font.size(f"Time: {elapsed_time:.2f}"))[0], HEADER_HEIGHT-margin))
    
    pygame.display.flip()

def animate_header_button():
    pygame.draw.circle(screen, (139,0,0), BUTTON_CENTRE, BUTTON_RADIUS)
    pygame.display.flip()
    time.sleep(0.5)
    pygame.draw.circle(screen, (255,0,0), BUTTON_CENTRE, BUTTON_RADIUS)
    pygame.display.flip()

def lose(grid):
    for row in range(SIZE):
        for column in range(SIZE):
            if grid[row][column] == "x":
                grid[row][column] = "xc"  # Reveal all mines
    draw_grid(grid)  # Update the grid display
    pygame.display.flip()
    
    click = False
    while not click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] - BUTTON_CENTRE[0])**2 + (pos[1] - BUTTON_CENTRE[1])**2 <= BUTTON_RADIUS**2:
                    animate_header_button()
                    click = True

def win():
    click = False
    while not click:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if (pos[0] - BUTTON_CENTRE[0])**2 + (pos[1] - BUTTON_CENTRE[1])**2 <= BUTTON_RADIUS**2:
                    animate_header_button()
                    click = True
                
    backend_grid = createMap(SIZE, NUM_X)
    add_numbers(backend_grid)

    screen.fill(BLACK)
    draw_grid(backend_grid)
    return backend_grid

def main():
    # Create backend grid
    backend_grid = createMap(SIZE, NUM_X)
    add_numbers(backend_grid)
    
    for row in backend_grid:
            print(row)
            
    # Draw grid
    screen.fill(BLACK)
    draw_grid(backend_grid)

    
    flags_left = NUM_X
    start_time = time.time()
    draw_header(start_time, flags_left)
    # Game loop
    while True:
        elapsed_time = time.time()-start_time
        draw_header(elapsed_time, flags_left)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if pos[1] > HEADER_HEIGHT:
                    column = pos[0] // (CELL_SIZE + MARGIN)
                    row = (pos[1]-HEADER_HEIGHT) // (CELL_SIZE + MARGIN)
                
                    if event.button == 1:
                        if is_bomb(backend_grid, column, row):
                            lose(backend_grid)  # Player loses
                            backend_grid = createMap(SIZE, NUM_X)  # Reset the game
                            add_numbers(backend_grid)
                            start_time = time.time()  # Reset the timer
                            flags_left = NUM_X
                        else:
                            clear(backend_grid, column, row)
                            remove_d(backend_grid)
                    elif event.button == 3:
                        flags_left = flag(backend_grid, column, row, flags_left)
                        
                        
                    print("")
                    for row in backend_grid:
                        print(row)
                    
                    draw_grid(backend_grid)
                    
                    if won(backend_grid):
                        end_time = time.time()
                        print(end_time-start_time)
                        backend_grid = win()
                        start_time = time.time()
                elif (pos[0] - BUTTON_CENTRE[0])**2 + (pos[1] - BUTTON_CENTRE[1])**2 <= BUTTON_RADIUS**2:
                    animate_header_button()
                    backend_grid = createMap(SIZE, NUM_X)
                    add_numbers(backend_grid)
                    screen.fill(BLACK)
                    draw_grid(backend_grid)
                    
                    start_time = time.time()
                    flags_left = NUM_X
                    draw_header(start_time, NUM_X)


if __name__ == "__main__":
    main()
