import cv2
import numpy as np
from webcolors import hex_to_name

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera. Change it if you have multiple cameras.

# Define a list of colors in hex format
colors = ['#FF0000', '#00FF00', '#0000FF']  # Red, Green, Blue

# Define variables to keep track of progress
total_mosaic_pixels = 0
colored_pixels = 0

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply a mosaic effect
    mosaic = cv2.resize(gray, None, fx=0.1, fy=0.1, interpolation=cv2.INTER_NEAREST)
    mosaic = cv2.resize(mosaic, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)

    # Threshold to create a binary mask of mosaic areas
    _, binary_mask = cv2.threshold(mosaic, 150, 255, cv2.THRESH_BINARY)

    # Invert the binary mask
    inverted_mask = cv2.bitwise_not(binary_mask)

    # Use the inverted mask to mask out the mosaic areas in the original frame
    result = cv2.bitwise_and(frame, frame, mask=inverted_mask)

    # Calculate the percentage of completion
    total_mosaic_pixels = np.sum(binary_mask > 0)
    if total_mosaic_pixels != 0:
        colored_pixels = np.sum(inverted_mask > 0)
        completion_percentage = (colored_pixels / total_mosaic_pixels) * 100
    else:
        completion_percentage = 100  # No mosaic pixels, assume it's fully colored

    # Get the color being used
    color_index = int(completion_percentage / 33.33)  # 3 colors, so each covers roughly 33.33%

    # Get the color name
    color_name = hex_to_name(colors[color_index])

    # Draw progress information on the frame
    progress_info = f'Progress: {completion_percentage:.2f}%'
    cv2.putText(result, progress_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    cv2.putText(result, f'Color: {color_name}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show the result
    cv2.imshow('Mosaic Detection', result)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
