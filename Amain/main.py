import random

def createMap(size, num_x):
    """Funktionen skapar en "map" med nollor och x, där x är minorna och 0 inte har minor.

    Args:
        size (integer): hur stor arrayen/spelplanen ska vara
            exempel: size = 8 --> skapar en map som är 8x8 rutor

        num_x (integer): hur många minor/x som arrayen ska innehålla

    Returns:
        map (array): (2 dimentionell) array innehållande ett grid med nollor och x i random ordning
    """
    
    # Create a 2D grid with zeros
    grid = [[0 for _ in range(size)] for _ in range(size)] 
     
    # Create an array of the grid coordinates
    coordinates = [(i, j) for i in range(size) for j in range(size)]    
    
    # Shuffle the coordinates
    random.shuffle(coordinates)
        
    # Place 'x' in the shuffled coordinates to num_x
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
        message = f"user_input_x får ej överstiga längden av arrayens rader. user_input_x = {user_input_x}, längden av arrayens rader = {len(grid[0])-1}"
        raise IndexError(message)
    elif user_input_y > len(grid)-1:
        message = f"user_input_y får ej överstiga längden av arrayen. user_input_y = {user_input_x}, längden av arrayen = {len(grid[0])-1}"
        raise IndexError(message)

    if grid[user_input_y][user_input_x] == "x":
        return True
    else:
        grid[user_input_y][user_input_x] = str(grid[user_input_y][user_input_x])
        grid[user_input_y][user_input_x] += "c"
        empty_squares -= 1
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
                empty_squares -= 1
            
            x += 1
            if x > len(grid[0])-1:
                break
            
        y += 1
        if y > len(grid)-1:
            break
        
    if "d" not in grid[pos_y][pos_x]:
        grid[pos_y][pos_x] += "d"

#pos_x: x-cordinat där spelaren klickat
#pos_y: y-cordinat där spelarn klickat
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
#Tar bort alla "d" från griddet
def remove_d(grid):
    for row in grid:
        cell = 0
        while cell < len(row):
            if isinstance(row[cell], str) and 'd' in row[cell]:
                row[cell] = row[cell].replace('d', '')
            cell += 1

def flag(grid, pos_x, pos_y):
    grid[pos_y][pos_x] = str(grid[pos_y][pos_x])
    
    if "c" not in grid[pos_y][pos_x]:
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

def won():
    return empty_squares == 0

size = 6
num_x = 6
empty_squares = size**2 - num_x

grid = createMap(size, num_x)
add_numbers(grid)

for row in grid:
    print(row)

while True:
    visible_grid = create_visible_grid(grid)
    for row in visible_grid:
        print(row)
    print("")
    
    input_x = int(input("x:"))
    input_y = int(input("y:"))
    
    mode = int(input("0: Clicka, 1: Flagga"))
    if mode == 0:
        if is_bomb(grid, input_x, input_y):
            print("Du förlorade")
            break
        else:
            clear(grid, input_x, input_y)
            remove_d(grid)
            empty_squares -= 1
    elif mode == 1:
        flag(grid, input_x, input_y)
        
    if empty_squares <= 0:
        print("Gratis! Du Vann!")
        break
    