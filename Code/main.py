"""
This file runs all the different algorithms and prints the value and the map of
each solution.
"""

# import necessary modules
import os, sys
 
# add current structure to path
directory = os.path.dirname(os.path.realpath("__file__"))
sys.path.append(os.path.join(directory, "functions"))
sys.path.append(os.path.join(directory, "functions/algoritmes"))
sys.path.append(os.path.join(directory, "functions/controle"))
sys.path.append(os.path.join(directory, "functions/datastructuur"))
sys.path.append(os.path.join(directory, "functions/visualisatie"))
 
# import class
from house_class import House
 
# import algorithms
from stoch_hill_climb import stoch_steepest_hill
from simulated_annealing import sim_ann
from hill_and_annealing_combination import hill_ann_combi
from min_max import min_max_alg

def algorithms(total_houses, number_it, idx_algorithm, a_par = None):
    
    if a_par == None:
        
        # max number of improvements which are allowed to be approximately 
        # the same
        max_same_improvement = 5
        
        # treshold value for which improvements are approximately the same
        same_improvement = 1
        
        # simulated annealing algorithm parameters
        start_temp = 800
        end_temp = 0.01
       
        # extra parameter for combi; maximum number of times hill climbing can
        # be applied and the number times simulated annealing will be applied
        max_times = 3
        
        # extra parameter for min max; the range to choose a step from in the
        # minimizing stage
        magni = 10
    method = 'exp'
       
    # create the class for houses and generate random solution
    house = House(total_houses, True, True)
    
    # print the value and the map from the random solution
    print("random", house.compute_value())
    house.show_house_grid()
    
    # save the random allocation as the starting solution
    mat_copy =  house.get_house_matrix().copy()
    
    if 1 in idx_algorithm:
        
        # stoch hill algorithm
        if a_par is not None:
            max_same_improvement = a_par[1][0]
            same_improvement = a_par[1][1]
        # stochastic hill climbing algorithm
        mat, local_max = stoch_steepest_hill(house, number_it,
                                             max_same_improvement,
                                             same_improvement)
        print("stoch hill", house.compute_value())
        house.show_house_grid()
         
        # reset matrix to starting solution
        house.set_house_distance(mat_copy)
        
    if 2 in idx_algorithm:
        
        # sim ann algorithm
        if a_par is not None:
            
            # set default parameters
            start_temp = a_par[2][0]
            end_temp = a_par[2][1]
            max_same_improvement = a_par[2][2]
            same_improvement = a_par[2][3]
            
        # simulated annealing algrotihm
        mat = sim_ann(house, number_it, start_temp, end_temp, 
                      max_same_improvement, same_improvement, method)
        print("sim annealing", house.compute_value())
        house.show_house_grid()
             
        # reset matrix to starting solution
        house.set_house_distance(mat_copy)
    
    if 3 in idx_algorithm:
        
        # combi algorithm
        if a_par is not None:
            
            # set default parameters
            start_temp = a_par[3][0]
            end_temp = a_par[3][1]
            max_same_improvement = a_par[3][2]
            same_improvement = a_par[3][3]
            max_times = a_par[3][4]
            
        # combi algorithm
        mat = hill_ann_combi(house, number_it, start_temp, end_temp,
                             max_same_improvement, same_improvement, max_times,
                             method)  
        print("combi", house.compute_value())
        house.show_house_grid()
        
        # reset matrix to starting solution
        house.set_house_distance(mat_copy)
        
    if 4 in idx_algorithm:
        
        # min max algorithm
        if a_par is not None:
            
            # set default parameters
            start_temp = a_par[4][0]
            end_temp = a_par[4][1]
            max_same_improvement = a_par[4][2]
            same_improvement = a_par[4][3]
            max_times = a_par[4][4]
            magni = a_par[4][5]
        
        # run minmax algorithm
        mat = min_max_alg(house, number_it, start_temp, end_temp,
                          max_same_improvement, same_improvement, max_times,
                          total_houses, magni, method)
        print("min max", house.compute_value())
        house.show_house_grid()
    
    print("\nThe optimal solutions of each algorithms are shown in the plots"
          "below. The order of the plots is random, stochastic hill"
          "simulated annealing, combination algorithm and minmax algorithm.")
      
def main():
    
    # ask the user for input to select a version of the problem
    print("#################### AMSTELHAEGE ####################\n")
    print("The goal of the Amstelhaege project is to maximize \n" 
          "the total property value of a neigbourhood. This is \n"
          "done by maximizing the free space between the houses.")
    
    while True:
        start = input("Enter 'continue' to start: ").lower()

        if start == "continue":
            break
    print("#####################################################")
    print("Enter the number of houses (20, 40 or 60)")
    while True:
        try:
            num_houses = int(input("Houses: "))
            if num_houses in [20, 40, 60]:
                break
        except:
            print("Invalid input. Input must be integer!")
            print("Try again")
            pass
    
    house = House(num_houses, True, True)
    
    # print the value and the map from the random solution
    print("random", house.compute_value())
    house.show_house_grid()
    
    # save the random allocation as the starting solution
    mat_copy =  house.get_house_matrix().copy()
    
    # 1 minute corresponds to about 10 iterations when running all algorithms
    print("Enter the number of iterations (1-...)")
    while True:
        try:
            num_iterations = int(input("Iterations: "))
            if num_iterations > 0:
                break
        except:
            print("Invalid input. Input must be integer!")
            print("Try again")
            pass
    
    
    # user choses which algorithm runs
    print("#####################################################")
    print("Choose optimization algorithm(s):\n")
    print("1) Stochastic ... ")
    print("2) Simulated Annealing")
    print("3) Stochastic ... + Simulated (combination)")
    print("4) MinMAX")
    print("5) Semi-Exhausting Search (takes up to 15 minutes" + 
         "per epoch for 40 houses)\n")
    
    print("Enter the desired number(s) preliminary to the algorithm \n"
          "to run it. For example 123 will run the first second\n"
          "and third algorithm.")
    while True:
        try:
            idx_algorithm = int(input("Algorithm: "))
            idx_algorithm = [int(d) for d in str(idx_algorithm)]
            if all([d in range(1,6) for d in idx_algorithm]):
                break
        except:
            print("Invalid input. Input must be 1,2,3,4,5 or 6!")
            print("Try again")
            pass
    print("#####################################################") 
    print("Enter 'yes' to run the algorithm(s) at its default setting \n"
          "or 'no' to specifiy the parameters by hand.")
    while True:
        try:
            default = input("Default: ").lower()
            if default in ['yes', 'no']:
                break
            print('\n')
        except:
            print("Invalid input. Input must be 1,2,3,4 or 5!")
            print("Try again")
            pass
    
    # specify parameters and algorithms    
    algs = {1: {'algo': 'stoch',
                'params': {'max_same_improvement': int,
                           'same_improvement': int}},
            2: {'algo': 'sim',
                'params': {'start_temp': float,
                           'end_temp': float,
                           'max_same_improvement': int,
                           'same_improvement': int}},
            3: {'algo': 'combi',
                'params': {'start_temp': float,
                           'end_temp': float,
                           'max_same_improvement': int,
                           'same_improvement': int,
                           'max_times': int}},
            4: {'algo': 'minmax',
                'params':  {'start_temp': float,
                           'end_temp': float,
                           'max_same_improvement': int,
                           'same_improvement': int,
                           'max_times': int,
                           'magni': float}}}
    
    # run code with default parameters
    if default == 'no':
        
        a_par = {}
        for algorithm in idx_algorithm:
            algo = algs[algorithm]['algo']
            print(algo)
            params = algs[algorithm]['params']
           
            # get parameters values
            f = ", ".join(list(params.keys()))
            print("Enter the parameters like '(" + f + ")'")
            while True:
                param = list(eval(input("Parameters: ")))
                try:
                    for i, t in zip(range(len(params)), params.values()):
                        param[i] = t(param[i])
                        
                    break
                except:
                    print("Parameter(s) are not valid. Try again.")
            a_par[algorithm] = param
        
        # run algorithms
        algorithms(num_houses, num_iterations, idx_algorithm, a_par)
    else:
        # run algorithms
        algorithms(num_houses, num_iterations, idx_algorithm)

if __name__ == '__main__':
    main()