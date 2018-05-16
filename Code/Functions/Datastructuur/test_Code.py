


new_matrix = np.zeros(shape = (self.total_houses + 4, self.matrix.shape[1]))
new_matrix[4:, :] = self.matrix.copy()
water_needed = GRID["height"] * GRID["width"] * 0.2
# random water amount
random_water = random.randint(1,4)

# 1 water body
if random_water == 1:
    ratio = np.random.uniform(low = 0.25 , high = 4)
    width= math.sqrt(water_needed/ratio)
    height = ratio * width
    new_matrix[0, 0] = np.random.uniform(low = height, high = GRID["height"])
    new_matrix[0, 1] = np.random.uniform(low = width , high = GRID["width"])
    new_matrix[0, 2] = new_matrix[0, 0] + width
    new_matrix[0, 3] = new_matrix[0, 1] - height
    new_matrix[0, 4] = 4
    new_matrix[0, 5] = random.randint(0,1)
    new_matrix[0, 7] = height
    new_matrix[0, 8] = width
    
# 2 water bodies
for i in range(random_water): 
    if i==0:              
        width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
        ratio = np.random.uniform(low = 0.25 , high = 4)
        height = ratio * width
        water_left = water_needed-width*height
        while water_left<0:
            width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
            ratio = np.random.uniform(low = 0.1 , high = 4)
            height = ratio * width
            water_left = water_needed-width*height
        new_matrix[i, 0] = np.random.uniform(low = height, high = GRID["height"])
        new_matrix[i, 1] = np.random.uniform(low = width , high = GRID["width"])
        new_matrix[i, 2] = new_matrix[0, 0] + width
        new_matrix[i, 3] = new_matrix[0, 1] - height
        new_matrix[i, 4] = 4
        new_matrix[i, 5] = random.randint(0,1)
        new_matrix[i, 7] = height
        new_matrix[i, 8] = width
    else:
        width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
        ratio = np.random.uniform(low = 0.25 , high = 4)
        height = ratio * width
        water_left = water_needed-width*height
        while water_left<0:
            width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
            ratio = np.random.uniform(low = 0.25 , high = 4)
            height = ratio * width
            water_left = water_needed-width*height
        new_matrix[i, 0] = np.random.uniform(low = height, high = GRID["height"])
        new_matrix[i, 1] = np.random.uniform(low = width , high = GRID["width"])
        new_matrix[i, 2] = new_matrix[0, 0] + width
        new_matrix[i, 3] = new_matrix[0, 1] - height
        new_matrix[i, 4] = 4
        new_matrix[i, 5] = random.randint(0,1)
        new_matrix[i, 7] = height
        new_matrix[i, 8] = width
        valid, distance = check_house(i, new_matrix)
        while valid == 1:
            width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
            ratio = np.random.uniform(low = 0.25 , high = 4)
            height = ratio * width
            water_left = water_needed-width*height
            while water_left<0:
                width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
                ratio = np.random.uniform(low = 0.25 , high = 4)
                height = ratio * width
                water_left = water_needed-width*height
            new_matrix[i, 0] = np.random.uniform(low = height, high = GRID["height"])
            new_matrix[i, 1] = np.random.uniform(low = width , high = GRID["width"])
            new_matrix[i, 2] = new_matrix[0, 0] + width
            new_matrix[i, 3] = new_matrix[0, 1] - height
            new_matrix[i, 4] = 4
            new_matrix[i, 5] = random.randint(0,1)
            new_matrix[i, 7] = height
            new_matrix[i, 8] = width
            valid, distance = check_house(i, new_matrix)
            
# 3 or more water bodies
for i in range(random_water): 
    if i==0:              
        width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
        ratio = np.random.uniform(low = 0.25 , high = 4)
        height = ratio * width
        water_left = water_needed-width*height
        while water_left<0:
            width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
            ratio = np.random.uniform(low = 0.1 , high = 4)
            height = ratio * width
            water_left = water_needed-width*height
        new_matrix[i, 0] = np.random.uniform(low = height, high = GRID["height"])
        new_matrix[i, 1] = np.random.uniform(low = width , high = GRID["width"])
        new_matrix[i, 2] = new_matrix[0, 0] + width
        new_matrix[i, 3] = new_matrix[0, 1] - height
        new_matrix[i, 4] = 4
        new_matrix[i, 5] = random.randint(0,1)
        new_matrix[i, 7] = height
        new_matrix[i, 8] = width
        
    elif i == (random_water - 1):
        ratio = np.random.uniform(low = 0.25 , high = 4)
        width= math.sqrt(water_left/ratio)
        height = ratio * width
        new_matrix[0, 0] = np.random.uniform(low = height, high = GRID["height"])
        new_matrix[0, 1] = np.random.uniform(low = width , high = GRID["width"])
        new_matrix[0, 2] = new_matrix[0, 0] + width
        new_matrix[0, 3] = new_matrix[0, 1] - height
        new_matrix[0, 4] = 4
        new_matrix[0, 5] = random.randint(0,1)
        new_matrix[0, 7] = height
        new_matrix[0, 8] = width
    else:
        width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
        ratio = np.random.uniform(low = 0.25 , high = 4)
        height = ratio * width
        water_left = water_needed-width*height
        while water_left<0:
            width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
            ratio = np.random.uniform(low = 0.25 , high = 4)
            height = ratio * width
            water_left = water_needed-width*height
        new_matrix[i, 0] = np.random.uniform(low = height, high = GRID["height"])
        new_matrix[i, 1] = np.random.uniform(low = width , high = GRID["width"])
        new_matrix[i, 2] = new_matrix[0, 0] + width
        new_matrix[i, 3] = new_matrix[0, 1] - height
        new_matrix[i, 4] = 4
        new_matrix[i, 5] = random.randint(0,1)
        new_matrix[i, 7] = height
        new_matrix[i, 8] = width
        valid, distance = check_house(i, new_matrix)
        while valid == 1:
            width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
            ratio = np.random.uniform(low = 0.25 , high = 4)
            height = ratio * width
            water_left = water_needed-width*height
            while water_left<0:
                width = np.random.uniform(low = GRID["width"]/4 , high = GRID["width"])
                ratio = np.random.uniform(low = 0.25 , high = 4)
                height = ratio * width
                water_left = water_needed-width*height
            new_matrix[i, 0] = np.random.uniform(low = height, high = GRID["height"])
            new_matrix[i, 1] = np.random.uniform(low = width , high = GRID["width"])
            new_matrix[i, 2] = new_matrix[0, 0] + width
            new_matrix[i, 3] = new_matrix[0, 1] - height
            new_matrix[i, 4] = 4
            new_matrix[i, 5] = random.randint(0,1)
            new_matrix[i, 7] = height
            new_matrix[i, 8] = width
            valid, distance = check_house(i, new_matrix)