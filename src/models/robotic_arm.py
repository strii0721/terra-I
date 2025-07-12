#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Fri Jul 11 2025
#
# IMMORTAL OMNISSIAH, HEAR OUR PRAYERS.
# WE ARE YOUR CHILDREN, PIOUS SCHOLARS OF THE PATH OF THE MACHINE. 
# WE PRIZE KNOWLEDGE ABOVE ALL ELSE, FOR IT IS YOUR ETERNAL GIFT UPON MANKIND. 
# WE ASPIRE TO THE BLESSED FORM OF THE MACHINE, AND ASCENSION THROUGH TECHNOLOGY, THAT WE MIGHT EMULATE THINE GLORY. 
# SHELTERED BY STEEL, AND PROTECTED BY THINE AVATARS OF WAR, WE PLY THE STARS IN SEARCH OF YOUR LOST GIFTS TO OUR KIND.
# MACHINE GOD, WATCH OVER US IN OUR TRAVELS, SHIELD US WITH METAL AND LIGHTNING, FOR THE UNIVERSE IS AN UNCARING VOID, AND THE WARP HUNGERS FOR US ALL.
# TOLL THE GREAT BELL ONCE! PULL THE LEVER FORWARD TO ENGAGE THE PISTON AND PUMP.
# TOLL THE GREAT BELL TWICE! WITH PUSH OF BUTTON FIRE THE ENGINE AND SPARK TURBINE INTO LIFE.
# TOLL THE GREAT BELL THRICE! SING PRAISE TO THE GOD OF ALL MACHINES!
#
# Copyright (c) 2025 S.I.C.
#

from models.interfaces.dh_assembly import DhAssembly
import pandas as pd
from enums.render_object_types import RenderObjectTypes
from utils.data_frame_utils import DataFrameUtils
from enums.part_types import PartTypes
from models.reference_frame import ReferenceFrame
from kinematics.kinematic_computer import KinematicComputer
import numpy as np

class RoboticArm(DhAssembly):
    
    def __init__(self) -> None:
        self._parts = pd.DataFrame(columns = [
            "index",
            "entity",
            "bound_reference_frame_index",
            "pose_matrix"
        ])
        self.parts["pose_matrix"] = self.parts["pose_matrix"].astype(object)
        self._reference_frames = pd.DataFrame(columns = [
            "index",
            "entity",
            "pose_matrix"
        ])
        self.reference_frames["pose_matrix"] = self.reference_frames["pose_matrix"].astype(object)
        self._inverse_kinematic_analysis_basis = []
    
    @property
    def parts(self) -> pd.DataFrame:
        return self._parts
    
    @property
    def reference_frames(self) -> pd.DataFrame:
        return self._reference_frames
    
    @property
    def inverse_kinematic_analysis_basis(self) -> list:
        return self._inverse_kinematic_analysis_basis
    
    def standard_input(self,
                       control_variable:list) -> None:
        kinematic_computer = KinematicComputer()
        pose_matrixs_dict = kinematic_computer.calculate_pose_matrixs(self,
                                                                 control_variable)
        self.update_control_variable(control_variable)
        self.update_pose_matrix(pose_matrixs_dict)
    
    def standard_output(self) -> list:
        return self.retrieve_joint_control_variables()
    
    def retrieve_render_list(self,
                             render_object_type:RenderObjectTypes) -> list:
        render_list = []
        match render_object_type:
            case RenderObjectTypes.LINE:
                start_point = (0, 0, 0)
                for _, part in self.parts.iterrows():
                    x_end_point = part["pose_matrix"][0,3]
                    y_end_point = part["pose_matrix"][1,3]
                    z_end_point = part["pose_matrix"][2,3]
                    end_point = (x_end_point, y_end_point, z_end_point)
                    if part["entity"].visibility:
                        render_list.append([start_point, end_point])
                    start_point = end_point
            case _:
                pass
                    
        return render_list
    
    def construct(self, 
                  part):
        """Assemble a robotic arm model using Joint and Link.
    
        Args:
            part (np.typing.NDArray): A part entity.
    
        Returns:
            Configuration: Returns the current instance for chained calls.
        """
        name = part.name
        existed_name_list = self.retrieve_part_indexs()
        if name in existed_name_list:
            raise Exception("Name conflict...")
        new_row = {"index": name, "entity": part, "pose_matrix": None}
        DataFrameUtils.append(self.parts, new_row)
        return self
        
    def bind_reference_frame(self) -> None:
        """Automatically create coordinate systems that comply with standard D-H analysis based on configuration and bind them.
    
        Args:
    
        Returns:
            None.
        """
        
        reference_frame_idx = 0
        reference_frame_name:str = f"_rf-{reference_frame_idx}"
        reference_frame = ReferenceFrame(reference_frame_name)
        new_row = {"index": reference_frame_name, "entity": reference_frame}
        DataFrameUtils.append(self.reference_frames, new_row)
        for idx, part in self.parts.iterrows():
            match part["entity"].type:
                case PartTypes.LINK:
                    self.parts.at[idx, "bound_reference_frame_index"] = reference_frame_name
                case PartTypes.ROTATIONAL_JOINT:
                    reference_frame_idx += 1
                    reference_frame_name = f"_rf-{reference_frame_idx}"
                    self.parts.at[idx, "bound_reference_frame_index"] = reference_frame_name
                    new_row = {"index": reference_frame_name, "entity": reference_frame, "pose_matrix": None}
                    DataFrameUtils.append(self.reference_frames, new_row)
                    
    def confirm_construct(self) -> None:
        """Actions after configuration construct completed.
    
        Args:
    
        Returns:
            None.
        """
        self.bind_reference_frame()
        initial_control_variable = self.retrieve_joint_control_variables()
        self.standard_input(initial_control_variable)
        
    def enable_inverse_kinematic(self,
                                 names: list) -> None:
        """Specify reference systems or components to participate in inverse kinematics analysis. This function is recommended to be called after the entire robotic arm has been constructed (using Configuration.confirm_construct()).
    
        Args:
            names (np.typing.NDArray): The names of the reference system or component that needs to participate in the inverse kinematics analysis.
    
        Returns:
            None.
        """
        
        part_names = self.retrieve_part_indexs()
        reference_frame_names = self.retrieve_reference_frame_indexs()
        for name in names:
            if name not in part_names + reference_frame_names:
                raise Exception(f"Fail to locate a joint or reference frame named {name}")
            self.inverse_kinematic_analysis_basis.append(name)
    
    def retrieve_part_indexs(self) -> list:
        index_list = self.parts["index"].tolist()
        return index_list
    
    def retrieve_reference_frame_indexs(self) -> list:
        index_list = self.reference_frames["index"].tolist()
        return index_list
    
    def retrieve_joint_control_variables(self) -> list:
        control_variable_list = []
        for _, part in self.parts.iterrows():
            if part["entity"].type in [PartTypes.ROTATIONAL_JOINT]:
                control_variable_list.append(part["entity"].control_variable)
        return control_variable_list
    
    def retrive_control_variables_num(self) -> int:
        control_variables_num = 0
        for _, part in self.parts.iterrows():
            if part["entity"].type in [PartTypes.ROTATIONAL_JOINT]:
                control_variables_num += 1
        return control_variables_num
    
    def retrive_control_variables(self) -> list:
        control_variables_list = []
        for _, part in self.parts.iterrows():
            if part["entity"].type in [PartTypes.ROTATIONAL_JOINT]:
                control_variables_list.append(part["entity"].control_variable)
        return control_variables_list
    
    def update_pose_matrix(self,
                           pose_matrixs:dict) -> None:
        part_names = self.retrieve_part_indexs()
        reference_frame_names = self.retrieve_reference_frame_indexs()
        for name, pose_matrix in pose_matrixs.items():
            if name in part_names:
                mask = self.parts["index"] == name
                if mask.sum() == 1:
                    idx = self.parts[mask].index[0]
                    self.parts.at[idx, "pose_matrix"] = pose_matrix
            if name in reference_frame_names:
                mask = self.reference_frames["index"] == name
                if mask.sum() == 1:
                    idx = self.reference_frames[mask].index[0]
                    self.reference_frames.at[idx, "pose_matrix"] = pose_matrix
    
    def update_control_variable(self,
                                 control_variables:list) -> None:
        control_variables_enum = enumerate(control_variables)
        for _, part in self.parts.iterrows():
            match part["entity"].type:
                case PartTypes.ROTATIONAL_JOINT:
                    _, control_variable = next(control_variables_enum)
                    part["entity"].control_variable = control_variable