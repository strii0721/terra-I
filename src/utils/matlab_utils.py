from scipy.io import loadmat

class MatlabUtils():
    @staticmethod
    def read_mat(mat_file_path:str,
                 property_name:str = "data") -> object:
        data = loadmat(mat_file_path)[property_name][0][0]
        return data