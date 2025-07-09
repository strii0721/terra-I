from math import pi
import numpy as np
import utils.kinematic_utils as kcal
import kinematics.dh_tables as dh_tables
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

if __name__ == "__main__":
    la_j1s = np.linspace(-pi/2, 0, 24)
    la_j2s = np.linspace(-pi, pi,  24)
    la_j3s = np.linspace(-pi, pi,  24)
    ra_j1s = np.linspace(0, pi/2,  24)
    ra_j2s = np.linspace(-pi, pi,  24)
    ra_j3s = np.linspace(-pi, pi,  24)
    
    workspace_left = []
    for la_j1 in la_j1s:
        for la_j2 in la_j2s:
            for la_j3 in la_j3s:
                angles = [la_j1, la_j2, la_j3]
                T_left = kcal.forward_kinematics(dh_tables.Config4V3.left(angles))
                xyz = T_left[:3, 3]
                workspace_left.append(xyz)
    workspace_left = np.array(workspace_left)
                
    workspace_right = []
    for ra_j1 in ra_j1s:
        for ra_j2 in ra_j2s:
            for ra_j3 in ra_j3s:
                angles = [ra_j1, ra_j2, ra_j3]
                T_right = kcal.forward_kinematics(dh_tables.Config4V3.right(angles))
                xyz = T_right[:3, 3]
                workspace_right.append(xyz)
    workspace_right = np.array(workspace_right)
                
    x1 = 0
    y1 = -(38.1+5)
    z1 = -(26.05-2)
    x2 = 360
    y2 = 220.3-(38.1+5)
    z2 = (2+23.95)
    framework = [
        [[x1, y1, z1], [x1, y2, z1], [x2, y2, z1], [x2, y1, z1]],
        [[x1, y1, z1], [x1, y1, z2], [x1, y2, z2], [x1, y2, z1]],
        [[x1, y1, z1], [x1, y1, z2], [x2, y1 ,z2], [x2, y1, z1]],
        [[x2, y1, z1], [x2, y1, z2], [x2, y2, z2], [x2, y2, z1]],
        [[x2, y2, z1], [x2, y2, z2], [x1, y2, z2], [x1, y2, z1]]
    ]
    
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111, projection='3d')
    pc = Poly3DCollection(framework, facecolors='skyblue', linewidths=1, edgecolors='k', alpha=0.7)
    ax.add_collection3d(pc)
    ax.scatter(workspace_left[:, 0], workspace_left[:, 1], workspace_left[:, 2], s=0.5, c="red")
    ax.scatter(workspace_right[:, 0], workspace_right[:, 1], workspace_right[:, 2], s=0.5, c="skyblue")
    ax.set_title('Workspace of the Arms (Config4 v4)')
    ax.set_xlabel('X (mm)')
    ax.set_ylabel('Y (mm)')
    ax.set_zlabel('Z (mm)')
    plt.tight_layout()
    plt.show()