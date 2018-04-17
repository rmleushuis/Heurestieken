tot_width = 160
tot_height = 180

class house(object):
    def __init__(self, index, x_left, y_left, x_right, y_right, dist, house_type):
        self.index = index
        self.x_left = x_left
        self.y_left = y_left
        self.x_right = x_right
        self.y_right = y_right
        self.dist = dist
        self.name = house_type[0]
        self.type_number = house_type[1]
        self.width = house_type[2]
        self.height = house_type[3]
        self.price = house_type[4]
        self.perc = house_type[5]
        # minimale VERPLICHTE AFSTAND
        self.min_dist = house_type[6]

    def get_index(self):
        return self.index        
    def getx_left(self):
        return self.x_left
    def gety_left(self):
        return self.y_left
    def getx_right(self):
        return self.x_right
    def gety_right(self):
        return self.y_right
    def get_width(self):
        return self.width
    def getdist(self):
        return self.dist
    def get_name(self):
        return self.name
    def get_height(self):
        return self.height
    def get_price(self):
        return self.price
    def get_perc(self):
        return self.perc
    def get_min_dist(self):
        return self.min_dist
    
    def move(self, x_left, y_left, x_right, y_right):
        self.x_left = x_left
        self.y_left = y_left
        self.x_right = x_right
        self.y_right = y_right
    def changedist(self, dist):
        # minimmale afstand tot VOLGEND huis
        self.dist = dist