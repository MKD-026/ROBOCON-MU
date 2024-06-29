import cv2
import numpy as np

def get_dominant_color(roi):
    # Convert the ROI to HSV color space
    hsv_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)

    # Compute the histogram for the H channel (hue)
    hist = cv2.calcHist([hsv_roi], [0], None, [180], [0, 180])

    # Find the hue with the maximum count in the histogram
    dominant_hue = np.argmax(hist)

    # Define a range for the dominant hue to detect the corresponding color
    dominant_color = "Unknown"
    if 0 <= dominant_hue < 30 or 160 <= dominant_hue < 180:
        dominant_color = "Red"
    elif 60 <= dominant_hue < 150:
        dominant_color = "Blue"
    elif 150 <= dominant_hue < 160:
        dominant_color = "Purple"

    return dominant_color