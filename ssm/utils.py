import os


def dir_check(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)
