import os
import time
import logging
import pandas as pd
import datetime as dt
import ssm.utils as utl
import ssm.imgapi as imgapi
import selenium.webdriver as wd


class SiteConfig(object):
    url = 'url'
    site = 'site'
    file_name = 'file_name'
    img_url = 'img_url'

    def __init__(self, file_name='site_config.csv'):
        logging.info('Getting config from {}.'.format(file_name))
        self.file_name = file_name
        self.file_name = os.path.join(utl.config_path, file_name)
        self.config = self.import_config()
        self.set_all_sites()

    def import_config(self):
        df = pd.read_csv(self.file_name)
        config = df.to_dict(orient='index')
        return config

    def set_site(self, index):
        site_dict = self.config[index]
        site = Site(site_dict)
        return site

    def get_site(self, index):
        site_dict = self.config[index][self.site]
        return site_dict

    def set_all_sites(self):
        for index in self.config:
            site = self.set_site(index)
            self.config[index][self.site] = site

    def take_screenshots(self):
        browser = Browser()
        for index in self.config:
            site = self.get_site(index)
            browser.take_screenshot(site.url, site.file_name)
        browser.quit()

    def upload_screenshots(self):
        api = imgapi.ImgApi()
        for index in self.config:
            site = self.get_site(index)
            url = api.upload_image(site.file_name)
            self.config[index][self.img_url] = url


class Site(object):
    prot = 'http'
    prots = 'https://'
    www = 'www'
    tlds = ['.com', '.net', '.de', '.org', '.gov', '.edu']
    base_file_path = 'screenshots'

    def __init__(self, site_dict=None, url=None, file_name=None):
        self.url = url
        self.file_name = file_name
        self.site_dict = site_dict
        if site_dict:
            for k in site_dict:
                setattr(self, k, site_dict[k])
        self.url, self.file_name = self.check_site_params(self.url,
                                                          self.file_name)

    def check_url(self, url=None):
        if url[:4] != self.prot and self.www not in url:
            url = '{}{}.{}'.format(self.prots, self.www, url)
        elif url[:4] != self.prot:
            url = '{}{}'.format(self.prots, url)
        return url

    def check_file_name(self, url=None, file_name=None):
        if url and not file_name:
            file_name = url
            for x in [self.prots, self.www] + self.tlds:
                file_name = file_name.replace(x, '')
            file_name = file_name.replace('.', '')
            file_name += '.png'
        file_name = self.add_file_path(file_name)
        return file_name

    def add_file_path(self, file_name):
        today_path = dt.datetime.today().strftime('%y%m%d_%H')
        file_path = os.path.join(self.base_file_path, today_path)
        utl.dir_check(file_path)
        file_name = os.path.join(file_path, file_name)
        return file_name

    def check_site_params(self, url=None, file_name=None):
        url = self.check_url(url)
        file_name = self.check_file_name(url, file_name)
        return url, file_name


class Browser(object):
    def __init__(self):
        self.browser = self.init_browser()

    @staticmethod
    def init_browser():
        browser = wd.Chrome()
        browser.maximize_window()
        return browser

    def go_to_url(self, url):
        self.browser.get(url)

    def take_screenshot(self, url=None, file_name=None):
        logging.info('Getting screenshot from {} and '
                     'saving to {}.'.format(url, file_name))
        self.go_to_url(url)
        time.sleep(5)
        self.browser.save_screenshot(file_name)

    def quit(self):
        self.browser.quit()
