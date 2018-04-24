import numpy as np
from global_vars import perc_solo, perc_bung, perc_vil

class house_matrix(object):
    def __init__(self, version):
        
        # initialize a empty matrix with all the future data
        matrix = np.zeros(shape = (version, 8))
        
        # for column 4 insert the array with number of house types
        matrix[:, 4] = np.concatenate((np.repeat(1, perc_solo * version), 
                                       np.repeat(2, perc_bung * version),
                                       np.repeat(3, perc_vil * version)))
        
        self.version = version
        self.matrix = matrix
        self.rows = version
        self.columns = matrix.shape[1]
        
houses = house_matrix(20)