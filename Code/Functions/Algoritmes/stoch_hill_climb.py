"""
This function uses a stochastic hill climbing algorithm to find a local maxima.
 
Input:  class containing the matrix and magnitude of max change
Output: plan of the optimized house positions and a binary variable for local maximum
"""
# import necessary modules
import random
import numpy as np

# import functions from other documents
from check_house import check_house
from gen_improvement import gen_improv


def stoch_steepest_hill(houses, max_it, stop_improv, criteria):
    
    # count iterations
    n = 0
    # count last stop_improv iterations
    counter = 0
    # count how often a step can be repeated
    counter2 = 0
    # local maximum check
    local_max = 0
    
    while n < max_it and counter < stop_improv:
        if n == 0:
            alpha = 4
            beta = 4
            eps = 4
            magni = alpha + beta + eps
            mat, improvement = stoch_steepest_hill_step(houses, magni, counter2)
            old_value = houses.compute_value().copy()
        else:
            # function which account for the position of the step in the total number of steps
            alpha = (max_it/n)**(1/3) * 50 * (20/houses.total_houses)**3
            # function which account for past improvement
            beta = improvement/old_value * 100
            # random component to change possible direction
            epsilon = np.random.uniform(low = 0 , high = 2*(alpha + beta))
            # calculate total range
            magni = 1/10 * (alpha + beta + epsilon)
            mat, improvement = stoch_steepest_hill_step(houses, magni, counter2)
            old_value = houses.compute_value().copy()
        n += 1
        houses.compute_value()
        if improvement < criteria:
            counter += 1
        else: 
            counter = 0   
    
    # check if the algorithm might be stuck in a local maximum
    if counter == stop_improv:
        local_max = 1
    
    houses.set_house_matrix(mat)
    return houses.get_house_matrix(), local_max

def stoch_steepest_hill_step(houses, magni, counter2):
    
    # choose a random house to move
    house = random.randint(0, houses.total_houses - 1)
    
    # set up for while loop
    improvement = -1
    new_value  = 'nan'
    max_repeats = 4
    counter3 = 0
    
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
            counter3 += 1
            houses.set_house_matrix(matrix_old)
            
            # continue until max_repeats is reached
            if max_repeats == counter3:
                counter2 += 1
                matrix_improv = matrix_old
                if counter2 < 21:
                    matrix_improv, improvement = stoch_steepest_hill_step(houses,magni, counter2)
                else:
                    continue
                break

    return matrix_improv, improvement