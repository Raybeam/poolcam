import cv2
import numpy as np
"""Contains utility methods for various CV behavior."""

class CVUtil(object):

  @staticmethod
  def find_biggest_rect(img,
      color_lower=np.array([50,50,50]),
      color_upper=np.array([200,255,255])):
    """Finds the largest rectangle in the image with the specified color hints."""
    # Shave off non-color parts of image.
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, color_lower, color_upper)
    color = cv2.bitwise_and(img, img, mask=mask)

    # Convert to grayscale for threshold function.
    thresh = cv2.threshold(color[:,:,2], 0, 255, cv2.THRESH_BINARY)[1]

    # Get the bounding rect of the largest contour (the table).
    contours = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[1]
    return cv2.boundingRect(max(contours, key=cv2.contourArea))
