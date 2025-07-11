#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Fri Jul 11 2025
#
# Copyright (c) 2025 S.I.C.
#

import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Renderer:
    
    def __init__(self,) -> None:
        self.lines:list = []
        self.faces:list = []
        
        self.fig = plt.figure()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax = self.fig.add_subplot(111, projection='3d')
        # self.x_min, self.x_max = -560, 560
        # self.y_min, self.y_max = -300, 300
        # self.z_min, self.z_max = 0, 560
        
        plt.ion()
        

    def render(self) -> None:
        
        self.ax.clear()
        x_min = y_min = z_min = 0
        x_max = y_max = z_max = 0
             
        # render lines
        for start_point, end_point in self.lines:
            x_min, x_max =min(x_min, start_point[0], end_point[0]), max(x_max, start_point[0], end_point[0])
            y_min, y_max =min(y_min, start_point[1], end_point[1]), max(y_max, start_point[1], end_point[1])
            z_min, z_max =min(z_min, start_point[2], end_point[2]), max(z_max, start_point[2], end_point[2])
            xs, ys, zs = zip(start_point, end_point)
            self.ax.plot(xs, ys, zs)
        
        # render faces
        pc = Poly3DCollection(self.faces, facecolors='skyblue', linewidths=1, edgecolors='k', alpha=0.1)
        self.ax.add_collection3d(pc)
        
        # set figure
        self.ax.set_xlim(x_min, x_max)
        self.ax.set_ylim(y_min, y_max)
        self.ax.set_zlim(z_min, z_max)
        self.ax.set_box_aspect([x_max - x_min,
                                y_max - y_min,
                                z_max - z_min])
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.grid(False)
        
        plt.draw()
        plt.pause(0.1)
        
    def add_lines(self,
                  lines_list:list) -> None:
        self.lines = self.lines + lines_list
        
    def clean_lines(self) -> None:
        self.lines = []
    
    def add_faces(self,
                  faces_list:list) -> None:
        self.faces = self.faces + faces_list
    
    def clean_faces(self) -> None:
        self.faces = []