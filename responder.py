import hide
import requests
import time
import re
import threading
import os

telegram_api_link = 'https://api.telegram.org/bot{TOKEN}/{METHOD_NAME}'
telegram_api_link = telegram_api_link.format(TOKEN = hide.API_TOKEN, METHOD_NAME = '{METHOD_NAME}')

send_message_link = telegram_api_link.format(METHOD_NAME = 'sendMessage')
send_document_link = telegram_api_link.format(METHOD_NAME = 'sendDocument')

class Responder:
    def __init__(self, req_queue, log_db):
        self.db = log_db
        self.q = req_queue
        

    def start(self):
        while True:
            if not self.q.empty():
                req = self.q.get()
                threading.Thread(target=lambda r=req: self.do(r), daemon=True).start()
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
                self.send_text(chat_id, 'You are searching for {}, it takes up to 2 minutes.'.format(nick))
                res = self.snoop_nickname_search(nick)
                self.send_text(chat_id, res)
            else:
                self.send_text(chat_id, 'Nickname you have written is not valid for the search!')

    def snoop_nickname_search(self, nick):
        '''
            Uses snoop project: https://github.com/snooppr/snoop
            Regex match used to prevent OS injections and inappropriate nicknames
            Snoop code must be in the same folder as bot code
        '''
        command = 'python3 snoop.py -n -f -t 10 ' + nick + '| grep [+]'
        stream = os.popen(command)
        res = stream.read()
        return res