"""
This file handles printing of the progress.
 
Input:
    n: current iteration
    max_it: the number of iterations that are performed
    value: the current profit
    max_same_improvement: a number; the algorithm stops before max_it if the 
                          improvement is max_same_improvement times 'small'
    local_max: binary variable that is one if max_same_improvement is reached, 
               ie the algorithm might be stuck in a (local) maximum.
Output: prints in the console
"""

def print_progress(n, max_it, value):
    """" This is function determines how often the user has to see the 
         progress. """
    
    if n == 0:
        print('--------------------Progress report--------------------')
    
    if max_it < 5:
        print_message(n, value)
    elif max_it < 10:
        if n%2 == 0:
            print_message(n, value)
    elif max_it < 100:
        if n%10 == 0:
            print_message(n, value)
    elif max_it < 1000:
        if n%100 == 0:
            print_message(n, value)
    else:
        if n%500 == 0:
            print_message(n, value)
    
    if n ==  max_it - 1:
        print('-------------------------------------------------------')
            
def print_message(n, value):
    """" This function prints the progress message. """
    
    print('After iteration ', n, ' the profit is: ', value)
    
def print_convergence(max_it, max_same_improvement, local_max):
    """" This function prints the right convergence message. """
    
    if local_max:
        print('While running', max_it, 'iterations, the algorithm seems to',
              'be stuck in a (local) maximum after', max_same_improvement,
              'iterations. Hence, the profit converges with the specified',
              'criteria.')
    else:
        print('With the specified criteria, the profit did not converge in',
              max_it, 'iterations.')