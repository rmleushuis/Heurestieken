"""
This file has all global variables which are used in other python documents.
"""

# distribution of houses on the grid
perc_solo = 0.6
perc_bung = 0.25
perc_vil = 0.15

# define the grid and the different houses
grid = {'width': 120, 'height': 180}
house_chars = {'1': {'height': 8, 'width': 8 , 'free': 2},
               '2': {'height': 10,'width': 7.5,'free': 3},
               '3': {'height': 11,'width': 10.5,'free': 4}}