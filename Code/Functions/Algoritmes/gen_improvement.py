"""
This function changes the solution by a randomly generated number from an input
range.
 
Input:  house matrix, which house should be moved and the range magnitude 
Output: house matrix with changed location of houses
"""

# import necessary modules
import numpy as np
import random
from check_house import check_house


def gen_improv(matrix, house, magni):
    
    # decide whether to random swap or random move a house
    decision = random.randint(0, 1)
    
    if decision == 0:
        matrix = move_house(matrix, house, magni)
    else:
        matrix = swap(matrix, house)

    return matrix

def move_house(matrix, house, magni):
    
    # generate new values for possible improvement step
    improv_x = np.random.uniform(low = -magni , high = magni)
    improv_y = np.random.uniform(low = -magni , high = magni)
    
    matrix[house, 0] += improv_x
    matrix[house, 1] += improv_y
    matrix[house, 5] = random.randint(0, 1)
    matrix[house, 2] += improv_x
    matrix[house, 3] += improv_y
    
    return matrix


def swap(matrix, house):
    # make copy of matrix
    matrix_copy = matrix.copy()
    
    for house_num in range(matrix.shape[0]):
        
        if matrix[house_num, 4] != matrix[house, 4]:
            x1_copy = matrix[house_num, 0]
            y1_copy = matrix[house_num, 1]
            
            # change house 1
            matrix[house_num, 0] = matrix[house, 0]
            matrix[house_num, 1] = matrix[house, 1]
            r = matrix[house_num, 5]
            matrix[house_num, 2] = matrix[house_num, 0] + (1 - r) * matrix[house_num, 7] + r * matrix[house_num, 8]
            matrix[house_num, 3] = matrix[house_num, 1] - (1 - r) * matrix[house_num, 8] - r * matrix[house_num, 7]
    
            # change house 2
            matrix[house, 0] = x1_copy
            matrix[house, 1] = y1_copy
            r = matrix[house, 5]
            matrix[house, 2] = matrix[house, 0] + (1 - r) * matrix[house, 7] + r * matrix[house, 8]
            matrix[house, 3] = matrix[house, 1] - (1 - r) * matrix[house, 8] - r * matrix[house, 7]
            
            # check if swapped houses are possible
            valid1, distance = check_house(house, matrix)
            valid2, distance = check_house(house_num, matrix)
            
            if valid1 + valid2 == 0:
                break
            else:
                matrix = matrix_copy
    return matrix