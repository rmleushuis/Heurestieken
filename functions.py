# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 13:15:20 2018

@author: LAKle
"""

import numpy as np
import pandas as pd

total_houses = [20, 40, 60]

# distribution of houses
perc_solo = 0.6
perc_bung = 0.25
perc_vil = 0.15

x = total_houses[0]
grid = {'width': 120, 'height': 180}
house_chars = {'1': {'height': 8,
                     'width': 8,
                     'free': 2},
                '2': {'height': 10,
                     'width': 7.5,
                     'free': 3},
                '3': {'height': 11,
                     'width': 10.5,
                     'free': 4}}

solo_type = np.repeat(1, round(perc_solo * x))
bungalows_type = np.repeat(2, round(perc_bung * x))
villas_type = np.repeat(3, round(perc_vil * x))

house_types = np.concatenate((solo_type, bungalows_type, villas_type))

# columns are x_1, y_1, x_2, y_2, house_type, free_space
house_mat = np.zeros(shape = (x, 6))
house_mat[:, 4] = house_types

rest = []
def func(x1,y1,x2,y2, idx):
    filled_houses_mat = house_mat[:idx, :]
    a = []
   
    first_condition = (x1 >= filled_houses_mat[:, 2]).astype(int) + ((((filled_houses_mat[:, 3] <=  y1).astype(int) + (y1 <= filled_houses_mat[:, 1]).astype(int)) == 2)  + (((filled_houses_mat[:, 3] <=  y2).astype(int) + (y2 <= filled_houses_mat[:, 1]).astype(int))  == 2) >=1 )  == 2       
    second_condition = (x1 > filled_houses_mat[:, 2]).astype(int) + (y1 < filled_houses_mat[:, 3]).astype(int) == 2
    eight_condition = (x1 > filled_houses_mat[:, 2]).astype(int) + (y2 > filled_houses_mat[:, 1]).astype(int) == 2
    fourth_condition = (x2 < filled_houses_mat[:, 0]).astype(int) + (y1 < filled_houses_mat[:, 3]).astype(int) == 2
    fifth_condition = (x2 <= filled_houses_mat[:, 0]).astype(int) + ((((filled_houses_mat[:, 3] <=  y1).astype(int) + (y1 <= filled_houses_mat[:, 1]).astype(int)) == 2) + (((filled_houses_mat[:, 3] <=  y2).astype(int) + (y2 <= filled_houses_mat[:, 1]).astype(int))  == 2) >=1) == 2               
    sixth_condition = (x2 < filled_houses_mat[:, 0]).astype(int) + (y2 > filled_houses_mat[:, 1]).astype(int) == 2
    third_condition = (y1 <= filled_houses_mat[:, 3]).astype(int) + ((((filled_houses_mat[:, 0] <=  x1).astype(int) + (x1 <= filled_houses_mat[:, 2]).astype(int)) == 2) + (((filled_houses_mat[:, 0] <=  x2).astype(int) + (x2 <= filled_houses_mat[:, 2]).astype(int)) == 2) >=1) ==2        
    seventh_condition = (y2 >= filled_houses_mat[:, 1]).astype(int) + ((((filled_houses_mat[:, 3] <=  x1).astype(int) + (x1 <= filled_houses_mat[:, 1]).astype(int)) == 2) + (((filled_houses_mat[:, 3] <=  x2).astype(int) + (x2 <= filled_houses_mat[:, 1])) == 2 )>=1) == 2              
    
    a = [second_condition, fourth_condition, sixth_condition, eight_condition, third_condition, fifth_condition, seventh_condition]
      
    a = np.array(a)
    

    if all(a.sum(0) <= 1):
        print(a)
        return 0
    else:
        return 1
    
    

for idx in range(x):
    house_type = str(int(house_mat[idx, 4]))
    house_h = house_chars[house_type]['height']
    house_w = house_chars[house_type]['width']
    house_f = house_chars[house_type]['free']
    
    house_mat[idx, 0] = np.random.uniform(low = 0 + house_f, high = grid['width'] - house_w - house_f)
    house_mat[idx, 1] = np.random.uniform(low = 0 + house_h + house_f, high = grid['height'] - house_f)
    house_mat[idx, 2] = house_mat[idx, 0] + house_w
    house_mat[idx, 3] = house_mat[idx, 1] - house_h
    if idx == 0:
        continue
    else:
        while func(house_mat[idx, 0], house_mat[idx, 1], house_mat[idx, 2], house_mat[idx, 3], idx) != 0:
            house_mat[idx, 0] = np.random.uniform(low = 0 + house_f, high = grid['width'] - house_w - house_f)
            house_mat[idx, 1] = np.random.uniform(low = 0 + house_h + house_f, high = grid['height'] - house_f)
            house_mat[idx, 2] = house_mat[idx, 0] + house_w
            house_mat[idx, 3] = house_mat[idx, 1] - house_h
            
            

    
