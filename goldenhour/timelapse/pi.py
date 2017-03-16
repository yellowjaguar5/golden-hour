import argparse
import os
import subprocess


def capture(output_dir, duration, interval):
    print('capturing one photo every {interval} seconds for {duration} seconds'.format(
        duration=duration,
        interval=interval,
    ))
    output_pattern = '{}/image%05d.png'.format(output_dir)
    # TODO check exit status
    subprocess.call([
        'raspistill',
        '-t', str(duration * 1000),
        '-tl', str(interval * 1000),
        '-n', # don't try to show a preview window
        '-w', '1280',
        '-h', '720',
        #'--rotation', '180', # set this to correct for camera orientation
        '--quality', '100',
        '--verbose',
        '--saturation', '50',
        '-o', output_pattern,
        '-e', 'png',
    ])


# TODO same as osx, factor out
def compile(photos_dir, output_filename, photos_per_second=30):
    print('compiling timelapse (photos per second: {photos_per_second})'.format(
        photos_per_second=photos_per_second,
    ))
    # TODO ensure output_filename ends with .mp4
    photos_pattern = '{}/image%05d.png'.format(photos_dir)
    # TODO check exit status
    subprocess.call([
        'ffmpeg',
        '-framerate', str(photos_per_second),
        '-i', photos_pattern,
        '-c:v', 'libx264',
        '-r', '30',
        '-pix_fmt', 'yuv420p',
        output_filename,
    ])


def main():
    parser = argparse.ArgumentParser(description='Record a timelapse.')
    parser.add_argument('--duration', metavar='seconds', required=True, type=int, help='total duration of timelapse capture in seconds')
    parser.add_argument('--interval', metavar='seconds', required=True, type=int, help='number of seconds between photo captures')
    parser.add_argument('--photos-per-second', type=int, default=30, help='number of photos displayed per second in video')
    args = parser.parse_args()
    print(args)

    # capture and compile timelapse
    if not os.path.exists('photos'):
        os.makedirs('photos')
    photos_dir = os.path.abspath('photos')
    output_filename = 'timelapse.mp4'
    print('created {}'.format(photos_dir))
    capture(photos_dir, args.duration, args.interval)
    compile(photos_dir, output_filename, args.photos_per_second)
    # TODO clean up temp dir


if __name__ == '__main__':
    main()
