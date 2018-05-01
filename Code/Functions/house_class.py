# import global vars
from global_vars import PERC_SOLO, PERC_BUNG, PERC_VIL
from global_vars import GRID, HOUSE_CHARS
# import necessary modules
import numpy as np

# this is a class for the houses
class House(object):
    def __init__(self, total_houses):
        
        # initialize a empty matrix with all the future data
        self.value = None
        self.total_houses = total_houses
        self.matrix = self.create_house_matrix()
        
        
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
        """
        
        total_houses = self.total_houses
        matrix = np.zeros(shape = (total_houses, 10))

        # for column 4 insert the array with number of house types
        matrix[:, 4] = np.concatenate((np.repeat(1, np.round(PERC_SOLO * total_houses)), 
                                       np.repeat(2, np.round(PERC_BUNG * total_houses)),
                                       np.repeat(3, np.round(PERC_VIL * total_houses))))
        
        height_func = np.vectorize(lambda x: HOUSE_CHARS[str(int(x))]['height'])
        width_func = np.vectorize(lambda x: HOUSE_CHARS[str(int(x))]['width'])
        free_func = np.vectorize(lambda x: HOUSE_CHARS[str(int(x))]['free'])

        matrix[:, 7] =  height_func(matrix[:, 4])
        matrix[:, 8] =  width_func(matrix[:, 4])
        matrix[:, 9] =  free_func(matrix[:, 4])
        
        return matrix
        
    def get_house_matrix(self):
        return self.matrix
    
    def set_house_matrix(self, matrix):
        self.matrix = matrix
        
    def get_total_houses(self):
        return self.total_houses
    
    def update_value(self, new_value):
        self.value = new_value