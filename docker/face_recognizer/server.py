import os
import json
import http.server
import socketserver
import requests
import tempfile
import face_recognition
from http.server import SimpleHTTPRequestHandler

"""
import json
import requests
url = 'https://portalpopline.com.br/wp-content/uploads/2022/05/tom-cruise-homem-de-ferro-2.jpg'
requests.post('http://face_recognizer.aplicativo.click', data=json.dumps(dict(url1=url, url2=url))).text
"""

class RequestHandler(SimpleHTTPRequestHandler):
 def do_POST(self):
  print(self.path)
  self.send_response(200)
  self.send_header('Content-type', 'text/plain')
  self.end_headers()
  data = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
  print(data)
  url1=data['url1']
  url2=data['url2']
  file_path1 = tempfile.mktemp()
  open(file_path1, 'wb').write(requests.get(url1).content)
  file_path2 = tempfile.mktemp()
  open(file_path2, 'wb').write(requests.get(url2).content)
  if1 = face_recognition.load_image_file(file_path1)
  if2 = face_recognition.load_image_file(file_path2)
  fe1 = face_recognition.face_encodings(if1)
  fe2 = face_recognition.face_encodings(if2)
  match = False
  if fe1 and fe2:
   result = face_recognition.compare_faces([fe1[0]], fe2[0])
   match = result and result[0]
  self.wfile.write(b'MATCH' if match else b'NOT MATCH')

try:
 with socketserver.TCPServer(("0.0.0.0", 8000), RequestHandler) as httpd: httpd.serve_forever()
finally:
 httpd.shutdown()
