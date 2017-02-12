#!/usr/bin/env python

import argparse
import datetime
import os
import random

from goldenhour import sunset, timelapse, twitter

def calculate_timelapse_duration(duration, interval, photo_display_rate=30.0):
    # return number of seconds
    return float(duration) / interval / photo_display_rate


def get_random_status_text():
    return random.choice([
        'wow.',
        'holy moly',
        'what a time to be alive',
        'inconceivable',
        'reverse sunrise',
    ])


def get_timelapse_filename(output_dir):
    filename_template = '{output_dir}/timelapse_{date}_{count:03d}.mp4'
    today_str = datetime.date.today().isoformat()
    count = 0
    while True:
        filename = filename_template.format(
            output_dir=output_dir,
            date=today_str,
            count=count,
        )
        if not os.path.exists(filename):
            return filename
        count += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration',
        metavar='seconds',
        type=int,
        default=7200, # 2 hours
        help='duration of timelapse capture',
    )
    # TODO might want to enforce minimum of 3 if using raspi cam
    parser.add_argument('--interval',
        metavar='seconds',
        type=int,
        default=8,
        help='time between captured photos',
    )
    parser.add_argument('--start-before-sunset',
        metavar='minutes',
        type=int,
        default=None,
        help='number of minutes before sunset to start timelapse',
    )
    parser.add_argument('--post-to-twitter',
        action='store_true',
        default=False,
        help='post video to twitter',
    )
    args = parser.parse_args()

    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)
    timelapse_filename = get_timelapse_filename(output_dir)

    if args.post_to_twitter:
        # TODO pre-check twitter auth (will also ensure we have an internet connection)
        # check the expected length of the video to make sure it's within twitter's rules
        video_duration = calculate_timelapse_duration(args.duration, args.interval)
        print('estimated video length: {} seconds'.format(video_duration))
        if video_duration < 5.0:
            print('Error: Timelapse video will be too short to upload to Twitter (min 5 seconds)')
            exit(1)
        if video_duration > 30.0:
            print('Error: Timelapse video will be too long to upload to Twitter (max 30 seconds)')
            exit(2)

    if args.start_before_sunset is not None:
        sunset.wait_for_sunset(args.start_before_sunset)

    timelapse.create_timelapse(args.duration, args.interval, timelapse_filename)

    if args.post_to_twitter:
        status_text = get_random_status_text()
        twitter.post_update(status_text, media=timelapse_filename)

    print('done!')


if __name__ == '__main__':
    main()
