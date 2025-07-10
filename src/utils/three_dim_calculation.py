from math import sqrt
import numpy as np

class ThreeDimCalculation:
    
    def convert_to_unit_vector(vector):
        """Return a unit vector align with a given vector.
    
        Args:
            vector (np.array(list)): Given vector.
    
        Returns:
            np.array(list): A unit vector align with a given vector.
        """
        
        magnitude = sqrt(sum(v**2 for v in vector))
        unit_vector = vector / magnitude
        return unit_vector
    
    def extend(current_vector, 
               direction_vector, 
               extend_distance):
        """Extend the vector along the given starting point, direction, and length.
    
        Args:
            current_vector (np.array(list)):    A given vector.
            direction_vector (np.array(list)):  Direction of vector extension.
            extend_distance (np.array(list)):   Distance of vector extension.
    
        Returns:
            np.array(list): A vector pointing from the starting point to the end point.
        """
        extended_vector = current_vector + direction_vector * extend_distance
        return extended_vector
    
    def calculate_rotation_angle_rad(start_vector, 
                                     end_vector, 
                                     normal):
        """Calculate the angle between two spatial vectors, given the positive direction of the angle.
    
        Args:
            start_vector (np.array(list)):  Start vector.
            end_vector (np.array(list)):    End vector.
            normal (np.array(list)):        Positive direction of rotation.
    
        Returns:
            np.array(list): A vector pointing from the starting point to the end point.
        """
        if np.linalg.norm(start_vector) < 1e-8 or np.linalg.norm(end_vector) < 1e-8: 
            return 0.0
        else:
            start_vector = ThreeDimCalculation.convert_to_unit_vector(start_vector)
            end_vector = ThreeDimCalculation.convert_to_unit_vector(end_vector)
            cross_product = np.cross(start_vector, end_vector)
            dot_product = np.dot(start_vector, end_vector)
            if np.linalg.norm(normal) < 1e-8:
                normal = np.array([1, 0, 0])
            normal = ThreeDimCalculation.convert_to_unit_vector(normal)
            sign = np.sign(np.dot(cross_product, normal))
            angle_rad = np.arctan2(np.linalg.norm(cross_product) * sign, dot_product)
            return angle_rad