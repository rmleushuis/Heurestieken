"""
This function uses a stochastic hill climbing algorithm to find a local maxima.
 
Input:  class containing the matrix and magnitude of max change
Output: plan of the optimized house positions
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

# import necessary modules
import random

# import functions from other documents
from check_house import check_house
from gen_improvement import gen_improv

def stoch_steepest_hill(houses, magni, max_it, stop_improv, criteria):
    
    # count iterations
    n = 0
    # count last stop_improv iterations
    counter = 0
    
    while n < max_it and counter < stop_improv:
        n += 1
        mat, improvement = stoch_steepest_hill_step(houses, magni)
        houses.compute_value()
        if improvement < criteria:
            counter += 1
        else: 
            counter = 0    
    houses.set_house_matrix(mat)
    return houses.get_house_matrix()

def stoch_steepest_hill_step(houses, magni):
    
    # choose a random house to move
    house = random.randint(0, houses.total_houses - 1)
    
    # set up for while loop
    improvement = -1
    new_value  = 'nan'
    max_repeats = 4
    counter = 0
    
    # calculate  old value and store old matrix
    old = houses.compute_value().copy()
    matrix_old = houses.get_house_matrix().copy()
    
    while improvement < 0:
        
        # generate copy of the matrix to try improvements on
        matrix_copy = houses.get_house_matrix().copy()
        matrix_improv = gen_improv(matrix_copy, house, magni)
        
        # calculate distance
        valid, distance = check_house(house, matrix_improv)
        
        # if new position is valid
        if valid == 0 :
            # calculate new value
            houses.set_house_matrix(matrix_improv)
            new_value = houses.compute_value()   
            # calculate improvement
            improvement = new_value - old

        
        # if new position is not valid or the improvement is negative
        if valid == 1 or improvement < 0:
            counter += 1
            houses.set_house_matrix(matrix_old)
            
            # continue until max_repeats is reached
            if max_repeats == counter:
                matrix_improv = matrix_old
                matrix_improv, improvement = stoch_steepest_hill_step(houses,magni)
                break

    return matrix_improv, improvement