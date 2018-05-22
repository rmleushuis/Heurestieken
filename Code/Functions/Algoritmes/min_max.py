"""
This function first tries to go to the optimum distance values. Then it tries
to maximize the profit.
 
Input:
    houses: the house class (containing the matrix)
    N: the number of iterations that are performed
    start_temp: the starting temperature
    end_temp: the end temperature
    stop_improv: a number; the algorithm stops before max_it if the 
                          improvement is max_same_improvement times 'small'
    criteria: a treshold value; if the improvement is below criteria, 
                      than the improvement is called 'small'
    max_times: maximum number of times stochastic hill climbing can be 
               executed in order to find a maximum. This is also the number
               of times the simulated annealing algorithm is executed.
    tot_houses: the total number of houses
    magni: the range out of which the step size in the first stage can be 
           choosen
    method: the funciton that specifies how the temperature decreases
Output: 
    houses.get_house_matrix(): plan of the optimized house positions 
"""

# import necessary modules
import random

# import functions from other documents
from check_house import check_house
from gen_improvement import gen_improv
from hill_and_annealing_combination import hill_ann_combi

# optimum values from upper bound (number of houses, kind : optimum)
OPTIMUM = {'20': {'1': 7, '2': 23, '3': 63},
           '40': {'1': 3, '2': 13, '3': 39},
           '60': {'1': 0.5, '2': 8, '3': 29}}

def min_max_alg(houses, N, start_temp, end_temp, stop_improv, criteria, 
                max_times, tot_houses, magni, method):
    """" This is the function that is called when a user wants to perform the 
         Min-Max algorithm. """
         
    # first minimize the score, wich is the difference between the optimum 
    # distance and the current distance
    print('Starting with first stage: go to optimum distance')
    mat = min_score(houses, N, magni, stop_improv, criteria, tot_houses)
    houses.set_house_distance(mat)
    
    # then maximize the profit
    print('Starting with second stage: maximize profit by combi algorithm')
    mat = hill_ann_combi(houses, N, start_temp, end_temp, stop_improv, 
                         criteria, max_times, method)
    houses.set_house_distance(mat)
    
    return houses.get_house_matrix()

def min_score(houses, N, magni, stop_improv, criteria, tot_houses):
    """" This is the function that is called in the first stage: minimzing the 
         difference between the optimum distance and the current distance. """    
    
    # counter for the iteration round
    n = 0
    
    # counter for stop_improv
    counter_same_improv = 0
    
    while n < N and counter_same_improv < stop_improv:
        n += 1
        
        # calculate new improvement
        mat, improvement = min_score_step(houses, n, N, magni, tot_houses)
        
        # check if the improvement is 'small' and adjust the counter
        if improvement < criteria:
            counter_same_improv += 1
        else: 
            counter_same_improv = 0    
    
    # put the right matrix in the house class houses        
    houses.set_house_distance(mat)
    
    return houses.get_house_matrix()


def min_score_step(houses, n, N, magni, tot_houses):
    """" This is the function that is called in each iteration step of the
         Min-Max algorithm. It chooses a random house and tries to reduce the 
         difference between the optimum distance and the current distacne of
         that house, by altering the position of that house."""
    
    # choose a random house to move
    house = random.randint(houses.water_num, 
                           houses.total_houses + houses.water_num - 1)
    
    # GLOBAL MAKEN?????????????????
    max_repeats = 4
    
    # counter for checking if the number of max_repeats is reached for
    # the choosen house
    counter_max_repeats = 0
    
    # store the old matrix
    matrix_old = houses.get_house_matrix().copy()
    
    # set up for while loop
    improvement = -1
    
    # calculate the old score
    old_score = 0
    for h in range(houses.water_num, tot_houses+houses.water_num):
        old_dist = matrix_old[h][6] - matrix_old[h][9]
        old_score += abs(OPTIMUM[str(tot_houses)][str(int(matrix_old[h][4]))] - old_dist)
    
    while improvement < 0:
        
        # generate copy of the matrix to try improvements on
        matrix_copy = houses.get_house_matrix().copy()
        matrix_improv = gen_improv(matrix_copy, house, magni, 1, houses.water_num)
        
        # calculate distance
        valid, distance = check_house(house, houses.water_num, matrix_improv)
        
        # if new position is valid
        if valid == 0 :
            houses.set_house_distance(matrix_improv)
            
            # calculate new value
            new_score = 0
            for h in range(houses.water_num, tot_houses+houses.water_num):
                new_dist = matrix_improv[h][6] - matrix_improv[h][9]
                new_score += abs(OPTIMUM[str(tot_houses)][str(int(matrix_improv[h][4]))] - new_dist)

            # calculate improvement (thus new score has to be lower)
            improvement = old_score - new_score
            
        
        # check validity of new position and improvement
        if valid == 1 or improvement < 0:
            counter_max_repeats += 1
            
            # restore the old position
            houses.set_house_distance(matrix_old)
     
            # continue until max_repeats is reached
            if max_repeats == counter_max_repeats:
                matrix_improv = matrix_old
                break

    return matrix_improv, improvement