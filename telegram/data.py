import time 

class MessageEntity:
    def __init__(self, ent:list) -> None:
        self.type = ent[0]['type']

    def __str__(self) -> str:
        return self.type

class Chat:
    def __init__(self, chat: dict) -> None:
        self.id = chat['id']

    def __str__(self) -> str:
        return str(self.id)

class Document:
    def __init__(self, doc:dict) -> None:
        self.file_id = doc['file_id']
        self.file_unique_id = doc['file_unique_id']
        try:
            self.file_name = doc['file_name']
        except KeyError:
            self.file_name = 'file'
    def __str__(self) -> str:
        return 'file_id: {}, file_unique_id: {}'.format(self.file_id, self.file_unique_id)

class Message:
    def __init__(self,message:dict) -> None:
        self.message_id = message['message_id']
        self.chat = Chat(message['chat'])
        try:
            self.text = message['text']
        except KeyError:
            try:
                self.text = message['caption']
            except KeyError:
                self.text = ''
        try:
            self.entities = MessageEntity(message['entities'])
        except KeyError:
            try:
                self.entities = MessageEntity(message['caption_entities'])
            except KeyError:
                self.entities = None
        try:
            self.document = Document(message['document'])
        except KeyError:
            self.document = None
    
    def is_bot_command(self):
        if self.entities:
            return self.entities.type == 'bot_command'

    def __str__(self) -> str:
        return 'message_id: {}, chat: {}, text: {}, entities: {}, document: {}'.format(self.message_id, self.chat, self.text, self.entities, self.document)

class Update:
    def __init__(self, update_id: int, message: Message, **other) -> None:
        self.update_id = int(update_id)
        self.message = message
        self.other = other
    
    def __str__(self) -> str:
        return 'update_id: {}, message: [{}]'.format(self.update_id, self.message)

    def is_bot_command(self):
        if self.message:
            return self.message.is_bot_command()

    def get_command(self):
        if not self.is_bot_command():
            return None, None
        command, *args = self.message.text.split(' ')
        return command, args
    
    def get_chat_id(self):
        return self.message.chat.id


