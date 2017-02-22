from server.message import Message
import time

message = Message()
message.create_message("new", "just some data")

message2 = Message()
message2.create_message("change", "again just some data")

while True:
    print message
    print message2
    time.sleep(3)
