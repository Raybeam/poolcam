"""
`python main.py` to run this application.

--server to stream to a webserver (localhost:5000)
"""
import logging
import sys
import cv2
import pool_util
from poolcam_reader import PoolcamReader
from game_info import GameInfo

URL = 'http://10.0.16.2:8081/frame.mjpg'

def main():
  use_server = '--server' in sys.argv
  if use_server:
    run_flask()
  else:
    run_imshow()

def run_imshow():
  gi = GameInfo(URL)
  gi.calibrate()
  for img in gi.stream():
    cv2.imshow('poolcam', img)

def run_flask():
  from flask import Flask, request, Response
  app = Flask(__name__)

  def stream_jpgs(gi):
    for img in gi.stream():
       frame = cv2.imencode('.jpg', img)[1].tostring()
       yield (b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

  @app.route('/', methods=['GET'])
  def serve():
    gi = GameInfo(URL)
    gi.calibrate()
    return Response(stream_jpgs(gi), mimetype='multipart/x-mixed-replace; boundary=frame')

  app.run(host='0.0.0.0', debug=False)


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
