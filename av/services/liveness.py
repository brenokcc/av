import tempfile
import requests
from PIL import Image

"""
from av.services.liveness import Service
url = 'https://av.cloud.aplicativo.click/media/fotos/1686159329549.png'
service = Service()
service.verify(url)
"""

class Service():
    def __init__(self):
        self.token = None

    def verify(self, url):
        data = requests.get(url).content if url.startswith('http') else open(file_path, 'r+b').read()
        # file_path = tempfile.mktemp(suffix='.png')
        # open(file_path, 'w+b').write(data)
        # im = Image.open(file_path)
        # resized_im = im.resize((round(im.size[0] * 0.25), round(im.size[1] * 0.25)))
        # resized_im.save(file_path)
        # print(file_path)
        # data = open(file_path, 'r+b').read()
        url = 'https://apilite.sandbox.ozforensics.com/v1/face/liveness/detect'
        response = requests.post(url, data=data, headers={'Content-Type': 'image/jpeg'})
        print(response.text)
        return 'MATCH' if response.json().get('passed') else 'NOT MATCH'

    def test(self):
        url = 'https://av.cloud.aplicativo.click/media/fotos/1686159329549.png'
        return self.verify(url) == 'MATCH'
