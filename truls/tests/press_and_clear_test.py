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

x = "x"

grid = [[0, 0, 0, 0, 0, 0],
        [1, 1, 1, 0, 0, 0],
        [1, x, 1, 1, 1, 1],
        [1, 1, 1, 2, x, 2],
        [0, 0, 1, x, 3, x],
        [0, 0, 1, 1, 2, 1]]

y = 1
x = 4

if not is_bomb(grid, x, y):
    clear(grid, x, y)
    remove_d(grid)
else:
    print("Bomb")
    
print(grid[y][x])
for row in grid:
    string_row = list(map(str, row))
    print(string_row)