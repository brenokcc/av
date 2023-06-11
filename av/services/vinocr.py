import os.path
import time
import json
import requests
import tempfile
from selenium.webdriver.common.by import By
from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
"""
from av.services.vinocr import Service
url = 'https://av.cloud.aplicativo.click/media/fotos/1685977179504_QJBA2gl.png'
print(Service().detect_vin(url))
"""

# docker run -d --network=host instrumentisto/geckodriver

class Service():
    def detect_vin(self, uri):
        if uri.startswith('http'):
            file_path = tempfile.mktemp(suffix='.png')
            open(file_path, 'wb').write(requests.get(uri).content)
        elif uri.startswith('/'):
            file_path = uri
        else:
            file_path = os.path.join(settings.BASE_DIR, uri)
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        if os.path.exists('/usr/local/bin/geckodriver'):
            br = webdriver.Firefox(options=options)
        else:
            br = webdriver.Remote(command_executor='http://geckodriver:4444', options=options)
        url = 'https://www.recognition.ws/service_vinocr_v2_demo.html'
        try:
            i = 0
            br.get(url)
            br.find_element(By.ID, 'fileUpload').send_keys(file_path)
            br.find_element(By.ID, 'btnUploadImage1').click()
            data = {}
            while i < 10 and not data:
                time.sleep(1)
                i += 1
                data = json.loads(br.find_element(By.ID, 'codes_json').text.strip() or '{}')
            vin = data.get('vin_captured', '')
        except NoSuchElementException:
            vin = ''
        br.close()
        # br.quit()
        print(vin)
        return vin

    def test(self):
        url = 'https://av.cloud.aplicativo.click/media/fotos/1685977179504_QJBA2gl.png'
        return self.detect_vin() == ''