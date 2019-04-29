import os
import sys
import json
import time
import logging
import requests
import ssm.utils as utl

config_path = os.path.join(utl.config_path)


class ImgApi(object):
    upload_url = 'https://api.imgur.com/3/upload'

    def __init__(self, config_file='imgapi.json'):
        self.config_file = config_file
        self.config = None
        self.client_id = None
        self.client_secret = None
        self.config_list = None
        self.headers = None
        if self.config_file:
            self.input_config(self.config_file)

    def input_config(self, config):
        if not config or str(config) == 'nan':
            logging.warning('Config file name not found.  Aborting.')
            sys.exit(0)
        logging.info('Loading img config file: {}'.format(config))
        self.config_file = os.path.join(config_path, config)
        self.load_config()
        self.check_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as f:
                self.config = json.load(f)
        except IOError:
            logging.error('{} not found.  Aborting.'.format(self.config_file))
            sys.exit(0)
        self.client_id = self.config['client_id']
        self.client_secret = self.config['client_secret']
        self.config_list = [self.config, self.client_id, self.client_secret]

    def check_config(self):
        for item in self.config_list:
            if item == '':
                logging.warning('{} not in img config file.  '
                                'Aborting.'.format(item))
                sys.exit(0)

    def set_headers(self):
        self.headers = {'Authorization': 'Client-ID {}'.format(self.client_id)}

    def make_request(self, url, data, req_type='GET'):
        if not self.headers:
            self.set_headers()
        if req_type == 'GET':
            r = requests.get(url, data=data, headers=self.headers)
        elif req_type == 'POST':
            r = requests.post(url, data=data, headers=self.headers)
        else:
            r = None
        return r

    @staticmethod
    def get_image_data(img_file_name):
        image = utl.image_to_binary(img_file_name)
        if image:
            data = {'image': image}
        else:
            data = None
        return data

    def read_image_and_upload(self, img_file_name):
        logging.info('Uploading img {}.'.format(img_file_name))
        data = self.get_image_data(img_file_name)
        if data:
            url = self.upload_image(data, img_file_name)
        else:
            url = None
        return url

    def upload_image(self, data, img_file_name):
        r = self.make_request(url=self.upload_url, data=data, req_type='POST')
        if 'link' in r.json()['data']:
            url = r.json()['data']['link']
        else:
            logging.warning('No link in response: {}'.format(r.json()))
            time.sleep(600)
            url = self.read_image_and_upload(img_file_name)
        return url
