# import house class
from house_class import house

# import functions from other documents
from draw_plan import draw_plan
from start_sol import start_sol

# import necessary modules
import os, sys

# add current structure to path 
directory = os.path.dirname(os.path.realpath("__file__"))
sys.path.append(os.path.join(directory, "functions"))

# define the 3 versions of the problem
total_houses = [20, 40, 60]

def starting_sol(version):
    
    # create the class for houses
    houses = house(version)
    
    # generate a starting solution
    houses.matrix = start_sol(houses)
    
    # draw the starting solution and don't save it
    draw_plan(houses, 0)

# create starting solution for first version of problem
starting_sol(40)