"""
This file contains a class containing functions which determine the discrete
exhaustive search solution.
"""

# import necessary modules
import numpy as np

# import global variables and classes
from global_vars import GRID
from draw_plan import Show_grid

class LuuksAlgo():
    
    def __init__(self, matrix, house):
        """This function initializes the class."""
        
        self.total_width = GRID['width']
        self.total_height = GRID['height']
        self.matrix_length = len(matrix)
        self.house = house
        self.matrix_sorted = matrix[matrix[:, 4].argsort()[::-1]]
        self.num_waters = sum(self.matrix_sorted[:, 4] == 4)
        
        
    def show_unused_spaces(self, matrix = None):
        """This function visualizes the free space of each house."""
        
        # make copy of the matrices
        if matrix is None:
            house_matrix = self.matrix_sorted.copy()
            house_matrix2 = self.matrix_sorted.copy()
        else:
            house_matrix = matrix.copy()
            house_matrix2 = matrix.copy()
        
        # make grid
        show_grid = Show_grid()
        
        # draw houses and water bodies
        for i in range(2):
            for loc in range(len(house_matrix)):
                if i == 0:
                    house_matrix2[loc, 4] = 4
                    show_grid.draw_house(house_matrix2[loc, :], loc,
                                         numbers = True, types = 'circles')
                else:
                    show_grid.draw_house(house_matrix[loc, :], loc,
                                         numbers = True)
                
    def compute_value(self, matrix):
        """This function calculates the total value of the grid."""
    
        return sum(matrix[:, 10] * (1 + matrix[:, 6] * matrix[:, 11]))
    
    def algo(self, epochs = 2, verbose = 0):
        """This function runs the exhaustive search to find the discrete
           optimal solution. """
        
        # make copy of the matrix
        print("Start exhaustive search")
        temp_matrix1 = self.matrix_sorted.copy()
        temp_matrix2 = self.matrix_sorted.copy()
        old_value = self.compute_value(temp_matrix1)
        
        # initialize values
        self.stop = 0
        epoch = 0
        self.combs = 0
        
        # function to try every possible combination
        while epoch < epochs:
            
            # start values
            start_value = old_value
            epoch += 1
            iterator = 0
            
            for loc in range(self.num_waters, self.matrix_length):
                iterator += 1
                for y1 in range(int(temp_matrix1[loc,9] + \
                          temp_matrix1[loc, 7]), int(self.total_height -  \
                          temp_matrix1[loc, 9])):
                    for x1 in range(int(temp_matrix1[loc, 9]),
                              int(self.total_width - temp_matrix1[loc, 9] - \
                              temp_matrix1[loc, 8])):
                        temp_matrix1[loc,0] = float(x1)
                        temp_matrix1[loc,1] = float(y1)
                        temp_matrix1[loc, 2] = temp_matrix1[loc, 0] + \
                                               temp_matrix1[loc, 8]
                        temp_matrix1[loc, 3] = temp_matrix1[loc, 1] - \
                                               temp_matrix1[loc, 7]
                        d = self.house.distancesf(loc, temp_matrix1)
                        
                        # calculate distances
                        if d not in [0,1]:
                            distancess = []
                            for j in range(self.num_waters,
                                           self.matrix_length):
                                d = self.house.distancesf(j, temp_matrix1)
                                distancess.append(d)                    
                            temp_matrix1[self.num_waters:, 6] = distancess
                            new_value = self.compute_value(temp_matrix1)
                            
                            # check if new value is higher
                            if new_value > old_value:
                                old_value = new_value
                                temp_matrix2 = temp_matrix1.copy()
                            else:
                                temp_matrix1 = temp_matrix2.copy()
                                
                if verbose == 2:
                    print("Epoch:", epoch, 'Iteration:', str(iterator) + \
                          '/' + str(self.matrix_length - self.num_waters) ,
                          "Increase:", old_value - start_value)
                                    
            temp_houses = temp_matrix2[np.argsort(temp_matrix2[:,6])[::-1],
                                       ].copy()
            
            # loop through matrix and see if solution is feasible
            for i in range(self.num_waters, self.matrix_length):
                
                # create temporary variables
                x1s = temp_matrix1[i, 0]
                y1s = temp_matrix1[i, 1]
                
                for k in range(self.matrix_length - self.num_waters):
                    x1 = temp_houses[k, 0]
                    y1 = temp_houses[k, 1]
                    
                    if x1 == x1s and y1 == y1s:
                        pass
                    else:
                        
                        # create temporary variables        
                        temp_matrix1[i, 0] = x1
                        temp_matrix1[i, 1] = y1
                        temp_matrix1[i,2] = temp_matrix1[i,0] + \
                                            temp_matrix1[i,5] * \
                                            temp_matrix1[i,7] + \
                                            (1 - temp_matrix1[i,5]) * \
                                            temp_matrix1[i, 8]
                        temp_matrix1[i, 3] = temp_matrix1[i, 1] - \
                                             temp_matrix1[i,5] * \
                                             temp_matrix1[i, 8] - \
                                             (1 - temp_matrix1[i,5]) * \
                                             temp_matrix1[i, 7]
                        loc = np.where(temp_matrix1[:, 0] == x1)[0][0]
                        temp_matrix1[loc, 0] = x1s
                        temp_matrix1[loc, 1] = y1s
                        temp_matrix1[loc,2] = temp_matrix1[loc,0] + \
                                              temp_matrix1[loc,5] * \
                                              temp_matrix1[loc,7] + \
                                              (1 - temp_matrix1[loc,5]) * \
                                              temp_matrix1[loc, 8]
                        temp_matrix1[loc, 3] = temp_matrix1[loc, 1] - \
                                               temp_matrix1[loc,5] *  \
                                               temp_matrix1[loc, 8] - \
                                               (1 - temp_matrix1[loc,5]) * \
                                               temp_matrix1[loc, 7]
                        d = self.house.distancesf(i, temp_matrix1)
                        
                        # calculate distances
                        if d is not None:
                            distancess = []
                            for j in range(self.num_waters,
                                           self.matrix_length):
                                d = self.house.distancesf(j, temp_matrix1)
                                distancess.append(d)                    
                            
                            # calculate increases
                            temp_matrix1[self.num_waters:, 6] = distancess
                            value_new = self.compute_value(temp_matrix1)
                            if value_new > old_value:
                                print('increase:', value_new - old_value)
                                old_value = value_new
                                temp_matrix2 = temp_matrix1.copy()
                            else:
                                temp_matrix1 = temp_matrix2.copy()
            
            # print optimization epochs
            if verbose == 1:
                print("Epoch:", epoch, "Increase:", old_value - start_value)
            if old_value - start_value < 0.01:
                print('Converged')
                break
            
        print('Did not converge')
        print("exhaustive search: ", old_value)
        
        self.matrix_sorted = temp_matrix2
        
    def get_matrix(self):
        """This function returns the matrix containing houses."""
        
        return self.matrix_sorted