"""
This function first uses a stochastic hill climbing algorithm to find a maximum.
To reduce the change that it is a local maxima, it then uses a simulated 
annealing algorithm.
 
Input:
    houses: the house class (containing the matrix)
    total_it: the number of iterations that are performed
    start_temp: the starting temperature
    end_temp: the end temperature
    max_same_improvement: a number; the algorithm stops before max_it if the 
                          improvement is max_same_improvement times 'small'
    same_improvement: a treshold value; if the improvement is below criteria, 
                      than the improvement is called 'small'
    max_times: maximum number of times stochastic hill climbing can be 
               executed in order to find a maximum. This is also the number
               of times the simulated annealing algorithm is executed.
    method: the funciton that specifies how the temperature decreases
Output: 
    houses.get_house_matrix(): plan of the optimized house positions 
"""
 
# import algorithms
from stoch_hill_climb import stoch_steepest_hill
from simulated_annealing import sim_ann

def hill_ann_combi(houses, total_it, start_temp, end_temp, max_same_improvement, 
                   same_improvement, max_times, method):
    """" This is the function that is called when a user wants to perform the 
         combi algorithm. """
    
    # start with stochastic steepest hill climbing
    print('Starting with stochastic steepest hill climbing')
    mat, local_max = stoch_steepest_hill(houses, total_it, max_same_improvement, 
                                         same_improvement)
    
    # counter for the number of times the algorithm is repeated
    time = 1
    
    # apply hill climbing until a local maximum is reached 
    # or until it is repeated to many times
    while local_max == 0 and time < max_times:
        time += 1
        
        # execute the stochastic steepest hill climbing algorithm
        mat, local_max = stoch_steepest_hill(houses, total_it, 
                                             max_same_improvement, 
                                             same_improvement)
        houses.set_house_distance(mat)
        
    # save best solution
    best_map = houses.get_house_matrix().copy()
    best_value= houses.compute_value()
    
    # apply simulated annealing until max_times is reached
    print()
    print('Starting with simulated annealing')
    for t in range(0, max_times):
        
        # execute the simulated annealing algorithm
        mat = sim_ann(houses, total_it, start_temp, end_temp, 
                      max_same_improvement, same_improvement, method)
        houses.set_house_distance(mat)
        
        # save best solution
        current_value = houses.compute_value()
        if current_value > best_value:
            best_map = houses.get_house_matrix().copy()
            best_value = current_value
        
    # put the right matrix in the house class houses
    houses.set_house_distance(best_map)
    
    return houses.get_house_matrix()

