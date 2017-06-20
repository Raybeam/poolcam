from poolcam_reader import PoolcamReader
import cv2

URL = 'http://10.0.1.102:8081/frame.mjpg'

for img in PoolcamReader(URL):
  print("Displaying image")
  cv2.imshow('Poolcam', img)
  cv2.waitKey()

