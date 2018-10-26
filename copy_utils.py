# coding=utf-8
import argparse
import os
import shutil
import subprocess
import sys

if sys.version_info[0] >= 3:
    raw_input = input


def get_path(file_path):
    """
    Process path, fix it on windows platform, by adding special characters, which allows to use long paths
    :param file_path: string, input path
    :return: string, processed path
    """
    if os.name == 'nt':  # if windows
        # based on https://stackoverflow.com/questions/36219317/pathname-too-long-to-open/36219497 solution
        # to work around long paths issue on windows, still wont helps with long file names
        path = os.path.abspath(file_path)
        if path.startswith("\\\\"):
            return "\\\\?\\UNC\\" + path[2:]
        return "\\\\?\\" + path
    return file_path


def _copy(src_path, dest_path, buffer=16 * 1024):
    """
    Base copy function, copy file be streaming it from src_path to dest_path
    :param src_path: string, path of source file
    :param dest_path: string, path to destiny file
    :param buffer: length of buffer used by shutil
    """
    src_path_fixed = get_path(src_path)
    dest_path_fixed = get_path(dest_path)
    dir_path = os.path.dirname(dest_path_fixed)

    if dir_path:
        try:
            os.makedirs(dir_path)
        except OSError as e:
            # catch file exists error
            if e.errno != os.errno.EEXIST:
                raise

    with open(src_path_fixed, 'rb') as src:
        with open(dest_path_fixed, 'wb') as dst:
            shutil.copyfileobj(src, dst, buffer)


def default_copy(src_path, dest_path):
    """
    coping file by streaming it from src_path to dest_path, using default buffer of 16KB
    :param src_path: string, path of source file
    :param dest_path: string, path to destiny file
    """
    # use buffer of 16KB
    _copy(src_path, dest_path)


def fast_copy(src_path, dest_path):
    """
    coping file by streaming it from src_path to dest_path, using buffer of 10MB
    :param src_path: string, path of source file
    :param dest_path: string, path to destiny file
    """
    _copy(src_path, dest_path, 10 * 1024 * 1024)


def copy_copy(src_path, dest_path):
    """
    coping file by using copy system function on windows
    or by streaming it from src_path to dest_path, using default buffer of 16KB on other platforms
    :param src_path: string, path of source file
    :param dest_path: string, path to destiny file
    """
    if os.name == 'nt':  # if windows
        src_path_fixed = get_path(src_path)
        dest_path_fixed = get_path(dest_path)
        os.makedirs(os.path.dirname(dest_path_fixed), exist_ok=True)
        subprocess.call(['copy', src_path_fixed, dest_path_fixed], shell=True)
    else:
        default_copy(src_path, dest_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('method', choices=['fast', 'default', 'system'], nargs='?', default="fast", help="""
method used for copying file, 

"fast" is for copying by streaming with 10MB buffer 
"default" is for copying by streaming with 16KB buffer 
"system" is for copying by system copy function on windows platform, or equivalent of default on other platforms
    """)
    parser.add_argument('src_path', help="path of source file, length can't exceed 1024 symbols", nargs='?')
    parser.add_argument('dest_path', help="path of destiny file, length can't exceed 3096 symbols", nargs='?')
    args = parser.parse_args()

    def check_path(pth, length, input_query):
        if not pth:
            pth = raw_input(input_query)

        if not pth:
            print("path can't be empty")
            exit(-1)

        if len(pth) >= length:
            print("Source path length can't exceed {} symbols".format(length))
            exit(-1)

        return pth


    args.src_path = check_path(args.src_path, 1024, "Enter source file path:\n")
    args.dest_path = check_path(args.dest_path, 3096, "Enter destiny file path:\n")

    method = {
        "fast": fast_copy,
        "default": default_copy,
        "system": copy_copy,
    }.get(args.method)

    method(args.src_path, args.dest_path)
