import cv2
import numpy as np
from dk.logger.log4p import Log4P
from cv.dual_camera import DualCamera
import scipy.io

logger = Log4P()
dual_camera = DualCamera()
image_left_path = "resources/stereo_calibration/stereo_ball/1753875535.3370924-left.bmp"
image_right_path = "resources/stereo_calibration/stereo_ball/1753875535.3370924-right.bmp"
image_left = cv2.imread(image_left_path)
image_right = cv2.imread(image_right_path)

image_marked_left = image_left
image_marked_right = image_right
center_left = DualCamera.calculate_center(image = image_left, 
                                          lower_bound = dual_camera.LOWER_BOUND_BLUE, 
                                          upper_bound = dual_camera.UPPER_BOUND_BLUE)
center_right = DualCamera.calculate_center(image = image_right, 
                                           lower_bound = dual_camera.LOWER_BOUND_BLUE, 
                                           upper_bound = dual_camera.UPPER_BOUND_BLUE)
mask_left = DualCamera.calculate_mask(image = image_left, 
                                      lower_bound = dual_camera.LOWER_BOUND_BLUE, 
                                      upper_bound = dual_camera.UPPER_BOUND_BLUE)
mask_right = DualCamera.calculate_mask(image = image_right, 
                                       lower_bound = dual_camera.LOWER_BOUND_BLUE, 
                                       upper_bound = dual_camera.UPPER_BOUND_BLUE)
gray_left = cv2.cvtColor(image_left, cv2.COLOR_BGR2GRAY)
gray_right = cv2.cvtColor(image_right, cv2.COLOR_BGR2GRAY)
cv2.circle(image_marked_left, 
           center_left, 
           radius = 5, 
           color = (0, 0, 255), 
           thickness = -1)
cv2.circle(image_marked_right, 
           center_right, 
           radius = 5, 
           color = (0, 0, 255), 
           thickness = -1)
cv2.imshow("Left", image_marked_left)
cv2.imshow("Right", image_marked_right)
# cv2.imshow("Left Mask", mask_left)
# cv2.imshow("Right Mask", mask_right)
# cv2.imshow("Left Grey", gray_left)
# cv2.imshow("Right Grey", gray_right)

x, y, z = dual_camera.calculate_3d_coordinate(image_left, 
                                              image_right)
logger.info(f"x = {x}")
logger.info(f"y = {y}")
logger.info(f"z = {z}")

cv2.waitKey(0)