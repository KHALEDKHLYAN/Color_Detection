import cv2
import os
import numpy as np

# Define the color range to track (in HSV)
lower_color = np.array([0, 100, 100])
upper_color = np.array([10, 255, 255])

# Initialize variables for percentage and border status
percentage_colored = 0
outside_borders = False

# Define your predefined borders (for example, a rectangular region)
border_x_min, border_x_max, border_y_min, border_y_max = 100, 300, 100, 400

# Define a function to calculate percentage of colored area
def calculate_percentage(mask):
    total_pixels = mask.size
    colored_pixels = np.count_nonzero(mask)
    return (colored_pixels / total_pixels) * 100

# Initialize video capture
cap = cv2.VideoCapture(0)  # 0 indicates the default camera

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert frame to HSV color space for color detection
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create a mask for the specified color range
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Calculate percentage of colored area
    percentage_colored = calculate_percentage(mask)

    # Check if any border pixels are colored
    border_area = mask[border_y_min:border_y_max, border_x_min:border_x_max]
    if np.count_nonzero(border_area) > 0:
        outside_borders = True
    else:
        outside_borders = False

    # Display feedback in the terminal
    feedback_text = f"Percentage Colored: {percentage_colored:.2f}% | Outside Borders: {outside_borders}"
    print(feedback_text)

    # Exit loop if 'q' is pressed
    if os.getenv('DISPLAY') is None:
        break


# Release video capture
cap.release()
cv2.destroyAllWindows()
