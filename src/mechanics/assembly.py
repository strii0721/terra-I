from dk.logger.log4p import Log4P
import numpy as np
from utils.kinematic_utils import KinematicUtils
from utils.three_dim_calculation import ThreeDimCalculation

class Assembly:
    
    components = {}
    
    
    def __init__(self):
        self.logger = Log4P()
    
    def construct(self, 
                  name, 
                  component):
        if name in self.components.keys:
            self.logger.info("Name conflict...")
            return self
        self.components[name] = component
        return self
    
    def confirm(self):
        self._get_dh_table
        
    def _get_dh_table(self):
        endpoint_vector = np.array([0,0,0])
        for component in self.components:
            match component.type:
                case "LINK":
                    endpoint_vector = ThreeDimCalculation.extend(endpoint_vector,
                                                                 component.translation_direction,
                                                                 component.translation_distance)
                case "JOINT":
                    a = KinematicUtils.calculate_a(endpoint_vector, 
                                                   component.axis_direction)