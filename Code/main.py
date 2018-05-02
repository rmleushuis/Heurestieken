# import necessary modules
import os, sys

# add current structure to path 
directory = os.path.dirname(os.path.realpath("__file__"))
sys.path.append(os.path.join(directory, "functions"))

# import house class
from house_class import House

# import functions from other documents

# define the 3 versions of the problem
total_houses = [20, 40, 60]
total_houses = 50

house = House(total_houses)
# create the class for houses

# generate a starting solution

mat = house.get_house_matrix()
value = house.get_value()
print('value:', value)
    
# draw the starting solution and don't save it

# create starting solution for first version of problem
