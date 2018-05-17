# import global vars
from global_vars import PERC_SOLO, PERC_BUNG, PERC_VIL, GRID
from global_vars import HOUSE_CHARS

# import start solution class
from start_sol import Start_sol
from draw_plan import Show_grid

# import necessary functions
from check_house import check_house

# import necessary modules
import numpy as np
import random
import math

class House(object):
    def __init__(self, total_houses, create_water = False, create_houses = True):
        self.total_houses = total_houses
        self.matrix = self.create_house_matrix()
        
        if create_water == True:
            water = self.create_water_planes()
            
        if create_houses == True:
            self.matrix[( create_water * water ):,:] = Start_sol(self.matrix, water).fill_house_matrix()
            
        self.water_num = water   
        self.value = self.compute_value()
        
    def create_water_planes(self):
        # random water amount
        random_water = random.randint(1,4)
        new_matrix = np.zeros(shape = (self.total_houses + random_water, self.matrix.shape[1]))
        new_matrix[random_water:, :] = self.matrix.copy()
        water_needed = GRID["height"] * GRID["width"] * 0.2
        
        for i in range(random_water):
            
            if i == (random_water -1):
                ratio = np.random.uniform(low = 0.25 , high = 4)
                width= math.sqrt(water_needed/ratio)
                height = ratio * width
            
            else:
                width = np.random.uniform(low = 0 , high = GRID["width"])
                ratio = np.random.uniform(low = 0.25 , high = 4)
                height = ratio * width
                old_water = water_needed
                water_needed= water_needed - width*height
                
                # not allowed to put more than 20% of water on the grid
                while water_needed < 0:
                    width = np.random.uniform(low = 0 , high = GRID["width"])
                    ratio = np.random.uniform(low = 0.25 , high = 4)
                    height = ratio * width
                    water_needed = old_water-width*height
                
            # fill class matrix with characteristics and position of water
            new_matrix[i, 0] = np.random.uniform(low = 0 , high = GRID["width"]-width)
            new_matrix[i, 1] = np.random.uniform(low = height, high = GRID["height"])
            new_matrix[i, 2] = new_matrix[i, 0] + width
            new_matrix[i, 3] = new_matrix[i, 1] - height
            new_matrix[i, 4] = 4
            new_matrix[i, 5] = random.randint(0,1)
            new_matrix[i, 7] = height
            new_matrix[i, 8] = width
            
            # check if location is valid
            valid, distance = check_house(i, random_water, new_matrix)
            while valid == 1:
                new_matrix[i, 0] = np.random.uniform(low = 0 , high = GRID["width"]-width)
                new_matrix[i, 1] = np.random.uniform(low = height, high = GRID["height"])
                new_matrix[i, 2] = new_matrix[i, 0] + width
                new_matrix[i, 3] = new_matrix[i, 1] - height
                new_matrix[i, 4] = 4
                new_matrix[i, 5] = random.randint(0,1)
                new_matrix[i, 7] = height
                new_matrix[i, 8] = width
                valid, distance = check_house(i, random_water, new_matrix)
    
                        
        self.matrix = new_matrix
        return random_water
        

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
        """

        # create an empty matrix
        matrix = np.zeros(shape = (self.total_houses, 13))
        
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
    
#     change house matrix
    def set_house_matrix(self, matrix):
        # by changing houses the distances in column 6 also need to be recalculated
        distance_mat = np.ones(shape = (self.total_houses + 4 , self.total_houses + 4)) * 1000
        
        try:
            for i in range(self.water_num,len(matrix[:,6])):
                valid, distance  = check_house(i,self.water_num, matrix)
                grid_distances = distance[-4:]
                distance = distance[:-4]
                distance_mat[i, :i] = distance 
                distance_mat[i, -4:] = grid_distances
            i_upper = np.triu_indices(self.total_houses, 1)
            distance_mat[i_upper] = distance_mat.transpose()[i_upper]
            distance_mat[-4:,:] = distance_mat[:,-4:].transpose()
            matrix[self.water_num:, 6] = np.min(distance_mat, axis = 0)[:-4]
        except:
            for i in range(self.water_num,len(matrix[:,6])):
                matrix[i, 6]=-100
        
        # change the matrix with the new distances
        self.matrix = matrix
         
    def compute_value(self):
        matrix = self.matrix
        
        # calculate the total value of the grid
        self.value = sum(matrix[:, 10] + matrix[:, 10] * matrix[:, 6] * matrix[:, 11])
        return self.value 
    
    def show_house_grid(self):
        
        # draw the stochastic hill climbing solution
        show_grid = Show_grid()
        mat = self.matrix
        for k in range(len(mat)):
            show_grid.draw_house(mat[k, :], k)
 