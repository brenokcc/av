import os
import requests

"""
from av.services.azure import Service
service = Service()
service.test()
"""

class Service():
    def detect_text(self, url):
        headers = {
            "Ocp-Apim-Subscription-Key": os.environ.get('AZURE_TOKEN'),
            "Content-Type": "application/json"
        }
        data = {"url": url}
        url = "https://sigplac.cognitiveservices.azure.com/computervision/imageanalysis:analyze?api-version=2023-02-01-preview&features=read&language=en&gender-neutral-caption=False"
        response = requests.post(url, json=data, headers=headers).json()
        print(response)
        text = response['readResult']['content'] if 'readResult' in response else ''
        return text

    def detect_chassi(self, uri):
        text = self.detect_text(uri).upper()
        text = ''.join(e for e in text if e.isalnum())
        return text.replace('I', '1').replace('O', '0').replace('Q', '0').replace('*', '').replace('\n', '').replace('\t', '').replace('#', '').replace(' ', '').replace('~', '')

    def test(self):
        url = 'https://av.cloud.aplicativo.click/media/fotos/1685977179504_PHEGA2R.png'
        return 'BRASIL' in self.detect_text(url)
