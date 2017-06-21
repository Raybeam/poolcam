import cv2
from urllib.request import urlopen
import numpy as np

class PoolcamReader(object):
  def __init__(self, url):
    self.url = url
    self.cap = cv2.VideoCapture(url)

  def __iter__(self):
    return self

  def __next__(self):
    status, frame = self.cap.read()
    if not status:
      print("Status was {}".format(status))
      raise StopIteration()
    return frame

