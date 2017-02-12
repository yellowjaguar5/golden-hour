#!/usr/bin/env python

import argparse

from goldenhour import sunset, timelapse, twitter

def calculate_timelapse_duration(duration, interval, photo_display_rate=30.0):
    # return number of seconds
    return float(duration) / interval / photo_display_rate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--duration',
        metavar='seconds',
        type=int,
        default=7200, # 2 hours
        help='duration of timelapse capture',
    )
    # TODO might want to enforce minimum to 2 to avoid pushing raspicam too hard
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

    print(args)

    # TODO date-based filename
    # TODO check if timelapse file already exists
    timelapse_filename = 'timelapse.mp4'

    if args.post_to_twitter:
        # TODO pre-check twitter auth (will also ensure we have an internet connection)
        # check the expected length of the video to make sure it's within twitter's rules
        video_duration = calculate_timelapse_duration(args.duration, args.interval)
        print('estimated video length: {} seconds'.format(video_duration))
        if video_duration < 5.0:
            print('Error: Timelapse video will be too short to upload to Twitter (min 5 seconds)')
            exit()
        if video_duration > 30.0:
            print('Error: Timelapse video will be too long to upload to Twitter (max 30 seconds)')
            exit()

    if args.start_before_sunset is not None:
        sunset.wait_for_sunset(args.start_before_sunset)

    timelapse.create_timelapse(args.duration, args.interval, timelapse_filename)

    if args.post_to_twitter:
        twitter.post_update('testing', media=timelapse_filename)

    print('done!')


if __name__ == '__main__':
    main()
