import cv2
import numpy as np
from cv_util import CVUtil
from poolcam_reader import PoolcamReader

URL = 'http://10.0.16.2:8081/frame.mjpg'

def find_play_area(imgs):
  rects = zip(*map(CVUtil.find_biggest_rect, imgs)) # ([x, x, x], [y, y, y], ...)
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
