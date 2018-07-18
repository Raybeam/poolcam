import logging
import sys
import cv2
import pool_util
from poolcam_reader import PoolcamReader
from game_info import GameInfo

URL = 'http://10.0.16.2:8081/frame.mjpg'

def main():
  gi = GameInfo(URL)
  gi.calibrate()
  gi.stream()

def enable_logging():
  root = logging.getLogger()
  root.setLevel(logging.INFO)

  ch = logging.StreamHandler(sys.stdout)
  ch.setLevel(logging.INFO)
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  ch.setFormatter(formatter)
  root.addHandler(ch)

if __name__ == '__main__':
  enable_logging()
  main()
