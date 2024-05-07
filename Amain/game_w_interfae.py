import pygame
import random
import sys
import time

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (192, 192, 192)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)


SIZE = 5
NUM_X = 2
CELL_SIZE = 40
MARGIN = 5
HEADER_HEIGHT = 50
WIDTH = SIZE * (CELL_SIZE + MARGIN) + MARGIN
HEIGHT = SIZE * (CELL_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
BUTTON_CENTRE = (WIDTH/2, HEADER_HEIGHT-30)
BUTTON_RADIUS = 20

tile_unknown = pygame.image.load('Amain/assets/TileUnknown.png')
tile_unknown = pygame.transform.scale(tile_unknown, (CELL_SIZE, CELL_SIZE))

tile_empty = pygame.image.load('Amain/assets/TileEmpty.png')
tile_empty = pygame.transform.scale(tile_empty, (CELL_SIZE, CELL_SIZE))

tile_exploded = pygame.image.load('Amain/assets/TileExploded.png') 
tile_exploded = pygame.transform.scale(tile_exploded, (CELL_SIZE, CELL_SIZE))

tile_flag = pygame.image.load('Amain/assets/TileFlag.png') 
tile_flag = pygame.transform.scale(tile_flag, (CELL_SIZE, CELL_SIZE))

tile_mine = pygame.image.load('Amain/assets/TileMine.png') 
tile_mine = pygame.transform.scale(tile_mine, (CELL_SIZE, CELL_SIZE))

tile_not_mine = pygame.image.load('Amain/assets/TileNotMine.png') 
tile_not_mine = pygame.transform.scale(tile_not_mine, (CELL_SIZE, CELL_SIZE))

tile_imgs = [pygame.image.load(f'Amain/assets/Tile{i}.png') for i in range(1, 8)]
for i in range(1,8):
    tile_imgs[i-1] = pygame.transform.scale(tile_imgs[i-1], (CELL_SIZE, CELL_SIZE))


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
            if "c" not in grid[y][x] and "f" not in grid[y][x]:
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
def draw_square(tile, column, row):
    if tile == "empty":
        img = tile_empty
    elif tile == "unknown":
        img = tile_unknown
    screen.blit(img, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                            (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))

def draw_num(grid, column, row):
    img = tile_imgs[int(grid[row][column][0])-1]
    
    screen.blit(img, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                            (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))

def draw_flag(column, row):
    img = tile_flag
    
    screen.blit(img, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                            (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))

def draw_grid(grid):
    for row in range(SIZE):
        for column in range(SIZE):
            if grid[row][column] == "xp":
                screen.blit(tile_exploded, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                            (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))
            elif grid[row][column] == "xc":
                screen.blit(tile_mine, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                            (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))
            elif "c" not in str(grid[row][column]) and "f" not in str(grid[row][column]):
                draw_square("unknown", column, row)
            elif "c" in grid[row][column]:
                if "0" in grid[row][column]:
                    draw_square("empty", column, row)
                else:
                    draw_num(grid, column, row)
            elif "f" in grid[row][column]:
                draw_flag(column, row)
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

def lose(grid, column, row):
    for row_tmp in range(SIZE):
        for column_tmp in range(SIZE):
            if grid[row_tmp][column_tmp] == "x":
                grid[row_tmp][column_tmp] = "xc"  # Reveal all mines
    grid[row][column] = "xp"
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

def save_time(name, game_time):
    game_time = "{:.3f}".format(game_time)
    
    with open('highscores.txt', 'r') as file:
        scores = file.readlines()
        
    scores.append(name + ": " + game_time + '\n')
    
    scores.sort(key=lambda x: float(x.split(': ')[1]))
    
    with open('highscores.txt', 'w') as file:
        file.writelines(scores)

def main():
    backend_grid = createMap(SIZE, NUM_X)
    add_numbers(backend_grid)
    
    for row in backend_grid:
            print(row)
            
    screen.fill(BLACK)
    draw_grid(backend_grid)

    
    flags_left = NUM_X
    start_time = 0
    first_press = True
    draw_header(start_time, flags_left)
    
    # Game loop
    while True:
        if not first_press:
            elapsed_time = time.time()-start_time
        else:
            elapsed_time = 0
        draw_header(elapsed_time, flags_left)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if first_press:
                    start_time = time.time()
                    first_press = False
                pos = pygame.mouse.get_pos()
                if pos[1] > HEADER_HEIGHT:
                    column = pos[0] // (CELL_SIZE + MARGIN)
                    row = (pos[1]-HEADER_HEIGHT) // (CELL_SIZE + MARGIN)
                
                    if event.button == 1:
                        if is_bomb(backend_grid, column, row):
                            lose(backend_grid, column, row)  # Player loses
                            backend_grid = createMap(SIZE, NUM_X)  # Reset the game
                            add_numbers(backend_grid)
                            first_press = True  # Reset the timer
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
                        draw_header(elapsed_time, flags_left)
                        
                        end_time = time.time()
                        game_time = end_time-start_time
                        save_time("user", game_time)

                        flags_left = NUM_X
                        backend_grid = win()
                        first_press = True
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
