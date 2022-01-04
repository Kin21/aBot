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

class Message:
    def __init__(self,message:dict) -> None:
        self.message_id = message['message_id']
        self.chat = Chat(message['chat'])
        self.text = message['text']
        try:
            self.entities = MessageEntity(message['entities'])
        except KeyError:
            self.entities = None
    

    def __str__(self) -> str:
        return 'message_id: {}, chat: {}, text: {}, entities: {}'.format(self.message_id, self.chat, self.text, self.entities)

class Update:
    def __init__(self, update_id: int, message: Message, **other) -> None:
        self.update_id = int(update_id)
        self.message = message
        self.other = other
    
    def __str__(self) -> str:
        return 'update_id: {}, message: [{}]'.format(self.update_id, self.message)
     


