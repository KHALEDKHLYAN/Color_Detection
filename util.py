import cv2
import numpy as np


def is_exit_key_pressed(delay=1):
    """
    Waits for 'q' to be pressed. The delay is 1 milliseconds by default but can be set.
    :param delay:
    :return:
    """
    return cv2.waitKey(delay) & 0XFF == ord('q')


def resize_image(image, percentage):
    """
    Returns a resized image. Not exactly precise, but good enough
    :param image:
    :param percentage: anything greater than 0
    :return:
    """
    if percentage <= 0:
        raise Exception("A percentage must be greater than  0")
    divisor = 100 / percentage
    dimension = int(image.shape[1] / divisor), int(image.shape[0] / divisor)
    return cv2.resize(image, dimension)


def stack_images(img_array, scale=1):
    """
    Stacks (and optionally scales) images and accepts varying color settings (unlike normal hstack or vstack).
    To create a grid, pass an array or arrays --> stack_images(([car, boat], [bike, skates]), 0.8)
    To create a single row, pass an array --> stack_images([car, boat, bike, skates], 0.8)
    :param scale: Optional scale setting, for instance 0.8 = 80%
    :param img_array:
    :return:
    """
    has_rows = isinstance(img_array[0], list)
    if has_rows:
        stack = _process_rows(img_array, scale)
    else:
        stack = _process_single_row(img_array, scale)
    return stack


def _process_single_row(img_array, scale):
    first_row = img_array[0]
    for x in range(0, len(img_array)):
        if img_array[x].shape[:2] == first_row.shape[:2]:
            img_array[x] = cv2.resize(img_array[x], (0, 0), None, scale, scale)
        else:
            img_array[x] = cv2.resize(img_array[x], (first_row.shape[1], first_row.shape[0]), None, scale, scale)
        if len(img_array[x].shape) == 2:
            img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
    return np.hstack(img_array)


def _process_rows(img_array, scale):
    first_row = img_array[0]
    columns = len(first_row)
    rows = len(img_array)
    for x in range(0, rows):
        for y in range(0, columns):
            if img_array[x][y].shape[:2] == first_row[0].shape[:2]:
                img_array[x][y] = cv2.resize(img_array[x][y], (0, 0), None, scale, scale)
            else:
                img_array[x][y] = cv2.resize(img_array[x][y], (first_row[0].shape[1], first_row[0].shape[0]),
                                             None, scale, scale)
            if len(img_array[x][y].shape) == 2:
                img_array[x][y] = cv2.cvtColor(img_array[x][y], cv2.COLOR_GRAY2BGR)
    width = first_row[0].shape[1]
    height = first_row[0].shape[0]
    blank_image = np.zeros((height, width, 3), np.uint8)
    hor = [blank_image] * rows
    for x in range(0, rows):
        hor[x] = np.hstack(img_array[x])
    return np.vstack(hor)