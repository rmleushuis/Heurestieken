"""
This function draws a solution by drawing blue rectangles representing houses
on a white canvas.

Input:  matrix with house locations, integer (0, 1) to save the plan or not, 
        number of houses
Output: plan of the houses
"""

# import global variables
from global_vars import GRID

# import necessary modules
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_plan(houses, save):

    # create an empty figure
    fig1, (axis) = plt.subplots(1, 1)
    # set axis to grid width and height
    plt.axis([0, GRID['width'] , 0, GRID['height']])
    
    # draw each house a rectangle in the plot
    for i in range(houses.version): 
        axis.add_patch(patches.Rectangle((houses.matrix[i, 0], houses.matrix[i, 3]),
                                         houses.matrix[i, 6], houses.matrix[i, 5], ))
    # save if input argument save is 1
    if save == 1:
        fig1.savefig('plan.png', dpi=90, bbox_inches='tight')