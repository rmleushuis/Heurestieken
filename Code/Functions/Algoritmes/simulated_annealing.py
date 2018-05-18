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

def sim_ann(houses, N, T0, TN, min_chance, magni, stop_improv, criteria):
    
    # count iterations
    n = 0
    # count last stop_improv iterations
    counter = 0
    
    while n < N and counter < stop_improv:
        if n == 0:
            alpha = 4
            beta = 4
            eps = 4
            magni = alpha + beta + eps
            n += 1
            mat, improvement = sim_ann_step(houses, n, N, T0, TN, min_chance, magni)
            old_value = houses.compute_value().copy()
        else:
            # function which account for the position of the step in the total number of steps
            alpha = (N/n)**(1/2) * 50 * (20/houses.total_houses)
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
            mat, improvement = sim_ann_step(houses, n, N, T0, TN, min_chance, magni)
            houses.compute_value()
        if improvement < criteria:
            counter += 1
        else: 
            counter = 0    
    houses.set_house_matrix(mat)
    return houses.get_house_matrix()


def sim_ann_step(houses, n, N, T0, TN, min_chance, magni):
    
    # choose a random house to move
    house = random.randint(0, houses.total_houses - 1)
    
    # set up for while loop
    improvement = -1
    max_repeats = 4
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

    return matrix_improv, improvement