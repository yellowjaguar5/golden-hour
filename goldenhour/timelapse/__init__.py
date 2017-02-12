import shutil
import tempfile

# TODO some way of specifying platform
from .pi import capture, compile


def create_timelapse(duration, interval, filename, persistent_photos_dir=None):
    print('recording timelapse (duration: {}, interval: {}, filename: {})'.format(
        duration, interval, filename))

    if persistent_photos_dir is None:
        photos_dir = tempfile.mkdtemp(suffix='_golden-hour')
    else:
        photos_dir = persistent_photos_dir

    capture(photos_dir, duration, interval)
    compile(photos_dir, filename)

    if persistent_photos_dir is None:
        shutil.rmtree(photos_dir)
