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
from global_vars import ALGOS

def algorithms(total_houses, number_it, algorithm):
    
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
    
    if algorithm == "stoch" or algorithm == "all":
        # stochastic hill climbing algorithm
        mat, local_max = stoch_steepest_hill(house, number_it,
                                             max_same_improvement,
                                             same_improvement)
        print("stoch hill", house.compute_value())
        house.show_house_grid()
         
        # reset matrix to starting solution
        house.set_house_distance(mat_copy)
        
    if algorithm == "sim" or algorithm == "all":  
        # simulated annealing algrotihm
        mat = sim_ann(house, number_it, start_temp, end_temp, 
                      max_same_improvement, same_improvement, method)
        print("sim annealing", house.compute_value())
        house.show_house_grid()
             
        # reset matrix to starting solution
        house.set_house_distance(mat_copy)
    
    if algorithm == "combi" or algorithm == "all":
        # combi algorithm
        mat = hill_ann_combi(house, number_it, start_temp, end_temp,
                             max_same_improvement, same_improvement, max_times, method)  
        print("combi", house.compute_value())
        house.show_house_grid()
        
        # reset matrix to starting solution
        house.set_house_distance(mat_copy)
        
    if algorithm == "minmax" or algorithm == "all":
        # min max algorithm
        mat = min_max_alg(house, number_it, start_temp, end_temp, max_same_improvement, 
                          same_improvement, max_times, total_houses, magni, method)
        print("min max", house.compute_value())
        house.show_house_grid()

def main():
    
    # ask the user for input to select a version of the problem
    total_houses = input("Number of houses would you like to optimize: ")
    
    # check if user provided integer
    while True:
        try:
            total_houses = int(total_houses)
            break
        except:
            print("Invalid characters. Stick to integers.")
            total_houses = input("Number of houses would you like to optimize: ")
            try:
                total_houses= int(total_houses)
            except:
                continue
    
    # check if selected version is a valid one
    while total_houses != 20 and total_houses != 40 and total_houses != 60:
        
        # ask user for input
        print("Invalid number of houses. Enter 20, 40 or 60.")
        
        # check again if user provided integers
        try:          
            # if not valid again ask the user for input
            total_houses = int(input("Number of houses would you like to optimize: "))
            total_houses = int(total_houses)            
        except:
            print("Invalid characters. Stick to integers.")
            continue
    
    # 1 minute corresponds to about 10 iterations when running all algorithms
    number_it = int(input("Number of iterations: "))
    
    # check if user provided integers
    try:
        number_it = int(number_it)
    except:
        print("Invalid characters. Stick to integers.")
        number_it = int(input("Number of iterations: "))
    
    # check if integer is larger than 0
    while number_it <= 0:
        # ask user for input
        print("Invalid number of iterations. Provide positive integer.")
        
        # check again if user provided integers
        try:          
            # if not valid again ask the user for input
            number_it = int(input("Number of iterations: "))           
        except:
            print("Invalid characters. Stick to integers.")
            continue

    # user choses which algorithm runs
    print("Choices of algorithms are: stoch, sim, combi, minmax and all")
    algorithm = input("Algorithms you would like to run: ")
    
    # check if provided algorithms
    valid = 0
    for i in range(len(ALGOS)):
        if algorithm == ALGOS[i]:
            valid += 1
    
    while valid == 0:     
        # user choses which algorithm runs
        print("Choices of algorithms are: stoch, sim, combi, minmax")
        algorithm = input("Algorithms you would like to run: ")
        
        # check if provided algorithms
        valid = 0
        for i in range(len(ALGOS)):
            if algorithm == ALGOS[i]:
                valid += 1
    
    # generate a random solution and visualize a series of optimizations 
    algorithms(total_houses, number_it, algorithm)
              
if __name__ == '__main__':
   main()