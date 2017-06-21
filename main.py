from poolcam_reader import PoolcamReader
import cv2
import numpy as np

URL = 'http://10.0.1.102:8081/frame.mjpg'
blue_lower = np.array([50,50,50])
blue_upper = np.array([200,255,255])

def find_biggest_rect(img):
  """Gets a rectangle bounding the play area of the pool table."""
  # Shave off non-blue parts of image.
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, blue_lower, blue_upper)
  blue = cv2.bitwise_and(img, img, mask=mask)

  # Convert to grayscale for threshold function.
  thresh = cv2.threshold(blue[:,:,2], 0, 255, cv2.THRESH_BINARY)[1]

  # Get the bounding rect of the largest contour (the table).
  contours = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)[1]
  return cv2.boundingRect(max(contours, key=cv2.contourArea))

def find_play_area(imgs):
  rects = zip(*map(find_biggest_rect, imgs)) # ([x, x, x], [y, y, y], ...)
  means = map(np.mean, rects)
  return tuple(map(int, means))

stream = PoolcamReader(URL)

# Gather a background reading to determine the play area.
background = []
for img in stream:
  background.append(img)
  cv2.imshow('poolcam', img)
  cv2.waitKey(10)
  if len(background) > 10:
    break
x, y, w, h = find_play_area(background)

for img in PoolcamReader(URL):
  cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
  cv2.imshow('poolcam', img[y:y + h, x:x + w])
  cv2.waitKey(10)
