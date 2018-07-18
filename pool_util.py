import cv2
import numpy as np
from cv_util import CVUtil

def get_background(stream):
  # Gather a background reading to determine the play area.
  background = []
  for img in stream:
    background.append(img)
    cv2.waitKey(10)
    if len(background) > 10:
      break
  return background

def find_play_area(imgs):
  rects = zip(*map(CVUtil.find_biggest_rect, imgs)) # ([x, x, x], [y, y, y], ...)
  means = map(np.mean, rects)
  return tuple(map(int, means))

ball_detector = cv2.SimpleBlobDetector_create()


def mask_colors(img, boundaries):
  result = {}
  for name, boundary in boundaries.items():
    lower = np.array(boundary[0], dtype="uint8")
    upper = np.array(boundary[1], dtype="uint8")

    mask = cv2.inRange(img, lower, upper)
    result[name] = cv2.bitwise_and(img, img, mask=mask)
  return result

def find_ball(masked_ball):
  """Finds count balls."""
  img = cv2.cvtColor(masked_ball, cv2.COLOR_BGR2GRAY)
  cv2.GaussianBlur(img, (9, 9), 2);
  candidates = cv2.HoughCircles(img, cv2.HOUGH_GRADIENT, 3, 10, minRadius=5, maxRadius=30)#, None, 10, 50, 5, 500)
  print(candidates)
  if candidates is None:
    return None
  return candidates[0][0]

