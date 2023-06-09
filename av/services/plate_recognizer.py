import os
import requests

"""
from av.services.plate_recognizer import Service
service = Service()
url = 'https://av.cloud.aplicativo.click/media/fotos/1685975118796_97NeDBC.png'
service.detect_plate(url)
"""

class Service():

    def __init__(self):
        self.url = 'https://api.platerecognizer.com/v1/plate-reader/'
        self.token = os.environ['PLATE_RECOGNIZER_TOKEN']

    def get_headers(self):
        return {'Authorization': 'Token {}'.format(self.token)}

    def detect_plate(self, uri):
        if uri.startswith('http'):
            file = requests.get(uri).content
        else:
            with open(image_path, "rb") as f:
                file = f.read()
        data = {'regions': 'br'}
        files = {'upload': file}
        response = requests.post(self.url, files=files, data=data, headers=self.get_headers())
        print(response.status_code, response.text)
        results = response.json()['results']
        for result in results:
            print(result['plate'].upper())
            plate = result['plate'].upper()
            plate = '{}-{}'.format(plate[0:3], plate[3:])
            return plate
        return None