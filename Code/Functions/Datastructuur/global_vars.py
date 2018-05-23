"""
This file has all global variables which are used in other python documents.
"""
# distribution of houses on the grid
PERC_SOLO = 0.6
PERC_BUNG = 0.25
PERC_VIL = 0.15
WATER_PERC = 0.20

# define the grid and the different houses
GRID = {'width': 160, 'height': 180}
HOUSE_CHARS = {'1': {'height': 8, 'width': 8 , 'free': 2, 'price': 285000,
                     'interest': 0.03},
               '2': {'height': 10,'width': 7.5,'free': 3, 'price': 399000,
                     'interest': 0.04},
               '3': {'height': 11,'width': 10.5,'free': 4, 'price': 610000,
                     'interest': 0.06},
               '4': {'height': 0,'width': 0,'free': 0, 'price': 0,
                     'interest': 0, 'height_width_ratio_min': 0.25,
                     'height_width_ratio_max': 4}}

WATER_M2 = WATER_PERC * ( GRID['width'] * GRID['height'] )
MAX_WATERS = 4

WATER_M2_REMAINING = WATER_M2

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

# all types of algorithms
ALGOS = ["stoch", "sim", "combi", "minmax", "all"]

# starting stap size
STARTING_STEP_SIZE = 12 

# maximum number of attempts to find improvement allowed
MAX_REPEATS = 4

# python function depth limit
PYTHON_DEPTH = 21

# optimum values from upper bound (number of houses, kind : optimum)
OPTIMUM = {'20': {'1': 7, '2': 23, '3': 63},
           '40': {'1': 3, '2': 13, '3': 39},
           '60': {'1': 0.5, '2': 8, '3': 29}}