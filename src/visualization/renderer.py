#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Sat Jul 12 2025
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

import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

class Renderer:
    
    def __init__(self,
                 render_interval = 0.1) -> None:
        self.render_interval = render_interval
        self.lines = []
        self.faces = []
        
        self.fig = plt.figure()
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax = self.fig.add_subplot(111, projection='3d')
        
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
        self.ax.set_xticks([])  # 可选，先清空自动刻度
        self.ax.xaxis.set_major_locator(MultipleLocator(50))
        self.ax.yaxis.set_major_locator(MultipleLocator(50))
        self.ax.zaxis.set_major_locator(MultipleLocator(50))
        self.ax.set_xlabel('X')
        self.ax.set_ylabel('Y')
        self.ax.set_zlabel('Z')
        self.ax.grid(False)
        
        plt.draw()
        plt.pause(self.render_interval)
        
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