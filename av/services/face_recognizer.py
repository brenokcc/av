import os
import json
import requests

"""
from av.services.face_recognizer import Service
url = 'https://portalpopline.com.br/wp-content/uploads/2022/05/tom-cruise-homem-de-ferro-2.jpg'
service = Service()
service.match(url, url)
"""

class Service():
    def match(self, url1, url2):
        response = requests.post(os.environ['FACE_RECOGNIZER_URL'], json=dict(url1=url1, url2=url2))
        print(response.text)
        return response.text
