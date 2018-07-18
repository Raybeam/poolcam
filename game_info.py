import cv2
import pool_util
import logging
from poolcam_reader import PoolcamReader

class GameInfo(object):
  ball_colors = {
      'cue': ([128, 128, 128], [255, 255, 255]),
  }

  def __init__(self, URL):
    self.URL = URL
    self.reader = PoolcamReader(URL)
    self.balls = {name: None for name in self.ball_colors}

  def calibrate(self):
    background = pool_util.get_background(self.reader)
    self.background = pool_util.find_play_area(background) # x, y, w, h

  def step(self, img):
    # Update ball positions
    for ball, color in self.ball_colors.items():
      pos = pool_util.find_ball(img, color)
      if pos is not None and pos.any():
        logging.info('Position of {} is now {}'.format(ball, pos))
        self.balls[ball] = pos

    #cv2.imshow('poolcam', cue[y:y + h, x:x + w])
    cv2.waitKey(10)

  def stream(self):
    for img in self.reader:
      self.step(img)
      img = self.render(img)
      cv2.imshow('poolcam', img)

  def render(self, img):
    """Marks up an image based on our current state."""
    # Highlight play area
    x, y, w, h = self.background
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Render balls
    for ball, pos in self.balls.items():
      if pos is not None:
        c_x, c_y, c_r = pos
        cv2.circle(img, (c_x, c_y), c_r, (0, 0, 255), 2)
        cv2.circle(img, (c_x, c_y), 3, (255, 0, 0), 2)

    return img

