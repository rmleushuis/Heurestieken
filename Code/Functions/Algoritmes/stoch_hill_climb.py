"""
This function uses a stochastic hill climbing algorithm to find a local maxima.
 
Input:  Class containing the matrix and magnitude of max change
Output: Plan of the optimized house positions and a binary variable for the 
        local maximum.
"""
# import necessary modules
import random
import numpy as np

# import functions from other documents
from check_house import check_house
from gen_improvement import gen_improv

# import global variables
from global_vars import STARTING_STEP_SIZE, MAX_REPEATS_STOCH, PYTHON_DEPTH

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
            magni = STARTING_STEP_SIZE
            mat, improvement = stoch_steepest_hill_step(houses, magni,
                        counter2)
            old_value = houses.compute_value().copy()
        else:
            # calculate variable step size as a function of momentum and
            # decaying learning rate and trend breaker termr
            magni = determine_stepsize(max_it, houses, old_value, n,
                improvement)
            # calculate new improvement 
            mat, improvement = stoch_steepest_hill_step(houses, magni,
                        counter2)
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
    
    houses.set_house_distance(mat)
    
    return houses.get_house_matrix(), local_max

def stoch_steepest_hill_step(houses, magni, counter2):
    
    # choose a random house to move
    house = random.randint(houses.water_num , len(houses.matrix[0,:]))
    
    # set up for while loop
    improvement = -1
    counter3 = 0
    
    # calculate  old value and store old matrix
    old = houses.compute_value().copy()
    matrix_old = houses.get_house_matrix().copy()
    
    while improvement < 0:

        # generate copy of the matrix to try improvements on
        matrix_copy = houses.get_house_matrix().copy()
        matrix_improv = gen_improv(matrix_copy, house, magni, 1,
                houses.water_num)
    
        # calculate distance
        valid, distance = check_house(house, houses.water_num , matrix_improv)
        
        # if new position is valid
        if valid == 0 :
            # calculate new value
            houses.set_house_distance(matrix_improv)
            new_value = houses.compute_value()   
            # calculate improvement
            improvement = new_value - old

        
        # if new position is not valid or the improvement is negative
        if valid == 1 or improvement < 0:
            counter3 += 1
            houses.set_house_distance(matrix_old)
            
            # continue until max_repeats is reached
            if counter3 == MAX_REPEATS_STOCH:
                counter2 += 1
                matrix_improv = matrix_old
                if counter2 < PYTHON_DEPTH:
                    matrix_improv, improvement = stoch_steepest_hill_step(
                            houses,magni, counter2)
                else:
                    continue
                break

    return matrix_improv, improvement

def determine_stepsize(max_it, houses, old_value, n , improvement):
    
    # function which account for the position of the step in the total 
    # number of steps
    alpha = (max_it/n)**(1/3) * 50 * (20/houses.total_houses)**3
    # function which account for past improvement
    beta = improvement/old_value * 100
    # random component to change trend direction
    epsilon = np.random.uniform(low = 0 , high = 0.5 * (alpha + beta))
    # calculate total range
    step_size = 0.1 * (alpha + beta + epsilon) 
    
    return step_size