import os
import requests

"""
from av.services.vinocr import Service
url = 'https://www.recognition.ws/img/samples/vinocr26.jpg'
print(Service().detect_vin(url))
"""

class Service():
    def detect_vin(self, uri):
        url = 'http://vinocr.aplicativo.click'
        data = {"url": url, "token": os.environ['VINOCR_TOKEN']}
        data = requests.post(url, json=data).json()
        print(data)
        return data.get('vin')

    def test(self):
        url = 'https://www.recognition.ws/img/samples/vinocr26.jpg'
        return self.detect_vin() == '3FADP4GX7GM105302'
