from global_vars import GRID, DIST, DIST2
from check_house import check_house
import numpy as np
from collections import defaultdict
from draw_plan import Show_grid
import matplotlib.pyplot as plt

class LuuksAlgo():

    def __init__(self, matrix, house):
        self.total_width = GRID['width']
        self.total_height = GRID['height']
        self.matrix_length = len(matrix)
        self.house = house
        
        self.matrix_sorted = matrix[matrix[:, 4].argsort()[::-1]]
        self.num_waters = sum(self.matrix_sorted[:, 4] == 4)
        
        
    def show_unused_spaces(self, matrix = None):
        if matrix is None:
            house_matrix = self.matrix_sorted.copy()
            house_matrix2 = self.matrix_sorted.copy()
        else:
            house_matrix = matrix.copy()
            house_matrix2 = matrix.copy()
            
#        house_matrix2[:, 4] = 4
        show_grid = Show_grid()
        for i in range(2):
            for loc in range(len(house_matrix)):
                if i == 0:
                    house_matrix2[loc, 4] = 4
    #                show_grid.draw_house(house_matrix2[loc, :], loc, numbers = True, circles = True)
                    show_grid.draw_house(house_matrix2[loc, :], loc, numbers = True, types = 'circles')
                else:
                    show_grid.draw_house(house_matrix[loc, :], loc, numbers = True)
                
    def compute_value(self, matrix):
        return sum(matrix[:, 10] * (1 + matrix[:, 6] * matrix[:, 11]))
    
    def algo(self, epochs = 2, verbose = 0):
        print("start LuuksAlgo")
        temp_matrix1 = self.matrix_sorted.copy()
        temp_matrix2 = self.matrix_sorted.copy()
        old_value = self.compute_value(temp_matrix1)
        
        self.stop = 0
        epoch = 0
        self.combs = 0
        
        while epoch < epochs:
            start_value = old_value
            epoch += 1
            iterator = 0
            for loc in range(self.num_waters, self.matrix_length):
                iterator += 1
                for y1 in range(int(temp_matrix1[loc,9] +  temp_matrix1[loc, 7]), int(self.total_height - temp_matrix1[loc, 9])):
                    for x1 in range(int(temp_matrix1[loc, 9]), int(self.total_width - temp_matrix1[loc, 9] -  temp_matrix1[loc, 8])):
                        temp_matrix1[loc,0] = float(x1)
                        temp_matrix1[loc,1] = float(y1)
            
                        temp_matrix1[loc, 2] = temp_matrix1[loc, 0] + temp_matrix1[loc, 8]
                        temp_matrix1[loc, 3] = temp_matrix1[loc, 1] - temp_matrix1[loc, 7]
            
                        d = self.house.distancesf(loc, temp_matrix1)
                        
                        if d not in [0,1]:
                            distancess = []
#                            print(d)
                            for j in range(self.num_waters, self.matrix_length):
                                d = self.house.distancesf(j, temp_matrix1)
                                
                                distancess.append(d)                    
                            
                            temp_matrix1[self.num_waters:, 6] = distancess
                            new_value = self.compute_value(temp_matrix1)
                            
                            if new_value > old_value:
                                old_value = new_value
                                temp_matrix2 = temp_matrix1.copy()
                            else:
                                temp_matrix1 = temp_matrix2.copy()
                if verbose == 2:
                    print("Epoch:", epoch, 'Iteration:', str(iterator) + '/' + str(self.matrix_length - self.num_waters) ,"Increase:", old_value - start_value)
                                    
            temp_houses = temp_matrix2[np.argsort(temp_matrix2[:,6])[::-1],].copy()
            
            for i in range(self.num_waters, self.matrix_length):
                        
                x1s = temp_matrix1[i, 0]
                y1s = temp_matrix1[i, 1]
                
                for k in range(self.matrix_length - self.num_waters):
                    x1 = temp_houses[k, 0]
                    y1 = temp_houses[k, 1]
                    
                    if x1 == x1s and y1 == y1s:
                        pass
                    else:
                        temp_matrix1[i, 0] = x1
                        temp_matrix1[i, 1] = y1
                        
                        temp_matrix1[i,2] = temp_matrix1[i,0] + temp_matrix1[i,5] * temp_matrix1[i,7] + \
                            (1 - temp_matrix1[i,5]) * temp_matrix1[i, 8]
                        temp_matrix1[i, 3] = temp_matrix1[i, 1] - temp_matrix1[i,5] * temp_matrix1[i, 8] - \
                        (1 - temp_matrix1[i,5]) * temp_matrix1[i, 7]
                        
                        loc = np.where(temp_matrix1[:, 0] == x1)[0][0]
                        
                        temp_matrix1[loc, 0] = x1s
                        temp_matrix1[loc, 1] = y1s
                        
                        temp_matrix1[loc,2] = temp_matrix1[loc,0] + temp_matrix1[loc,5] * temp_matrix1[loc,7] + \
                            (1 - temp_matrix1[loc,5]) * temp_matrix1[loc, 8]
                        temp_matrix1[loc, 3] = temp_matrix1[loc, 1] - temp_matrix1[loc,5] * temp_matrix1[loc, 8] - \
                        (1 - temp_matrix1[loc,5]) * temp_matrix1[loc, 7]
                    
                        d = self.house.distancesf(i, temp_matrix1)
                            
                        if d is not None:
                            distancess = []
                            for j in range(self.num_waters, self.matrix_length):
                                d = self.house.distancesf(j, temp_matrix1)
                                
                                distancess.append(d)                    
                            
                            temp_matrix1[self.num_waters:, 6] = distancess
                            value_new = self.compute_value(temp_matrix1)
                            if value_new > old_value:
                                print('increase:', value_new - old_value)
                                old_value = value_new
                                temp_matrix2 = temp_matrix1.copy()
                            else:
                                temp_matrix1 = temp_matrix2.copy()  
            
            if verbose == 1:
                print("Epoch:", epoch, "Increase:", old_value - start_value)
            if old_value - start_value < 0.01:
                print('Converged')
                break
            
        print('Did not converge')
        
        self.matrix_sorted = temp_matrix2
        
    def get_matrix(self):
        return self.matrix_sorted
        
#if __name__ == '__main__':
LA = LuuksAlgo(mat_copy, house)
new = LA.algo(verbose = 2)
LA.show_unused_spaces(new)
            
#
#total_width = GRID['width']
#total_height = GRID['height']
#mat = mat[mat[:,4].argsort()[::-1]]
#mat2 = mat.copy()
#mat3 = mat.copy()
#old_value = sum(mat[:, 10] + mat[:, 10] * mat[:, 6] * mat[:, 11])
#show_unused_spaces(mat_copy)
#print(old_value)
#total_start = time.time()
#waters = sum(mat[:,4] == 4)
#stop = 0
#iterations = 0
#combs = 0
#while stop == 0:
#    print('iterations:', iterations)
#    a = list(range(waters, len(mat)))
#    iterations +=1
#    prog = 0
#    for loc in a:
#        prog+=1
#        print('progress:',  prog, '/', len(mat) - 2)    
#        start = time.time()
#        rotate = 0
#        for y1 in range(int(mat2[loc,9] + rotate * mat2[loc, 8] + (1 - rotate) * mat2[loc, 7]), int(total_height - mat2[loc, 9])):
#            for x1 in range(int(mat2[loc, 9]), int(total_width - mat2[loc, 9] - rotate * mat2[loc, 7] - (1 - rotate) * mat2[loc, 8])):
#                mat2[loc,0] = float(x1)
#                mat2[loc,1] = float(y1)
#    
#                mat2[loc,2] = mat2[loc,0] + rotate * mat2[loc,7] + \
#                (1 - rotate) * mat2[loc, 8]
#                mat2[loc, 3] = mat2[loc, 1] - rotate * mat2[loc, 8] - \
#                (1 - rotate) * mat2[loc, 7]
#    
#                valid, f = distancesf(loc, mat2, waters)
#                
#                if valid == 0:
#                    combs += 1
#                    distancess = []
#                    for j in range(waters, len(mat2)):
#                        valid, new_dist = distancesf(j, mat2, waters)
#                        
#                        distancess.append(new_dist)                    
#                    
#                    mat2[waters:, 6] = distancess
#                    value_new = sum(mat2[:, 10] + mat2[:, 10] * mat2[:, 6] * mat2[:, 11])
#                    
#                    if value_new > old_value:
#                        old_value = value_new
#                        mat3 = mat2.copy()
#                    else:
#                        mat2 = mat3.copy()
#        
#        end = time.time()
#        print('increase:', old_value)
#    total_end = time.time()
#    
#    mat3_houses = mat3[np.argsort(mat3[:,6])[::-1],].copy()
#    
#    
#    mat3 = mat3[np.argsort(mat3[:,4])[::-1],].copy()
#    mat4 = mat3.copy()
#    
#    for i in range(waters, len(mat4)):
#                
#        x1s = mat4[i, 0]
#        y1s = mat4[i, 1]
#        
#        for k in range(len(mat3_houses) - waters):
#            x1 = mat3_houses[k, 0]
#            y1 = mat3_houses[k, 1]
#            
#            if x1 == x1s and y1 == y1s:
#                pass
#            else:
#                mat4[i, 0] = x1
#                mat4[i, 1] = y1
#                
#                mat4[i,2] = mat4[i,0] + mat4[i,5] * mat4[i,7] + \
#                    (1 - mat4[i,5]) * mat4[i, 8]
#                mat4[i, 3] = mat4[i, 1] - mat4[i,5] * mat4[i, 8] - \
#                (1 - mat4[i,5]) * mat4[i, 7]
#                
#                loc = np.where(mat4[:, 0] == x1)[0][0]
#                
#                mat4[loc, 0] = x1s
#                mat4[loc, 1] = y1s
#                
#                mat4[loc,2] = mat4[loc,0] + mat4[loc,5] * mat4[loc,7] + \
#                    (1 - mat4[loc,5]) * mat4[loc, 8]
#                mat4[loc, 3] = mat4[loc, 1] - mat4[loc,5] * mat4[loc, 8] - \
#                (1 - mat4[loc,5]) * mat4[loc, 7]
#            
#                valid, f = distancesf(i, mat4, waters)
#                    
#                if valid == 0:
#                    distancess = []
#                    for j in range(waters, len(mat4)):
#                        valid, new_dist = distancesf(j, mat4, waters)
#                        
#                        distancess.append(new_dist)                    
#                    
#                    mat4[waters:, 6] = distancess
#                    value_new = sum(mat4[:, 10] + mat4[:, 10] * mat4[:, 6] * mat4[:, 11])
#                    
#                    if value_new > old_value:
#                        print('increase:', value_new - old_value)
#                        old_value = value_new
#                        mat3 = mat4.copy()
#                        mat2 = mat4.copy()
#                    else:
#                        mat4 = mat3.copy()
#                
#    mat_value = sum(mat[:, 10] + mat[:, 10] * mat[:, 6] * mat[:, 11])
#    mat3_value = sum(mat3[:, 10] + mat3[:, 10] * mat3[:, 6] * mat3[:, 11])
#    print('original value:', mat_value)
#    print('new optimal value:', mat3_value)
#    if value_new > old_value:
#        pass
#    else:
#        if iterations > 3:
#            stop = 1
#        else:
#            random.shuffle(a)
#show_unused_spaces(mat4)
#
#def show_unused_spaces(house_matrix):
#    house_matrix = house_matrix.copy()
#    house_matrix2 = house_matrix.copy()
#    show_grid = Show_grid()
#    for i in range(2):
#        for loc in range(len(house_matrix)):
#            if i == 0:
#                house_matrix2[loc, 4] = 4
##                show_grid.draw_house(house_matrix2[loc, :], loc, numbers = True, circles = True)
#                show_grid.draw_house(house_matrix2[loc, :], loc, numbers = True, types = 'circles')
#            else:
#                show_grid.draw_house(house_matrix[loc, :], loc, numbers = True)
#        
#def distancesf(loc, matrix, waters):
#    matrix = matrix.copy()
#    free_space_cur = matrix[loc, 9]
#    x1 = matrix[loc, 0]
#    y1 = matrix[loc, 1]
#    x2 = matrix[loc, 2]
#    y2 = matrix[loc, 3]
#    temp = np.delete(matrix, loc, 0)
#    
#    house_free_space = temp[:, 9]
#    
#    right_side = temp[:, 2] 
#    left_side = temp[:, 0]
#    top_side = temp[:, 1] 
#    bottom_side = temp[:, 3]
#    
#    free_space = np.ones((len(house_free_space), 2)) * free_space_cur
#    
#    free_space[:, 0] = house_free_space
#    
#    free_space[:waters, 1] = 0.0
#    
#    free_space = np.max(free_space, 1)
#    
#    
#    
#    first_condition = np.logical_and( x1 >= (right_side + free_space) ,
#                                      np.logical_or.reduce(( np.logical_and( y1 <= top_side,
#                                      y1 >= bottom_side ), np.logical_and( y2 <= top_side,
#                                      y2 >= bottom_side ), np.logical_and(y2 <= bottom_side, y1 >= top_side),
#                                        np.logical_and( y2 >= bottom_side, y1 <= top_side))))
#    second_condition = np.logical_and( x1 > (right_side + free_space),
#                                       y1 < (bottom_side - free_space) )
#    third_condition = np.logical_and( y1 <= (bottom_side - free_space),
#                                      np.logical_or.reduce(( np.logical_and( x1 <= right_side,
#                                      x1 >= left_side ), np.logical_and( x2 <= right_side,
#                                      x2 >= left_side ), np.logical_and(x1 <= left_side, x2 >= right_side),
#                                        np.logical_and( x1 >= left_side, x2 <= right_side))))
#    fourth_condition = np.logical_and( y1 < (bottom_side - free_space),
#                                      x2 < (left_side - free_space) )
#       
#    fifth_condition = np.logical_and( x2 <= (left_side - free_space),
#                                      np.logical_or.reduce(( np.logical_and( y1 <= top_side,
#                                      y1 >= bottom_side ), np.logical_and( y2 <= top_side,
#                                      y2 >= bottom_side ), np.logical_and( y2 <= bottom_side, y1 >= top_side),
#                                        np.logical_and( y2 >= bottom_side, y1 <= top_side))))
#    sixth_condition = np.logical_and( x2 < (left_side - free_space),
#                                      y2 > (top_side + free_space) )
#    seventh_condition = np.logical_and( y2 >= (top_side +  free_space),
#                                        np.logical_or.reduce(( np.logical_and( x1 <= right_side,
#                                        x1 >= left_side ), np.logical_and( x2 <= right_side,
#                                        x2 >= left_side ), np.logical_and( x1 <= left_side, x2 >= right_side),
#                                        np.logical_and( x1 >= left_side, x2 <= right_side))))
#    eigth_condition = np.logical_and( y2 > (top_side + free_space),
#                                      x1 > (right_side + free_space) )
#    
#    # put all conditions into an numpy array to test them all at once
#    all_cond = np.array([first_condition, second_condition, third_condition,
#                         fourth_condition, fifth_condition, sixth_condition,
#                         seventh_condition, eigth_condition])    
#    
##    print(all_cond)
#    if all( all_cond.sum(0) == 1 ):
##        print(all_cond.shape)
#        
#        all_cond = all_cond[:, waters:]
#        
#        temp = temp[waters:]
#        
#        positions = np.array([x1, y1, x2, y2])    
#        distance_ind = np.argmax(all_cond, axis = 0)
#        distances = np.array( [0.0] * ( len(distance_ind) + 4 ) )
#        
#        # calculate the minimum distance of the house to other houses
#        positions = np.array([x1, y1, x2, y2])
#        
#        for i in range(len(temp)):
#            plane = distance_ind[i]
#        #            print(plane)
#            m = np.abs(positions[DIST2[str(plane)]] - temp[i, DIST[str(plane)]]) 
#            # if even
#        #            print(plane, m)
#            if plane % 2 == 0:
#                distances[i] = np.abs(m) - free_space_cur
#            # if odd
#            else:
#                distances[i] = np.sqrt( np.dot(m, m) ) - free_space_cur
#        
#        distances[-1] = y2 -  free_space_cur
#        distances[-2] = (GRID['height'] - free_space_cur) - y1
#        distances[-3] = (GRID['width'] - free_space_cur) - x2
#        distances[-4] = x1 - free_space_cur
#        
#        return 0, np.min(distances)
#    return 1, None
