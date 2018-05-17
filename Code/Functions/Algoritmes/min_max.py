"""
This function first tries to go to the optimum distance values. Then it tries
to maximize the profit.
 
Input:  .........................................................
Output: plan of the optimized house positions
"""

# import necessary modules
import random

# import functions from other documents
from check_house import check_house
from gen_improvement import gen_improv
from hill_and_annealing_combination import hill_ann_combi

#optimum values from upper bound (number of houses, kind : optimum)
OPTIMUM = {'20': {'1': 7, '2': 23, '3': 63},
           '40': {'1': 3, '2': 13, '3': 39},
           '60': {'1': 0.5, '2': 8, '3': 29}}

def min_max_alg(houses, N, start_temp, end_temp, acceptance_limit, magni, stop_improv, criteria, max_times, tot_houses):
    
    # first minimize the score, wich is the difference between the optimum distance
    # and the current distance
    mat = min_score(houses, N, magni, stop_improv, criteria, tot_houses)
    houses.set_house_matrix(mat)
    print("value of min ", houses.compute_value())
    
    # then maximize the profit
    mat = hill_ann_combi(houses, N, start_temp, end_temp, acceptance_limit,
              magni, stop_improv, criteria, max_times)
    print("value of max ", houses.compute_value())
    houses.set_house_matrix(mat)
    return houses.get_house_matrix()

def min_score(houses, N, magni, stop_improv, criteria, tot_houses):    
    
    # count iterations
    n = 0
    # count last stop_improv iterations
    counter = 0
    
    while n < N and counter < stop_improv:
        n += 1
        mat, improvement = min_score_step(houses, n, N, magni, tot_houses)
        houses.compute_value()
        if improvement < criteria:
            counter += 1
        else: 
            counter = 0    
    houses.set_house_matrix(mat)
    return houses.get_house_matrix()


def min_score_step(houses, n, N, magni, tot_houses):

    # choose a random house to move
    house = random.randint(0, houses.total_houses - 1)
    
    # set up for while loop
    improvement = -1
    max_repeats = 4
    counter = 0
    
    # calculate old value and store old matrix
    matrix_old = houses.get_house_matrix().copy()
    old_score = 0
    for h in range(houses.water_num, tot_houses+houses.water_num):
        old_dist = matrix_old[h][6] - matrix_old[h][9]
        old_score += abs(OPTIMUM[str(tot_houses)][str(int(matrix_old[h][4]))] - old_dist)
    print('-------------------------')
    print('step ', n)
    print('old score ', old_score)
    
    while improvement < 0:
        
        # generate copy of the matrix to try improvements on
        matrix_copy = houses.get_house_matrix().copy()
        matrix_improv = gen_improv(matrix_copy, house, magni, 1, houses.water_num)
        
        # calculate distance
        valid, distance = check_house(house, houses.water_num, matrix_improv)
        
        # if new position is valid
        if valid == 0 :
            # calculate new value
            houses.set_house_matrix(matrix_improv)
            new_score = 0
            for h in range(houses.water_num, tot_houses+houses.water_num):
                new_dist = matrix_improv[h][6] - matrix_improv[h][9]
                new_score += abs(OPTIMUM[str(tot_houses)][str(int(matrix_improv[h][4]))] - new_dist)
        
            print('new score ', new_score)
            # calculate improvement (thus new score has to be lower)
            improvement = old_score - new_score
            print('imp ', improvement)
            
        
        # check validity of new position and improvement
        if valid == 1 or improvement < 0:
            counter += 1
            houses.set_house_matrix(matrix_old)
     
            # continue until max_repeats is reached
            if max_repeats == counter:
                matrix_improv = matrix_old
                break

    return matrix_improv, improvement