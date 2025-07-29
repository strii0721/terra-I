import cv2
import numpy as np
import csv
from datetime import datetime

# === CAMERA PARAMETERS (replace with your real calibration output) ===
fx = 1177.3
fy = 1176.9
cx = 740.0
cy = 585.6
camera_matrix = np.array([[fx, 0, cx],
                          [0, fy, cy],
                          [0,  0,  1]], dtype=np.float32)
dist_coeffs = np.array([-0.32, 0.11, 0, 0, 0], dtype=np.float32)

focal_length = fx  # assume fx and fy ~ equal

# === Load Test Image ===
image_path = "output/calibration/1753802979.5773597-calibration.bmp"
# image_path = "resources/coord_test_single/coord_test.jpg"
frame = cv2.imread(image_path)
image_size = (frame.shape[1], frame.shape[0])

# === Undistort the Image ===
frame_undistorted = cv2.undistort(frame, camera_matrix, dist_coeffs)

# === Convert to HSV and Detect Blue Objects ===
hsv = cv2.cvtColor(frame_undistorted, cv2.COLOR_BGR2HSV)
lower_blue = np.array([100, 100, 70])
upper_blue = np.array([130, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

# === Find Contours ===
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# === Setup CSV Logging ===
with open('object_coordinates_log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'ObjectType', 'X', 'Y', 'Z'])

    if contours:
        cnt = max(contours, key=cv2.contourArea)
        if len(cnt) >= 5:
            ellipse = cv2.fitEllipse(cnt)
            (x, y), (major_axis, minor_axis), _ = ellipse
            circularity = minor_axis / major_axis

            if circularity > 0.85:
                object_type = 'ball'
                object_size_cm = 5
            else:
                object_type = 'cube'
                object_size_cm = 3

            # === Calculate Distance ===
            Z = (object_size_cm * focal_length) / major_axis
            X = ((x - cx) * Z) / fx
            Y = ((y - cy) * Z) / fy

            # Convert to meters
            X_m, Y_m, Z_m = X / 100, Y / 100, Z / 100

            # Log and visualize
            print(f"[{object_type.upper()}] @ ({X_m:.2f}, {Y_m:.2f}, {Z_m:.2f}) meters")
            writer.writerow([datetime.now().strftime('%H:%M:%S'), object_type, X_m, Y_m, Z_m])

            # Draw results
            output = frame_undistorted.copy()
            cv2.ellipse(output, ellipse, (255, 0, 0), 2)
            cv2.circle(output, (int(x), int(y)), 5, (0, 0, 255), -1)
            cv2.putText(output, f'{object_type} ({X_m:.2f}, {Y_m:.2f}, {Z_m:.2f}) m',
                        (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.imshow('Object Tracker', output)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
        else:
            print("Not enough points to fit ellipse.")
    else:
        print("No object detected.")