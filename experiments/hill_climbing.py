import random
import math

tot_width = 160
tot_height = 180
tot = 20

tot_eens = 0.6 * tot
tot_bung = 0.25 * tot
tot_mai = 0.15 * tot

# naam, nummer, breedte, hoogte, prijs, procentuele toename, minimale vrije ruimte
house_types = {"single" : ["eensgezinswoning", 1, 8 ,8 , 285000, 3, 2],
               "bungalow":["bungalow",2, 10, 7.5 , 399000, 4 ,3],
               "maison":["maison", 3, 11, 10.5, 610000, 6, 6]}


# functie voro eengezindshuizen
def genereer():
    x_left = math.floor(random.random() * (tot_width - house_types["eensgezinswoning"][2]))
    y_left = math.floor(random.random() * (tot_width - house_types["eensgezinswoning"][3]))
    x_right = x_left + house_types["eensgezinswoning"][2]
    y_right = y_left - house_types["eensgezinswoning"][3]
    position = [x_left, y_left, x_right, y_right]
    return position

# Eengezinshuizen
for i in range(tot_eens):
    positie = genereer()
    # check if not in another house
    
    
    # calculate distance to other house and check if > 6
    
    
    
    # set the house in stone
    





