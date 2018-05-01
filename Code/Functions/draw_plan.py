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

class Show_grid():
    
    def __init__(self):
        
        self.ax = None
        self.fig = None
        
        self.create_grid()
    
    def create_grid(self):
        
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xbound(0, GRID['width'])
        self.ax.set_ybound(0, GRID['height'])
        plt.gca().set_aspect('equal', adjustable='box')
        
    def draw_house(self, new_house, index):
        
        measures = {'lowerleft': (new_house[0], new_house[3]),
                    'width': new_house[2] - new_house[0],
                    'height': new_house[1] - new_house[3]}
        
        self.ax.add_patch(patches.Rectangle(measures['lowerleft'],
                                                 measures['width'], 
                                                 measures['height']))
        plt.text(measures['lowerleft'][0], measures['lowerleft'][1], str(index))
           