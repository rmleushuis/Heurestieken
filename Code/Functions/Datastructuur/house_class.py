# import necessary modules
import os, sys

# add current structure to path
directory = os.path.dirname(os.path.realpath("__file__"))
sys.path.append(os.path.join(directory, "functions"))
sys.path.append(os.path.join(directory, "functions/algoritmes"))
sys.path.append(os.path.join(directory, "functions/controle"))
sys.path.append(os.path.join(directory, "functions/datastructuur"))
sys.path.append(os.path.join(directory, "functions/visualisatie"))

# import global vars
from global_vars import PERC_SOLO, PERC_BUNG, PERC_VIL, GRID, MAX_WATERS, WATER_M2_REMAINING
from global_vars import HOUSE_CHARS

# import start solution class
from start_sol import Start_sol

# import necessary functions
from check_house import check_house, check_water

# import necessary modules
import numpy as np

class House(object):
    def __init__(self, total_houses):
        self.total_houses = total_houses
        self.matrix = self.create_house_matrix()
        self.matrix = Start_sol(self.matrix).fill_house_matrix()
        self.value = self.compute_value()
        self.water_m2_remaining = WATER_M2_REMAINING
        
    def create_house_matrix(self):
        """
        The house matrix consists of the following columns:
           variables: 
            0) x_1 (x coordinate of top right corner)
            1) y_1 (y coordinate of top right corner)
            2) x_2 (x coordinate of bottom left corner)
            3) y_2 (y coordinate of bottom left corner)
            4) type (1 = solo, 2 = bungalow, 3 = villa, 4 = water)
            5) rotated (0 = no rotation, 1 = 90 degree rotation)
            6) distance (minimum distance to other house, wall to wall)
           constants:
            7) height (grid height of the house)
            8) width  (grid width of the house)
            9) free space (minimum free space needed for the type house)
            10) price (price of the type house)
            11) interest (percentage received for each extra meter of free space)
            12) extra-worth/m2 ratio
            13) diagonal
        """

        # create an empty matrix
        matrix = np.zeros(shape = (self.total_houses, 14))
        
        # generate the different types of houses with their characteristics
        matrix[:, 4] = np.concatenate((np.repeat(1, np.round(PERC_SOLO * self.total_houses)), 
                                       np.repeat(2, np.round(PERC_BUNG * self.total_houses)),
                                       np.repeat(3, np.round(PERC_VIL * self.total_houses)),
                                       ))
        # shuffle
        np.random.shuffle(matrix[:, 4])
        matrix[:, 7] =  np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['height']))(matrix[:, 4])
        matrix[:, 8] =  np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['width']))(matrix[:, 4])
        matrix[:, 9] =  np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['free']))(matrix[:, 4])
        matrix[:, 10] = np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['price']))(matrix[:, 4])
        matrix[:, 11] = np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))]['interest']))(matrix[:, 4])
        matrix[:, 12] = matrix[:, 11] * matrix[:, 10] / (matrix[:, 9] * matrix[:, 8] * 2 + matrix[:, 9] * matrix[:, 7] * 2)
        return matrix
    
    # request house matrix
    def get_house_matrix(self):
        return self.matrix
    
    def create_water(self):
        for i in range(-4, 0):
            while True:
                self.matrix[i, 0] = np.random.uniform(0, GRID['width'])
                self.matrix[i, 1] = np.random.uniform(0, GRID['height'])
                self.matrix[i, 2] = np.random.uniform(self.matrix[i, 0], GRID['width'])
                self.matrix[i, 3] = np.random.uniform(0, self.matrix[i, 1])
                valid = check_water(i, self.matrix, self.water_m2_remaining)
                if valid == 0:
                    break
#     change house matrix
    def set_house_matrix(self, matrix):
        
        # by changing houses the distances in column 6 also need to be recalculated
        distance_mat = np.ones(shape = (self.total_houses + 4, self.total_houses + 4)) * 1000
        try:
            for i in range(self.total_houses):
                valid, distance  = check_house(i, matrix)
                grid_distances = distance[-4:]
                distance = distance[:-4]
                distance_mat[i, :i] = distance 
                distance_mat[i, -4:] = grid_distances
            i_upper = np.triu_indices(self.total_houses, 1)
            distance_mat[i_upper] = distance_mat.transpose()[i_upper]
            distance_mat[-4:,:] = distance_mat[:,-4:].transpose()
            matrix[:, 6] = np.min(distance_mat, axis = 0)[:-4]
        except:
            for i in range(len(matrix[:,6])):
                matrix[i, 6]=-1
        
        # change the matrix with the new distances
        self.matrix = matrix
         
    def compute_value(self):
        matrix = self.matrix
        
        # calculate the total value of the grid
        self.value = sum(matrix[:, 10] + matrix[:, 10] * matrix[:, 6] * matrix[:, 11])
        return self.value 