import random

def createMap(gridSize, mines):
    rutor = gridSize**2
    
    result_string = 'x' * mines + '0' * (rutor - mines)
    result_string = ''.join(random.sample(result_string,len(result_string)))
    
    map = []
    
    
    print (result_string)

    
    
    
    
    return map

createMap(4, 7)
"""    


# Using string formatting
result_string = '{1}' * x + '{0}' * y
result_string = result_string.format('0', '1')
print(result_string)  # Output: '11100000'





>>> import random
>>> s="abcdef123"
>>> ''.join(random.sample(s,len(s)))
'1f2bde3ac'
"""
    
    
    
    
    
    
