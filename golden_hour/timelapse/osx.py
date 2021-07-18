import argparse
import logging
import os
import subprocess

from .ffmpeg import compile_video


logger = logging.getLogger()


def capture(output_dir, duration, interval):
    logger.info('capturing one photo every {interval} seconds for {duration} seconds'.format(
        duration=duration,
        interval=interval,
    ))
    capture_rate = '1/{}'.format(interval)
    output_pattern = '{}/image%05d.png'.format(output_dir)
    try:
        subprocess.check_call([
            'ffmpeg',
            '-loglevel', 'warning',
            '-t', str(duration),
            '-f', 'avfoundation',
            '-pix_fmt', 'uyvy422',
            '-s', '1280x720',
            '-framerate', '30',
            '-i', 'FaceTime',
            '-r', capture_rate,
            output_pattern,
        ])
    except subprocess.CalledProcessError as error:
        logger.error('Error encountered while capturing using ffmpeg', exc_info=True)


def main():
    parser = argparse.ArgumentParser(description='Record a timelapse.')
    parser.add_argument('--duration', metavar='minutes', required=True, type=int, help='total duration of timelapse capture in minutes')
    parser.add_argument('--interval', metavar='seconds', required=True, type=int, help='number of seconds between photo captures')
    parser.add_argument('--photos-per-second', type=int, default=30, help='number of photos displayed per second in video')
    args = parser.parse_args()
    logger.debug(args)

    # capture and compile timelapse
    if not os.path.exists('photos'):
        os.makedirs('photos')
    photos_dir = os.path.abspath('photos')
    logger.info('created {}'.format(photos_dir))
    capture(photos_dir, args.duration, args.interval)
    compile_video(photos_dir, args.photos_per_second)
    # TODO clean up temp dir


if __name__ == '__main__':
    main()
