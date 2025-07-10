from utils.three_dim_calculation import ThreeDimCalculation
import numpy as np
from model.components.compunent_types import ComponentTypes as CT

class Link:
    
    def __init__(self, 
                 endpoint_vector,
                 visibility = True):
        self.type:CT = CT.LINK
        self.endpoint_vector:np.typing.NDArray = np.asarray(endpoint_vector, dtype=np.float64)
        self.visibility:bool = visibility