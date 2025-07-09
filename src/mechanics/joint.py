from utils.three_dim_calculation import ThreeDimCalculation
import numpy as np

class Joint:
    
    def __init__(self, 
                 axis_direction,
                 visibility = True
                 ):
        self.type = "JOINT"
        self.axis_direction = ThreeDimCalculation.convert_to_unit_vector(np.array(axis_direction))
        self.visibility = visibility