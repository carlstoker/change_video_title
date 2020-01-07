#!/usr/bin/env python3
import argparse
import os
import shutil
import subprocess
from tempfile import TemporaryDirectory


def select_title(filename, **kwargs):
    if kwargs['title'] is None:
        if kwargs['filetitle']:
            new_title = os.path.splitext(os.path.basename(filename))[0]
        elif kwargs['interactive']:
            new_title = input('Enter new title for {}: '.format(filename))
        else:
            print('Title for {} unchanged.'.format(filename))
            return False
    else:
        new_title = kwargs['title']
    return new_title


def update_title(filename, title):
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


def main():
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

    for filename in settings['FILE']:
        title = select_title(filename, **settings)
        update_title(filename, title)

    if settings['prompt']:
        input('Press Enter to continue.')


if __name__ == "__main__":
    main()
