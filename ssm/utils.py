import os

config_path = 'config/'


def dir_check(directory):
    if not os.path.isdir(directory):
        os.makedirs(directory)


def image_to_binary(file_name):
    with open(file_name, 'rb') as image_file:
        image_data = image_file.read()
    return image_data
