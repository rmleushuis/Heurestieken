"""
This function changes the solution by a randomly generated number from an input
range.
 
Input:  house matrix, which house should be moved and the range magnitude 
Output: house matrix with changed location of houses
"""

# import necessary modules
import numpy as np
import random

def gen_improv(matrix, house, magni):
    # generate new values for possible improvement step
    improv_x = np.random.uniform(low = -magni , high = magni)
    improv_y = np.random.uniform(low = -magni , high = magni)
    
    matrix[house, 0] += improv_x
    matrix[house, 1] += improv_y
    matrix[house, 5] = random.randint(0, 2)
    matrix[house, 2] += improv_x
    matrix[house, 3] += improv_y
    return matrix