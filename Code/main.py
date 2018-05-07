# import necessary modules
import os, sys

# add current structure to path 
directory = os.path.dirname(os.path.realpath("__file__"))
sys.path.append(os.path.join(directory, "functions"))

# import house class
from house_class import House
from draw_plan import Show_grid
from stoch_hill_climb import stoch_steepest_hill

#show_grid = Show_grid()
# import functions from other documents

# define the 3 versions of the problem
total_houses = [20, 40, 60]
total_houses = 20

# create the class for houses and generate random solution
house = House(total_houses)

## generate a starting solution
mat = house.get_house_matrix()
value = house.compute_value()
print('value:', value)

for i in range(100):
    mat = stoch_steepest_hill(house)
    price = house.compute_value()
    print(price)
house.set_house_matrix(mat)


show_grid = Show_grid()
mat = house.get_house_matrix()
for k in range(total_houses):
     show_grid.draw_house(mat[k, :], k)