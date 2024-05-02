#To do:
#Rensa plats när man inte klickar på bomb

#True = bomb, False = inte bomb
#user_input_x och user_input_y har samma indexering som arrayen (Börjar på 0).
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
        if "f" not in str(grid[user_input_y][user_input_x]):
            grid[user_input_y][user_input_x] = str(grid[user_input_y][user_input_x])
            grid[user_input_y][user_input_x] += "c"
            return False



#Testing:
x = "x"

grid = [[x, 1, x, 2, x, x],
        [1, 1, 1, 2, 3, 3],
        [x, 1, 0, 0, 1, x],
        [1, 1, 1, 2, 3, 3],
        [x, 1, x, 2, x, x]]

while True:
    user_input_x = input("Position X:")
    user_input_y = input("Position Y:")
    user_input_x = int(user_input_x)
    user_input_y = int(user_input_y)
    
    if is_bomb(grid, user_input_x, user_input_y):
        print("Bomb")
    else:
        print("inte bomb")
