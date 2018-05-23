"""" 
This code contains the class for a numpy array containing the coordinates of
all houses and water bodies and a series of functions to perform basic tasks
on this matrix.
"""

# import global vars
from global_vars import PERC_SOLO, PERC_BUNG, PERC_VIL, GRID
from global_vars import HOUSE_CHARS, DIST2, DIST, MAX_WATERS

# import start solution class
from start_sol import Start_sol
from draw_plan import Show_grid

# import necessary modules
import numpy as np
import random
import math

class House(object):
    
    def __init__(self, total_houses, create_water = False,
                 create_houses = True, verbose = False):
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
            11) interest (percentage received for each extra meters free space)
        """
        """ This function initializes the class."""
        
        if type(total_houses) is not int:
            try:
                total_houses = int(total_houses)
            except:
                print("please insert a integer amount of houses!")
        
        self.total_houses = total_houses
        self.water_num = 0
        self.value = 0
        self.matrix = None
        
        self.grid_width = GRID['width']
        self.grid_height = GRID['height']
        
        self.conditions = {'right': self.right,
                      'lower_right': self.lower_right,
                      'lower': self.lower,
                      'lower_left': self.lower_left,
                      'left': self.left,
                      'upper_left': self.upper_left,
                      'upper': self.upper,
                      'upper_right': self.upper_right
                      }
        self.constant_columns = ['height', 'width', 'free', 'price',
                                 'interest']
        self.column_defs = {'x1': 0,
                       'y1': 1,
                       'x2': 2,
                       'y2': 3,
                       'type': 4,
                       'rotated': 5,
                       'distance': 6,
                       'height': 7,
                       'width': 8,
                       'free': 9,
                       'price': 10,
                       'interest': 11}
        
        self.grid_index = {'bottom': -1,
                          'left': -4,
                          'right': -2,
                          'top': -3}
        
        self.index_free = {'others': 0,
                      'current': 1}
        
        # initialize matrix with class function
        self.create_house_matrix()
        
        # create water planes
        if create_water:
            self.create_water_planes()  
            self.total_length = self.water_num + self.total_houses
            if verbose == True:
                print("Water elements created")
        else:
            if verbose:
                print("No water elements created")
            
        # create houses and compute total value
        if create_houses:
            self.matrix = Start_sol(self.matrix, self.water_num).fill_house_matrix()
            self.set_house_distance(self.matrix)
            self.value = self.compute_value()
            if verbose:
                print("House elements created")
        else:
            if verbose:
                print("No house elements created")
    
    """ Create a random amount of water bodies and gives them
        feasible coordinates. """        
    def create_water_planes(self):
        
        # create random water body amount
        random_water = random.randint(1, MAX_WATERS)
        
        # create temporary matrices to give the water coordinates
        new_matrix = np.zeros(shape = (self.total_houses + random_water,
                                       self.matrix.shape[1]))
        new_matrix[random_water:, :] = self.matrix.copy()
        
        # calculate the area of the total amount of water needed on the map
        water_needed = self.grid_height * self.grid_width * 0.2
        
        # loop throughe very body of water and give it coordinates
        for i in range(random_water):
            ratio = np.random.uniform(low = 0.25 , high = 4)
            # last water body has to have the remaining area of water left
            if i is (random_water - 1):
                width= math.sqrt(water_needed / ratio)
                height = ratio * width
            
            # every other water body can have a random area
            else:
                # generate random width and ratio for the water body
                width = np.random.uniform(low = 0 , high = self.grid_width)
                height = ratio * width
                
                # store old value of water needed in case invalid water body
                old_water = water_needed
                water_needed= water_needed - width * height
                
                # not allowed to put more than 20% of water on the grid
                while water_needed < 0:
                    
                    # try again to generate valid random width and ratio
                    width = np.random.uniform(low = 0 , high = self.grid_width)
                    ratio = np.random.uniform(low = 0.25 , high = 4)
                    height = ratio * width
                    water_needed = old_water - width * height
                
            while True:
            
                # fill class matrix with characteristics and position of water
                new_matrix[i, self.column_defs['x1']] = np.random.uniform(low = 0 , high = self.grid_width-width)
                new_matrix[i, self.column_defs['y1']] = np.random.uniform(low = height, high = self.grid_height)
                new_matrix[i, self.column_defs['x2']] = new_matrix[i, self.column_defs['x1']] + width
                new_matrix[i, self.column_defs['y2']] = new_matrix[i, self.column_defs['y1']] - height
                new_matrix[i, self.column_defs['type']] = 4
                new_matrix[i, self.column_defs['rotated']] = random.randint(0, 1)
                new_matrix[i, self.column_defs['height']] = height
                new_matrix[i, self.column_defs['width']] = width
                
                
                # check if location is valid
                if i > 0:
                    d = self.distancesf(i, new_matrix[:(i+1)], start = 1)
                    
                    if d:
                        break
                else:
                    break

        # store new matrix including the new water and water body number
        self.matrix = new_matrix
        self.water_num = random_water
        
    """" Create the house matrix filled with houses including their
         characteristics. """
    def create_house_matrix(self):
        
        # define the amount of columnns needed
        column_len = len(self.column_defs)

        # create an empty matrix
        matrix = np.zeros(shape = (self.total_houses, column_len))
        
        # generate the different types of houses with their characteristics
        matrix[:, self.column_defs['type']] = np.concatenate((
                np.repeat(1, np.round(PERC_SOLO * self.total_houses)), 
                np.repeat(2, np.round(PERC_BUNG * self.total_houses)),
                np.repeat(3, np.round(PERC_VIL * self.total_houses))
                ))
        
        # shuffle houses in order to avoid bias in starting solutions
        np.random.shuffle(matrix[:, self.column_defs['type']])
        
        # group the individualvectors of the constant characteristics for each house
        for const_col in self.constant_columns:
            matrix[:, self.column_defs[const_col]] =  np.vectorize(lambda x: float(HOUSE_CHARS[str(int(x))][const_col]))(matrix[:, self.column_defs['type']])
        
        self.matrix = matrix
    
    """ Return the matrix containing the houses and water bodies."""
    def get_house_matrix(self):
        return self.matrix
    
    """ Change the matrix containing the houses and water bodies
        and calculates the distances in column 6, which need to be recalculated
        for the new matrix. """
    def set_house_distance(self, matrix):
        
        if matrix.shape[0] is not self.total_length:
            print("You are trying to pass an invalid matrix for this instance")
            return 0
        # make empty list to fill up with minimum distances
        distancess = []
        # loop through every house (non water body) and calculate distance
        for j in range(self.water_num, self.total_length):
            new_dist = self.distancesf(j, matrix)
            distancess.append(new_dist)
        
        # set column 6
        matrix[self.water_num:, self.column_defs['distance']] = distancess
        
        # change the matrix with the new distances
        self.matrix = matrix
        
    """ This function calculates the total value of the grid accounting for the
        free distance between houses and the different types of houses."""        
    def compute_value(self):
        matrix = self.matrix
        self.value = sum(matrix[:, self.column_defs['price']] * (1 + matrix[:, self.column_defs['distance']] * matrix[:, self.column_defs['interest']]))
        
        return self.value 

    """ This function creates a class for a visualisation of the grid containing
        all houses and water bodies."""    
    def show_house_grid(self):
        # create grid object
        show_grid = Show_grid()
        
        # draw each water body and house iterative
        for it in range(self.total_length):
            show_grid.draw_house(self.matrix[it, :], it)
            
    def upper_right(self, sides, positions):
        
        x1 = positions['x1']
        y2 = positions['y2']
        
        right_side = sides['right']
        top_side = sides['upper']
        
        upper_right = np.logical_and(x1 > right_side, y2 > top_side)
        
        return upper_right
    
    def lower_right(self, sides, positions):
        
        x1 = positions['x1']
        y1 = positions['y1']
        
        right_side = sides['right']
        bottom_side = sides['bottom']
        
        lower_right = np.logical_and(x1 > right_side, y1 < bottom_side)
        
        return lower_right
    
    def right(self, sides, positions):
        
        x1 = positions['x1']
        y1 = positions['y1']
        y2 = positions['y2']
        
        right_side = sides['right']
        top_side = sides['upper']
        bottom_side = sides['bottom']
        
        right = np.logical_and(x1 > right_side, np.logical_and(y2 <= top_side, y1 >= bottom_side))
    
        return right
    
    def upper_left(self, sides, positions):
        
        x2 = positions['x2']
        y2 = positions['y2']
        
        left_side = sides['left']
        top_side = sides['upper']
        
        upper_left = np.logical_and(x2 < left_side, y2 > top_side)
        
        return upper_left
    
    def lower_left(self, sides, positions):
        
        x2 = positions['x2']
        y1 = positions['y1']
        
        left_side = sides['left']
        bottom_side = sides['bottom']
        
        lower_left = np.logical_and(x2 < left_side, y1 < bottom_side)
        
        return lower_left
    
    def left(self, sides, positions):
        
        x2 = positions['x2']
        y1 = positions['y1']
        y2 = positions['y2']
        
        left_side = sides['left']
        top_side = sides['upper']
        bottom_side = sides['bottom']
        
        left = np.logical_and(x2 < left_side, np.logical_and(y2 <= top_side, y1 >= bottom_side))
        
        return left
    
    def upper(self, sides, positions):
        
        x1 = positions['x1']
        x2 = positions['x2']
        y2 = positions['y2']
        
        left_side = sides['left']
        top_side = sides['upper']
        right_side = sides['right']
        
        upper = np.logical_and(y2 > top_side, np.logical_and(x2 >= left_side, x1 <= right_side))
        
        return upper
    
    def lower(self, sides, positions):
        
        x1 = positions['x1']
        x2 = positions['x2']
        y1= positions['y1']
        
        left_side = sides['left']
        right_side = sides['right']
        bottom_side = sides['bottom']
        
        lower = np.logical_and(y1 < bottom_side, np.logical_and(x2 >= left_side, x1 <= right_side))
        
        return lower
    
    def grid_conditions(self, positions, free_space_cur):
        
        left = positions['x1'] >= free_space_cur
        right = positions['x2'] <= (self.grid_width - free_space_cur)
        top = positions['y1'] <= (self.grid_height - free_space_cur)
        bottom = positions['y2'] >= free_space_cur
        
        grid_conditions = np.array([left, right, bottom, top])
        
        return grid_conditions
        
        
    """ This function evaluates whether none of the free space conditions are
        violated and calculates the minimum distance between houses.""" 
    def distancesf(self, loc, matrix, start = 0):
        
        matrix = matrix.copy()
        
        # obligated free space of the current house
        free_space_cur = matrix[loc, self.column_defs['free']]
        
        positions_ = {'x1': matrix[loc, self.column_defs['x1']],
                     'y1': matrix[loc, self.column_defs['y1']],
                     'x2': matrix[loc, self.column_defs['x2']],
                     'y2': matrix[loc, self.column_defs['y2']]}
        
        temp = np.delete(matrix, loc, axis = 0)
        
        # obligated free space of all other houses
        house_free_space = temp[:, self.column_defs['free']]
        
        
        free_space = np.ones((len(house_free_space), len(self.index_free))) * free_space_cur
        free_space[:, self.index_free['others']] = house_free_space
        
        # allow houses to be placed directly to the water
        free_space[:self.water_num, self.index_free['current']] = 0.0
        
        # find the maximum obligated free space
        free_space = np.max(free_space, axis = 1)
        
        sides = {'right': temp[:, self.column_defs['x2']] + free_space,
                 'left': temp[:, self.column_defs['x1']] - free_space,
                 'upper': temp[:, self.column_defs['y1']] + free_space,
                 'bottom': temp[:, self.column_defs['y2']] - free_space}
        
        """ 
        The following 8 conditions check the minimum distance in each of the 8 
        areas around a house, as defined in the comment visualisation below.
        """
        # UL # U # UR
        # L # H # R
        # LL # L # LR
        
        all_conditions = []
        
        for condition in self.conditions.values():
            all_conditions.append(condition(sides, positions_))
         
        all_conditions = np.array(all_conditions)
        
        # create a matrix of all 4 grid conditions to test them all at once
        grid_cond = self.grid_conditions(positions_, free_space_cur)

        # check whether all conditions are satisfied
        if all(all_conditions.sum(0)) and all(grid_cond):
            
            if start:
                return 1
            
            # remove water bodies as they have no influence on the minimal distance
            all_conditions = all_conditions[:, self.water_num:]
            temp = temp[self.water_num:]
            
            # initaite a empty vector of distances to all other houses
            distance_ind = np.argmax(all_conditions, axis = 0)
            
            # make an empty distance vector (houses + grid distances)
            distances = np.array([0.0] * (len(distance_ind) + grid_cond.shape[0]))
            
            # calculate the minimum distance of the house to other houses
            positions = np.array(list(positions_.values()))
            
            # iterate over all other houses and find its distance
            for i in range(len(temp)):
                plane = distance_ind[i]
                
                # 2d vector of the differences in x and y position
                m = np.abs(positions[DIST2[str(plane)]] - temp[i, DIST[str(plane)]]) 

                # use the corresponding distance measure
                if not plane % 2:
                    distances[i] = np.abs(m) - free_space_cur
                else:
                    distances[i] = np.sqrt(np.dot(m, m)) - free_space_cur
            
            # calculate grid distances
            
            distances[self.grid_index['bottom']] = positions_['y2'] - free_space_cur
            distances[self.grid_index['right']] = self.grid_width- (free_space_cur + positions_['x2'])
            distances[self.grid_index['top']] = self.grid_height - (free_space_cur + positions_['y1'])
            distances[self.grid_index['left']] = positions_['x1'] - free_space_cur
            # return valid and the minimal distance
#            print(distances)
            return np.min(distances)
        
        # if conditions are not satisfied return not valid
        return 0