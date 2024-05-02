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
    

grid = [
    ["0c", "1c", "2c", "3c"],
    ["xf", "0c", "4c", "4c"],
    ["1c", "xf", "3c", "5c"]
]

print(won(grid))