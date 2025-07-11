import matplotlib.pyplot as plt
import numpy as np

class Renderer:
    
    def __init__(self,) -> None:
        self.lines:list = []
    
    def render(self) -> None:
        
        x_min = y_min = z_min = 0
        x_max = y_max = z_max = 0
        
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')  
              
        for start_point, end_point in self.lines:
            x_min = min(x_min, start_point[0], end_point[0])
            y_min = min(y_min, start_point[1], end_point[1])
            z_min = min(z_min, start_point[2], end_point[2])
            x_max = max(x_max, start_point[0], end_point[0])
            y_max = max(y_max, start_point[1], end_point[1])
            z_max = max(z_max, start_point[2], end_point[2])
            xs, ys, zs = zip(start_point, end_point)
            ax.plot(xs, ys, zs)
            
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xticks(np.arange(x_min, x_max, 10))
        ax.set_yticks(np.arange(y_min, y_max, 10))
        ax.set_zticks(np.arange(z_min, z_max, 10)) 
        ax.set_box_aspect([x_max - x_min,
                           y_max - y_min,
                           z_max - z_min])
        plt.show()
        
    def add_lines(self,
                  lines_list:list) -> None:
        self.lines = self.lines + lines_list