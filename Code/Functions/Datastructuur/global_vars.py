"""
This file has all global variables which are used in other python documents.
"""
# distribution of houses on the grid
PERC_SOLO = 0.6
PERC_BUNG = 0.25
PERC_VIL = 0.15

# define the grid and the different houses
GRID = {'width': 160, 'height': 180}
HOUSE_CHARS = {'1': {'height': 8, 'width': 8 , 'free': 2, 'price': 285000, 'interest': 0.03},
               '2': {'height': 10,'width': 7.5,'free': 3, 'price': 399000, 'interest': 0.04},
               '3': {'height': 11,'width': 10.5,'free': 4, 'price': 610000, 'interest': 0.06}}

# define which column of the matrix the minimum distance function should grab
# for house i
DIST = {'0': 2 ,
     '1': [2, 3],
     '2': 3,
     '3': [0, 3],
     '4': 0,
     '5': [0, 1],
     '6': 1,
     '7': [2, 1]}

# define which column of the matrix the minimum distance function should grab
# for house j (i != j)
DIST2 = {'0': 0 ,
     '1': [0, 1],
     '2': 1,
     '3': [2, 1],
     '4': 2,
     '5': [2, 3],
     '6': 3,
     '7': [0, 3]}
