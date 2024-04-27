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

grid = createMap(6, 3)

for row in grid:
    string_row = list(map(str, row))
    print(string_row)
    
add_numbers(grid)
print("")
print("")
print("")

for row in grid:
    string_row = list(map(str, row))
    print(string_row)
