#!/usr/bin/env python3
"""
Change title metadata for a specified video file or files using FFmpeg.

usage: change_video_title.py [-h] [--filetitle] [--interactive] [--prompt]
                      [--title TITLE] FILE [FILE ...]
"""
import argparse
import os
import shutil
import subprocess
from tempfile import TemporaryDirectory


def select_title(filename, **kwargs):
    """
    Select a title based on supplied parameters.

    Keyword arguments:
    filename -- Filename of video.
    **filetitle -- Generate a title from the filename.
    **interactive -- Prompt the user for a title.
    **title -- Pre-determined title for filename.
    """
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


def change_title(filename, title):
    """
    Change the title metadata tag on a file.

    Keyword arguments:
    filename -- Filename to modify.
    title -- New title for specified filename.
    """
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
    return True


def main():
    parser = argparse.ArgumentParser(
                        description='Change title metadata for a specified video file or files using FFmpeg.')
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
        change_title(filename, title)
        print('Title for {} changed to "{}".'.format(filename, title))

    if settings['prompt']:
        input('Press Enter to continue.')


if __name__ == "__main__":
    main()
