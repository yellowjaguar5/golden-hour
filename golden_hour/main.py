#!/usr/bin/env python

import argparse
from datetime import date
import logging
import logging.handlers
import sys
from os.path import isfile, expanduser, join, dirname, exists
from os import mkdir

from golden_hour import configuration, sunset, timelapse, tweet, darksky_weather, climacell_weather
from golden_hour.location import get_location

logger = logging.getLogger()


def calculate_timelapse_duration(duration, interval,
                                 photo_display_rate=30.0):
    """return number of seconds"""
    return float(duration) / interval / photo_display_rate


def get_timelapse_filename(output_dir):
    filename_template = '{output_dir}/timelapse_{date}_{count:03d}.mp4'
    today_str = date.today().isoformat()
    count = 0
    while True:
        filename = filename_template.format(
            output_dir=output_dir,
            date=today_str,
            count=count,
        )
        if not exists(filename):
            return filename
        count += 1


def main():
    if sys.stdout.isatty():
        handler = logging.StreamHandler(sys.stdout)
        logger.setLevel(logging.DEBUG)
    else:
        handler = logging.handlers.SysLogHandler(address='/dev/log')
        logger.setLevel(logging.INFO)
    logger.addHandler(handler)

    parser = argparse.ArgumentParser()
    parser.add_argument('--config-file',
                        default=expanduser(
                            '~/.config/golden-hour.yaml'),
                        help='configuration file where to find API keys '
                             'and location information. '
                             'Defaults to ~/.config/golden-hour.yaml'
                        )
    parser.add_argument('--duration',
                        metavar='seconds',
                        type=int,
                        default=7200,  # 2 hours
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
    parser.add_argument('--skip-timelapse',
                        action='store_true',
                        default=False,
                        help='skip recording the timelapse (useful for debugging)',
                        )
    parser.add_argument('--air-quality-sensor',
                        action='store_true',
                        default=False,
                        help='Get air quality data from connected Adafruit 4632 (PMSA003I) sensor',
                        )
    args = parser.parse_args()

    if isfile(args.config_file):  # try file supplied in args
        config = configuration.load_configuration(args.config_file)
    else:  # try default location
        config = configuration.load_configuration(expanduser('~/.config/golden-hour.yaml'))

    location = get_location(config['location'])

    output_dir = 'output'
    if not exists(output_dir):
        mkdir(output_dir)
    timelapse_filename = get_timelapse_filename(output_dir)

    if args.post_to_twitter:
        twitter_credentials = config['twitter']
        logger.info('verifying twitter credentials')
        tweet.TWITTER_CONFIG_SCHEMA.validate(twitter_credentials)

        # check the expected length of the video
        # to make sure it's within twitter's rules
        video_duration = calculate_timelapse_duration(args.duration, args.interval)
        logger.info(
            'estimated video length: {} seconds'.format(video_duration))
        if video_duration < 5.0:
            logger.error(
                'Error: Timelapse video will be too short to upload to Twitter (min 5 seconds)')
            exit(1)
        if video_duration > 30.0:
            logger.error(
                'Error: Timelapse video will be too long to upload to Twitter (max 30 seconds)')
            exit(2)

    if args.start_before_sunset is not None:
        sunset.wait_for_sunset(location, args.start_before_sunset)

    if not args.skip_timelapse:
        timelapse.create_timelapse(args.duration, args.interval, timelapse_filename)

    if 'climacell_key' in config:
        status_text = climacell_weather.get_status_text(
            config['climacell_key'], location,
            args.air_quality_sensor or config['use_air_quality_sensor'])
    elif 'darksky_key' in config:
        sunset_time = sunset.get_today_sunset_time(location)
        forecast = darksky_weather.get_sunset_forecast(
            config['darksky_key'],
            sunset_time,
            lat_long=(location.latitude, location.longitude))
        status_text = darksky_weather.get_status_text(forecast, sunset_time)
    else:
        status_text = '🌅 sunset at {}'.format(
            sunset.get_today_sunset_time(location).strftime('%I:%M%p'))

    logger.info(status_text)

    if args.post_to_twitter and not args.skip_timelapse:
        logger.info("Posting status and timelapse")
        tweet.post_update(config['twitter'], status_text, timelapse_filename)

    elif args.post_to_twitter and args.skip_timelapse:
        logger.info("Posting status only, no timelapse")
        tweet.post_update(config['twitter'], status_text)

    logger.info('done!')


if __name__ == '__main__':
    main()
