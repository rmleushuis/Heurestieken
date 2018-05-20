from global_vars import GRID, DIST, DIST2
from check_house import check_house
import numpy as np
from collections import defaultdict
import time
from draw_plan import Show_grid

total_width = GRID['width']
total_height = GRID['height']
mat = mat[mat[:,4].argsort()[::-1]]
mat2 = mat.copy()
mat3 = mat.copy()
old_value = sum(mat[:, 10] + mat[:, 10] * mat[:, 6] * mat[:, 11])
show_unused_spaces(mat)
print(old_value)
total_start = time.time()

for loc in range(1, len(mat3)):
    print(loc)    
    start = time.time()
    rotate = 0    
    for y1 in range(int(mat2[loc,9] + rotate * mat2[loc, 8] + (1 - rotate) * mat2[loc, 7]), int(total_height - mat2[loc, 9])):
        for x1 in range(int(mat2[loc, 9]), int(total_width - mat2[loc, 9] - rotate * mat2[loc, 7] - (1 - rotate) * mat2[loc, 8])):
            mat2[loc,0] = float(x1)
            mat2[loc,1] = float(y1)

            mat2[loc,2] = mat2[loc,0] + rotate * mat2[loc,7] + \
            (1 - rotate) * mat2[loc, 8]
            mat2[loc, 3] = mat2[loc, 1] - rotate * mat2[loc, 8] - \
            (1 - rotate) * mat2[loc, 7]

            valid, f = distancesf(loc, mat2)
            
            if valid == 0:
                distancess = []
                for j in range(1, len(mat2)):
                    valid, new_dist = distancesf(j, mat2)
                    
                    distancess.append(new_dist)                    
                    
#                    distancess = np.array(distancess)
#                    distancess = distancess.max(0)
                
                mat2[1:, 6] = distancess
                value_new = sum(mat2[:, 10] + mat2[:, 10] * mat2[:, 6] * mat2[:, 11])
                
                if value_new > old_value:
                    old_value = value_new
                    mat3 = mat2.copy()
                else:
                    mat2 = mat3.copy()
                    
    end = time.time()
    print(old_value)
    print(end - start)
total_end = time.time()
print(total_end - total_start)

show_unused_spaces(mat)
show_unused_spaces(mat3)
mat_value = sum(mat[:, 10] + mat[:, 10] * mat[:, 6] * mat[:, 11])
mat3_value = sum(mat3[:, 10] + mat3[:, 10] * mat3[:, 6] * mat3[:, 11])
print(mat_value)
print(mat3_value)



def show_unused_spaces(house_matrix):
    house_matrix = house_matrix.copy()
    house_matrix2 = house_matrix.copy()
    show_grid = Show_grid()
    for i in range(2):
        for loc in range(len(house_matrix)):
            if i == 0:
#                house_matrix2[loc, 0] -= (house_matrix2[loc, 6] + house_matrix2[loc, 9])
#                house_matrix2[loc, 1] += (house_matrix2[loc, 6]  + house_matrix2[loc, 9])
#                house_matrix2[loc, 2] += (house_matrix2[loc, 6]  + house_matrix2[loc, 9])
#                house_matrix2[loc, 3] -= (house_matrix2[loc, 6]  + house_matrix2[loc, 9])
                house_matrix2[loc, 4] = 4
#                show_grid.draw_house(house_matrix2[loc, :], loc, numbers = True, circles = True)
                show_grid.draw_house(house_matrix2[loc, :], loc, numbers = True, types = 'circles')
            else:
                show_grid.draw_house(house_matrix[loc, :], loc, numbers = True)
        


def distancesf(loc, matrix):
    matrix = matrix.copy()
    free_space_cur = matrix[loc, 9]
    x1 = matrix[loc, 0]
    y1 = matrix[loc, 1]
    x2 = matrix[loc, 2]
    y2 = matrix[loc, 3]
    temp = np.delete(matrix, loc, 0)
    
    house_free_space = temp[:, 9]
    
    right_side = temp[:, 2] 
    left_side = temp[:, 0]
    top_side = temp[:, 1] 
    bottom_side = temp[:, 3]
    
    free_space = np.ones((len(house_free_space), 2)) * free_space_cur
    
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
    
    # put all conditions into an numpy array to test them all at once
    all_cond = np.array([first_condition, second_condition, third_condition,
                         fourth_condition, fifth_condition, sixth_condition,
                         seventh_condition, eigth_condition])    
    
#    print(all_cond)
    if all( all_cond.sum(0) == 1 ):
#        print(all_cond.shape)
        
        all_cond = all_cond[:, 1:]
        
        temp = temp[1:]
        
        positions = np.array([x1, y1, x2, y2])    
        distance_ind = np.argmax(all_cond, axis = 0)
        distances = np.array( [0.0] * ( len(distance_ind) + 4 ) )
        
        # calculate the minimum distance of the house to other houses
        positions = np.array([x1, y1, x2, y2])
        
        for i in range(len(temp)):
            plane = distance_ind[i]
        #            print(plane)
            m = np.abs(positions[DIST2[str(plane)]] - temp[i, DIST[str(plane)]]) 
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
        
#        print('ffff', matrix[loc, 6])
    #    print(np.array([temp[:,6], distances[:-4]]))
        #                    temp[:, 6] = np.max(np.array([temp[:,6], distances[:-4]]))
        
#        selector = [x for x in range(len(matrix)) if x != loc]
#        matrix[selector, 6] = temp[:,6]
#
#        print(distances)
        return 0, np.min(distances)
    return 1, None


#
#istance_mat = np.ones(shape = (len(mat2) + 4, len(mat2) + 4)) * 1000
#                    for j in range(len(mat2)):
#                        valid, distance = check_house(j, mat2)
##                        print(valid, j)
#                        
#                        grid_distances = distance[-4:]
#                        distance_mat[j, -4:] = grid_distances
#                        print(grid_distances)
#                        if j != 0:
#                            distance = distance[:j]
#
#                            distance_mat[j, :j] = distance
#                            
#                    
#                    i_upper = np.triu_indices(len(mat2), 1)
#                    distance_mat[i_upper] = distance_mat.transpose()[i_upper]
#                    distance_mat[-4:,:] = distance_mat[:,-4:].transpose()
#                    # store the minimum distance in the last column of the matrix in the class
#                    mat2[:, 6] = np.min(distance_mat, axis = 0)[:-4]
                                  