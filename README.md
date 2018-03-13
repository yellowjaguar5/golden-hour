# golden-hour

A python script to generate a timelapse video. Designed specifically to record at sunset, and post to twitter with a weather report.

## Installing Dependencies

`pip install -r requirements` (I recommend doing this in a virtualenv)

### Raspberry Pi

Requires ffmpeg with libx264: http://www.jeffreythompson.org/blog/2014/11/13/installing-ffmpeg-for-raspberry-pi/

Currently expects a CSI-port camera (and camera must be enabled in raspi-config)

### OS X/macOS

`brew install ffmpeg`
