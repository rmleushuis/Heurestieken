# import global vars
from global_vars import PERC_SOLO, PERC_BUNG, PERC_VIL
from global_vars import GRID, HOUSE_CHARS
from start_sol import Start_sol
import time
# import necessary modules
import numpy as np

# this is a class for the houses
class House(object):
    def __init__(self, total_houses):
        
        # initialize a empty matrix with all the future data
        
        self.total_houses = total_houses
        self.matrix = self.create_house_matrix()
        self.matrix = Start_sol(self.matrix).fill_house_matrix()
        self.value = self.compute_value()
        
    def create_house_matrix(self):
        """
        The house matrix consists of the following columns:
           Variable: 
            0) x_1
            1) y_1
            2) x_2
            3) y_2
            4) house type (1 = solo, 2 = bungalow, 3 = villa)
            5) rotated (1 = 90 degree rotation, 0 = no rotation)
            6) distance
           Predifined:
            7) height
            8) width 
            9) free space
            10) price
            11) interest
        """
        
        total_houses = self.total_houses
        matrix = np.zeros(shape = (total_houses, 12))

        # for column 4 insert the array with number of house types
        matrix[:, 4] = np.concatenate((np.repeat(1, np.round(PERC_SOLO * total_houses)), 
                                       np.repeat(2, np.round(PERC_BUNG * total_houses)),
                                       np.repeat(3, np.round(PERC_VIL * total_houses))))
        
        height_func = np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['height']))
        width_func = np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['width']))
        free_func = np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['free']))
        price_func = np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['price']))
        interest_func = np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['interest']))
        matrix[:, 7] =  height_func(matrix[:, 4])
        matrix[:, 8] =  width_func(matrix[:, 4])
        matrix[:, 9] =  free_func(matrix[:, 4])
        matrix[:, 10] =  price_func(matrix[:, 4])
        matrix[:, 11] =  interest_func(matrix[:, 4])
        
        return matrix
        
    def get_house_matrix(self):
        return self.matrix
    
    def set_house_matrix(self, matrix):
        self.matrix = matrix
        
    def get_total_houses(self):
        return self.total_houses
    
    def compute_value(self):
        matrix = self.matrix
        return np.sum(matrix[:, 10] + matrix[:, 10] * matrix[:, 6] * matrix[:, 11])
        
    def get_value(self):
        return self.value