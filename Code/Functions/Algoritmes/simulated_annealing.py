"""
This function uses a simulated annealing algorithm to try to find the maxmum 
profit that can be obtained.
 
Input:
    houses: the house class (containing the matrix)
    N: the number of iterations that are performed
    T0: the starting temperature
    TN: the end temperature
    max_same_improvement: a number; the algorithm stops before max_it if the 
                          improvement is max_same_improvement times 'small'
    criteria: a treshold value; if the improvement is below criteria, than the 
              improvement is called 'small'
    tem_function: the funciton that specifies how the temperature decreases
Output: 
    houses.get_house_matrix(): plan of the optimized house positions 
"""

# import necessary modules
import random
import math
import numpy as np

# import functions from other documents
from check_house import check_house
from gen_improvement import gen_improv
from printing_progress import print_progress, print_convergence    

def sim_ann(houses, N, T0, TN, max_same_improvement, criteria, tem_function):
    """" This is the function that is called when a user wants to perform the 
         simulated annealing algorithm. It continues to improve the solution
         untill the maximum number of iterations is reached or until the
         algorithm might be stuck in a (local) maximum. """
    
    # counter for the iteration round
    n = 0
    
    # counter for max_same_improvement
    counter_same_improv = 0
    
    # boolean that is true if the algrithm might be in a (local) maximum
    local_max = 0
    
    while n < N and counter_same_improv < max_same_improvement:
        
        # store the old profit value
        old_value = houses.compute_value().copy()
        
        # MOET NOG GEDAAN WORDEN: ---------------------------------------
        if n == 0:
            alpha = 4
            beta = 4
            eps = 4
            magni = alpha + beta + eps
            mat, improvement = sim_ann_step(houses, n, N, T0, TN, magni, tem_function)
            old_value = houses.compute_value().copy()
        else:
            # function which account for the position of the step in the total number of steps
            alpha = (N/n)**(1/3) * 50 * (20/houses.total_houses)**2
            # function which account for past improvement
            beta = improvement/old_value * 100
            # random component to change possible direction
            epsilon = np.random.uniform(low = 0 , high = 0.5*(alpha + beta))
            # calculate total range
            magni = 1/10 * (alpha + beta + epsilon)
            if magni<0:
                magni = - magni
            else:
                magni = magni
            mat, improvement = sim_ann_step(houses, n, N, T0, TN, magni, tem_function)
            houses.compute_value()
        # TOT HIER------------------------------------------------------------
        
        # check if the improvement is 'small' and adjust the counter
        if improvement < criteria:
            counter_same_improv += 1
        else: 
            counter_same_improv = 0   
        
        # print progress for user
        print_progress(n, N, houses.compute_value())
        
        n += 1
            
    # check if the algorithm might be stuck in a local maximum
    if counter_same_improv == max_same_improvement:
        local_max = 1
    
    print_convergence(N, max_same_improvement,  local_max)
    
    # put the right matrix in the house class houses
    houses.set_house_distance(mat)
    
    return houses.get_house_matrix()


def sim_ann_step(houses, n, N, T0, TN, magni, tem_function):
    """" This is the function that is called in each iteration step of the
         simulated annealing algorithm. It chooses a random house and 
         tries to improve the profit by altering the position of that house."""
    
    # choose a random house to move
    house = random.randint(houses.water_num, houses.total_houses + houses.water_num - 1)
    
    # GLOBAL MAKEN?????????????????
    max_repeats = 4
    
    # counter for checking if the number of max_repeats is reached for
    # the choosen house
    counter_max_repeats = 0
    
    # store the old value and the old matrix
    old_value = houses.compute_value().copy()
    matrix_old = houses.get_house_matrix().copy()
    
    # set up for while loop
    improvement = -1
    
    while improvement < 0:
        
        # generate copy of the matrix to try improvements on
        matrix_copy = houses.get_house_matrix().copy()
        
        # generate an improvement
        matrix_improv = gen_improv(matrix_copy, house, magni, 0, houses.water_num)
        
        # calculate distance
        valid, distance = check_house(house, houses.water_num, matrix_improv)
        
        # calculate the improvement if the new position is valid
        if valid == 0 :
            
            # update the matrix in the house class
            houses.set_house_distance(matrix_improv)
            
            # calculate the new value
            new_value = houses.compute_value()   
            
            # calculate the improvement
            improvement = new_value - old_value
            
            # check acceptance if the improvement is negative
            if improvement < 0:
                curr_temp = temp(T0, TN, n, N, tem_function)
                improv_chance = math.exp(improvement/curr_temp)
                
                # determine if the negative improvement is accepted
                if improv_chance > np.random.uniform(low=0, high=1):
                    improvement = 10
        
        # check validity of new position and acceptance 
        # the positition is not accepted if improvement is still negative
        if valid == 1 or improvement < 0:
            counter_max_repeats += 1
            
            # restore the old position
            houses.set_house_distance(matrix_old)
     
            # continue until max_repeats is reached
            if max_repeats == counter_max_repeats:
                matrix_improv = matrix_old
                break

    return matrix_improv, improvement

def temp(T0, TN, n, N, needed_cooling_scheme):
    """" This is the function contains the different functions for the cooling 
         scheme. It returns the right current temperature. """
         
    TEMP = {'lin': T0 - n*(T0 - TN)/N,
           'exp': T0*math.pow((TN/T0),(n/N)),
           'sig': TN + (T0-TN)/(1 + math.exp(0.3*(n-N/2))),
           'geman': T0/(math.log(n + 1.005))}
    return TEMP[needed_cooling_scheme]