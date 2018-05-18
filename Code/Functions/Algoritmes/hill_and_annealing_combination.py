"""
This function first uses a stochastic hill climbing algorithm to find a maxima.
To reduce the change that it is a local maxima, it then uses a simulated 
annealing algorithm.
 
Input:  class containing the matrix, total iterations, starting temperature,
        end temperature, minimum change that is accepted, .................
Output: plan of the optimized house positions
"""
 
# import algorithms
from stoch_hill_climb import stoch_steepest_hill
from simulated_annealing import sim_ann

def hill_ann_combi(houses, total_it, start_temp, end_temp, max_same_improvement, 
                   same_improvement, max_times):
    
    # start with stochastic hill climbing
    mat, local_max = stoch_steepest_hill(houses, total_it, max_same_improvement, same_improvement)
    time = 1
    
    # apply hill climbing until a local maximum is reached 
    # or until it is repeated to many times
    while local_max == 0 and time < max_times:
        time += 1
        mat, local_max = stoch_steepest_hill(houses, total_it, max_same_improvement, same_improvement)
        houses.set_house_matrix(mat)
        
    # save best solution
    best_map = houses.get_house_matrix().copy()
    best_value= houses.compute_value()
    
    # apply simulated annealing until max_times is reached
    for t in range(0, max_times):
        mat = sim_ann(houses, total_it, start_temp, end_temp, max_same_improvement, same_improvement, 'lin')
        houses.set_house_matrix(mat)
        
        # save best solution
        current_value = houses.compute_value()
        if current_value > best_value:
            best_map = houses.get_house_matrix().copy()
            best_value = current_value
        
    houses.set_house_matrix(best_map)
    return houses.get_house_matrix()

