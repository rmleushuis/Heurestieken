"""
This function checks if a house has the minimum distance required to all other
houses around it. 

Input: coordinates of top left an bottom right corners, index of the house and
       a matrix containing the same data of all other houses.
Output: 0 if the house violates the minimum distance required
        1 if the house does not violate the minimum distance required
"""
# import global_vars
from global_vars import DIST, DIST2, GRID

# import necessary modules
import numpy as np

def check_house(house, water_num, house_mat, water_mat= None):

    # retrieve variables of the evaluated house
    if water_mat is not None:
        house_mat = np.concatenate((water_mat, house_mat))
        house += len(water_mat)
    
    x1 = house_mat[house, 0]
    y1 = house_mat[house, 1]
    x2 = house_mat[house, 2]
    y2 = house_mat[house, 3]
    free_space = house_mat[house, 9]
       
    # create a temporary matrix to work with
    filled_houses_mat = house_mat[:house, :]
    free_space_cur = free_space
    
    house_free_space = filled_houses_mat[:, 9]

    right_side = filled_houses_mat[:, 2] 
    left_side = filled_houses_mat[:, 0]
    top_side = filled_houses_mat[:, 1] 
    bottom_side = filled_houses_mat[:, 3]
    
    sides = {'right': right_side,
             'left': left_side,
             'top': top_side,
             'bottom': bottom_side}
    
    free_space = np.ones((len(house_free_space), 2)) * free_space

    free_space[:, 0] = house_free_space
    
    free_space = np.max(free_space, 1)
    
    first_condition = np.logical_and( x1 >= (right_side + free_space) ,
                                      np.logical_or.reduce(( np.logical_and( y1 <= top_side,
                                      y1 >= bottom_side ), np.logical_and( y2 <= top_side,
                                      y2 >= bottom_side ), np.logical_and(y2 <= bottom_side, y1 >= top_side),
                                        np.logical_and( y2 >= bottom_side, y1 <= top_side))))
    second_condition = np.logical_and( x1 > (right_side + free_space),
                                       y1 < (bottom_side - free_space) )
    third_condition = np.logical_and( y1 <= (bottom_side - free_space),
                                      np.logical_or.reduce(( np.logical_and( x1 <= right_side,
                                      x1 >= left_side ), np.logical_and( x2 <= right_side,
                                      x2 >= left_side ), np.logical_and(x1 <= left_side, x2 >= right_side),
                                        np.logical_and( x1 >= left_side, x2 <= right_side))))
    fourth_condition = np.logical_and( y1 < (bottom_side - free_space),
                                      x2 < (left_side - free_space) )
       
    fifth_condition = np.logical_and( x2 <= (left_side - free_space),
                                      np.logical_or.reduce(( np.logical_and( y1 <= top_side,
                                      y1 >= bottom_side ), np.logical_and( y2 <= top_side,
                                      y2 >= bottom_side ), np.logical_and( y2 <= bottom_side, y1 >= top_side),
                                        np.logical_and( y2 >= bottom_side, y1 <= top_side))))
    sixth_condition = np.logical_and( x2 < (left_side - free_space),
                                      y2 > (top_side + free_space) )
    seventh_condition = np.logical_and( y2 >= (top_side +  free_space),
                                        np.logical_or.reduce(( np.logical_and( x1 <= right_side,
                                        x1 >= left_side ), np.logical_and( x2 <= right_side,
                                        x2 >= left_side ), np.logical_and( x1 <= left_side, x2 >= right_side),
                                        np.logical_and( x1 >= left_side, x2 <= right_side))))
    eigth_condition = np.logical_and( y2 > (top_side + free_space),
                                      x1 > (right_side + free_space) )
    
    ninth_condition = x1 >= free_space_cur
    tenth_condition = x2 <= (GRID['width'] - free_space_cur)
    eleventh_condition = y1 <= (GRID['height'] - free_space_cur)
    twelfth_condition = y2 >= free_space_cur
    
    
    # put all conditions into an numpy array to test them all at once
    all_cond = np.array([first_condition, second_condition, third_condition,
 
                        fourth_condition, fifth_condition, sixth_condition,
                         seventh_condition, eigth_condition])    
    
    grid_cond = np.array([ninth_condition, tenth_condition, eleventh_condition,
                          twelfth_condition])

    
    # check if the location of the tested house violates minimum distance rules
#    print(all_cond)
    if all( all_cond.sum(0) == 1 ) and all( grid_cond == 1):
        
        if water_mat is not None:
            all_cond = all_cond[water_num:,:]
        positions = np.array([x1, y1, x2, y2])    
        distance_ind = np.argmax(all_cond, axis = 0)
        distances = np.array( [0.0] * ( len(distance_ind) + 4 ) )
        
        # calculate the minimum distance of the house to other houses
        for i in range(len(distance_ind)):
            plane = distance_ind[i]
#            print(plane)
            m = np.abs(positions[DIST2[str(plane)]] - filled_houses_mat[i, DIST[str(plane)]]) 
            # if even
#            print(plane, m)
            if plane % 2 == 0:
                distances[i] = np.abs(m) - free_space_cur
            # if odd
            else:
                distances[i] = np.sqrt( np.dot(m, m) ) - free_space_cur
        
        distances[-1] = y2 -  free_space_cur
        distances[-2] = (GRID['height'] - free_space_cur) - y1
        distances[-3] = (GRID['width'] - free_space_cur) - x2
        distances[-4] = x1 - free_space_cur
#        print(distances)
        # house does not violate requirement
        return 0, distances
    else:
        # house violates requirements
        return 1, None
    