"""
This function uses a stochastic hill climbing algorithm to find a local maxima.

Input:  class containing the matrix
Output: plan of the optimized houses
"""

# import necessary modules
import numpy as np
import random

# import functions from other documents
from check_house import check_house

def stoch_steepest_hill(houses):
    
    # choose a random house to move
    house = random.int(0, houses.version)
    
    valid = 0
    while valid == 0:
        # generate copy of the matrix to try improvements on
        matrix_copy = gen_improv(house.matrix, house)
    
        # check and calculate distance
        valid, distance = check_house(houses.matrix[house, 0], houses.matrix[house, 1], 
                                              houses.matrix[house, 2], houses.matrix[house, 3], house, 
                                              houses.matrix, houses.matrix[house, 7])
        
    
        
def gen_improv(matrix, house):
    # generate new values for possible improvement step
    matrix[house, 0] = matrix[house, 0] + np.random.uniform(low = -3 , high = 3)
    matrix[house, 1] = matrix[house, 1] + np.random.uniform(low = -3 , high = 3)
    matrix[house, 9] = random.int(0, 2)
    matrix[house, 2] =  matrix[house, 0] + (1 - matrix[house, 9]) * matrix[house, 6] + 
                             matrix[house, 9] * matrix[house, 5] 
    matrix[house, 3] = matrix[house, 1] - (1 - matrix[house, 9]) * matrix[house, 5] - 
                             matrix[house, 9] * matrix[house, 6]
    return matrix
   
    
    
    
    