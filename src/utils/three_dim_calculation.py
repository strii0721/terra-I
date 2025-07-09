from math import sqrt
import numpy as np

class ThreeDimCalculation:
    
    def convert_to_unit_vector(vector):
        magnitude = sqrt(sum(v**2 for v in vector))
        unit_vector = [v / magnitude for v in vector]
        return unit_vector
    
    def extend(current_vector, 
               direction_vector, 
               extend_distance):
        extended_vector = current_vector + direction_vector * extend_distance
        return extended_vector
    
    def calculate_rotation_angle_rad(start_vector,
                                 end_vector,
                                 normal):
        start_vector = ThreeDimCalculation.convert_to_unit_vector(start_vector)
        end_vector = ThreeDimCalculation.convert_to_unit_vector(end_vector)
        normal = ThreeDimCalculation.convert_to_unit_vector(normal)
        cross_product = np.cross(start_vector, end_vector)
        dot_product = np.dot(start_vector, end_vector)
        sign = np.sign(np.dot(cross_product, normal))
        angle_rad = np.arctan2(np.linalg.norm(cross_product) * sign, dot_product)
        return angle_rad