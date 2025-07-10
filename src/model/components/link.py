from utils.three_dim_calculation import ThreeDimCalculation
import numpy as np
from model.components.compunent_types import ComponentTypes as CT

class Link:
    
    def __init__(self, 
                 translation_direction,
                 translation_distance,
                 visibility = True):
        self.type:CT = CT.LINK
        self.translation_direction:np.typing.NDArray = ThreeDimCalculation.convert_to_unit_vector(translation_direction)
        self.translation_distance:float = translation_distance
        self.visibility:bool = visibility