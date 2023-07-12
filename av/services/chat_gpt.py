import os
import openai

"""
from av.services.chat_gpt import Service
service = Service()
service.test()
"""

class Service():
    def prompt(self, question):
        openai.api_key = os.environ.get('CHATGBT_TOKEN')
        response = openai.ChatCompletion.create(model='gpt-3.5-turbo', messages=[{"role": "user", "content": question}], temperature=0, max_tokens=10)
        print(response)
        answer = response['choices'][0]['message']['content']
        return answer

    def test(self):
        question = 'In one word, which color is the RGB code (229, 234, 240)'
        return self.prompt(question)
