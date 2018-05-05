"""
This function uses a stochastic hill climbing algorithm to find a local maxima.
 
Input:  class containing the matrix
Output: plan of the optimized house positions
"""
 
# import necessary modules
import numpy as np
import random

# import global variables
from global_vars import GRID

# import functions from other documents
from check_house import check_house

np.warnings.filterwarnings('ignore')

def stoch_steepest_hill(houses):
    
    # choose a random house to move
    house = random.randint(0, houses.total_houses - 1)
    # set up for while loop
    valid = 1
    improvement = -1
    new  = 'nan'
    
    while valid == 1 or improvement <= 0 or str(new)=='nan':
        # calculate  old value and store old matrix
        old = houses.compute_value()
        matrix_old = houses.get_house_matrix()
        
        # generate copy of the matrix to try improvements on
        matrix_copy = houses.get_house_matrix()
        matrix_improv = gen_improv(matrix_copy, house)
        
        
        r = matrix_improv[house, 5]
        left = matrix_improv[house, 9]
        right = GRID["width"] - matrix_improv[house, 9] - r *matrix_improv[house, 8] - (1-r)*matrix_improv[house, 7]
        top = GRID["height"] - matrix_improv[house, 9]
        bot = matrix_improv[house, 9] + (1-r) *matrix_improv[house, 8] + r*matrix_improv[house, 7]
        
        while matrix_improv[house, 0] < left or matrix_improv[house, 0] > right or\
            matrix_improv[house, 1] < bot or matrix_improv[house, 1]> top:
                
            matrix_improv = gen_improv(matrix_copy, house)
        
                               
        # check and calculate distance
        valid, distance = check_house(house, matrix_improv)
        
        if valid == 0 :
            # calculate new value
            houses.set_house_matrix(matrix_improv)
            new = houses.compute_value()
            
            # calculate improvement
            improvement = new - old
        
        if valid == 1 or improvement < 0:
            houses.set_house_matrix(matrix_old)
        
        house = random.randint(0, houses.total_houses - 1)
    return matrix_improv

                
def gen_improv(matrix, house):
    # generate new values for possible improvement step
    
    matrix[house, 0] = matrix[house, 0] + np.random.uniform(low = -0.001 , high = 0.001)
    matrix[house, 1] = matrix[house, 1] + np.random.uniform(low = -0.001 , high = 0.001)
    matrix[house, 5] = random.randint(0, 2)
    matrix[house, 2] =  matrix[house, 0] + (1 - matrix[house, 9]) * matrix[house, 6] +  \
                             matrix[house, 9] * matrix[house, 5] 
    matrix[house, 3] = matrix[house, 1] - (1 - matrix[house, 9]) * matrix[house, 5] - \
                             matrix[house, 9] * matrix[house, 6]
    return matrix