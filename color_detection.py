import cv2
import pandas as pd

# Declaring global variables (are used later on)
clicked = False
x_pos = y_pos = 0

# Reading csv file with pandas and giving names to each column
index = ["color", "color_name", "hex", "R", "G", "B"]
csv = pd.read_csv('colors.csv', names=index, header=None)

# Function to get x, y coordinates of mouse double click
def draw_function(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDBLCLK:
        global x_pos, y_pos, clicked
        clicked = True
        x_pos = x
        y_pos = y

# Initialize camera capture
cap = cv2.VideoCapture(0)  # 0 indicates the default camera (you can change it to a different camera if needed)

while True:
    ret, frame = cap.read()  # Read a frame from the camera
    if not ret:
        break

    cv2.imshow("Camera Feed", frame)

    cv2.setMouseCallback('Camera Feed', draw_function)

    if clicked:
        b, g, r = frame[y_pos, x_pos]
        b = int(b)
        g = int(g)
        r = int(r)
        clicked = False

        # Calculate the color name
        minimum = 10000
        color_name = "Undefined"  # Default value if no matching color is found
        for i in range(len(csv)):
            d = abs(r - int(csv.loc[i, "R"])) + abs(g - int(csv.loc[i, "G"])) + abs(b - int(csv.loc[i, "B"]))
            if d <= minimum:
                minimum = d
                color_name = csv.loc[i, "color_name"]

        print("Detected Color: ", color_name)  # Print the detected color name to the terminal

    # Break the loop when the user hits the 'esc' key
    if cv2.waitKey(20) & 0xFF == 27:
        break

# Release the camera and close all OpenCV windows
cap.release()
cv2.destroyAllWindows()
