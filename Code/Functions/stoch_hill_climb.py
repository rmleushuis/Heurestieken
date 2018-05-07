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
    improvement = -1
    new_value  = 'nan'
    max_repeats = 4000
    counter = 0
    
    # calculate  old value and store old matrix
    old = houses.compute_value().copy()
    matrix_old = houses.get_house_matrix().copy()
    
    while improvement <= 0:
        
        # generate copy of the matrix to try improvements on
        matrix_copy = houses.get_house_matrix().copy()
        matrix_improv = gen_improv(matrix_copy, house)
        
        # calculate distance
        valid, distance = check_house(house, matrix_improv)
        
        # if new position is valid
        if valid == 0 :
            # calculate new value
            houses.set_house_matrix(matrix_improv)
            new_value = houses.compute_value()
            
            # calculate improvement
            improvement = new_value - old
        
        # if new position is not valid or the improvement is negative
        if valid == 1 or improvement < 0:
            counter += 1
            houses.set_house_matrix(matrix_old)
            
            # continue until max_repeats is reached
            if max_repeats == counter:
                matrix_improv = matrix_old
                break

    return matrix_improv

                
def gen_improv(matrix, house):
    # generate new values for possible improvement step
    improv_x = np.random.uniform(low = -0.001 , high = 0.001)
    improv_y = np.random.uniform(low = -0.001 , high = 0.001)
    
    matrix[house, 0] += improv_x
    matrix[house, 1] += improv_y
    matrix[house, 5] = random.randint(0, 2)
    matrix[house, 2] += improv_x
    matrix[house, 3] += improv_y
    return matrix