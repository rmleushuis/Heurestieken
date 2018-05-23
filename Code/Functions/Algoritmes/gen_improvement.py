"""
This function changes the solution by a randomly generated number from an input
range.
 
Input:  
    house matrix, which house should be moved and the range magnitude 
Output: 
    house matrix with changed location of houses
"""

# import global vars
from global_vars import COLUMN_DEFS

# import necessary modules
import numpy as np
import random
from check_house import check_house


def gen_improv(matrix, house, magni, swap_allowed, waternum):
    """" This function decides to whether swap 2 houses or to move 1 house. """
    
    # decide whether to random swap or random move a house
    if swap_allowed:
        decision = random.randint(0, 1)
    else:
        decision = 0
    
    # call the functions for moving house and swapping houses
    if decision == 0:
        matrix = move_house(matrix, house, magni)
    else:
        matrix = swap(matrix, house, waternum)

    return matrix

def move_house(matrix, house, magni):
    """" This function generates random direction and magnitude to move a
         house."""
    
    # generate new values for possible improvement step
    improv_x = np.random.uniform(low = - magni , high = magni)
    improv_y = np.random.uniform(low = - magni , high = magni)
    
    # change the matrix coordinates to match improvement step
    matrix[house, COLUMN_DEFS['x1']] += improv_x
    matrix[house, COLUMN_DEFS['y1']] += improv_y
    matrix[house, COLUMN_DEFS['x2']] += improv_x
    matrix[house, COLUMN_DEFS['y1']] += improv_y
    
    # change whether the house is rotated 90 degrees (1 for yes, 0 for no)
    matrix[house, COLUMN_DEFS['rotated']] = random.randint(0, 1)
    
    return matrix


def swap(matrix, house, waternum):
    """" This function swaps a house of a certain kind with a house of a
         different house (i.e. swapping villa with bungalow)."""
         
    # make copy of matrix
    matrix_copy = matrix.copy()
    
    # go through the matrix to find different house type
    for house_num in range(waternum, matrix.shape[0]):
        
        if matrix[house_num, 4] != matrix[house, 4] and matrix[house, 4] != 4 :
            
            # temporary store coordinates of a house to use in the swap
            x1_copy = matrix[house_num, COLUMN_DEFS['x1']]
            y1_copy = matrix[house_num, COLUMN_DEFS['y1']]
            
            # change house 1
            matrix[house_num, COLUMN_DEFS['x1']] = matrix[house,
                                                      COLUMN_DEFS['x1']]
            matrix[house_num, COLUMN_DEFS['y1']] = matrix[house,
                                                      COLUMN_DEFS['y1']]
            r = matrix[house_num, COLUMN_DEFS['rotated']]
            matrix[house_num, 2] = matrix[house_num, 0] + (1 - r) * \
                                   matrix[house_num, 7] + r * \
                                   matrix[house_num, 8]
            matrix[house_num, 3] = matrix[house_num, 1] - (1 - r) * \
                                   matrix[house_num, 8] - r * \
                                   matrix[house_num, 7]
    
            # change house 2
            matrix[house, 0] = x1_copy
            matrix[house, 1] = y1_copy
            r = matrix[house, 5]
            matrix[house, 2] = matrix[house, 0] + (1 - r) * matrix[house, 7] \
                               + r * matrix[house, 8]
            matrix[house, 3] = matrix[house, 1] - (1 - r) * matrix[house, 8] \
                               - r * matrix[house, 7]
            
            # check if swapped houses generate feasible solution
            valid1, distance = check_house(house, waternum , matrix)
            valid2, distance = check_house(house_num, waternum, matrix)
            
            # if both valid break
            if valid1 + valid2 == 0:
                break
            else:
                matrix = matrix_copy
    return matrix