import numpy as np
from utils.kinematic_utils import KinematicUtils
from utils.three_dim_calculation import ThreeDimCalculation
from model.components.compunent_types import ComponentTypes as CT
import pandas as pd


class Configuration:
    
    def __init__(self):
        self.link_num:int = 0
        self.rotation_joint_num:int = 0
        self.prismatic_joint_num:int = 0
        self.components:pd.DataFrame = pd.DataFrame(columns = [
            "name",
            "entity",
            "bound_reference_frames",
            "compensate_transformation_matrix"
        ])
        self.components["compensate_transformation_matrix"] = self.components["compensate_transformation_matrix"].astype(object)
        self.reference_frames:pd.DataFrame = pd.DataFrame(columns = [
            "name"
        ])
    
    def construct(self, 
                  name, 
                  component):
        """Assemble a robotic arm model using Joint and Link.
    
        Args:
            name (np.typing.NDArray):      Name of the component, used for positioning components.
            component (np.typing.NDArray): A component.
    
        Returns:
            Assembly: Returns the current instance for chained calls.
        """
        if name in self.components.keys():
            raise Exception("Name conflict...")
        match component.type:
            case CT.LINK:
                self.link_num += 1
            case CT.ROTATION_JOINT:
                self.rotation_joint_num += 1
            case CT.PRISMATIC_JOINT:
                self.prismatic_joint_num += 1
            case _:
                raise Exception(f"Unsupport component type...")
        new_row = pd.DataFrame([
            {"name": name, "entity": component}
            ])
        self.components = pd.concat([self.components, new_row], ignore_index = True)
        return self
    
    def confirm_construct(self) -> None:
        """Actions after configuration construct completed.
    
        Args:
    
        Returns:
            None.
        """
        self.bind_reference_frame()
        self.calculate_compensation_transformation_matrix()
        
    def bind_reference_frame(self) -> None:
        """Automatically create coordinate systems that comply with standard D-H analysis based on configuration and bind them.
    
        Args:
    
        Returns:
            None.
        """
        reference_frame_idx:int = 0
        reference_frame_name:str = f"_rf-{reference_frame_idx}"
        new_row = pd.DataFrame([
            {"name": reference_frame_name}
            ])
        self.reference_frames = pd.concat([self.reference_frames, new_row], ignore_index = True)
        # self.reference_frames[reference_frame_name] = "_base"
        
        for idx, component in self.components.iterrows():
            match component["entity"].type:
                case CT.LINK:
                    self.components.at[idx, "bound_reference_frames"] = reference_frame_name
                case CT.ROTATION_JOINT:
                    reference_frame_idx += 1
                    reference_frame_name = f"_rf-{reference_frame_idx}"
                    self.components.at[idx, "bound_reference_frames"] = reference_frame_name
                    new_row = pd.DataFrame([
                        {"name": reference_frame_name}
                        ])
                    self.reference_frames = pd.concat([self.reference_frames, new_row], ignore_index = True)
    
    def calculate_compensation_transformation_matrix(self) -> None:
        """Calculate the transformation matrix between each component and its bound reference frame.
    
        Args:
    
        Returns:
            None.
        """
        consecutive_endpoint_vector = np.array([0, 0, 0])
        for idx, component in self.components.iterrows():
            match component["entity"].type:
                case CT.LINK:
                    consecutive_endpoint_vector = ThreeDimCalculation.extend(consecutive_endpoint_vector,
                                                                             component["entity"].translation_direction,
                                                                             component["entity"].translation_distance)
                    endpoint_vector = component["entity"].translation_direction * component["entity"].translation_distance
                    x = endpoint_vector[0]
                    y = endpoint_vector[1]
                    z = endpoint_vector[2]
                    self.components.at[idx, "compensate_transformation_matrix"] = np.array([
                        [1, 0, 0, x],
                        [0, 1, 0, y],
                        [0, 0, 1, z],
                        [0, 0, 0, 1]
                    ])
                case CT.ROTATION_JOINT:
                    rotation_direction = component["entity"].axis_direction
                    lam = KinematicUtils.calculate_lam(consecutive_endpoint_vector,
                                                       rotation_direction)
                    self.components.at[idx, "compensate_transformation_matrix"] = np.array([
                        [1, 0, 0, 0],
                        [0, 1, 0, 0],
                        [0, 0, 1, -lam],
                        [0, 0, 0, 1]
                    ])
                    consecutive_endpoint_vector = np.array([0, 0, -lam])
    
    def get_dh_table(self, 
                      inputs:list) -> np.typing.NDArray:
        """Generate standard D-H table from given inputs. It should be noted that the generated D-H table is the parameters of each reference frame rather than each joint.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            np.typing.NDArray: Standard D-H table
        """
        
        if len(inputs) != self.rotation_joint_num + self.prismatic_joint_num:
            raise Exception("The number of input signals does not match the number of joints...")
        inputs_enum:enumerate = enumerate(inputs)
        last_input:float = 0.0
        consecutive_endpoint_vector:np.typing.NDArray = np.array([0.0, 0.0, 0.0])
        dh_table:np.typing.NDArray = np.array([[0.0, 0.0, 0.0, 0.0]])
        
        for _, component in self.components.iterrows():
            match component["entity"].type:
                case CT.LINK:
                    consecutive_endpoint_vector = ThreeDimCalculation.extend(consecutive_endpoint_vector,
                                                                             component["entity"].translation_direction,
                                                                             component["entity"].translation_distance)
                    # if idx == len(self.components) - 1:
                    #     dh_parameters = (0, 
                    #                      consecutive_endpoint_vector[2],
                    #                      consecutive_endpoint_vector[0],
                    #                      0)
                    #     dh_parameters = np.array(dh_parameters)
                    #     last_rotation_rad = last_input
                    #     dh_parameters[0] += last_rotation_rad
                    #     dh_table = np.vstack([dh_table, dh_parameters.reshape(1, 4)])
                case CT.ROTATION_JOINT:
                    
                    rotation_direction:np.typing.NDArray = component["entity"].axis_direction
                    dh_parameters:tuple = KinematicUtils.calculate_dh_parameters(consecutive_endpoint_vector,
                                                                           rotation_direction)
                    dh_parameters:np.typing.NDArray = np.array(dh_parameters)
                    last_rotation_rad:float = last_input
                    dh_parameters[0] += last_rotation_rad
                    dh_table = np.vstack([dh_table, dh_parameters.reshape(1, 4)])
                    
                    lam = KinematicUtils.calculate_lam(consecutive_endpoint_vector,
                                                       rotation_direction)
                    consecutive_endpoint_vector = np.array([0, 0, -lam])
                    _, rotation_rad = next(inputs_enum)
                    last_input = rotation_rad
                                  
        return dh_table
    
    def get_po_matrixs(self,
                       inputs:list) -> dict:
        """Perform forward kinematic analysis and return position-orientation matrixs of each reference frame.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            dict: Position-orientation matrix of each joints from base to tip.
        """

        dh_table:np.typing.NDArray = self.get_dh_table(inputs)
        reference_frame_po_matrixs:dict = KinematicUtils.forward_kinematics(dh_table = dh_table,
                                                                            names = self.reference_frames["name"].tolist())
        reference_frame_po_matrixs_enum = enumerate(reference_frame_po_matrixs.items())
        po_matrixs = {}
        reference_frame_name:None | str = None
        for _, component in self.components.iterrows():
        # for key, component in self.components.items():
            if component["bound_reference_frames"] != reference_frame_name or reference_frame_name is None:
                _, (reference_frame_name, last_po_matrix) = next(reference_frame_po_matrixs_enum)
                po_matrixs[reference_frame_name] = last_po_matrix
            transformation_matrix = component["compensate_transformation_matrix"]
            last_po_matrix = last_po_matrix @ transformation_matrix
            po_matrixs[component["name"]] = last_po_matrix
        return po_matrixs
    