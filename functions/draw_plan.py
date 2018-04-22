"""
This function draws a solution by drawing blue rectangles representing houses
on a white canvas.

Input:  matrix with house locations, integer (0, 1) to save the plan or not, 
        number of houses
Output: plan of the houses
"""

# import global variables
from global_vars import *

# import necessary modules
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_plan(house_mat, save, x):

    # create an empty figure
    fig1, (axis) = plt.subplots(1, 1)
    # set axis to grid width and height
    plt.axis([0, grid['width'] , 0, grid['height']])
    
    # draw each house a rectangle in the plot
    for i in range(x): 
        axis.add_patch(patches.Rectangle((house_mat[i, 0], house_mat[i, 3]),
                                         house_mat[i, 6], house_mat[i, 5], ))
        
    if save == 1:
        fig1.savefig('plan.png', dpi=90, bbox_inches='tight')