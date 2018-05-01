# import global vars
from global_vars import PERC_SOLO, PERC_BUNG, PERC_VIL

# import necessary modules
import numpy as np

# this is a class for the houses
class House(object):
    def __init__(self, version):
        self.version = version
        self.matrix = self.conc(version)
        self.rows = version
        self.value = -10000000
        self.columns = self.matrix.shape[1]
            
        
    def conc(self, version):
        # initialize a empty matrix with all the future data
        matrix = np.zeros(shape = (version, 9))
        
        # for column 4 insert the array with number of house types
        matrix[:, 4] = np.concatenate((np.repeat(1, PERC_SOLO * version), 
                                       np.repeat(2, PERC_BUNG * version),
                                       np.repeat(3, PERC_VIL * version)))
        return matrix
    
    
    def update_value(self, new_value):
        self.value = new_value
