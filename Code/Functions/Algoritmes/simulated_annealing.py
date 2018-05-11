"""
This function uses a simulated annealing algorithm to find a local maxima.
 
Input:  class containing the matrix, current iteration (n), starting temperature 
        (T0) that will go to ending temperature (TN) when the 
        maximum number of iterations (N) is reached, the minimum change that is
        accepted (min_chance)
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
import math

# import functions from other documents
from check_house import check_house
from gen_improvement import gen_improv

def sim_ann(houses, n, N, T0, TN, min_chance, magni):
    
    # choose a random house to move
    house = random.randint(0, houses.total_houses - 1)
    
    # set up for while loop
    improvement = -1
    max_repeats = 4000
    counter = 0
    
    # geef als parameter temperatuur afname structuur mee en kies hier dan juiste
    # lin: curr_temp = T0 - n*(T0 - TN)/N
    # exp: curr_temp = math.pow(T0*(TN/T0),(n/N))
    # sigmoidal: curr_temp = TN + (T0-TN)/(1 + math.exp(0.3*n-N/2))
    # geman: curr_temp = c/math.log(n) + d --> c en d?
    
    
    # calculate old value and store old matrix
    old_value = houses.compute_value().copy()
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
            improvement = new_value - old_value
            
            # check acceptance
            if improvement < 0:
                curr_temp = math.pow(T0*(TN/T0),(n/N))
                improv_chance = math.exp(improvement/curr_temp)
                if improv_chance > min_chance:
                    improvement = 10
        
        # check validity of new position and acceptance (not accepted if imp still neg)
        if valid == 1 or improvement < 0:
            counter += 1
            houses.set_house_matrix(matrix_old)
     
            # continue until max_repeats is reached
            if max_repeats == counter:
                matrix_improv = matrix_old
                break

    return matrix_improv