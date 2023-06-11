import base64
import os
import unicodedata
import requests

"""
from av.services.google_vision import Service
service = Service()
url = 'https://av.cloud.aplicativo.click/media/fotos/1685975118796_HwR5rma.png'
service.detect_chassi(url)
labels = service.detect_labels(url)
service.is_chassi(labels)
placa_carro = 'https://av.cloud.aplicativo.click/media/fotos/1685975118796_KErHj0W.png'
service.detect_text(placa_carro)
placa_moto = 'https://av.cloud.aplicativo.click/media/fotos/1685977179504_PHEGA2R.png'
service.detect_text(placa_moto)
frente_carro = 'https://av.cloud.aplicativo.click/media/fotos/1685975118796_97NeDBC.png'
service.detect_text(placa_moto)
"""

class Service():
    TYPE_UNSPECIFIED = 0
    FACE_DETECTION = 1
    LANDMARK_DETECTION = 2
    LOGO_DETECTION = 3
    LABEL_DETECTION = 4
    TEXT_DETECTION = 5
    DOCUMENT_TEXT_DETECTION = 11
    SAFE_SEARCH_DETECTION = 6
    IMAGE_PROPERTIES = 7
    CROP_HINTS = 9
    WEB_DETECTION = 10
    PRODUCT_SEARCH = 12
    OBJECT_LOCALIZATION = 19


    def __init__(self):
        self.token = os.environ['GOOGLE_VISION_TOKEN']

    def base64(self, path):
        return base64.b64encode(open(path, 'rb').read()).decode()

    def detect_text(self, uri):
        image = {"source": {"image_uri": uri}} if uri.startswith('http') else {"content": uri}
        url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(self.token)
        data = {"requests": [{"image": image, "features": {"type": "TEXT_DETECTION"}}]}
        response = requests.post(url, json=data).json()
        for item in response['responses']:
            if item and 'fullTextAnnotation' in item:
                return item['fullTextAnnotation']['text']
        return ''

    def detect_labels(self, uri):
        image = {"source": {"image_uri": uri}} if uri.startswith('http') else {"content": uri}
        url = 'https://vision.googleapis.com/v1/images:annotate?key={}'.format(self.token)
        data = {"requests": [{"image": image, "features": {"type": "LABEL_DETECTION"}}]}
        response = requests.post(url, json=data).json()
        for item in response['responses']:
            if item and 'labelAnnotations' in item:
                return [value['description'].lower() for value in item['labelAnnotations']]
        return []

    def detect_chassi(self, uri):
        text = self.detect_text(uri).upper()
        text = ''.join(e for e in text if e.isalnum())
        text = text.replace('I', '1').replace('O', '0').replace('Q', '0')
        return text

    def check_words(self, text, words=()):
        text = unidecode(' '.join(text.split()).upper())
        missing = []
        for word in words:
            for token in word.split(' '):
                if unidecode(token.upper()) not in unidecode(text):
                    missing.append(token)
        return missing

    def test(self):
        url = 'https://av.cloud.aplicativo.click/media/fotos/1685977179504_PHEGA2R.png'
        return 'QGZ' in self.detect_text(url)


def unidecode(text):
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode()