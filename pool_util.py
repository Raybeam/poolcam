"""Does openCV detection stuff related to pool"""

import cv2
import numpy as np
from cv_util import CVUtil

def get_background(stream):
  """Gather a background reading to determine the play area."""
  background = []
  for img in stream:
    background.append(img)
    cv2.waitKey(10)
    if len(background) > 10:
      break
  return background

def find_play_area(stream):
  """Finds the current play area (edge of the felt)."""
  imgs = get_background(stream)
  rects = zip(*map(CVUtil.find_biggest_rect, imgs)) # ([x, x, x], [y, y, y], ...)
  means = map(np.mean, rects)
  return tuple(map(int, means))

def mask(img, boundary):
  """Masks an image based on a color boundary."""
  lower = np.array(boundary[0], dtype="uint8")
  upper = np.array(boundary[1], dtype="uint8")
  mask = cv2.inRange(img, lower, upper)
  return cv2.bitwise_and(img, img, mask=mask)

def find_ball(img, color_boundary, minRadius=5, maxRadius=20):
  """Finds a ball in img based on the color boundary."""
  img = mask(img, color_boundary)
  img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  img = cv2.GaussianBlur(img, (13, 13), 0);
  candidates = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 3, 10, minRadius=minRadius, maxRadius=maxRadius)
  if candidates is None:
    return None
  return candidates[0][0]
