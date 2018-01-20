import subprocess


def compile_video(photos_dir, output_filename, photos_per_second=30):
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