import cv2
import numpy as np
import csv
from datetime import datetime

# === CAMERA PARAMETERS ===
fx, fy = 1177.3, 1176.9
cx, cy = 740.0, 585.6
camera_matrix = np.array([[fx, 0, cx],
                          [0, fy, cy],
                          [0,  0,  1]], dtype=np.float32)
dist_coeffs = np.array([-0.32, 0.11, 0, 0, 0], dtype=np.float32)

# === Load Input Image ===
image_path = 'resources/coord_test_single/ball_1.jpg'
frame = cv2.imread(image_path)
if frame is None:
    raise FileNotFoundError(f"Image not found at {image_path}")

image_size = (frame.shape[1], frame.shape[0])

# === Compute New Camera Matrix for Undistortion ===
new_camera_matrix, _ = cv2.getOptimalNewCameraMatrix(camera_matrix, dist_coeffs, image_size, 1, image_size)
frame_undistorted = cv2.undistort(frame, camera_matrix, dist_coeffs, None, new_camera_matrix)

# === Extract new intrinsic parameters ===
fx_new = new_camera_matrix[0, 0]
fy_new = new_camera_matrix[1, 1]
cx_new = new_camera_matrix[0, 2]
cy_new = new_camera_matrix[1, 2]

# === Convert to HSV and Mask Blue ===
hsv = cv2.cvtColor(frame_undistorted, cv2.COLOR_BGR2HSV)
lower_blue = np.array([90, 50, 50])
upper_blue = np.array([140, 255, 255])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))

# === Find Contours ===
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# === Prepare CSV Logging ===
with open('ball_coordinates_log.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Time', 'ObjectType', 'X (m)', 'Y (m)', 'Z (m)'])

    ball_detected = False
    for cnt in contours:
        if len(cnt) < 5:
            continue

        ellipse = cv2.fitEllipse(cnt)
        (x, y), (major_axis, minor_axis), _ = ellipse

        # === Shape Analysis ===
        area = cv2.contourArea(cnt)
        perimeter = cv2.arcLength(cnt, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * (area / (perimeter ** 2))

        # === Only detect circular shapes (balls) ===
        if circularity < 0.85:
            continue  # Reject non-circular

        # === Object Identified as Ball ===
        object_type = 'ball'
        object_size_cm = 5  # known real-world diameter of ball

        # === Estimate Depth ===
        avg_axis = (major_axis + minor_axis) / 2
        Z_cm = (object_size_cm * fx_new) / avg_axis
        X_cm = ((x - cx_new) * Z_cm) / fx_new
        Y_cm = ((y - cy_new) * Z_cm) / fy_new

        # === Convert to meters ===
        X_m, Y_m, Z_m = X_cm / 100, Y_cm / 100, Z_cm / 100

        # === Logging ===
        print(f"[BALL] @ ({X_m:.2f}, {Y_m:.2f}, {Z_m:.2f}) meters")
        writer.writerow([datetime.now().strftime('%H:%M:%S'), object_type, X_m, Y_m, Z_m])

        # === Visualization ===
        output = frame_undistorted.copy()
        cv2.ellipse(output, ellipse, (255, 0, 0), 2)
        cv2.circle(output, (int(x), int(y)), 5, (0, 0, 255), -1)
        cv2.putText(output, f'{object_type} ({X_m:.2f}, {Y_m:.2f}, {Z_m:.2f}) m',
                    (int(x), int(y) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

        cv2.imshow('Ball Detection', output)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        ball_detected = True
        break  # Only detect the most prominent ball

    if not ball_detected:
        print("No ball detected.")