"""
This file contains functions which form a stochastic steepest hill climbing 
algorithm which attempts to find the maximum profit that can be obtained.
 
Input:
    houses: the house class (containing the matrix)
    max_it: the number of iterations that are performed
    max_same_improvement: a number; the algorithm stops before max_it if the 
                          improvement is max_same_improvement times 'small'
    criteria: a treshold value; if the improvement is below criteria, than the 
              improvement is called 'small'
Output: 
    houses.get_house_matrix(): plan of the optimized house positions 
    local_max: binary variable that is one if max_same_improvement is reached, 
               ie the algorithm might be stuck in a (local) maximum.
"""

# import necessary modules
import random
import numpy as np

# import functions from other documents
from check_house import check_house
from gen_improvement import gen_improv
from printing_progress import print_progress, print_convergence

# import global variables
from global_vars import STARTING_STEP_SIZE, MAX_REPEATS, PYTHON_DEPTH

def stoch_steepest_hill(houses, max_it, max_same_improvement, criteria):
    """" This is the function that is called when a user wants to perform the 
         stochastic steepest hill algorithm. It continues to improve the
         solution untill the maximum number of iterations is reached or until 
         the algorithm might be stuck in a (local) maximum. """
    
    # counter for the iteration round
    n = 0
    
    # counter for max_same_improvement
    counter_same_improv = 0
    
    # counter for how often a step can be repeated
    counter_repeated = 0
    
    # boolean that is true if the algrithm might be in a (local) maximum
    local_max = 0
    
    while n < max_it and counter_same_improv < max_same_improvement:
        
        # store the old profit value
        old_value = houses.compute_value().copy()
        
        # alter the position of the house and determine the improvement
        if n == 0:
            
            # in the first iteration the variable step size is fixed to
            # STARTING_STEP_SIZE
            mat, improvement = stoch_steepest_hill_step(houses, 
                        STARTING_STEP_SIZE, counter_repeated)
        else:
            
            # calculate variable step size as a function of momentum and
            # decaying learning rate and trend breaker term
            magni = determine_stepsize(max_it, houses, old_value, n,
                improvement)
            
            # calculate new improvement 
            mat, improvement = stoch_steepest_hill_step(houses, magni,
                        counter_repeated)
        
        # check if the improvement is 'small' and adjust the counter
        if improvement < criteria:
            counter_same_improv += 1
        else: 
            counter_same_improv = 0   
        
        # print progress for user
        print_progress(n, max_it, houses.compute_value())
        
        n += 1
    
    # check if the algorithm might be stuck in a local maximum
    if counter_same_improv == max_same_improvement:
        local_max = 1
    
    print_convergence(max_it, max_same_improvement,  local_max)
    
    # put the right matrix in the house class houses
    houses.set_house_distance(mat)
    
    return houses.get_house_matrix(), local_max

def stoch_steepest_hill_step(houses, magni, counter_repeated):
    """" This is the function that is called in each iteration step of the
         stochastic steepest hill algorithm. It chooses a random house and 
         tries to improve the profit by altering the position of that house."""
    
    # choose a random house to move
    house = random.randint(houses.water_num , len(houses.matrix[0,:]))
    
    # counter for checking if the number of MAX_REPEATS_STOCH is reached for
    # the choosen house
    counter_max_repeats = 0
    
    # store the old value and the old matrix
    old = houses.compute_value().copy()
    matrix_old = houses.get_house_matrix().copy()
    
     # set up for while loop
    improvement = -1
    
    while improvement < 0:

        # generate copy of the matrix to try improvements on
        matrix_copy = houses.get_house_matrix().copy()
        
        # generate an improvement
        matrix_improv = gen_improv(matrix_copy, house, magni, 1,
                houses.water_num)
    
        # calculate distance
        valid, distance = check_house(house, houses.water_num , matrix_improv)
        
        # calculate the improvement if the new position is valid
        if valid == 0 :
            
            # update the matrix in the house class
            houses.set_house_distance(matrix_improv)
            
            # calculate the new value
            new_value = houses.compute_value()   
            
            # calculate the improvement
            improvement = new_value - old

        # make sure the new position is valid and the improvement positive
        if valid == 1 or improvement < 0:
            counter_max_repeats += 1
            
            # restore the old position
            houses.set_house_distance(matrix_old)
            
            # when the maximum number of tries for this house is reached
            # try to improve by chaning the position of another house
            if counter_max_repeats == MAX_REPEATS:
                counter_repeated += 1
                
                # choose new house and try again untill PYTHON_DEPTH is reached
                if counter_repeated < PYTHON_DEPTH:
                    matrix_improv, improvement = stoch_steepest_hill_step(
                            houses,magni, counter_repeated)
                else:
                    # return the old matrix
                    matrix_improv = matrix_old
                    improvement = 0
                break

    return matrix_improv, improvement

def determine_stepsize(max_it, houses, old_value, n , improvement):
    """" This function returns the bounds for the step size that can be choosen
         to alter the position of a house. """
    
    # function that decreases with the number of iterations
    alpha = (max_it/n)**(1/3) * 50 * (20/houses.total_houses)**3
    
    # function that increases with the hight of the previous improvement
    beta = improvement/old_value * 100
    
    # random component to change trend direction
    epsilon = np.random.uniform(low = 0 , high = 0.5 * (alpha + beta))
    
    # calculate total range
    step_size = 0.1 * (alpha + beta + epsilon) 
    
    return step_size