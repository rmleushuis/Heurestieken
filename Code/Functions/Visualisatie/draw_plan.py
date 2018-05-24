"""
This class contains the grid specifications which are needed in order to
draw a solution by drawing blue rectangles representing houses on a white 
canvas.

Input:  matrix with house locations, integer (0, 1) to save the plan or not, 
        number of houses
Output: plan of the houses
"""

# import global variables
from global_vars import GRID

# import necessary modules
import matplotlib.pyplot as plt
import matplotlib.patches as patches

class Show_grid():
    
    def __init__(self):
        "This function initilizaes the parameters and settings for the grid."
        
        # initialize with None and create grid
        self.ax = None
        self.fig = None
        self.create_grid()
    
    
    def create_grid(self):
        "This function creates an matplot body and axes for the future figure."
        
        # create matplot figure
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xbound(0, GRID['width'])
        self.ax.set_ybound(0, GRID['height'])
        plt.gca().set_aspect('equal', adjustable='box')
        
        
    def draw_house(self, new_house, index, numbers = True, types = None):    
       "This function draws a single house."
       
       # characteristic of a single house for the canvas
       measures = {'lowerleft': (new_house[0], new_house[3]),
                   'width': new_house[2] - new_house[0],
                   'height': new_house[1] - new_house[3],
                   'type': new_house[4]}
       
       # different colours for the different kinds of  houses
       color = {1:'g',
                2:'r',
                3:'y',
                4:'blue'}
       
       # draw the only the houses
       if types == None:
            self.ax.add_patch(patches.Rectangle(measures['lowerleft'],
                              measures['width'], measures['height'],
                              color = color[measures['type']]))
       
       # draw the houses and their free space 
       if types == 'circles':
            self.ax.add_patch(patches.Ellipse((measures['lowerleft'][0] + \
                                               measures['width']/2,
                                               measures['lowerleft'][1] + \
                                               measures['height']/2), width = \
                                               2 * (measures['width']/2 + \
                                               new_house[9] + new_house[6]),
                                               height = 2 * \
                                               (measures['height']/2 + \
                                               new_house[9] + new_house[6]),
                                               angle = 360))
                                               
       # put numbers in the houses
       if numbers == True:
            plt.text(measures['lowerleft'][0], measures['lowerleft'][1],
                                               str(index))