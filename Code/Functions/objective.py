# define function to calculate total value

# import variables
from global_vars import HOUSE_CHARS

def calc_value(houses):
    
    value = 0
    for i in range(houses.version):
        value = value + HOUSE_CHARS[houses.matrix[i, 4]]['price'] * \
        (1 + HOUSE_CHARS[houses.matrix[i, 4]]['inc'] * houses.matrix[i, 8])
        
        
    return value