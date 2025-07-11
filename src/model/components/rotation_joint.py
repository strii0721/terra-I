#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Thu Jul 10 2025
#
# Copyright (c) 2025 S.I.C.
#

from utils.three_dim_calculation import ThreeDimCalculation
import numpy as np
from model.components.compunent_types import ComponentTypes as CT

class RotationJoint:
    
    def __init__(self, 
                 axis_direction,
                 visibility = True
                 ):
        self.type:CT = CT.ROTATION_JOINT
        self.axis_direction:np.typing.NDArray = np.asarray(ThreeDimCalculation.convert_to_unit_vector(np.array(axis_direction)), dtype = np.float64)
        self.visibility:bool = visibility