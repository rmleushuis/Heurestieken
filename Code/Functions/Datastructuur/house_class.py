"""" 
This code contains the class for a numpy array containing the coordinates of
all houses and water bodies and a series of functions to perform basic tasks
on this matrix.
"""

# import global vars
from global_vars import PERC_SOLO, PERC_BUNG, PERC_VIL, GRID
from global_vars import HOUSE_CHARS, DIST2, DIST

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
        """ This function initializes the class."""
        self.total_houses = total_houses
        self.water_num = 0
        self.value = 0
        self.matrix = None
        
        # initialize matrix with class function
        self.create_house_matrix()
        
        # create water planes
        if create_water == True:
            self.create_water_planes()  
            
        # create houses and compute total value
        if create_houses == True:
            self.matrix = Start_sol(self.matrix, self.water_num).fill_house_matrix()
            self.set_house_distance(self.matrix)
            self.value = self.compute_value()
    
    """ This function creates a random amount of water bodies and gives them
        feasible coordinates. """        
    def create_water_planes(self):
        
        # create random water body amount
        random_water = random.randint(1, 4)
        
        # create temporary matrices to give the water coordinates
        new_matrix = np.zeros(shape = (self.total_houses + random_water,
                                       self.matrix.shape[1]))
        new_matrix[random_water:, :] = self.matrix.copy()
        
        # calculate the area of the total amount of water needed on the map
        water_needed = GRID["height"] * GRID["width"] * 0.2
        
        # loop throughe very body of water and give it coordinates
        for i in range(random_water):
            
            # last water body has to have the remaining area of water left
            if i == (random_water - 1):
                ratio = np.random.uniform(low = 0.25 , high = 4)
                width= math.sqrt(water_needed/ratio)
                height = ratio * width
            
            # every other water body can have a random area
            else:
                
                # generate random width and ratio for the water body
                width = np.random.uniform(low = 0 , high = GRID["width"])
                ratio = np.random.uniform(low = 0.25 , high = 4)
                height = ratio * width
                
                # store old value of water needed in case invalid water body
                old_water = water_needed
                water_needed= water_needed - width*height
                
                # not allowed to put more than 20% of water on the grid
                while water_needed < 0:
                    
                    # try again to generate valid random width and ratio
                    width = np.random.uniform(low = 0 , high = GRID["width"])
                    ratio = np.random.uniform(low = 0.25 , high = 4)
                    height = ratio * width
                    water_needed = old_water - width * height
                
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
            
            # if invalid generate new position
            while check_house(i, random_water, new_matrix)[0]:
                new_matrix[i, 0] = np.random.uniform(low = 0 , high = GRID["width"]-width)
                new_matrix[i, 1] = np.random.uniform(low = height, high = GRID["height"])
                new_matrix[i, 2] = new_matrix[i, 0] + width
                new_matrix[i, 3] = new_matrix[i, 1] - height
                new_matrix[i, 4] = 4
                new_matrix[i, 5] = random.randint(0, 1)
                new_matrix[i, 7] = height
                new_matrix[i, 8] = width
                valid, distance = check_house(i, random_water, new_matrix)
    
        # store new matrix including the new water and water body number
        self.matrix = new_matrix
        self.water_num = random_water
        
    """" This function creates the house matrix filled with houses including their
         characteristics. """
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
        """
        
        # define basic characteristics
        constants = ['height', 'width', 'free', 'price', 'interest']
        columns = 12
        constant_columns = range(7, columns)

        # create an empty matrix
        matrix = np.zeros(shape = (self.total_houses, columns))
        
        # generate the different types of houses with their characteristics
        matrix[:, 4] = np.concatenate((
                np.repeat(1, np.round(PERC_SOLO * self.total_houses)), 
                np.repeat(2, np.round(PERC_BUNG * self.total_houses)),
                np.repeat(3, np.round(PERC_VIL * self.total_houses)),
                ))
        
        # shuffle houses in order to avoid bias in starting solutions
        np.random.shuffle(matrix[:, 4])
        
        # group the individualvectors of the constant characteristics for each house
        for i, const in zip(constant_columns, constants):
            matrix[:, i] =  np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))] \
                                          [const]))(matrix[:, 4])
        self.matrix = matrix
    
    """ This function returns the matrix containing the houses and water bodies."""
    def get_house_matrix(self):
        return self.matrix
    
    """ This function changes the matrix containing the houses and water bodies
        and calculates the distances in column 6, which need to be recalculated
        for the new matrix. """
    def set_house_distance(self, matrix):
        
        # make empty list to fill up with minimum distances
        distancess = []
        
        # loop through every house (non water body) and calculate distance
        for j in range(self.water_num, len(matrix)):
            valid, new_dist = self.distancesf(j, matrix)
            distancess.append(new_dist)
        
        # set column 6
        matrix[self.water_num:, 6] = distancess
        
        # change the matrix with the new distances
        self.matrix = matrix
        
    """ This function calculates the total value of the grid accounting for the
        free distance between houses and the different types of houses."""        
    def compute_value(self):
        matrix = self.matrix
        self.value = sum(matrix[:, 10] + matrix[:, 10] * matrix[:, 6] * matrix[:, 11])
        return self.value 

    """ This function creates a class for a visualisation of the grid containing
        all houses and water bodies."""    
    def show_house_grid(self):
        mat = self.matrix
        
        # create grid object
        show_grid = Show_grid()
        
        # draw each water body and house iterative
        for it in range(self.total_houses + self.water_num):
            show_grid.draw_house(mat[it, :], it)
        
    
    """ This function evaluates whether none of the free space conditions are
        violated and calculates the minimum distance between houses.""" 
    def distancesf(self, loc, matrix):
        
        matrix = matrix.copy()
        
        # obligated free space of the current house
        free_space_cur = matrix[loc, 9]
        
        # coordinates of water bodies and houses
        x1 = matrix[loc, 0]
        y1 = matrix[loc, 1]
        x2 = matrix[loc, 2]
        y2 = matrix[loc, 3]
        temp = np.delete(matrix, loc, 0)
        
        # obligated free space of all other houses
        house_free_space = temp[:, 9]
        
        # retrieve the positions of all sides of each house
        right_side = temp[:, 2] 
        left_side = temp[:, 0]
        top_side = temp[:, 1] 
        bottom_side = temp[:, 3]
        
        # combine the free space of all the houses
        free_space = np.ones((len(house_free_space), 2)) * free_space_cur
        free_space[:, 0] = house_free_space
        
        # allow houses to be placed directly to the water
        free_space[:self.water_num, 1] = 0.0
        
        # find the maximum obligated free space
        free_space = np.max(free_space, 1)
        
        """ 
        The following 8 conditions check the minimum distance in each of the 8 
        areas around a house, as defined in the comment visualisation below.
        """
        # 1 # 2 # 3
        # 8 # H # 4
        # 7 # 6 # 5
        first_condition = np.logical_and( x1 >= (right_side + free_space) ,
                          np.logical_or.reduce(( np.logical_and( y1 <= top_side,
                          y1 >= bottom_side ), np.logical_and( y2 <= top_side,
                          y2 >= bottom_side ), np.logical_and(y2 <= bottom_side,
                          y1 >= top_side), np.logical_and( y2 >= bottom_side,
                          y1 <= top_side))))
        second_condition = np.logical_and( x1 > (right_side + free_space),
                           y1 < (bottom_side - free_space))
        third_condition = np.logical_and( y1 <= (bottom_side - free_space),
                          np.logical_or.reduce(( np.logical_and( x1 <= right_side,
                          x1 >= left_side ), np.logical_and( x2 <= right_side,
                          x2 >= left_side ), np.logical_and(x1 <= left_side,
                          x2 >= right_side), np.logical_and( x1 >= left_side,
                          x2 <= right_side))))
        fourth_condition = np.logical_and( y1 < (bottom_side - free_space),
                           x2 < (left_side - free_space) )
        fifth_condition = np.logical_and( x2 <= (left_side - free_space),
                          np.logical_or.reduce(( np.logical_and( y1 <= top_side,
                          y1 >= bottom_side ), np.logical_and( y2 <= top_side,
                          y2 >= bottom_side ), np.logical_and( y2 <= bottom_side,
                          y1 >= top_side), np.logical_and( y2 >= bottom_side,
                        y1 <= top_side))))
        sixth_condition = np.logical_and( x2 < (left_side - free_space),
                          y2 > (top_side + free_space) )
        seventh_condition = np.logical_and( y2 >= (top_side +  free_space),
                            np.logical_or.reduce(( np.logical_and( x1 <= right_side,
                            x1 >= left_side ), np.logical_and( x2 <= right_side,
                            x2 >= left_side ), np.logical_and( x1 <= left_side, 
                            x2 >= right_side), np.logical_and( x1 >= left_side,
                            x2 <= right_side))))
        eigth_condition = np.logical_and( y2 > (top_side + free_space),
                          x1 > (right_side + free_space) )
        
        # create a matrix of all 8  distance conditions to test them all at once
        all_cond = np.array([first_condition, second_condition, third_condition,
                             fourth_condition, fifth_condition, sixth_condition,
                             seventh_condition, eigth_condition])    
        
        # the following 4 conditions test whether the house is inside the grid
        ninth_condition = x1 >= free_space_cur
        tenth_condition = x2 <= (GRID['width'] - free_space_cur)
        eleventh_condition = y1 <= (GRID['height'] - free_space_cur)
        twelfth_condition = y2 >= free_space_cur
        
        # create a matrix of all 4 grid conditions to test them all at once
        grid_cond = np.array([ninth_condition, tenth_condition, eleventh_condition,
                              twelfth_condition])

        
        # check whether all conditions are satisfied
        if all( all_cond.sum(0) == 1 ) and all( grid_cond == 1):
            
            # remove water bodies as they have no influence on the minimal distance
            all_cond = all_cond[:, self.water_num:]
            temp = temp[self.water_num:]
            positions = np.array([x1, y1, x2, y2])    
            
            # initaite a empty vector of distances to all other houses
            distance_ind = np.argmax(all_cond, axis = 0)
            distances = np.array( [0.0] * ( len(distance_ind) + 4 ) )
            
            # calculate the minimum distance of the house to other houses
            positions = np.array([x1, y1, x2, y2])
            
            # iterate over all other houses and find its distance
            for i in range(len(temp)):
                plane = distance_ind[i]
                
                # 2d vector of the differences in x and y position
                m = np.abs(positions[DIST2[str(plane)]] - temp[i, DIST[str(plane)]]) 

                # use the corresponding distance measure
                if plane % 2 == 0:
                    distances[i] = np.abs(m) - free_space_cur
                else:
                    distances[i] = np.sqrt(np.dot(m, m)) - free_space_cur
            
            # calculate grid distances
            distances[-1] = y2 - free_space_cur
            distances[-2] = (GRID['height'] - free_space_cur) - y1
            distances[-3] = (GRID['width'] - free_space_cur) - x2
            distances[-4] = x1 - free_space_cur

            # return valid and the minimal distance
            return 0, np.min(distances)
        
        # if conditions are not satisfied return not valid
        return 1, 0