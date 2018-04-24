"""
This function checks if a house has the minimum distance required to all other
houses around it. 

Input: coordinates of top left an bottom right corners, index of the house and
       a matrix containing the same data of all other houses.
Output: 0 if the house violates the minimum distance required
        1 if the house does not violate the minimum distance required
"""

import numpy as np

def check_house(x1, y1, x2, y2, index, house_mat):
    
    # create a temporary matrix to work with
    filled_houses_mat = house_mat[:index, :]
    
    right_side = filled_houses_mat[:, 2]
    left_side = filled_houses_mat[:, 0]
    top_side = filled_houses_mat[:, 1]
    bottom_side = filled_houses_mat[:, 3]
    
    first_condition = np.logical_and( x1 >= right_side, np.logical_or \
                     ( np.logical_and( y1 <= top_side, y1 >= bottom_side ),
                      np.logical_and( y2 <= top_side, y2 >= bottom_side )))
    
    second_condition = np.logical_and( x1 >= right_side, y1 < bottom_side )
    
    third_condition = np.logical_and( y1 <= bottom_side, np.logical_or( np.logical_and( x1 <= right_side, x1 >= left_side ), np.logical_and( x2 <= right_side, x2 >= left_side )))
   
    fourth_condition = np.logical_and( y1 <= bottom_side, x2 < right_side )
    
    fifth_condition = np.logical_and( x2 <= left_side, np.logical_or( np.logical_and( y1 <= top_side, y1 >= bottom_side ), np.logical_or( y2 <= top_side, y2 >= bottom_side )))
    
    sixth_condition = np.logical_and( x2 <= left_side, y2 > top_side )
    
    seventh_condition = np.logical_and( y2 >= top_side, np.logical_or( np.logical_and( x1 <= right_side, x1 >= left_side ), np.logical_and( x2 <= right_side, x2 >= left_side )))
    
    eigth_condition = np.logical_and( y2 >= top_side, y1 > right_side )
    
    
    # put all conditions into an numpy array to test them all at once
    all_cond = np.array([first_condition, second_condition, third_condition,
                         fourth_condition, fifth_condition, sixth_condition,
                         seventh_condition, eigth_condition])
    
    # check if the location of the tested house violates minimum distance rules
    if all(all_cond.sum(0) >= 1):
        # house violates requirements
        return 0
    else:
        # house does not violate requirement
        return 1