from dk.logger.log4p import Log4P
import numpy as np
from utils.kinematic_utils import KinematicUtils
from utils.three_dim_calculation import ThreeDimCalculation
from structure.components.compunent_types import ComponentTypes as CT

class Assembly:
    
    components = {}
    
    
    def __init__(self):
        self.logger = Log4P()
        self.rotation_joint_num = 0
        self.prismatic_joint_num = 0
    
    def construct(self, 
                  name, 
                  component):
        """Assemble a robotic arm model using Joint and Link.
    
        Args:
            name (np.array(list)):      Name of the component, used for positioning components.
            component (np.array(list)): A component.
    
        Returns:
            Assembly: Returns the current instance for chained calls.
        """
        if name in self.components.keys:
            raise Exception("Name conflict...")
            return 0
        match component.type:
            case CT.LINK:
                pass
            case CT.ROTATION_JOINT:
                self.rotation_toint_num += 1
            case CT.PRISMATIC_JOINT:
                pass
            case _:
                raise Exception(f"Unsupport component type...")
        self.components[name] = component
        return self
    
    def get_dh_tables(self, 
                   inputs):
        """Control signals for each joint.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            tuple: Standard D-H table and modified D-H table
        """
        
        if len(inputs) != self.rotation_joint_num + self.prismatic_joint_num:
            raise Exception("The number of input signals does not match the number of joints...")
        inputs_enum = enumerate(inputs)
        last_input = 0
        consecutive_endpoint_vector = np.array([0, 0, 0])
        dh_table = np.array([])
        modified_dh_table = np.array([])
        
        for idx, component in enumerate(self.components):
            match component.type:
                case CT.LINK:
                    endpoint_vector = ThreeDimCalculation.extend(consecutive_endpoint_vector, 
                                                         component.translation_direction,
                                                         component.translation_distance)
                    rotation_direction = np.array([0, 0, 1])
                    modified_dh_parameters = KinematicUtils.calculate_dh_parameters(endpoint_vector, 
                                                                                    rotation_direction)
                    modified_dh_parameters = list(modified_dh_parameters)
                    modified_dh_table.append(modified_dh_parameters)
                    consecutive_endpoint_vector = consecutive_endpoint_vector + endpoint_vector
                    if idx == len(self.components) - 1:
                        dh_parameters = KinematicUtils.calculate_dh_parameters(consecutive_endpoint_vector,
                                                                           rotation_direction)
                        dh_parameters = list(dh_parameters)
                        last_rotation_rad = last_input
                        dh_parameters[0] += last_rotation_rad
                        dh_table.append(dh_parameters)
                case CT.ROTATION_JOINT:
                    endpoint_vector = np.array([0, 0, 0])
                    rotation_direction = component.axis_direction
                    modified_dh_parameters = KinematicUtils.calculate_dh_parameters(endpoint_vector,
                                                                                    rotation_direction)
                    modified_dh_parameters = list(modified_dh_parameters)
                    rotation_rad = next(inputs_enum)
                    modified_dh_parameters[0] += rotation_rad
                    modified_dh_table.append(modified_dh_parameters)
                    dh_parameters = KinematicUtils.calculate_dh_parameters(consecutive_endpoint_vector,
                                                                           rotation_direction)
                    dh_parameters = list(dh_parameters)
                    last_rotation_rad = last_input
                    dh_parameters[0] += last_rotation_rad
                    dh_table.append(dh_parameters)
                    last_input = rotation_direction
        return dh_table, modified_dh_table
                    