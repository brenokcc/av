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

        self.data = {}

    def info(self):
        payload = {"email": self.email, "password": self.password}
        r = requests.post(self.server_url + "api/v2/serverSystemInfo", data=payload)
        if r.status_code != 200:
            raise ValueError("Server returned error code {}".format(r.status_code))
        info_result = json.loads(r.content.decode("utf-8"))
        return info_result

    def _get_data(self, uri):
        if uri in self.data:
            return self.data[uri]
        else:
            self.data[uri] = []
        payload = {"email": self.email, "password": self.password}
        if uri.startswith('http'):
            file = requests.get(uri).content
        else:
            with open(image_path, "rb") as f:
                file = f.read()
        files = {"file": (uri.split('/')[-1], file)}
        r = requests.post(self.server_url + "api/v2/mmrdetect", data=payload, files=files)
        # print(r.json())
        if r.status_code != 200:
            raise ValueError("Server returned error code {}".format(r.status_code))
        classification = json.loads(r.content.decode("utf-8"))
        if 'tags' in classification and classification['tags']:
            for tag in classification['tags']:
                color = None
                make = None
                plate = None
                mmr_result = tag.get('mmrResult')
                if mmr_result:
                    color = mmr_result.get('color')
                    make = mmr_result.get('make')
                anpr_result = tag.get('anprResult')
                if anpr_result:
                    plate = anpr_result.get('ocrText')
                item = dict(color=color, make=make, plate=plate)
                print(item)
                self.data[uri].append(item)
        return self.data[uri]

    def detect_colors(self, uri):
        return [item['color'] for item in self._get_data(uri) if item['color']]

    def detect_plates(self, uri):
        return [item['plate'] for item in self._get_data(uri) if item['plate']]

    def detect_color(self, uri):
        return self.detect_colors(uri)[0]

    def test(self):
        url = 'https://av.cloud.aplicativo.click/media/fotos/1685975118796_emRFCt1.png'
        print(self.detect_colors(url))
        return 'GRAY' in self.detect_colors(url)
