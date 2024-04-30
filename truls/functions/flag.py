def flag(grid, pos_x, pos_y):
    grid[pos_y][pos_x] = str(grid[pos_y][pos_x])
    
    if "f" in grid[pos_y][pos_x]:
        grid[pos_y][pos_x] = grid[pos_y][pos_x][0]
    
    elif "c" not in grid[pos_y][pos_x]:
        grid[pos_y][pos_x] += "f"
        
# Testing
x = "x"

grid = [[0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, x, 1, 1, 1, 1],
        [1, 1, 1, 2, x, 2],
        [0, 0, 1, x, 3, x],
        [0, 0, 1, 1, 2, 1]]

flag(grid, 1,2)

for row in grid:
    print(row)
