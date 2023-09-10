import cv2
import numpy as np
import util

webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
webcam.set(3, 640)
webcam.set(4, 480)


def noop(f):
    pass


trackbar_window = "Color Picker"
trackbar_hue_min = "Hue min"
trackbar_hue_max = "Hue max"
trackbar_saturation_min = "Sat min"
trackbar_saturation_max = "Sat max"
trackbar_value_min = "Value min"
trackbar_value_max = "Value max"

cv2.namedWindow(trackbar_window)
cv2.resizeWindow(trackbar_window, 800, 600)

cv2.createTrackbar(trackbar_hue_min, trackbar_window, 0, 179, noop)
cv2.createTrackbar(trackbar_hue_max, trackbar_window, 179, 179, noop)
cv2.createTrackbar(trackbar_saturation_min, trackbar_window, 0, 255, noop)
cv2.createTrackbar(trackbar_saturation_max, trackbar_window, 255, 255, noop)
cv2.createTrackbar(trackbar_value_min, trackbar_window, 0, 255, noop)
cv2.createTrackbar(trackbar_value_max, trackbar_window, 255, 255, noop)


# You can manually find a color if you drag the 6 values up or down
# An example of setting for orange like colors:
# Hue min 5 Hue max 19 Sat min 107 Sat max 255 Value min 0 Value max 255
while not util.is_exit_key_pressed():
    _, img = webcam.read()
    hsv_image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hue_min = cv2.getTrackbarPos(trackbar_hue_min, trackbar_window)
    hue_max = cv2.getTrackbarPos(trackbar_hue_max, trackbar_window)
    sat_min = cv2.getTrackbarPos(trackbar_saturation_min, trackbar_window)
    sat_max = cv2.getTrackbarPos(trackbar_saturation_max, trackbar_window)
    value_min = cv2.getTrackbarPos(trackbar_value_min, trackbar_window)
    value_max = cv2.getTrackbarPos(trackbar_value_max, trackbar_window)
    print(trackbar_hue_min, hue_min, trackbar_hue_max, hue_max, trackbar_saturation_min, sat_min,
          trackbar_saturation_max, sat_max, trackbar_value_min, value_min, trackbar_value_max, value_max)

    lower_bound = np.array([hue_min, sat_min, value_min])
    upper_bound = np.array([hue_max, sat_max, value_max])
    mask = cv2.inRange(hsv_image, lower_bound, upper_bound)
    result = cv2.bitwise_and(img, img, mask=mask)

    mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    cv2.imshow('original, masked, result', np.hstack([img, mask, result]))

webcam.release()
cv2.destroyAllWindows()