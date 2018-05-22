"""
This function generates a random position for a house, inserts its location
into the provided matrix after checking if the location is viable and returns
the matrix.

Input:  matrix with all the types of houses, number of houses
Output: matrix with the coordinates of random generated houses
"""

# import variables
from global_vars import GRID

# import functions from other documents
from check_house import check_house
from draw_plan import Show_grid
import time

# import necessary modules
import numpy as np

#show_grid = Show_grid()

class Start_sol():
    def __init__(self, matrix, water_num):

        self.house_matrix = matrix
        self.water_num = water_num
        self.total_houses = len(self.house_matrix) - water_num

    def fill_house_matrix(self):
        total_houses = self.total_houses + self.water_num
        house_matrix = self.house_matrix
        max_repeats = 40000
        start = time.time()
        i = self.water_num
        
        while i < total_houses:
            counter = 0
            while True:
                self.generate_house(house_matrix, i)
                valid, distance = check_house(i, self.water_num, house_matrix, start = 1)
                if valid == 0:
                    break
                else:
                    counter += 1
                    if (time.time() - start) > 20:
                        start = time.time()
                        i = 0
                        print('start again')
                    if max_repeats is counter:
                        i -= 10
                        break
                    continue
                    
                break
            i += 1
        
        return self.house_matrix
    
    def generate_house(self, matrix, house_num):
            
        # generate a random coordinates for the left right corner of a house
        cur_house_height = matrix[house_num, 7]
        cur_house_width = matrix[house_num, 8]
        cur_house_free = matrix[house_num, 9]
        
        # rotate house 90 degrees
        r = np.random.choice([0,1])
        matrix[house_num, 5]  = r
        
         
        matrix[house_num, 0] = np.random.uniform(low = 0 + cur_house_free,
                               high = GRID['width'] - (1-r) * cur_house_width - r * cur_house_height -
                               cur_house_free)
                        
        matrix[house_num, 1] = np.random.uniform(low = 0 + (1-r) * cur_house_height + r * cur_house_width + cur_house_free,
              high = GRID['height'] - cur_house_free)
        matrix[house_num, 2] = matrix[house_num, 0] + (1 - r) * cur_house_width + r * cur_house_height
        matrix[house_num, 3] = matrix[house_num, 1] - (1 - r) * cur_house_height - r * cur_house_width
        
        return matrix