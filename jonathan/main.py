""" Description:
This code implements the Minesweeper game using the Pygame library. Here's an overview of what the code does:

1.Game Settings and Graphics Initialization: The code initializes settings for game size, colors, and graphics.
It also loads images for different types of routes.
2.Create and manage the game board: Functions to create the game board and place mines on it are created. There are also functions for laying
the numbers around mines to indicate how many mines are around each square.
3.User interaction: The code handles user interaction by letting the player left click
to reveal a square and right-click to mark a square as a potential mine by flagging.
4.Game logic: There are functions to control the game logic, such as checking the user
clicked on a mine and lost, or if all squares except the mines have been revealed and the player wins.
5.Main Menu and Leaderboard: The code also contains a main menu where the player can select game settings and start the game.
In addition, there is a leaderboard where the five best times are displayed depending on the game mode.
6.Error handling and menu handling: There are functions to handle errors, such as checking if the user has entered a valid name and chooses to launch the game without
to specify all necessary settings. Menu management features allow the player to return to the main menu from other parts of the game.

In summary, the code allows the player to play Minesweeper with different settings and offers a user-friendly interface for interaction.

Date:              2024-05-08
Author:            Truls borgvall, Jonathan Rönnäs och Jamal Mohammed
""" 

import pygame
import random
import sys
import time

# Initialize Pygame
pygame.init()

def game(size, difficulty, name):
    if size == "Small":
        SIZE = 5
        if difficulty == "Easy":
            MINES = 1
        elif difficulty == "Medium":
            MINES = 5
        elif difficulty == "Hard":
            MINES = 10
    elif size == "Medium":
        SIZE = 10
        if difficulty == "Easy":
            MINES = 8
        elif difficulty == "Medium":
            MINES = 15
        elif difficulty == "Hard":
            MINES = 30
    elif size == "Big":
        SIZE = 12
        if difficulty == "Easy":
            MINES = 13
        elif difficulty == "Medium":
            MINES = 20
        elif difficulty == "Hard":
            MINES = 30

    # Constants
    CELL_SIZE = 40
    MARGIN = 5
    HEADER_HEIGHT = 50
    WIDTH = SIZE * (CELL_SIZE + MARGIN) + MARGIN
    HEIGHT = SIZE * (CELL_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
    BUTTON_CENTRE = (WIDTH/2, HEADER_HEIGHT-30)
    BUTTON_RADIUS = 20
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    # Load & resize images
    tile_unknown = pygame.image.load("Amain/assets/TileUnknown.png")
    tile_unknown = pygame.transform.scale(tile_unknown, (CELL_SIZE, CELL_SIZE))

    tile_empty = pygame.image.load("Amain/assets/TileEmpty.png")
    tile_empty = pygame.transform.scale(tile_empty, (CELL_SIZE, CELL_SIZE))

    tile_exploded = pygame.image.load("Amain/assets/TileExploded.png") 
    tile_exploded = pygame.transform.scale(tile_exploded, (CELL_SIZE, CELL_SIZE))

    tile_flag = pygame.image.load("Amain/assets/TileFlag.png") 
    tile_flag = pygame.transform.scale(tile_flag, (CELL_SIZE, CELL_SIZE))

    tile_mine = pygame.image.load("Amain/assets/TileMine.png") 
    tile_mine = pygame.transform.scale(tile_mine, (CELL_SIZE, CELL_SIZE))

    tile_not_mine = pygame.image.load("Amain/assets/TileNotMine.png") 
    tile_not_mine = pygame.transform.scale(tile_not_mine, (CELL_SIZE, CELL_SIZE))

    tile_imgs = [pygame.image.load(f"Amain/assets/Tile{i}.png") for i in range(1, 8)]
    for i in range(1,8):
        tile_imgs[i-1] = pygame.transform.scale(tile_imgs[i-1], (CELL_SIZE, CELL_SIZE))


    # Start screen
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minesweeper")

    # Backend functions:
    # Generates the game grid with randomly placed mines.
    def createMap(size, mines):
        grid = [[0 for _ in range(size)] for _ in range(size)]
        coordinates = [(i, j) for i in range(size) for j in range(size)]
        random.shuffle(coordinates)
        for i in range(mines):
            x, y = coordinates[i]
            grid[x][y] = "x"
        return grid

    # Adds numbers to non-mine cells indicating the number of adjacent mines.
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

    # Checks if the selected cell contains a mine.
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

    # Clears the cells around the selected cell recursively.
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

    # Clears the selected cell and its adjacent cells if the selected cell is 0.
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

    # Removes the "d" flag used during cell clearing.
    def remove_d(grid):
        for row in grid:
            cell = 0
            while cell < len(row):
                if isinstance(row[cell], str) and "d" in row[cell]:
                    row[cell] = row[cell].replace("d", "")
                cell += 1

    # Flags or unflags a cell.
    def flag(grid, pos_x, pos_y, flags_left):
        grid[pos_y][pos_x] = str(grid[pos_y][pos_x])
        
        if "f" in grid[pos_y][pos_x]:
            grid[pos_y][pos_x] = grid[pos_y][pos_x][0]
            flags_left += 1
        
        elif "c" not in grid[pos_y][pos_x]:
            grid[pos_y][pos_x] += "f"
            flags_left -= 1
        return flags_left

    # Checks if the game is won.
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

    # Handles the game-over scenario.
    def lose(grid, column, row):
        for row_tmp in range(SIZE):
            for column_tmp in range(SIZE):
                if grid[row_tmp][column_tmp] == "x":
                    grid[row_tmp][column_tmp] = "xc"  # Reveal all mines
                elif "f" in str(grid[row_tmp][column_tmp]) and "x" not in str(grid[row_tmp][column_tmp]): #handles wrongly placed flags
                    grid[row_tmp][column_tmp] = "w"
        grid[row][column] = "xp"
        draw_grid(grid)
        pygame.display.flip()
        
        click = False
        while not click:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if (pos[0] - BUTTON_CENTRE[0])**2 + (pos[1] - BUTTON_CENTRE[1])**2 <= BUTTON_RADIUS**2:
                        animate_header_button()
                        click = True
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

    # Handles the win scenario.
    def win():
        click = False
        while not click:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if (pos[0] - BUTTON_CENTRE[0])**2 + (pos[1] - BUTTON_CENTRE[1])**2 <= BUTTON_RADIUS**2:
                        animate_header_button()
                        click = True
                elif event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    
        grid = createMap(SIZE, MINES)
        add_numbers(grid)

        screen.fill(BLACK)
        draw_grid(grid)
        return grid

    # Saves player's time in a high score file.
    def save_time(name, game_time, size, difficulty):
        game_time = "{:.3f}".format(game_time)
        
        with open(f"highscores_{size}_{difficulty}.txt", "r") as file:
            scores = file.readlines()
            
        scores.append(name + ": " + game_time + "\n")
        
        scores.sort(key=lambda x: float(x.split(": ")[1]))
        
        with open(f"highscores_{size}_{difficulty}.txt", "w") as file:
            file.writelines(scores)


    # Frontend functions:
    # Draws a cell on the screen based on its state.
    def draw_square(tile, column, row):
        if tile == "empty":
            img = tile_empty
        elif tile == "unknown":
            img = tile_unknown
        screen.blit(img, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                                (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))

    # Draws the number of adjacent mines on a cell.
    def draw_num(grid, column, row):
        img = tile_imgs[int(grid[row][column][0])-1]
        
        screen.blit(img, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                                (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))

    # Draws a flag on a cell.
    def draw_flag(column, row):
        img = tile_flag
        
        screen.blit(img, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                                (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))

    # Draws the entire game grid on the screen.
    def draw_grid(grid):
        for row in range(SIZE):
            for column in range(SIZE):
                if grid[row][column] == "xp":
                    screen.blit(tile_exploded, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                                (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))
                elif grid[row][column] == "xc":
                    screen.blit(tile_mine, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                                (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))
                elif "c" not in str(grid[row][column]) and "f" not in str(grid[row][column]) and "w" not in str(grid[row][column]):
                    draw_square("unknown", column, row)
                elif "c" in grid[row][column]:
                    if "0" in grid[row][column]:
                        draw_square("empty", column, row)
                    else:
                        draw_num(grid, column, row)
                elif "f" in grid[row][column]:
                    draw_flag(column, row)
                elif "w" == grid[row][column]:
                    screen.blit(tile_not_mine, ((MARGIN + CELL_SIZE) * column + MARGIN,
                                                (MARGIN + CELL_SIZE) * row + MARGIN + HEADER_HEIGHT))
        pygame.display.flip()

    # Draws the header displaying elapsed time and remaining flags.
    def draw_header(elapsed_time, flags_left):
        screen.fill((255,255,255), pygame.Rect(0, 0, WIDTH, HEADER_HEIGHT))
        pygame.draw.circle(screen, (255,0,0), BUTTON_CENTRE, BUTTON_RADIUS)
        

        font_size = 25
        margin = 20
        font = pygame.font.Font(None, font_size)
        
        flags_text = font.render(f"Mines: {flags_left}", True, BLACK)
        time_text = font.render(f"Time: {elapsed_time:.2f}", True, BLACK)

        screen.blit(flags_text, (MARGIN, HEADER_HEIGHT-margin))
        screen.blit(time_text, (WIDTH-(font.size(f"Time: {elapsed_time:.2f}"))[0], HEADER_HEIGHT-margin))
        
        if SIZE == 5:
            draw_button(screen, BLACK, 0+MARGIN, 0+MARGIN, 70, 15, "Main Menu", font_size-10)
        else:
            draw_button(screen, BLACK, 0+MARGIN, 0+MARGIN, 100, 20, "Main Menu", font_size-5)
        
        pygame.display.flip()

    # Animates the button in the header.
    def animate_header_button():
        pygame.draw.circle(screen, (139,0,0), BUTTON_CENTRE, BUTTON_RADIUS)
        pygame.display.flip()
        time.sleep(0.5)
        pygame.draw.circle(screen, (255,0,0), BUTTON_CENTRE, BUTTON_RADIUS)
        pygame.display.flip()

    # Draws a button on the screen.
    def draw_button(screen, color, x, y, width, height, text, fontsize):
        pygame.draw.rect(screen, color, (x, y, width, height))
        
        font = pygame.font.Font(None, fontsize)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surface, text_rect)

    def game_loop():
        grid = createMap(SIZE, MINES)
        add_numbers(grid)
                
        screen.fill(BLACK)
        draw_grid(grid)

        flags_left = MINES
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
                    pos = pygame.mouse.get_pos()
                    
                    if pos[1] > HEADER_HEIGHT:
                        if first_press:
                            start_time = time.time()
                            first_press = False

                        column = pos[0] // (CELL_SIZE + MARGIN)
                        row = (pos[1]-HEADER_HEIGHT) // (CELL_SIZE + MARGIN)
                    
                        if event.button == 1:
                            if is_bomb(grid, column, row):
                                lose(grid, column, row)
                                grid = createMap(SIZE, MINES)
                                add_numbers(grid)
                                first_press = True
                                flags_left = MINES
                            else:
                                clear(grid, column, row)
                                remove_d(grid)
                        elif event.button == 3:
                            flags_left = flag(grid, column, row, flags_left)
                            
                        draw_grid(grid)
                        
                        if won(grid):
                            draw_header(elapsed_time, flags_left)
                            
                            end_time = time.time()
                            game_time = end_time-start_time
                            save_time(name, game_time, size, difficulty)

                            flags_left = MINES
                            grid = win()
                            first_press = True
                    elif (pos[0] - BUTTON_CENTRE[0])**2 + (pos[1] - BUTTON_CENTRE[1])**2 <= BUTTON_RADIUS**2:
                        animate_header_button()
                        grid = createMap(SIZE, MINES)
                        add_numbers(grid)
                        screen.fill(BLACK)
                        draw_grid(grid)
                        
                        first_press = True
                        flags_left = MINES
                        draw_header(start_time, MINES)
                    else:
                        if SIZE == 5:
                            if 0+MARGIN <= pos[0] <= 70 and 0+MARGIN <= pos[1] <= 15:
                                main()
                        else:
                            if 0+MARGIN <= pos[0] <= 100 and 0+MARGIN <= pos[1] <= 20:
                                main()

    game_loop()

# Displays the main menu where players can choose game settings and start the game.
def main_menu():
    # Constants
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    RED = (255, 0, 0)

    BUTTON_WIDTH = 200
    BUTTON_HEIGHT = 50

    # Start screen
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Main Menu")

    # Draws a button on the screen.
    def draw_button(screen, color, x, y, width, height, text):
        pygame.draw.rect(screen, color, (x, y, width, height))
        
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, BLACK)
        text_rect = text_surface.get_rect(center=(x + width / 2, y + height / 2))
        screen.blit(text_surface, text_rect)

    def main_menu_loop():
        size = "Medium"
        difficulty = "Medium"
        input_font = pygame.font.Font(None, 24)
        name = ""
        no_name = WHITE
        while True:
            screen.fill(WHITE)
            
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("Minesweeper", True, BLACK)
            title_text_rect = title_text.get_rect(center=(SCREEN_WIDTH / 2, 50))
            screen.blit(title_text, title_text_rect)

            creator_font = pygame.font.Font(None, 24)
            creator_text = creator_font.render("Created by Jamal, Truls, & Jonathan", True, BLACK)
            creator_text_rect = creator_text.get_rect(center=(SCREEN_WIDTH / 2, 90))
            screen.blit(creator_text, creator_text_rect)
            
            # Size
            draw_button(screen, RED if size == "Small" else GRAY, SCREEN_WIDTH / 2 - 350, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "Small")
            draw_button(screen, RED if size == "Medium" else GRAY, SCREEN_WIDTH / 2 - 100, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "Medium")
            draw_button(screen, RED if size == "Big" else GRAY, SCREEN_WIDTH / 2 + 150, 150, BUTTON_WIDTH, BUTTON_HEIGHT, "Big")

            # Difficulty
            draw_button(screen, RED if difficulty == "Easy" else GRAY, SCREEN_WIDTH / 2 - 350, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "Easy")
            draw_button(screen, RED if difficulty == "Medium" else GRAY, SCREEN_WIDTH / 2 - 100, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "Medium")
            draw_button(screen, RED if difficulty == "Hard" else GRAY, SCREEN_WIDTH / 2 + 150, 250, BUTTON_WIDTH, BUTTON_HEIGHT, "Hard")

            # Box to enter name
            input_text = input_font.render("Enter your name:    (Max 20 characters)", True, BLACK, no_name)
            input_rect = input_text.get_rect(topleft=(50, 100))
            screen.blit(input_text, input_rect)

            name_text = input_font.render(name, True, BLACK)
            name_rect = name_text.get_rect(topleft=(50, 130))
            pygame.draw.rect(screen, WHITE, name_rect, 2)
            screen.blit(name_text, name_rect)


            # Start game
            draw_button(screen, GRAY, SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 350, BUTTON_WIDTH, BUTTON_HEIGHT, "Start Game")

            # Leaderboard
            draw_button(screen, GRAY, SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 450, BUTTON_WIDTH, BUTTON_HEIGHT, "Leaderboard")

            # Quit
            draw_button(screen, GRAY, SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 550, BUTTON_WIDTH, BUTTON_HEIGHT, "Quit")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()                   
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    
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
                        if size is not None and difficulty is not None and name != "" and len(name) < 20:
                            return size, difficulty, name
                        else:
                            no_name = RED
                            
                            
                    # Check if leaderboard button clicked
                    leaderboard_button = pygame.Rect(SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 450, BUTTON_WIDTH, BUTTON_HEIGHT)
                    if leaderboard_button.collidepoint(mouse_pos):
                        show_leaderboard(size, difficulty)
                    
                    # Check if quit button clicked
                    quit_button = pygame.Rect(SCREEN_WIDTH / 2 - BUTTON_WIDTH / 2, 550, BUTTON_WIDTH, BUTTON_HEIGHT)
                    if quit_button.collidepoint(mouse_pos):
                        pygame.quit()
                        sys.exit()
                # Name input:
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_BACKSPACE:
                        name = name[:-1]
                    elif event.key == pygame.K_RETURN:
                        if size is not None and difficulty is not None and name != "" and len(name) < 20:
                            return size, difficulty, name
                        else:
                            no_name = RED
                    else:
                        name += event.unicode
            
            pygame.display.flip()

    return main_menu_loop()
  
# Displays the leaderboard showing top scores for a specific game size and difficulty.
def show_leaderboard(size, difficulty):
    with open(f"highscores_{size}_{difficulty}.txt", "r") as f:
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

    # Draws text on the screen.
    def draw_text(text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.center = (x, y)
        surface.blit(text_obj, text_rect)

    while True:
        screen.fill(WHITE)
        draw_text(f"Leaderboard for {size} & {difficulty}", font, BLACK, screen, WIDTH // 2, 100)

        #Main menu
        menu_rect = pygame.Rect(WIDTH // 6 - 50, 75, 100, 50)
        pygame.draw.rect(screen, BLACK, menu_rect)
        draw_text("Menu", font, WHITE, screen, WIDTH // 6, 100)

        #Leaders
        title_y = 100
        available_height = HEIGHT - 2 * 100
        box_height = 50
        space_between_boxes = (available_height - 5 * box_height) / 4

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
                    main()             

        pygame.display.update()

def main():
    size, difficulty, name = main_menu()
    game(size, difficulty, name)
    
main()