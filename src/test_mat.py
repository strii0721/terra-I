import h5py
from scipy.io import loadmat

# with h5py.File('./resources/cameraParams.mat', 'r') as f:
#     print(list(f.keys()))  # 查看顶层变量名
#     data = f["FolcalLength"]
#     print(data)



data = loadmat('./resources/cameraParams.mat')

print(data.keys())  # 查看包含哪些变量
print(data['FolcalLength'])  # 访问名为 my_matrix 的变量