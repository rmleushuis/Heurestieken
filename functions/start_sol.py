"""
This function generates a random position for a house, inserts its location
into the provided matrix after checking if the location is viable and returns
the matrix.

Input:  matrix with all the types of houses, number of houses
Output: matrix with the coordinates of random generated houses
"""

# import global variables
from global_vars import *

# import functions from other documents
from check_house import check_house

# import necessary modules
import numpy as np
def start_sol(house_mat, x):
    def generate_house(matrix, house_num):
            
        # generate a random coordinates for the left right corner of a house
        matrix[house_num, 0] = np.random.uniform(low = 0 + house_mat[house_num, 7],
                               high = grid['width'] - house_mat[house_num, 6] -
                               house_mat[house_num, 7])
        matrix[house_num, 1] = np.random.uniform(low = 0 + house_mat[house_num, 6]
                               + house_mat[house_num, 7], high = grid['height'] - 
                               house_mat[house_num, 7])
        matrix[house_num, 2] = matrix[i, 0] + house_mat[house_num, 6]
        matrix[house_num, 3] = matrix[i, 1] - house_mat[house_num, 5]
        
        return matrix
    
    # generate a starting solution 
    for i in range(x):
        
        # select the variables of the house being placed in this iteration
        house_type = str(int(house_mat[i, 4]))
        house_mat[i, 5] = house_chars[house_type]['height']
        house_mat[i, 6] = house_chars[house_type]['width']
        house_mat[i, 7] = house_chars[house_type]['free']
        
        if i == 0:
            # the first house can be placed nearly anywhere and has no constraints
            generate_house(house_mat, i)
        else:
            generate_house(house_mat, i)
            # keep generating new location for house i until it satisfies condition
            while check_house(house_mat[i, 0], house_mat[i, 1], house_mat[i, 2],
                        house_mat[i, 3], i, house_mat) != 0:
                generate_house(house_mat, i)
                
    return house_mat