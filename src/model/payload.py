#
# Author:       strii0721
# Email:        strii0721@outlook.com
# Created on:   Fri Jul 11 2025
#
# Copyright (c) 2025 S.I.C.
#

class Payload:
    
    def get_render_list(self) -> list:
        x1 = 0
        y1 = -(38.1+5)
        z1 = -(26.05-2)
        x2 = 360
        y2 = 220.3-(38.1+5)
        z2 = (2+23.95)
        faces_list = [
            [(x1, y1, z1), (x1, y2, z1), (x2, y2, z1), (x2, y1, z1)],
            [(x1, y1, z1), (x1, y1, z2), (x1, y2, z2), (x1, y2, z1)],
            [(x1, y1, z1), (x1, y1, z2), (x2, y1 ,z2), (x2, y1, z1)],
            [(x2, y1, z1), (x2, y1, z2), (x2, y2, z2), (x2, y2, z1)],
            [(x2, y2, z1), (x2, y2, z2), (x1, y2, z2), (x1, y2, z1)]
        ]
        return faces_list