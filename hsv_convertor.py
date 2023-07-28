import numpy as np
import cv2 as cv

def get_range_hsv(rgb_color_array):
    """
    Return the range of color in HSV space

    Args:
        rgb_color_array (numpy): Numpy array that describe the input color (RGB)
    
    Output:
        The function returns the range of the input color in HSV color space.
        low  : The lowest value where the RGB color starts in HSV.
        high : The highest value where the RGB color ends in HSV.

    """
    rgb_color_array = np.uint8([[rgb_color_array]])
    # Convert the RGB color to HSV
    hsv_color_array = cv.cvtColor(rgb_color_array,cv.COLOR_BGR2HSV)
    low = hsv_color_array[0][0][0] - 10, 100, 100
    high = hsv_color_array[0][0][0] + 10, 255, 255
    
    
    return np.array(low, dtype=np.uint8), np.array(high, dtype=np.uint8)

