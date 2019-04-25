import os
import logging

config_path = 'config/'


def dir_check(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)


def image_to_binary(file_name):
    if os.path.isfile(file_name):
        with open(file_name, 'rb') as image_file:
            image_data = image_file.read()
    else:
        logging.warning('{} does not exist returning None'.format(file_name))
        image_data = None
    return image_data
