import cv2
import numpy as np
import scipy.io

class DualCamera():
    def __init__(self,) -> None:
        self.LOWER_BOUND_BLUE = np.array([100, 150, 50])
        self.UPPER_BOUND_BLUE = np.array([140, 255, 255])
        essential_parameters = scipy.io.loadmat("resources/essential_parameters.mat")
        self.intrinsic_matrix_left = essential_parameters["intrinsic_matrix_left"]
        self.intrinsic_matrix_right = essential_parameters["intrinsic_matrix_right"]
        self.distortion_left = essential_parameters["distortion_left"]
        self.distortion_right = essential_parameters["distortion_right"]
        self.rotation_matrix = essential_parameters["rotation_matrix"]
        self.translation = essential_parameters["translation"][0]
        self.image_size = essential_parameters["image_size"][0][::-1]
        self.R1, self.R2, self.P1, self.P2, self.Q, _, _ = cv2.stereoRectify(self.intrinsic_matrix_left, 
                                                                             self.distortion_left, 
                                                                             self.intrinsic_matrix_right, 
                                                                             self.distortion_right, 
                                                                             self.image_size, 
                                                                             self.rotation_matrix, 
                                                                             self.translation)
        self.map_x_left, self.map_y_left = cv2.initUndistortRectifyMap(self.intrinsic_matrix_left, 
                                                                       self.distortion_left, 
                                                                       self.R1, 
                                                                       self.P1, 
                                                                       self.image_size, 
                                                                       cv2.CV_32FC1)
        self.map_x_right, self.map_y_right = cv2.initUndistortRectifyMap(self.intrinsic_matrix_right, 
                                                                         self.distortion_right, 
                                                                         self.R2, 
                                                                         self.P2, 
                                                                         self.image_size, 
                                                                         cv2.CV_32FC1)
    
    def calculate_3d_coordinate(self, 
                                image_left:str, 
                                image_right:str) -> tuple:
        block_size = 3
        image_channel_num = 3
        stereo = cv2.StereoSGBM_create(minDisparity=1,
                                       numDisparities=64,
                                       blockSize = block_size,
                                       P1=8 * image_channel_num * block_size * block_size,
                                       P2=32 * image_channel_num * block_size * block_size,
                                       disp12MaxDiff=-1,
                                       preFilterCap=1,
                                       uniquenessRatio=10,
                                       speckleWindowSize=100,
                                       speckleRange=32,
                                       mode=cv2.STEREO_SGBM_MODE_SGBM_3WAY)
        image_left_rectified = cv2.remap(image_left, self.map_x_left, self.map_y_left, cv2.INTER_LINEAR)
        image_right_rectified = cv2.remap(image_right, self.map_x_right, self.map_y_right, cv2.INTER_LINEAR)
        disparity = stereo.compute(image_left_rectified, image_right_rectified)
        cv2.imshow("", image_left_rectified)
        cv2.waitKey(0)
        center_left = self.calculate_center(image_left_rectified, self.LOWER_BOUND_BLUE, self.UPPER_BOUND_BLUE)
        center_right = self.calculate_center(image_right_rectified, self.LOWER_BOUND_BLUE, self.UPPER_BOUND_BLUE)

        disparity_map = np.array([[disparity]], dtype=np.float32)
        points_3D = cv2.reprojectImageTo3D(disparity_map, self.Q)
        x, y, z = points_3D[0, 0]
        
        
        return x, y, z
        
    @staticmethod
    def calculate_mask(image:np.typing.NDArray, 
                       lower_bound:np.typing.NDArray,
                       upper_bound:np.typing.NDArray) -> np.typing.NDArray:
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower_bound, upper_bound)
        return mask
    
    @staticmethod
    def calculate_center(image:np.typing.NDArray, 
                         lower_bound:np.typing.NDArray,
                         upper_bound:np.typing.NDArray) -> tuple|None:
        mask = DualCamera.calculate_mask(image, 
                                         lower_bound, 
                                         upper_bound)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            main_contour = max(contours, key=cv2.contourArea)
            M = cv2.moments(main_contour)
            if M['m00'] != 0:
                x = int(M['m10'] / M['m00'])
                y = int(M['m01'] / M['m00'])
                return (x, y)
        return None