"""
This file contains functions which generate a random starting solution for the
different versions of the problem.

Input:  
    matrix: matrix with all the types of houses
    water_num: number of water planes on the grid
Output: 
    matrix: matrix with the coordinates of random generated houses
"""

# import variables
from global_vars import GRID, MAX_START, MAX_TIME, COLUMNS

# import functions from other documents
from check_house import check_house
import time

# import necessary modules
import numpy as np

class Start_sol():
    def __init__(self, matrix, water_num):
        """ This function initializes the class with needed parameters. """  
      
        self.house_matrix = matrix
        self.water_num = water_num
        self.total_houses = len(self.house_matrix) - water_num

    def fill_house_matrix(self):
        """ This function fills the matrix with randomly generated houses. """  
        
        # define parameters needed in the loop
        total_houses = self.total_houses + self.water_num
        house_matrix = self.house_matrix
        start = time.time()
        i = self.water_num
        
        # generate houses house by house
        while i < total_houses:
            counter = 0
            while True:
                self.generate_house(house_matrix, i)
                valid, distance = check_house(i, self.water_num, house_matrix,
                                              start = 1)
                if valid == 0:
                    break
                else:
                    counter += 1
                    
                    # if house could not be placed in 20 seconds try again
                    if (time.time() - start) > MAX_TIME:
                        start = time.time()
                        i = 0
                        print('Start again.')
                        
                    # if after 40000 atempts house could not be placed go back
                    # 10 houses and place them again
                    if MAX_START is counter:
                        i -= 10
                        break
                    continue
                break
            i += 1
        
        return self.house_matrix
    
    def generate_house(self, matrix, house_num):
        """ This function generates a house with random coordinates. """  
            
        # generate a random coordinates for the left right corner of a house
        cur_house_height = matrix[house_num, COLUMNS["height"]]
        cur_house_width = matrix[house_num, COLUMNS["width"]]
        cur_house_free = matrix[house_num, COLUMNS["free"]]
        
        # rotate house 90 degrees
        r = np.random.choice([0,1])
        matrix[house_num, COLUMNS["rotated"]]  = r
        
        # generate random coordinated for the house
        matrix[house_num, COLUMNS["x1"]] = np.random.uniform(low = \
                                           cur_house_free, high = \
                                           GRID['width'] - (1-r) * \
                                           cur_house_width - r * \
                                           cur_house_height - cur_house_free)
        matrix[house_num, COLUMNS["y1"]] = np.random.uniform(low = (1-r) * \
                                           cur_house_height + r * \
                                           cur_house_width + cur_house_free,
                                           high = GRID['height'] - \
                                           cur_house_free)
        matrix[house_num, COLUMNS["x2"]] = matrix[house_num, COLUMNS["x1"]] + \
                                           (1 - r) * cur_house_width + r * \
                                           cur_house_height
        matrix[house_num, COLUMNS["y2"]] = matrix[house_num, COLUMNS["y1"]] - \
                                           (1 - r) * cur_house_height - r * \
                                           cur_house_width
        
        return matrix