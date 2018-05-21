"""
This file runs all the different algorithms and prints the value and the map of
each solution.
"""

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
 
# import algorithms
from stoch_hill_climb import stoch_steepest_hill
from simulated_annealing import sim_ann
from hill_and_annealing_combination import hill_ann_combi
from min_max import min_max_alg
 
# chose the number of houses: 20, 40 or 60
total_houses = 20

# number of iterations an algorithm has to perform
total_it = 1

# max number of improvements which are allowed to be approximately the same
max_same_improvement = 5

# treshold value for which improvements are approximately the same
same_improvement = 1

# simulated annealing algorithm parameters
start_temp = 800
end_temp = 0.01
method = 'exp'
 
# extra parameter for combi; maximum number of times hill climbing can be applied
# and the number of times simulated annealing will be applied
max_times = 3

# extra parameter for min max; the range to choose a step from in the minimizing stage
magni = 10
 

# create the class for houses and generate random solution
house = House(total_houses, True, True)

# print the value and the map from the random solution
print("random", house.compute_value())
house.show_house_grid()

# save the random allocation as the starting solution
mat_copy =  house.get_house_matrix().copy()

# stochastic hill climbing algorithm
mat, local_max = stoch_steepest_hill(house, total_it, max_same_improvement, same_improvement)
print("stoch hill", house.compute_value())
house.show_house_grid()
 
     
# reset matrix to starting solution
house.set_house_distance(mat_copy)
     
# simulated annealing algrotihm
mat = sim_ann(house, total_it, start_temp, end_temp, 
              max_same_improvement, same_improvement, method)
print("sim annealing", house.compute_value())
house.show_house_grid()
     
# reset matrix to starting solution
house.set_house_distance(mat_copy)

# combi algorithm
mat = hill_ann_combi(house, total_it, start_temp, end_temp, max_same_improvement, 
                     same_improvement, max_times, method)  
print("combi", house.compute_value())
house.show_house_grid()

# reset matrix to starting solution
house.set_house_distance(mat_copy)

# min max algorithm
mat = min_max_alg(house, total_it, start_temp, end_temp, max_same_improvement, 
                  same_improvement, max_times, total_houses, magni, method)
print("min max", house.compute_value())
house.show_house_grid()

