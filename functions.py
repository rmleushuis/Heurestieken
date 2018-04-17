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

for idx in range(x):
    house_type = str(int(house_mat[idx, 4]))
    house_h = house_chars[house_type]['height']
    house_w = house_chars[house_type]['width']
    house_f = house_chars[house_type]['free']
    if idx == 0:
        house_mat[idx, 0] = np.random.uniform(low = 0 + house_f, high = grid['width'] - house_w - house_f)
        house_mat[idx, 1] = np.random.uniform(low = 0 + house_h + house_f, high = grid['height'] - house_f)
        house_mat[idx, 2] = house_mat[idx, 0] + house_w
        house_mat[idx, 3] = house_mat[idx, 1] - house_h

    
