import cv2
import pool_util
from poolcam_reader import PoolcamReader

URL = 'http://10.0.16.2:8081/frame.mjpg'

def main():
  stream = PoolcamReader(URL)
  background = pool_util.get_background(stream)
  x, y, w, h = pool_util.find_play_area(background)

  for img in PoolcamReader(URL):
    # Highlight play area
    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Select balls
    boundaries = {
        'cue': ([128, 128, 128], [255, 255, 255]),
    }

    cue = pool_util.mask_colors(img, boundaries)['cue']
    cue_coords = pool_util.find_ball(cue)
    cue_coords
    if cue_coords is not None:
      c_x, c_y, c_r = cue_coords
      cv2.circle(img, (c_x, c_y), c_r, (0, 0, 255), 2)
      cv2.circle(img, (c_x, c_y), 3, (255, 0, 0), 2)
    cv2.imshow('poolcam', img[y:y + h, x:x + w])
    #cv2.imshow('poolcam', cue[y:y + h, x:x + w])
    cv2.waitKey(10)

if __name__ == '__main__':
  main()
