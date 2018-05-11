# import necessary modules
import os, sys

# add current structure to path
directory = os.path.dirname(os.path.realpath("__file__"))
sys.path.append(os.path.join(directory, "functions"))
sys.path.append(os.path.join(directory, "functions/algoritmes"))
sys.path.append(os.path.join(directory, "functions/controle"))
sys.path.append(os.path.join(directory, "functions/datastructuur"))
sys.path.append(os.path.join(directory, "functions/visualisatie"))

# import class
from house_class import House
from draw_plan import Show_grid

# import algorithms
from stoch_hill_climb import stoch_steepest_hill
from simulated_annealing import sim_ann

# define the 3 versions of the problem
total_houses = [20, 40, 60]

# select a version of the problem
total_houses = 20

# make lists to store the solutions in
random = []
stoch = []
ann = []


# create the class for houses and generate random solution
house = House(total_houses)
#house.create_water()

# link the starting solution
mat = house.get_house_matrix()
# store a copy of the starting solution
mat_copy = house.get_house_matrix().copy()
value = house.compute_value()
print("random", value)
random.append(value)

## number of iterations the algorithm has to perform
#total_it = 50
## magnitude of maximal step in generate improvement
#magni = 10
#
## stochastic hill climbing algorithm
#for iteration in range(total_it):
#    mat = stoch_steepest_hill(house, magni)
#    price = house.compute_value()
#house.set_house_matrix(mat)
#
#stoch.append(price)
## print solution
#print("stoch hill", price)
#
## draw the stochastic hill climbing solution
show_grid = Show_grid()
#mat = house.get_house_matrix()
for k in range(total_houses):
     show_grid.draw_house(mat[k, :], k)
#
## reset matrix to starting solution
#house.set_house_matrix(mat_copy)
#     
## simulated annealing algorithm  parameters
#start_temp = 1000
#end_temp = 10
#acceptance_limit = 0.1
#
#for iteration in range(total_it):
#    mat = sim_ann(house, iteration, total_it, start_temp, end_temp, acceptance_limit, magni)
#    price = house.compute_value()
#house.set_house_matrix(mat)
#
#ann.append(price)
## print solution   
#print("sim annealing", price)
#
## draw the simulated annealing algorithm solution
#show_grid = Show_grid()
#mat = house.get_house_matrix()
#for k in range(total_houses):
#     show_grid.draw_house(mat[k, :], k)