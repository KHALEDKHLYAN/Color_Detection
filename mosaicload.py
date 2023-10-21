import cv2
import numpy as np
import webcolors
from webcolors import rgb_to_name

# Initialize the camera
cap = cv2.VideoCapture(0)  # Use 0 for the default camera. Change it if you have multiple cameras.

def get_color_name(rgb):
    closest_color = min(webcolors.CSS3_HEX_TO_NAMES, key=lambda name: sum((a - b) ** 2 for a, b in zip(webcolors.hex_to_rgb(name), rgb)))
    return webcolors.CSS3_HEX_TO_NAMES[closest_color]

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

    # Get the color being used
    colored_pixels = result[inverted_mask > 0]
    avg_color = np.mean(colored_pixels, axis=0)

    # Get the color name
    color_name = get_color_name(avg_color.astype(int))

    # Draw progress information on the frame
    progress_info = f'Color: {color_name}'
    cv2.putText(result, progress_info, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show the result
    cv2.imshow('Mosaic Detection', result)

    # Exit on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and destroy all windows
cap.release()
cv2.destroyAllWindows()
