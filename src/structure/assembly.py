import numpy as np
from utils.kinematic_utils import KinematicUtils
from utils.three_dim_calculation import ThreeDimCalculation
from structure.components.compunent_types import ComponentTypes as CT

class Assembly:
    
    components = {}
    
    
    def __init__(self):
        self.rotation_joint_num = 0
        self.prismatic_joint_num = 0
        self.components = {}
    
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
        if name in self.components.keys():
            raise Exception("Name conflict...")
        match component.type:
            case CT.LINK:
                pass
            case CT.ROTATION_JOINT:
                self.rotation_joint_num += 1
            case CT.PRISMATIC_JOINT:
                pass
            case _:
                raise Exception(f"Unsupport component type...")
        self.components[name] = component
        return self
    
    def get_dh_table(self, 
                      inputs):
        """Generate standard D-H table from given inputs.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            np.array(list): Standard D-H table
        """
        
        if len(inputs) != self.rotation_joint_num + self.prismatic_joint_num:
            raise Exception("The number of input signals does not match the number of joints...")
        inputs_enum = enumerate(inputs)
        last_input = 0
        consecutive_endpoint_vector = np.array([0, 0, 0])
        last_rotation_direction = np.array([0, 0, 1])
        dh_table = np.empty((0, 4))
        
        for idx, key in enumerate(self.components.keys()):
            match self.components[key].type:
                case CT.LINK:
                    consecutive_endpoint_vector = ThreeDimCalculation.extend(consecutive_endpoint_vector,
                                                                             self.components[key].translation_direction,
                                                                             self.components[key].translation_distance)
                    if idx == len(self.components) - 1:
                        dh_parameters = (0, 
                                         consecutive_endpoint_vector[2],
                                         consecutive_endpoint_vector[0],
                                         0)
                        dh_parameters = np.array(dh_parameters)
                        last_rotation_rad = last_input
                        dh_parameters[0] += last_rotation_rad
                        dh_table = np.vstack([dh_table, dh_parameters.reshape(1, 4)])
                case CT.ROTATION_JOINT:
                    rotation_direction = self.components[key].axis_direction
                    dh_parameters = KinematicUtils.calculate_dh_parameters(consecutive_endpoint_vector,
                                                                           rotation_direction)
                    lam = KinematicUtils.calculate_lam(consecutive_endpoint_vector,
                                                       rotation_direction)
                    consecutive_endpoint_vector = np.array([0, 0, -lam])
                    dh_parameters = np.array(dh_parameters)
                    last_rotation_rad = last_input
                    dh_parameters[0] += last_rotation_rad
                    dh_table = np.vstack([dh_table, dh_parameters.reshape(1, 4)])
                    _, rotation_rad = next(inputs_enum)
                    last_input = rotation_rad
                    
        return dh_table
    
    def get_modified_dh_table(self, 
                               inputs):
        """Generate modified D-H table from given inputs.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            tuple: Modified D-H table
        """
        
        if len(inputs) != self.rotation_joint_num + self.prismatic_joint_num:
            raise Exception("The number of input signals does not match the number of joints...")
        inputs_enum = enumerate(inputs)
        modified_dh_table = np.empty((0, 4))
        
        for key in self.components.keys():
            match self.components[key].type:
                case CT.LINK:
                    endpoint_vector = ThreeDimCalculation.extend(np.array([0, 0, 0]),
                                                                 self.components[key].translation_direction,
                                                                 self.components[key].translation_distance)
                    rotation_direction = np.array([0, 0, 1])
                    modified_dh_parameters = KinematicUtils.calculate_dh_parameters(endpoint_vector, 
                                                                                    rotation_direction)
                    modified_dh_parameters = np.array(modified_dh_parameters)
                    modified_dh_table = np.vstack([modified_dh_table, modified_dh_parameters.reshape(1, 4)])
                case CT.ROTATION_JOINT:
                    endpoint_vector = np.array([0, 0, 0])
                    rotation_direction = self.components[key].axis_direction
                    modified_dh_parameters = KinematicUtils.calculate_dh_parameters(endpoint_vector,
                                                                                    rotation_direction)
                    modified_dh_parameters = np.array(modified_dh_parameters)
                    _, rotation_rad = next(inputs_enum)
                    modified_dh_parameters[0] += rotation_rad
                    modified_dh_table = np.vstack([modified_dh_table, modified_dh_parameters.reshape(1, 4)])
                    
        return modified_dh_table
                    
    def get_po_matrixs(self,
                       inputs):
        """Perform forward kinematic analysis and return position-orientation matrixs of each components.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            set(np.array(list)): Position-orientation matrix of each joints from base to tip.
        """
        names = []
        for key in self.components.keys():
            if self.components[key].type == CT.ROTATION_JOINT:
                names.append(key)
        dh_table = self.get_dh_table(inputs)
        po_matrixs = KinematicUtils.forward_kinematics(dh_table,
                                                       names)
        return po_matrixs
    
    def get_fullscale_po_matrixs(self,
                                 inputs):
        names = []
        for key in self.components.keys():
            names.append(key)
        modified_dh_table = self.get_modified_dh_table(inputs)
        fullscale_po_matrixs = KinematicUtils.forward_kinematics(modified_dh_table,
                                                                 names)
        return fullscale_po_matrixs