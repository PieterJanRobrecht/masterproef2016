import ast
import socket
from dock import Dock
from message import Message
from collections import defaultdict
from threading import Thread


def determine_port(message_type):
    if message_type == "release" or message_type == "update":
        return 54321
    else:
        return 12345


def send_notification(subscriber, port, notification):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((subscriber, port))
    s.sendall(str(notification))
    s.close()


def data_to_dict(message):
    if type(message) is dict:
        d = message
    else:
        d = ast.literal_eval(message)
    return d


class Broker(Dock):
    def __init__(self, host, port):
        super(Broker, self).__init__()
        self.host = host
        self.port = port
        self.lookup = {}
        self.initiate_lookup()
        self.actions = {}
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
        print("BROKER -- Notifying action: " + message.message_type)
        self.actions[message.message_type](message)
        print("BROKER -- Action " + message.message_type + " notification send")

    def other_action(self, message):
        """Perform an action other than un/subscribe

        Take the message and make a dictionary out of it
        Put the message in payload of notification
        Send notification to everyone in the list

        :param message: received message from elsewhere
        :return:
        """
        print("BROKER -- Performing action: OTHER")
        # Send everyone in the correct list a message
        d = data_to_dict(str(message))
        notification = Message()
        notification.create_message(None, "notification", d)
        message_type = d["type"]
        call_list = self.lookup[str(message_type)]
        if len(call_list) > 0:
            for subscriber in call_list:
                port = determine_port(message_type)
                send_notification(subscriber, port, notification)
        print("BROKER -- Done with: OTHER")
        # Save message in queue somewhere

    def subscribe(self, message):
        print("BROKER -- Subscribing new Dock " + message.sender + " for \n\t\t" + str(message.data))
        d = data_to_dict(message.data)
        list_for_subscribing = d["type"]
        for subscription in list_for_subscribing:
            self.lookup[subscription].append(message.sender)
        # TODO send back message with counter

    def unsubscribe(self, message):
        print("BROKER -- Unsubscribing Dock " + message.sender)
        d = data_to_dict(message.data)
        list_for_unsubscribing = d["type"]
        for unsub in list_for_unsubscribing:
            self.lookup[unsub].remove(message.sender)

    def initiate_lookup(self):
        # lists with all the release docks listening for new or changed field docks
        self.lookup["new"] = []
        self.lookup["change"] = []
        self.lookup["rapport"] = []

        # lists with field docks listening for new releases or updates
        self.lookup["release"] = []
        self.lookup["update"] = []

    def initiate_actions(self):
        self.actions["new"] = self.other_action
        self.actions["change"] = self.other_action
        self.actions["rapport"] = self.other_action
        self.actions["update"] = self.other_action
        self.actions["release"] = self.other_action
        self.actions["subscribe"] = self.subscribe
        self.actions["unsubscribe"] = self.unsubscribe
