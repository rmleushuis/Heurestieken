# import global vars
from global_vars import PERC_SOLO, PERC_BUNG, PERC_VIL
from global_vars import GRID, HOUSE_CHARS
# import necessary modules
import numpy as np

# this is a class for the houses
<<<<<<< HEAD
class house(object):
    def __init__(self, version):
=======
class House(object):
<<<<<<< HEAD
    def __init__(self, total_houses):
=======
    def __init__(self, version):
        self.version = version
        self.matrix = self.conc(version)
        self.rows = version
        self.value = -10000000
        self.columns = self.matrix.shape[1]
            
>>>>>>> a22226728e76800b257e2e88e31ec426c5b058e3
>>>>>>> 2957726b5e6eae439ce692ca5089787fc20e7f5e
        
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
<<<<<<< HEAD
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
=======
        matrix[:, 4] = np.concatenate((np.repeat(1, PERC_SOLO * version), 
                                       np.repeat(2, PERC_BUNG * version),
                                       np.repeat(3, PERC_VIL * version)))
<<<<<<< HEAD
        
        self.version = version
        self.matrix = matrix
        self.rows = version
        self.columns = matrix.shape[1]
=======
        return matrix
    
    
    def update_value(self, new_value):
        self.value = new_value
>>>>>>> a22226728e76800b257e2e88e31ec426c5b058e3
>>>>>>> 2957726b5e6eae439ce692ca5089787fc20e7f5e
