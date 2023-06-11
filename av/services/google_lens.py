import os

import requests

"""
from av.services.google_lens import Service
url = 'https://av.cloud.aplicativo.click/media/fotos/1685975118796_emRFCt1.png'
service = Service()
service.detect_brand(url)
"""

class Service():
    def detect_brand(self, url):
        data = {"url": url, "token": os.environ['LENS_TOKEN']}
        data = requests.post('http://lens.aplicativo.click', json=data).json()
        print(data)
        return data.get('text')

    def test(self):
        url = 'https://av.cloud.aplicativo.click/media/fotos/1685975118796_emRFCt1.png'
        return self.detect_brand(url).upper() == 'Hyundai HB20'.upper()