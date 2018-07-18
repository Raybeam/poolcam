import cv2
import pool_util
import logging
from poolcam_reader import PoolcamReader

class GameInfo(object):
  """Contains info about the state of a pool game.

    Properties:
      URL: the URL of the game
      reader: the PoolcamReader we're fetching images from
      balls: A dictionary of last seen ball positions as {ballname: (x, y, r)}
      ball_radius: the min and max potential radius of a ball in pixels
      ball_colors: the min and max color range for a given ball
      background: the (x, y, w, h) of the playing field for normalization

    Methods:
      calibrate: Set up pre-game stuff, such as finding background and lighting
      step: Get information from a raw game image
      render: Marks up an image based on our current state.
      stream: call step, render, and cv2.imshow for as long as we have images.
  """
  ball_radius = (10, 20)
  ball_colors = {
      'cue': ([128, 128, 128], [255, 255, 255]),
  }

  def __init__(self, URL):
    self.URL = URL
    self.reader = PoolcamReader(URL)
    self.balls = {name: None for name in self.ball_colors}
    self.display_colors = {name: list(map(lambda c: sum(c)/2, zip(*r))) for name, r in self.ball_colors.items()}

  def calibrate(self):
    """Set up pre-game stuff, such as finding background and lighting."""
    self.background = pool_util.find_play_area(self.reader) # x, y, w, h

  def step(self, img):
    # Update ball positions
    for ball, color in self.ball_colors.items():
      pos = pool_util.find_ball(
          img,
          color,
          minRadius=self.ball_radius[0],
          maxRadius=self.ball_radius[1])
      if pos is not None and pos.any():
        logging.info('Position of {} is now {}'.format(ball, pos))
        self.balls[ball] = pos

    #cv2.imshow('poolcam', cue[y:y + h, x:x + w])
    cv2.waitKey(10)

  def stream(self):
    """call step and render for as long as we have images."""
    for img in self.reader:
      self.step(img)
      img = self.render(img)
      yield img

  def render(self, img):
    """Marks up an image based on our current state."""
    # Highlight play area
    x, y, w, h = self.background
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Render balls
    for ball, pos in self.balls.items():
      if pos is not None:
        self.render_ball(img, ball, pos)

    return img

  def render_ball(self, img, ball, pos):
    c_x, c_y, c_r = pos
    cv2.circle(img, (c_x, c_y), c_r, self.display_colors[ball], 2)
    cv2.circle(img, (c_x, c_y), 3, (0, 0, 255), 2)

    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 1
    fontColor = (255,255,255)
    lineType = 2

    cv2.putText(img, ball, (c_x, c_y), font, fontScale, fontColor, lineType)

    return img

