import cv2
import numpy as np
import matplotlib.pyplot as plt

# --- Load camera parameters ---
# Assuming you saved MATLAB cameraParams as a .npz or similar Python-readable format.
# Here, I create a dummy example. Replace with your actual camera parameters loading.

# Replace above with your actual values

# Example (replace these with your actual cameraParams.mat data)
fx, fy = 1000, 1000   # Example focal lengths in pixels
cx, cy = 640, 360     # Example principal point (image center for 1280x720)
dist_coeffs = np.zeros(5)  # Assuming zero distortion for simplicity

ball_diameter = 5.0  # cm
camera_params = {
    'FocalLength': np.array([fx, fy]),        # pixels
    'PrincipalPoint': np.array([cx, cy]),     # pixels
    'DistortionCoefficients': np.array([k1, k2, p1, p2, k3])  # example
}
# Load image
img_path = 'reousrces/stereo_calibration/ball/left/1753961707.9742987-left.bmp'
frame = cv2.imread(img_path)

# Resize frame if needed - must match camera parameters image size
# frame = cv2.resize(frame, (cameraParams.ImageSize(2), cameraParams.ImageSize(1))) # width, height

# Undistort image
h, w = frame.shape[:2]
camera_matrix = np.array([[fx, 0, cx],
                          [0, fy, cy],
                          [0,  0,  1]])
frame_undist = cv2.undistort(frame, camera_matrix, dist_coeffs)

# Convert to HSV
hsv = cv2.cvtColor(frame_undist, cv2.COLOR_BGR2HSV)

# Define HSV thresholds for blue color segmentation (adjust if needed)
# MATLAB: h in [0.55, 0.62], s > 0.6, v > 0.4
# OpenCV Hue range is 0-179 (half of MATLAB's 0-1), scale accordingly:
lower_h = int(0.55 * 179)
upper_h = int(0.62 * 179)
lower_s = int(0.6 * 255)
lower_v = int(0.4 * 255)

lower_blue = np.array([lower_h, lower_s, lower_v])
upper_blue = np.array([upper_h, 255, 255])

mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Morphological closing and filling holes
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (11, 11))
mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
mask_filled = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)

# Remove small objects (contours with area < 200 pixels)
contours, _ = cv2.findContours(mask_filled, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 200]

if filtered_contours:
    # Find largest contour by major axis length approximation
    def major_axis_length(cnt):
        if len(cnt) >= 5:
            ellipse = cv2.fitEllipse(cnt)
            (center, axes, angle) = ellipse
            return max(axes)
        else:
            return 0

    largest_contour = max(filtered_contours, key=major_axis_length)

    if len(largest_contour) >= 5:
        ellipse = cv2.fitEllipse(largest_contour)
        (center, axes, angle) = ellipse
        c_x, c_y = center
        major_axis_length = axes[1]  # axes returns (major, minor) but in OpenCV sometimes reversed, verify
        minor_axis_length = axes[0]

        # Use major axis length as ball size in pixels
        ball_size_pixels = max(major_axis_length, minor_axis_length)

        # Estimate depth Z (cm)
        Z = (ball_diameter * fx) / ball_size_pixels

        # Convert pixel to camera coordinates
        X = ((c_x - cx) * Z) / fx
        Y = -((c_y - cy) * Z) / fy  # invert Y axis to match MATLAB

        # Visualization
        frame_vis = frame_undist.copy()
        center_int = (int(c_x), int(c_y))
        radius_pix = int(ball_size_pixels / 2)
        cv2.circle(frame_vis, center_int, radius_pix, (0, 0, 255), 2)  # red circle
        cv2.drawMarker(frame_vis, center_int, (0, 255, 0), markerType=cv2.MARKER_CROSS, 
                       markerSize=20, thickness=2)  # green cross at center

        # Show with matplotlib (convert BGR to RGB)
        plt.imshow(cv2.cvtColor(frame_vis, cv2.COLOR_BGR2RGB))
        plt.title(f"Object at X={X:.2f} cm, Y={Y:.2f} cm, Z={Z:.2f} cm")
        plt.axis('off')
        plt.show()

        print(f"Pixel Centroid: ({c_x:.1f}, {c_y:.1f})")
        print(f"Ball size (pixels): {ball_size_pixels:.1f}")
        print(f"Estimated Position: X={X:.2f} cm, Y={Y:.2f} cm, Z={Z:.2f} cm")
    else:
        print("Contour too small for ellipse fitting")
else:
    print("Object not found")