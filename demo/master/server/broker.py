import ast
from dock import Dock
from server.message import Message
from collections import defaultdict


class Broker(Dock):
    def __init__(self, host, port):
        super(Broker, self).__init__()
        self.host = host
        self.port = port
        self.lookup = {}
        self.initiate_lookup()
        self.actions = defaultdict(self.other_action)
        self.initiate_actions()

    def start_service(self):
        print("BROKER -- Starting services")
        thread = super(Broker, self).start_service()
        print("BROKER -- Services started")
        return thread

    def handle_message(self):
        while True:
            data = self.message_queue.get()
            if Message.check_format(data):
                message = Message.convert_to_message(data)
                self.perform_action(message)

    def perform_action(self, message):
        print("BROKER -- performing action")
        if callable(self.actions[message.message_type]):
            self.actions[message.message_type](message)

    def other_action(self, message):
        print("BROKER -- Performing other action")
        # TODO

    def subscribe(self, message):
        print("BROKER -- Subscribing new Dock " + message.sender + " for \n\t\t" + message.data)
        d = ast.literal_eval(message.data)
        list_for_subscribing = d["type"]
        for subscription in list_for_subscribing:
            self.lookup[subscription].append(message.sender)
        # TODO send back message with counter

    def unsubscribe(self, message):
        print("BROKER -- Unsubscribing Dock " + message.sender)
        # TODO

    def initiate_lookup(self):
        # lists with all the release docks listening for new or changed field docks
        self.lookup["new"] = []
        self.lookup["change"] = []
        self.lookup["rapport"] = []

        # lists with field docks listening for new releases or updates
        self.lookup["release"] = []
        self.lookup["update"] = []

    def initiate_actions(self):
        self.actions["subscribe"] = self.subscribe
        self.actions["unsubscribe"] = self.unsubscribe
