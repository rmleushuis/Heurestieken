<<<<<<< HEAD
<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
>>>>>>> 9f722308696a7d0cd284b1f7813d04428b280552
# import necessary modules
import os, sys

# add current structure to path 
directory = os.path.dirname(os.path.realpath("__file__"))
sys.path.append(os.path.join(directory, "functions"))
<<<<<<< HEAD
=======
# import function
from Functions import draw_plan
from draw_plan import draw_plan

>>>>>>> 2957726b5e6eae439ce692ca5089787fc20e7f5e
# import house class
from house_class import house

# import functions from other documents
from draw_plan import draw_plan
from start_sol import start_sol

<<<<<<< HEAD
# import necessary modules
import os, sys

# add current structure to path 
directory = os.path.dirname(os.path.realpath("__file__"))
sys.path.append(os.path.join(directory, "functions"))
=======
>>>>>>> a22226728e76800b257e2e88e31ec426c5b058e3
=======
>>>>>>> 9f722308696a7d0cd284b1f7813d04428b280552

# import house class
from house_class import House

# import functions from other documents
from start_sol import Start_sol
>>>>>>> 2957726b5e6eae439ce692ca5089787fc20e7f5e

# define the 3 versions of the problem
total_houses = [20, 40, 60]
total_houses = 10

house = House(total_houses)
# create the class for houses

# generate a starting solution
start_sol = Start_sol(house)
f = start_sol.fill_house_matrix()
    
    # draw the starting solution and don't save it

# create starting solution for first version of problem
