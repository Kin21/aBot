import hide
import requests
import time
import re
import os

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

    def send_text(self, chat_id, text):
        payload = {'chat_id': chat_id, 'text': text}
        requests.post(send_message_link, data=payload)

    def do(self, req):
        command, args = req.get_command()
        chat_id = req.get_chat_id()
        if command == '/start':
            self.send_text(chat_id, 'Hello there !')
        if command == '/nick':
            nick = ' '.join(args)
            if re.fullmatch(r'[A-Za-z0-9@\\. ]{3,20}', nick):
                nick = '"' + nick + '"'
                self.send_text(chat_id, 'You are trying to search: {}'.format(nick))
            else:
                self.send_text(chat_id, 'Nickname you have written is not valid for the search!')
