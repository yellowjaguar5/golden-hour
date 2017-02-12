from .osx import capture, compile

def create_timelapse(duration, interval, filename):
    print('recording timelapse (duration: {}, interval: {}, filename: {})'.format(
        duration, interval, filename))

    # TODO use temp dir for photos
    photos_dir = 'photos'
    capture(photos_dir, duration, interval)
    compile(photos_dir, filename)
    # TODO clean up photos dir
    pass
