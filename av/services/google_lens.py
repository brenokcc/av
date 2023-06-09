import os.path
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
"""
from av.services.google_lens import Service
url = 'https://av.cloud.aplicativo.click/media/fotos/1685975118796_emRFCt1.png'
service = Service()
service.detect_brand(url)
"""

# docker run -d --network=host instrumentisto/geckodriver

class Service():
    def detect_brand(self, url):
        service = None
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        if not os.path.exists('/usr/local/bin/geckodriver'):
            service = webdriver.firefox.service.Service('geckodriver', port=4444)
        url = 'https://lens.google.com/uploadbyurl?url={}&hl=pt-br'.format(url)
        print(url)
        br = webdriver.Firefox(service=service, options=options)
        br.get(url)
        try:
            marca = br.find_element('class name', 'DeMn2d').text
        except NoSuchElementException:
            marca = ''
        br.close()
        br.quit()
        print(marca)
        return marca
