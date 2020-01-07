#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
from tempfile import TemporaryDirectory


def process_video(filename):
    global settings

    if settings['title'] is None:
        if settings['filetitle']:
            title = os.path.splitext(os.path.basename(filename))[0]
        elif settings['interactive']:
            title = input('Enter new title for {}: '.format(filename))
        else:
            print('Title for {} unchanged.'.format(filename))
            return False
    else:
        title = settings['title']

    with TemporaryDirectory() as temp:
        command = [
            'ffmpeg',
            '-i', filename,
            '-c', 'copy',
            '-metadata', 'title={}'.format(title),
            '-loglevel', 'fatal',
            '{}'.format(os.path.basename(filename))
        ]
        subprocess.call(command, cwd=temp)
        shutil.move('{}/{}'.format(temp, os.path.basename(filename)), filename)
        print('Title for {} changed to "{}".'.format(filename, title))
    return True


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Change metadata for video files using FFmpeg')
    parser.add_argument('FILE', nargs='+')
    parser.add_argument('--filetitle',
                        help='sets new title based on filename (default: %(default)s)',
                        default=False, action='store_true'),
    parser.add_argument('--interactive',
                        help='prompt for each file\'s new title (default: %(default)s)',
                        default=False, action='store_true'),
    parser.add_argument('--prompt',
                        help='prompt before exiting (default: %(default)s)',
                        default=False, action='store_true'),
    parser.add_argument('--title',
                        help='sets new title',
                        default=None),
    settings = parser.parse_args().__dict__

    for f in settings['FILE']:
        process_video(f)

    if settings['prompt']:
        input('Press Enter to continue.')
