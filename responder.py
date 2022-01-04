import hide
import requests
from telegram.data import  Message, Update
import time

telegram_api_link = 'https://api.telegram.org/bot{TOKEN}/{METHOD_NAME}'
telegram_api_link = telegram_api_link.format(TOKEN = hide.API_TOKEN, METHOD_NAME = '{METHOD_NAME}')

send_message_link = telegram_api_link.format(METHOD_NAME = 'sendMessage')

class Responder:
    def __init__(self, req_queue, log_db):
        self.db = log_db
        self.q = req_queue
        

    def start(self):
        while True:
            if not self.q.empty():
                req = self.q.get()
                self.do(req)
            else:
                time.sleep(0.5)
    
    def do(self, req):
        command, args = req.get_command()
        chat_id = req.get_chat_id()
        if command == '/start':
            payload = {'chat_id': chat_id, 'text': 'Hello there !'}
            res = requests.post(send_message_link, data=payload)