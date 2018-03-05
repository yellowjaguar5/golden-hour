# golden-hour

Currently only works with python 3 due to a bug in python-twitter (https://github.com/bear/python-twitter/issues/438)

## Installing Dependencies

`pip install -r requirements` (I recommend doing this in a virtualenv)

### Raspberry Pi

Requires ffmpeg with libx264: http://www.jeffreythompson.org/blog/2014/11/13/installing-ffmpeg-for-raspberry-pi/

Currently expects a CSI-port camera (and camera must be enabled in raspi-config)

### OS X/macOS

`brew install ffmpeg`

## TODO

- way of configuring which camera is used with osx/ffmpeg capture (always uses FaceTime camera currently)
- handle failed commands in capture/compile functions
- turn this into an installable python package with commands in setup.py's console_scripts
- documentation
    - prepping a new Raspberry Pi (ffmpeg, webcam enable, git installation, etc.)
    - creating cron job
    - authenticating twitter
    - commands
