#!/bin/bash

# chrontab entry
# 30 15 * * *   cd /home/pi/golden-hour-private; bash ./run.sh >> error.log 2>&1


set -e;
set -x;

GOLDEN_HOUR_DIR="$(dirname "$(realpath $0)")"
GOLDEN_HOUR_PATH="$GOLDEN_HOUR_DIR/golden_hour/main.py"

PATH="$PATH:/usr/local/bin"

date

# 7200 seconds with a frame every 8 seconds, starting 60 minutes before sunset
python3 $GOLDEN_HOUR_PATH \
	--start-before-sunset 20 \
	--duration 4800 \
	--interval 6 \
	--post-to-twitter \
	--air-quality-sensor

git add output
git commit -m "Add sunset timelapse for $(date +'%m/%d/%Y')"
git push

