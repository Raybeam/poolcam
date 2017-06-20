from poolcam_reader import PoolcamReader
import cv2
import numpy as np

URL = 'http://10.0.1.102:8081/frame.mjpg'
blue_lower = np.array([50,50,50])
blue_upper = np.array([200,255,255])

for img in PoolcamReader(URL):
  # Shave off non-blue parts of image.
  hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
  mask = cv2.inRange(hsv, blue_lower, blue_upper)
  blue = cv2.bitwise_and(img, img, mask=mask)

  # Convert to grayscale for threshold function.
  thresh = cv2.threshold(blue[:,:,2], 0, 255, cv2.THRESH_BINARY)[1]

  # Get the bounding rect.
  contours = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
  cnt = contours[0]
  x, y, w, h = cv2.boundingRect(cnt)
  cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
  cv2.imshow('threshold', img)
  cv2.waitKey()