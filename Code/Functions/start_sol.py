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
from draw_plan import Show_grid

# import necessary modules
import numpy as np

show_grid = Show_grid()

class Start_sol():
    
    def __init__(self, matrix):
        self.house_matrix = matrix
        self.total_houses = len(matrix)
        self.distance_mat = np.ones(shape = (self.total_houses, self.total_houses )) * 1000
        
    def fill_house_matrix(self):
        total_houses = self.total_houses
        house_matrix = self.house_matrix
        max_repeats = 40000
        i = 0
        while i < total_houses:
            counter = 0
            while True:
                self.generate_house(house_matrix, i)
                if i != 0:
                    
                    valid, distance = check_house(i, house_matrix)
                    
                    if valid == 0:
                        self.distance_mat[i, :i] = distance
                        break
                    else:
                        counter += 1
                        if max_repeats == counter:
                            i -= 10
                            break
                        continue
                    
                show_grid.draw_house(house_matrix[i, :], i)
                break
            
            i += 1
            
        for k in range(total_houses):
            show_grid.draw_house(house_matrix[k, :], k)
            
        i_upper = np.triu_indices(total_houses, 1)
        self.distance_mat[i_upper] = self.distance_mat.transpose()[i_upper]
        
        # store the minimum distance in the last column of the matrix in the class
        house_matrix[:, 6] = np.min(self.distance_mat, axis = 0)
        
        return self.house_matrix
        # generate a starting solution 
        
    
    def generate_house(self, matrix, house_num):
            
        # generate a random coordinates for the left right corner of a house
        cur_house_height = matrix[house_num, 7]
        cur_house_width = matrix[house_num, 8]
        cur_house_free = matrix[house_num, 9]
        
        # rotate house 90 degrees
        r = np.random.choice([0,1])
        #matrix[house_num, 6] =r
        
        matrix[house_num, 0] = np.random.uniform(low = 0 + cur_house_free,
                               high = GRID['width'] - (1-r) * cur_house_width - r * cur_house_height -
                               cur_house_free)
                        
        matrix[house_num, 1] = np.random.uniform(low = 0 + (1-r) * cur_house_height + r * cur_house_width + cur_house_free,
              high = GRID['height'] - cur_house_free)
        matrix[house_num, 2] = matrix[house_num, 0] + (1 - r) * cur_house_width + r * cur_house_height
        matrix[house_num, 3] = matrix[house_num, 1] - (1 - r) * cur_house_height - r * cur_house_width
    
        return matrix