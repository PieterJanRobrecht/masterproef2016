import time
import ast


class Message(object):
    message_counter = 0

    def __init__(self):
        self.id = None
        self.sender = None
        self.timestamp = None
        self.message_type = None
        self.data = None

    def create_message(self, sender, message_type, data):
        self.id = Message.message_counter
        Message.message_counter += 1
        self.sender = sender
        # time in seconds since epoch
        self.timestamp = time.time()
        self.message_type = message_type
        self.data = data

    def __str__(self):
        keys = ("id", "sender", "type", "timestamp", "data")
        values = (self.id, self.sender, self.message_type, self.timestamp, self.data)
        d = dict(zip(keys, values))
        return str(d)

    def __len__(self):
        return len(str(self))

    @classmethod
    def check_format(cls, data):
        # TODO
        return True

    @classmethod
    def convert_to_message(cls, data):
        if type(data) is not dict:
            d = ast.literal_eval(data)
        else:
            d = data
        message = Message()
        message.id = d["id"]
        message.sender = d["sender"]
        message.timestamp = d["timestamp"]
        message.message_type = d["type"]
        message.data = d["data"]
        return message
