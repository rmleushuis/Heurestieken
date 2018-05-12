# import variables
from global_vars import GRID
import numpy as np
import random

def make_water_matrix(matrix):
    total_water = GRID['height'] * 0.2 *  GRID['width']
    
    # generate random amount of water bodies
    water_bodies = random.randint(1, 4)
    
    for i in range(water_bodies):
        matrix = generate_water(matrix, i, total_water)
        total_water = total_water - (matrix[i, 2]  - matrix[i, 0]) * (matrix[i, 1] - matrix[i, 3])
        
        

def generate_water(self, matrix, water_num, sorted_ = False):
    
    
    if water_num == 0:
        # generate water body 1
        height =  np.random.uniform(low = 0 , high = GRID['height'])
        width = np.random.uniform(low = 0 , high = height/GRID['height'] * 0.2 *  GRID['width'])
     
        matrix[water_num, 0] = np.random.uniform(low = 0 , high = GRID['width'] - width)
        matrix[water_num, 1] = np.random.uniform(low = 0 +  height, high = GRID['height'])
        matrix[water_num, 2] = matrix[water_num, 0] +  width
        matrix[water_num, 3] = matrix[water_num, 1] - height
    
    else:
        # generate water body 1
        height =  np.random.uniform(low = 0 , high = GRID['height'])
        width = np.random.uniform(low = 0 , high = height/GRID['height'] * 0.2 *  GRID['width'])
     
        matrix[water_num, 0] = np.random.uniform(low = 0 , high = GRID['width'] - width)
        matrix[water_num, 1] = np.random.uniform(low = 0 +  height, high = GRID['height'])
        matrix[water_num, 2] = matrix[water_num, 0] +  width
        matrix[water_num, 3] = matrix[water_num, 1] - height
    
    
    return matrix