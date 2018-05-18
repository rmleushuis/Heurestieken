"""
This function uses a simulated annealing algorithm to find a local maxima.
 
Input:  class containing the matrix, starting temperature 
        (T0) that will go to ending temperature (TN) when the 
        maximum number of iterations (N) is reached, the minimum change that is
        accepted (min_chance)
Output: plan of the optimized house positions
"""

# import necessary modules
import random
import math
import numpy as np

# import functions from other documents
from check_house import check_house
from gen_improvement import gen_improv
    

def sim_ann(houses, N, T0, TN, max_same_improvement, criteria, tem_function):
    
    # count iterations
    n = 0
    # count last max_same_improvement iterations
    counter = 0
    
    while n < N and counter < max_same_improvement:
        if n == 0:
            alpha = 4
            beta = 4
            eps = 4
            magni = alpha + beta + eps
            n += 1
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
            n += 1
            mat, improvement = sim_ann_step(houses, n, N, T0, TN, magni, tem_function)
            houses.compute_value()
        if improvement < criteria:
            counter += 1
        else: 
            counter = 0    
    houses.set_house_matrix(mat)
    return houses.get_house_matrix()


def sim_ann_step(houses, n, N, T0, TN, magni, tem_function):
    
    # choose a random house to move
    house = random.randint(houses.water_num, houses.total_houses + houses.water_num - 1)
    
    # set up for while loop
    improvement = -1
    max_repeats = 4
    counter = 0
    
    # calculate old value and store old matrix
    old_value = houses.compute_value().copy()
    matrix_old = houses.get_house_matrix().copy()
    
    while improvement < 0:
        
        # generate copy of the matrix to try improvements on
        matrix_copy = houses.get_house_matrix().copy()
        matrix_improv = gen_improv(matrix_copy, house, magni, 0, houses.water_num)
        
        # calculate distance
        valid, distance = check_house(house, houses.water_num, matrix_improv)
        
        # if new position is valid
        if valid == 0 :
            # calculate new value
            houses.set_house_matrix(matrix_improv)
            new_value = houses.compute_value()
            
            # calculate improvement
            improvement = new_value - old_value
            
            # check acceptance
            if improvement < 0:
                curr_temp = temp(T0, TN, n, N, tem_function)
                improv_chance = math.exp(improvement/curr_temp)
                if improv_chance > np.random.uniform(low=0, high=1):
                    improvement = 10
        
        # check validity of new position and acceptance (not accepted if imp still neg)
        if valid == 1 or improvement < 0:
            counter += 1
            houses.set_house_matrix(matrix_old)
     
            # continue until max_repeats is reached
            if max_repeats == counter:
                matrix_improv = matrix_old
                break

    return matrix_improv, improvement

# different functions for the cooling scheme
def temp(T0, TN, n, N, needed):
    TEMP = {'lin': T0 - n*(T0 - TN)/N,
           'exp': math.pow(T0*(TN/T0),(n/N)),
           'sig': TN + (T0-TN)/(1 + math.exp(0.3*n-N/2)),
           'geman': T0/(math.log(n) + 1)}
    return TEMP[needed]