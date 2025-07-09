from utils.three_dim_calculation import ThreeDimCalculation
import numpy as np
from structure.components.compunent_types import ComponentTypes as CT

class Link:
    
    def __init__(self, 
                 translation_direction,
                 translation_distance,
                 visibility = True):
        self.type = CT.LINK
        self.translation_direction = ThreeDimCalculation.convert_to_unit_vector(translation_direction)
        self.translation_distance = translation_distance
        self.visibility = visibility