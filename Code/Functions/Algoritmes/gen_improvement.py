"""
This function changes the solution by a randomly generated number from an input
range.
 
Input:  
    house matrix, which house should be moved and the range magnitude 
Output: 
    house matrix with changed location of houses
"""

# import global variables
from global_vars import COLUMNS

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
    matrix[house, COLUMNS["x1"]] += improv_x
    matrix[house, COLUMNS["y1"]] += improv_y
    matrix[house, COLUMNS["x2"]] += improv_x
    matrix[house, COLUMNS["y2"]] += improv_y
    
    # change whether the house is truned 90 degrees (1 for yes, 0 for no)
    matrix[house, COLUMNS["rotated"]] = random.randint(0, 1)
    
    return matrix


def swap(matrix, house, waternum):
    """" This function swaps a house of a certain kind with a house of a
         different house (i.e. swapping villa with bungalow)."""
         
    # make copy of matrix
    matrix_copy = matrix.copy()
    
    # go through the matrix to find different house type
    for house_num in range(waternum, matrix.shape[0]):
        
        if matrix[house_num, COLUMNS["type"]] != matrix[house,
                                                 COLUMNS["type"]] and \
                                                 matrix[house,
                                                 COLUMNS["type"]] != \
                                                 COLUMNS["type"] :
            
            # temporary store coordinates of a house to use in the swap
            x1_copy = matrix[house_num, COLUMNS["x1"]]
            y1_copy = matrix[house_num, COLUMNS["y1"]]
            
            # change house 1
            matrix[house_num, COLUMNS["x1"]] = matrix[house, COLUMNS["x1"]]
            matrix[house_num, COLUMNS["y1"]] = matrix[house, COLUMNS["y1"]]
            r = matrix[house_num, COLUMNS["rotated"]]
            matrix[house_num, COLUMNS["x2"]] = matrix[house_num, 
                                               COLUMNS["x1"]] + (1 - r) * \
                                               matrix[house_num,
                                               COLUMNS["height"]] + r * \
                                               matrix[house_num,
                                               COLUMNS["width"]]
            matrix[house_num, COLUMNS["y2"]] = matrix[house_num,
                                               COLUMNS["y1"]] - (1 - r) * \
                                               matrix[house_num,
                                               COLUMNS["width"]] - r * \
                                               matrix[house_num,
                                               COLUMNS["height"]]
    
            # change house 2
            matrix[house, COLUMNS["x1"]] = x1_copy
            matrix[house, COLUMNS["y1"]] = y1_copy
            r = matrix[house, COLUMNS["rotated"]]
            matrix[house, COLUMNS["x2"]] = matrix[house, COLUMNS["x1"]] + \
                                          (1 - r) * matrix[house,
                                          COLUMNS["height"]] + r * \
                                          matrix[house, COLUMNS["width"]]
            matrix[house, COLUMNS["y2"]] = matrix[house, COLUMNS["y1"]] - \
                                          (1 - r) * matrix[house,
                                          COLUMNS["width"]] - r * \
                                          matrix[house, COLUMNS["height"]]
            
            # check if swapped houses generate feasible solution
            valid1, distance = check_house(house, waternum , matrix)
            valid2, distance = check_house(house_num, waternum, matrix)
            
            # if both valid break
            if valid1 + valid2 == 0:
                break
            else:
                matrix = matrix_copy
    return matrix