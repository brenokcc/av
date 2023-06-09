import os
import json
import requests
from pathlib import Path
from typing import Optional

"""
from av.services.eyedea import Service
url = 'https://av.cloud.aplicativo.click/media/fotos/1685975118796_emRFCt1.png'
service = Service()
service.detect_color(url)
"""

NET_ADDRESS = "https://cloud.eyedea.cz/"
EMAIL = "brenokcc@yahoo.com.br"
PASSWORD = os.environ['EYEDEA_PASSWORD']


class Service:

    def __init__(self):
        self.server_url = NET_ADDRESS
        self.email = EMAIL
        self.password = PASSWORD

    def info(self):
        payload = {"email": self.email, "password": self.password}
        r = requests.post(self.server_url + "api/v2/serverSystemInfo", data=payload)
        if r.status_code != 200:
            raise ValueError("Server returned error code {}".format(r.status_code))
        info_result = json.loads(r.content.decode("utf-8"))
        return info_result

    def detect_color(self, uri):
        color = ''
        payload = {"email": self.email, "password": self.password}
        if uri.startswith('http'):
            file = requests.get(uri).content
        else:
            with open(image_path, "rb") as f:
                file = f.read()
        files = {"file": (uri.split('/')[-1], file)}
        r = requests.post(self.server_url + "api/v2/mmrdetect", data=payload, files=files)
        print(r.json())
        if r.status_code != 200:
            raise ValueError("Server returned error code {}".format(r.status_code))
        classification = json.loads(r.content.decode("utf-8"))
        if 'tags' in classification and classification['tags']:
            result = classification['tags'][0].get('mmrResult')
            color = result.get('color', '')
        return color
