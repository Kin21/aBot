import hide
import requests
from telegram.data import  Message, Update

telegram_api_link = 'https://api.telegram.org/bot{TOKEN}/{METHOD_NAME}'
telegram_api_link = telegram_api_link.format(TOKEN = hide.API_TOKEN, METHOD_NAME = '{METHOD_NAME}')

update_link = telegram_api_link.format(METHOD_NAME = 'getUpdates')
get_bot_link = telegram_api_link.format(METHOD_NAME = 'getMe')

class Updater:
    def __init__(self, req_queue):
        self.req_queue = req_queue
        if not self.check_bot():
            print("Something wrong with bot or API.")
            raise RuntimeError
        self.current_offset = None
    
    def check_bot(self):
        get_bot_req = requests.post(get_bot_link)
        return get_bot_req.json()['ok']        
        
    def start(self):
        payload = {'offset': 0, 'timeout': 100}
        while True:
            if self.current_offset:
                payload['offset'] = self.current_offset
            update_req = requests.post(update_link, data=payload)
            if update_req.json()['ok'] == True:
                self.feed_queue(update_req.json())

    def feed_queue(self, update_req):
        if not update_req['ok']:
            self.current_offset = 0
            return
        result = update_req['result']
        for update in result:
            try:
                tmp_update = Update(update['update_id'], Message(update['message']))
                self.req_queue.put(tmp_update)
            except KeyError:
                continue
        else:
            try:
                if update:
                    self.current_offset = update['update_id'] + 1
                else:
                    self.current_offset = 0
            except:
                return