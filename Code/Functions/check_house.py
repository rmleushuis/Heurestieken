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
    
   # check if the distance to the nearest house satisfies the minimum distance
    first_condition = (x1 >= filled_houses_mat[:, 2]).astype(int) + \
                      ((((filled_houses_mat[:, 3] <=  y1).astype(int) + \
                      (y1 <= filled_houses_mat[:, 1]).astype(int)) == 2)  + \
                      (((filled_houses_mat[:, 3] <=  y2).astype(int) + \
                      (y2 <= filled_houses_mat[:, 1]).astype(int))  == 2) \
                      >=1 )  == 2      
    second_condition = (x1 > filled_houses_mat[:, 2]).astype(int) + \
                        (y1 < filled_houses_mat[:, 3]).astype(int) == 2
    third_condition = (y1 <= filled_houses_mat[:, 3]).astype(int) + \
                      ((((filled_houses_mat[:, 0] <=  x1).astype(int) + \
                      (x1 <= filled_houses_mat[:, 2]).astype(int)) == 2) + \
                      (((filled_houses_mat[:, 0] <=  x2).astype(int) + \
                      (x2 <= filled_houses_mat[:, 2]).astype(int)) == 2) \
                       >=1) ==2
    fourth_condition = (x2 < filled_houses_mat[:, 0]).astype(int) +  \
                       (y1 < filled_houses_mat[:, 3]).astype(int) == 2
    fifth_condition = (x2 <= filled_houses_mat[:, 0]).astype(int) + \
                      ((((filled_houses_mat[:, 3] <=  y1).astype(int) + \
                      (y1 <= filled_houses_mat[:, 1]).astype(int)) == 2) + \
                      (((filled_houses_mat[:, 3] <=  y2).astype(int) + \
                      (y2 <= filled_houses_mat[:, 1]).astype(int))  == 2) \
                      >=1) == 2               
    sixth_condition = (x2 < filled_houses_mat[:, 0]).astype(int) + \
                      (y2 > filled_houses_mat[:, 1]).astype(int) == 2      
    seventh_condition = (y2 >= filled_houses_mat[:, 1]).astype(int) + \
                        ((((filled_houses_mat[:, 3] <=  x1).astype(int) + \
                        (x1 <= filled_houses_mat[:, 1]).astype(int)) == 2) + \
                        (((filled_houses_mat[:, 3] <=  x2).astype(int) + \
                        (x2 <= filled_houses_mat[:, 1])) == 2 )>=1) == 2
    eight_condition = (x1 > filled_houses_mat[:, 2]).astype(int) + \
                      (y2 > filled_houses_mat[:, 1]).astype(int) == 2
    
    # put all conditions into an numpy array to test them all at once
    all_cond = np.array([first_condition, second_condition, third_condition,
                         fourth_condition, fifth_condition, sixth_condition,
                         seventh_condition, eight_condition])
    
    # check if the location of the tested house violates minimum distance rules
    if all(all_cond .sum(0) == 1):
        # house violates requirements
        return 0
    else:
        # house does not violate requirement
        return 1