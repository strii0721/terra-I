#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Thu Jul 10 2025
#
# Copyright (c) 2025 S.I.C.
#

import numpy as np
from utils.kinematic_utils import KinematicUtils
from numpy import sin as s, cos as c
from model.components.compunent_types import ComponentTypes as CT
import pandas as pd


class RoboticArm:
    
    def __init__(self):
        self.link_num:int = 0
        self.rotation_joint_num:int = 0
        self.prismatic_joint_num:int = 0
        self.components:pd.DataFrame = pd.DataFrame(columns = [
            "name",
            "entity",
            "bound_reference_frames",
            "compensate_transformation_matrix",
            "po_matrix"
        ])
        self.components["compensate_transformation_matrix"] = self.components["compensate_transformation_matrix"].astype(object)
        self.components["po_matrix"] = self.components["po_matrix"].astype(object)
        self.reference_frames:pd.DataFrame = pd.DataFrame(columns = [
            "name",
            "dh_parameters",
            "po_matrix"
        ])
        self.reference_frames["po_matrix"] = self.reference_frames["po_matrix"].astype(object)
        self.inverse_kinematics_enabled = []
    
    def construct(self, 
                  name, 
                  component):
        """Assemble a robotic arm model using Joint and Link.
    
        Args:
            name (np.typing.NDArray):      Name of the component, used for positioning components.
            component (np.typing.NDArray): A component.
    
        Returns:
            Configuration: Returns the current instance for chained calls.
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
        init_inputs = self.get_joint_outputs()
        self.control(init_inputs)        
        
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
    
    def calculate_compensation_transformation_matrix(self,
                                                     inputs:list) -> None:
        """Calculate the transformation matrix between each component and its bound reference frame.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            None.
        """
        
        inputs_enum:enumerate = enumerate(inputs)
        consecutive_endpoint_vector = np.array([0, 0, 0], dtype=np.float64)
        for idx, component in self.components.iterrows():
            match component["entity"].type:
                case CT.LINK:
                    consecutive_endpoint_vector += component["entity"].endpoint_vector
                    endpoint_vector = component["entity"].endpoint_vector
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
                    _, rotation_rad = next(inputs_enum)
                    rotation_direction = component["entity"].axis_direction
                    lam = KinematicUtils.calculate_lam(consecutive_endpoint_vector,
                                                       rotation_direction)
                    self.components.at[idx, "compensate_transformation_matrix"] = np.array([
                        [c(rotation_rad), -s(rotation_rad), 0, 0],
                        [s(rotation_rad), c(rotation_rad), 0, 0],
                        [0, 0, 1, -lam],
                        [0, 0, 0, 1]
                    ])
                    consecutive_endpoint_vector = np.array([0, 0, -lam])
                    
    def enabled_inverse_kinematic(self,
                                 names: list) -> None:
        """Specify reference systems or components to participate in inverse kinematics analysis. This function is recommended to be called after the entire robotic arm has been constructed (using Configuration.confirm_construct()).
    
        Args:
            name (np.typing.NDArray): The name of the reference system or component that needs to participate in the inverse kinematics analysis.
    
        Returns:
            None.
        """
        
        component_names = self.components["name"].tolist()
        reference_frame_names = self.reference_frames["name"].tolist()
        for name in names:
            if name not in component_names and name not in reference_frame_names:
                raise Exception(f"Fail to locate a joint or reference frame named {name}")
            self.inverse_kinematics_enabled.append(name)
    
    def _get_dh_table(self, 
                     inputs:list) -> list:
        """Generate standard D-H table from given inputs. It should be noted that the generated D-H table is the parameters of each reference frame rather than each joint.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            None.
        """
        
        if len(inputs) != self.rotation_joint_num + self.prismatic_joint_num:
            raise Exception("The number of input signals does not match the number of joints...")
        self.calculate_compensation_transformation_matrix(inputs)
        inputs_enum:enumerate = enumerate(inputs)
        last_input:float = 0.0
        consecutive_endpoint_vector:np.typing.NDArray = np.array([0.0, 0.0, 0.0])

        dh_table:list = [(0.0, 0.0, 0.0, 0.0)]
        for _, component in self.components.iterrows():
            match component["entity"].type:
                case CT.LINK:
                    consecutive_endpoint_vector = consecutive_endpoint_vector + component["entity"].endpoint_vector

                case CT.ROTATION_JOINT:
                    rotation_direction:np.typing.NDArray = component["entity"].axis_direction
                    dh_parameters:tuple = KinematicUtils.calculate_dh_parameters(consecutive_endpoint_vector,
                                                                                 rotation_direction)
                    last_rotation_rad:float = last_input
                    dh_parameters = list(dh_parameters)
                    dh_parameters[0] += last_rotation_rad
                    dh_parameters = tuple(dh_parameters)
                    dh_table.append(dh_parameters)
                    lam = KinematicUtils.calculate_lam(consecutive_endpoint_vector,
                                                       rotation_direction)
                    consecutive_endpoint_vector = np.array([0, 0, -lam])
                    _, rotation_rad = next(inputs_enum)
                    last_input = rotation_rad
                    
        return dh_table
    
    def get_po_matrixs(self,
                       inputs:list) -> dict:
        """Perform forward kinematic analysis and return position-orientation matrixs of each joints and reference frame.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            dict: Position-orientation matrix of each joints and reference frame.
        """
        
        if len(inputs) != self.rotation_joint_num + self.prismatic_joint_num:
            raise Exception("The number of input signals does not match the number of joints...")
        dh_table:list = self._get_dh_table(inputs)
        names:list = self.reference_frames["name"].tolist()
        reference_frame_po_matrixs:dict = KinematicUtils.forward_kinematics(dh_table = dh_table,
                                                                            names = names)
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
    
    def get_ik_po_matrixs(self, 
                          inputs:list) -> dict:
        """Perform forward kinematic analysis and return position-orientation matrixs of joints and reference frames that enabled inverse kinematic analysis.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            dict: Position-orientation matrix of joints and reference frames that enabled inverse kinematic analysis.
        """
        
        po_matrixs_dict:dict = self.get_po_matrixs(inputs)
        ik_po_matrics = {}
        for name, po_matrix in po_matrixs_dict.items():
            if name in self.inverse_kinematics_enabled:
                ik_po_matrics[name] = po_matrix
                
        return ik_po_matrics
    
    def apply_inverse_kinematic_analysis(self,
                                         target_po_matrix:np.typing.NDArray) -> list:
        """Apply inverse kinematic analysis on joints and reference frames that enabled inverse kinematic analysis.
    
        Args:
            target_po_matrix (np.typing.NDArray):   Target given position-orientation.
    
        Returns:
            list: Target joint inputs that make end of the configuration reach a given position-orientation.
        """
        
        current_joint_inputs = self.get_joint_outputs()
        target_joint_inputs = KinematicUtils.inverse_kinematics(po_matrixs_getter = self.get_ik_po_matrixs,
                                                                target_po_matrix = target_po_matrix,
                                                                current_joint_outputs = current_joint_inputs)
        return target_joint_inputs
    
    def get_joint_outputs(self) -> list:
        """Get current outputs of all joints
    
        Args:
    
        Returns:
            list: Current outputs of all joints (from base to tip)
        """
        joint_outputs = []
        for _, component in self.components.iterrows():
            match component["entity"].type:
                case CT.ROTATION_JOINT:
                    joint_outputs.append(component["entity"].angle)
                case CT.PRISMATIC_JOINT:
                    pass
                case _:
                    pass
        return joint_outputs
    
    def set_joint_inputs(self,
                         inputs:list) -> None:
        """Set the inputs for all joints.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            None.
        """
        inputs_enum = enumerate(inputs)
        for idx, component in self.components.iterrows():
            match component["entity"].type:
                case CT.ROTATION_JOINT:
                    _, input = next(inputs_enum)
                    self.components.at[idx, "entity"].angle = input
                case CT.PRISMATIC_JOINT:
                    pass
                case _:
                    pass
        
    def control(self,
                inputs:list) -> None:
        """Perform a control of the robotic arm. Please note that the input through this function will change the state of the current robot arm instance.
    
        Args:
            inputs (list): Input sequence.
    
        Returns:
            None.
        """
        po_matrixs = self.get_po_matrixs(inputs)
        component_names = self.components["name"].tolist()
        reference_frame_names = self.reference_frames["name"].tolist()
        for name, po_matrix in po_matrixs.items():
            if name in component_names:
                mask = self.components["name"] == name
                if mask.sum() == 1:
                    idx = self.components[mask].index[0]
                    self.components.at[idx, "po_matrix"] = po_matrix
            if name in reference_frame_names:
                mask = self.reference_frames["name"] == name
                if mask.sum() == 1:
                    idx = self.reference_frames[mask].index[0]
                    self.reference_frames.at[idx, "po_matrix"] = po_matrix
        self.set_joint_inputs(inputs)
        
    def get_render_list(self) -> list:
        """Output the coordinate information of the components that the current component needs to render in list form, and pass it to the renderer for visualisation.
    
        Args:
    
        Returns:
            list: A list of coordinate systems containing all components that need to be rendered.
        """
        
        render_list = []
        start_point = (0, 0, 0)
        for idx, component in self.components.iterrows():
            x_end_point = component["po_matrix"][0,3]
            y_end_point = component["po_matrix"][1,3]
            z_end_point = component["po_matrix"][2,3]
            end_point = (x_end_point, y_end_point, z_end_point)
            if component["entity"].visibility:
                render_list.append([start_point, end_point])
            start_point = end_point
        return render_list