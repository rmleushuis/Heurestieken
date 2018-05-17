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
from hill_and_annealing_combination import hill_ann_combi
from min_max import min_max_alg
from hill_climb import hill
 
# define the 3 versions of the problem
total_houses = [20, 40, 60]
 
# select a version of the problem
total_houses = 20
 
# make lists to store the solutions in
random = []
stoch = []
ann = []
# create the class for houses and generate random solution
house = House(total_houses, True, True)


# link the starting solution
mat = house.get_house_matrix().copy()
house.set_house_matrix(mat)

# store a copy of the starting solution
mat_copy = house.get_house_matrix().copy()
value = house.compute_value()
print("random", value)
random.append(value)

show_grid = Show_grid()
mat = house.get_house_matrix()
for k in range(len(mat[:,1])):
     show_grid.draw_house(mat[k, :], k)


# number of iterations the algorithm has to perform
total_it =10
# magnitude of maximal step in generate improvement
magni = 10
# max improvements which are allowed to be approximately the same
max_same_improvement = 3
# treshold value for which improvements are approximately the same
same_improvement = 1

# stochastic hill climbing algorithm
mat, local_max = stoch_steepest_hill(house, total_it, max_same_improvement, same_improvement)
 
# print solution
print("stoch hill", house.compute_value())
 
# draw the stochastic hill climbing solution
show_grid = Show_grid()
mat = house.get_house_matrix()
for k in range(len(mat[:,1])):
     show_grid.draw_house(mat[k, :], k)
 
     
# reset matrix to starting solution
house.set_house_matrix(mat_copy)
     
# simulated annealing algorithm  parameters
start_temp = 1000
end_temp = 10
acceptance_limit = 0.5
 
mat = sim_ann(house, total_it, start_temp, end_temp, acceptance_limit,
              magni, max_same_improvement, same_improvement)
 
# print solution   
print("sim annealing", house.compute_value())
 
# draw the simulated annealing algorithm solution
show_grid = Show_grid()
mat = house.get_house_matrix()
for k in range(len(mat[:,1])):
     show_grid.draw_house(mat[k, :], k)
     
# reset matrix to starting solution
house.set_house_matrix(mat_copy)

# extra combi parameter; maximum number of times hill climbing can be applied
max_times = 3

mat = hill_ann_combi(house, total_it, start_temp, end_temp, acceptance_limit,
              magni, max_same_improvement, same_improvement, max_times)

# print solution   
print("combi", house.compute_value())
 
# draw the simulated annealing algorithm solution
show_grid = Show_grid()
mat = house.get_house_matrix()
for k in range(len(mat[:,1])):
     show_grid.draw_house(mat[k, :], k)

# reset matrix to starting solution
house.set_house_matrix(mat_copy)

mat = min_max_alg(house, total_it, start_temp, end_temp, acceptance_limit, magni, 
                  max_same_improvement, same_improvement, max_times, total_houses)

# print solution   
print("min max", house.compute_value())
 
# draw the simulated annealing algorithm solution
show_grid = Show_grid()
mat = house.get_house_matrix()
for k in range(len(mat[:,1])):
     show_grid.draw_house(mat[k, :], k)

