# import function
from Functions import draw_plan
from draw_plan import draw_plan

# import house class
from house_class import house

# import functions from other documents
from start_sol import start_sol


# define the 3 versions of the problem
total_houses = [20, 40, 60]

def starting_sol(version):
    
    # create the class for houses
    houses = house(version)
    
    # generate a starting solution
    houses.matrix = start_sol(houses)
    
    # draw the starting solution and don't save it
    draw_plan(houses, 0)

# create starting solution for first version of problem
starting_sol(40)