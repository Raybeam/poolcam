poolcam
-------
A client application for reading and processing images from the [pool server](10.0.16.2:8081).

# Setup
Install opencv 3.x (be sure to include FFMPEG support)

# Running
just `python main.py`

if you want to run a local mjpeg server to serve the rendered results, run:

`python main.py --server`

# Developing
All of what we know about a game is contained in `GameInfo`.  Update the docs as you add stuff

`pool_util.py` contains functions to help us do image processing.

`GameInfo` uses `pool_util` to turn an image into information.

It's a good policy to have GameInfo store the last known good information it has.
