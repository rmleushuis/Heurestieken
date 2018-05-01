"""
This function generates a random position for a house, inserts its location
into the provided matrix after checking if the location is viable and returns
the matrix.

Input:  matrix with all the types of houses, number of houses
Output: matrix with the coordinates of random generated houses
"""

# import variables
from global_vars import GRID, HOUSE_CHARS

# import functions from other documents
from check_house import check_house

# import necessary modules
import numpy as np

def start_sol(houses):
    
    # generate a starting solution 
    distance_mat = np.ones(shape = (houses.version, houses.version)) * 1000
    
    for i in range(houses.version):
        
        # select the variables of the house being placed in this iteration
        house_type = str(int(houses.matrix[i, 4]))
        houses.matrix[i, 5] = HOUSE_CHARS[house_type]['height']
        houses.matrix[i, 6] = HOUSE_CHARS[house_type]['width']
        houses.matrix[i, 7] = HOUSE_CHARS[house_type]['free']
        
        if i == 0:
            # the first house can be placed nearly anywhere and has no constraints
            generate_house(houses.matrix, i)
        else:
            while True:
                generate_house(houses.matrix, i)
                valid, distance = check_house(houses.matrix[i, 0], houses.matrix[i, 1], 
                                          houses.matrix[i, 2], houses.matrix[i, 3], i, 
                                          houses.matrix, houses.matrix[i, 7])
                if valid == 0:
                    break
                
            # store final distance 
            distance_mat[i, :i] = distance
            
    # use the upper triangle matrix to make a projection to calculate minimum
    # distance
    i_upper = np.triu_indices(houses.version, 1)
    distance_mat[i_upper] = distance_mat.transpose()[i_upper]
    
    # store the minimum distance in the last column of the matrix in the class
    houses.matrix[:, 8] = np.min(distance_mat, axis = 0)
                
    return houses.matrix


def generate_house(matrix, house_num):
        
    # generate a random coordinates for the left right corner of a house
    matrix[house_num, 0] = np.random.uniform(low = 0 + matrix[house_num, 7],
                           high = GRID['width'] - matrix[house_num, 6] -
                           matrix[house_num, 7])
    matrix[house_num, 1] = np.random.uniform(low = 0 + matrix[house_num, 6]
                           + matrix[house_num, 7], high = GRID['height'] - 
                           matrix[house_num, 7])
    matrix[house_num, 2] = matrix[house_num, 0] + matrix[house_num, 6]
    matrix[house_num, 3] = matrix[house_num, 1] - matrix[house_num, 5]
    
    return matrix