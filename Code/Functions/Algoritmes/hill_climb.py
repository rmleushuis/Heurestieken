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
from gen_improvement_strict import gen_improv


def hill(houses, max_it, stop_improv, criteria):
    
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
            magni = 5
            # generate random value and store it
            improv_x = np.random.uniform(low = -magni , high = magni)
            improv_y = np.random.uniform(low = -magni , high = magni)
            # make a copy of the original matrix
            org_mat = houses.get_house_matrix().copy()
            value = []
            for i in range(4):
                if i<2:
                    improv_x = improv_x * (-1)**i
                    improv_y = improv_y * (-1)**(i-1)
                    mat, improvement = steepest_hill_step(houses, counter2, improv_x, improv_y)
                    value.append(improvement.copy())
                    houses.set_house_matrix(org_mat)
                else:
                    improv_x = improv_x * (-1)**i
                    improv_y = improv_y * (-1)**(i-1)
                    mat, improvement = steepest_hill_step(houses, counter2, improv_x, improv_y)
                    value.append(improvement.copy())
                    houses.set_house_matrix(org_mat)
                    
            max_pos = value.index(max(value))
            
            if max_pos<2:
                improv_x = improv_x * (-1)**i
                improv_y = improv_y * (-1)**(i-1)
                mat, improvement = steepest_hill_step(houses, counter2, improv_x, improv_y)
            else:
                improv_x = improv_x * (-1)**i
                improv_y = improv_y * (-1)**(i-1)
                mat, improvement = steepest_hill_step(houses, counter2, improv_x, improv_y)                
            
            old_value = houses.compute_value().copy()
        else:
            # calculate total range
            magni = 5
            improv_x = np.random.uniform(low = -magni , high = magni)
            improv_y = np.random.uniform(low = -magni , high = magni)
            # make a copy of the original matrix
            org_mat = houses.get_house_matrix().copy()
            value = []
            for i in range(4):
                if i<2:
                    improv_x = improv_x * (-1)**i
                    improv_y = improv_y * (-1)**(i-1)
                    mat, improvement = steepest_hill_step(houses, counter2, improv_x, improv_y)
                    value.append(improvement.copy())
                    houses.set_house_matrix(org_mat)
                else:
                    improv_x = improv_x * (-1)**i
                    improv_y = improv_y * (-1)**(i-1)
                    mat, improvement = steepest_hill_step(houses, counter2, improv_x, improv_y)
                    value.append(improvement.copy())
                    houses.set_house_matrix(org_mat)
                    
            max_pos = value.index(max(value))
            
            if max_pos<2:
                improv_x = improv_x * (-1)**i
                improv_y = improv_y * (-1)**(i-1)
                mat, improvement = steepest_hill_step(houses, counter2, improv_x, improv_y)
            else:
                improv_x = improv_x * (-1)**i
                improv_y = improv_y * (-1)**(i-1)
                mat, improvement = steepest_hill_step(houses, counter2, improv_x, improv_y)                
            
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

def steepest_hill_step(houses, counter2,improv_x, improv_y):
    
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
        matrix_improv = gen_improv(matrix_copy, house, 1, improv_x, improv_y)
        
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
                    matrix_improv, improvement = steepest_hill_step(houses, counter2, improv_x, improv_y)
                else:
                    continue
                break

    return matrix_improv, improvement