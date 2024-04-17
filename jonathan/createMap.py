import random
  
"""
Todo:
lägg till validering:
    size == integer
    3 <= size <= 50 (?)
    num_x == integer
    0 < num_x < (totalt antal rutor = size**2)
"""
      
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

# Hur man använder:
size = 4
num_x = 10
grid = createMap(size, num_x)

for row in grid:
    print(row)
