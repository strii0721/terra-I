from scipy.io import loadmat
import numpy as np

class MatlabUtils():
    @staticmethod
    def read_mat(mat_file_path:str,
                 property_name:str = "data") -> dict:
        mat_data = loadmat(mat_file_path)[property_name][0, 0]
        mat_dict = MatlabUtils.convert_to_dict(mat_data)
        return mat_dict
    
    @staticmethod
    def convert_to_dict(mat_data) -> dict:
        mat_dict = {}
        property_name_list = list(mat_data.dtype.names)
        for property_name in property_name_list:
            if mat_data[property_name].dtype.names is None:
                mat_dict[property_name] = mat_data[property_name]
            else:
                sub_mat_dict = MatlabUtils.convert_to_dict(mat_data[property_name])
                mat_dict[property_name] = sub_mat_dict
        return mat_dict