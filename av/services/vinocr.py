import os
import requests

"""
from av.services.vinocr import Service
url = 'https://www.recognition.ws/img/samples/vinocr26.jpg'
print(Service().detect_vin(url))
"""

class Service():
    def detect_vin(self, uri):
        data = {"url": uri, "token": os.environ['VINOCR_TOKEN']}
        data = requests.post('http://vinocr.aplicativo.click', json=data).json()
        print(data)
        return data.get('vin')

    def test(self):
        url = 'https://www.recognition.ws/img/samples/vinocr26.jpg'
        return self.detect_vin() == '3FADP4GX7GM105302'
