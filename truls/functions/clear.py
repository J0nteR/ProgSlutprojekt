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

#pos_x: x-cordinat där spelaren klickat
#pos_y: y-cordinat där spelarn klickat
def clear(grid, pos_x, pos_y):
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
            
#Testing:
x = "x"

grid = [[0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, x, 1, 1, 1, 1],
        [1, 1, 1, 2, x, 2],
        [0, 0, 1, x, 3, x],
        [0, 0, 1, 1, 2, 1]]

clear(grid, 0,5)

remove_d(grid)

for row in grid:
    print(row)
