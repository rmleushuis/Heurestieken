# import necessary modules
import os, sys
import numpy as np

# add current structure to path 
directory = os.path.dirname(os.path.realpath("__file__"))
sys.path.append(os.path.join(directory, "functions"))

# import functions from other documents
from draw_plan import draw_plan
from start_sol import start_sol
from global_vars import perc_solo, perc_bung, perc_vil

# define the 3 versions of the problem
total_houses = [20, 40, 60]

def starting_sol(x):
    # create an empty house matrix [x_1 y_1 x_2 y_2 house_type free_space]
    house_mat = np.zeros(shape = (x, 8))
    
    # for column 4 insert the array with number of house types
    house_mat[:, 4] = np.concatenate((np.repeat(1, round(perc_solo * x)), 
                                      np.repeat(2, round(perc_bung * x)),
                                      np.repeat(3, round(perc_vil * x))))
    
    # generate a starting solution
    house_mat = start_sol(house_mat, x)
    
    # draw the starting solution and don't save it
    draw_plan(house_mat, 0, x)
 
# create starting solution for first version of problem
starting_sol(total_houses[0])