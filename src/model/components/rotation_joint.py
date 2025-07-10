from utils.three_dim_calculation import ThreeDimCalculation
import numpy as np
from model.components.compunent_types import ComponentTypes as CT

class RotationJoint:
    
    def __init__(self, 
                 axis_direction,
                 visibility = True
                 ):
        self.type:CT = CT.ROTATION_JOINT
        self.axis_direction:np.typing.NDArray = ThreeDimCalculation.convert_to_unit_vector(np.array(axis_direction))
        self.visibility:bool = visibility