from blinker import signal
import time
from threading import Thread

started = signal('round-started')


def waiting():
    while True:
        print("wachten")
        time.sleep(2)


def printing(round):
    print("ja hoor het werkt")


started.connect(printing)
thread = Thread(target=waiting)
thread.start()
