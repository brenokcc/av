import os.path
import time
import json
import tempfile
from selenium.webdriver.common.by import By
from django.conf import settings
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
"""
from av.services.vinocr import Service
url = 'https://av.cloud.aplicativo.click/media/fotos/1685977179504_QJBA2gl.png'
print(Service().detect_vin())
"""

# docker run -d --network=host instrumentisto/geckodriver

class Service():
    def detect_vin(self, uri='av/static/images/chassi.png'):
        if uri.startswith('http'):
            uri = tempfile.mktemp(suffix='.png')
            open(uri, 'wb').write(requests.get(uri))
        elif not uri.startswith('/'):
            uri = os.path.join(settings.BASE_DIR, uri)
        service = None
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")
        if not os.path.exists('/usr/local/bin/geckodriver'):
            service = webdriver.firefox.service.Service('geckodriver', port=4444)
        url = 'https://www.recognition.ws/service_vinocr_v2_demo.html'
        br = webdriver.Firefox(service=service, options=options)
        try:
            i = 0
            br.get(url)
            br.find_element(By.ID, 'fileUpload').send_keys(uri)
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
        br.quit()
        print(vin)
        return vin

    def test(self):
        url = 'https://av.cloud.aplicativo.click/media/fotos/1685977179504_QJBA2gl.png'
        return self.detect_vin() == ''