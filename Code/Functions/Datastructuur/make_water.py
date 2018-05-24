"""" 
This code contains functions which create the water planes and store it in the
provided matrix.

Input:
    matrix: the house class matrix
Output: 
    matrix: matrix with the characteristics and coordinates of the newly
            generated water planes
"""             
# import global variables
from global_vars import GRID, WATER_M2, COLUMNS, WATER_PERC, MAX_WATERS

# import necessary modules
import numpy as np
import random

def make_water_matrix(matrix):
    """ This function generates a random number of water bodies and puts their
        corresponding characteristics into the provided matrix. """
         
    # at first total water to be distributed is equal to the total water amount
    total_water = WATER_M2
    
    # generate random amount of water bodies
    water_bodies = random.randint(1, MAX_WATERS)
    
    for i in range(water_bodies):
        matrix = generate_water(matrix, i, total_water)
        total_water = total_water - (matrix[i, COLUMNS["x2"]]  - \
                      matrix[i, COLUMNS["x1"]]) * (matrix[i, COLUMNS["y1"]] - \
                      matrix[i, COLUMNS["y2"]])
        
        

def generate_water(self, matrix, water_num, sorted_ = False):
    """ This function generates a water body with random characteristics and
        coordinates. """   
        
    # generate characteristics of water body
    height =  np.random.uniform(low = 0 , high = GRID['height'])
    width = np.random.uniform(low = 0 , high = height/GRID['height'] * \
                              GRID['width'] * WATER_PERC)
    
    # generate coordinates of water body
    matrix[water_num, COLUMNS["x1"]] = np.random.uniform(low = 0 ,
                                       high = GRID['width'] - width)
    matrix[water_num, COLUMNS["y1"]] = np.random.uniform(low = height,
                                       high = GRID['height'])
    matrix[water_num, COLUMNS["x2"]] = matrix[water_num, COLUMNS["x1"]] \
                                       +  width
    matrix[water_num, COLUMNS["y2"]] = matrix[water_num, COLUMNS["y1"]] \
                                       - height
     
    return matrix