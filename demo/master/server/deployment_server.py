import wx

from release_dock import ReleaseDock
from broker import Broker
from threading import Thread

from server.release_creator_impl import ReleaseCreator


def start_release_dock():
    print("RELEASE DOCK -- Initialisation")
    release_dock = ReleaseDock('localhost', 12345)
    # '' = symbolic meaning for all interfaces
    return release_dock, release_dock.start_service()


def start_broker():
    print("BROKER -- Initialisation")
    broker = Broker('localhost', 12346)
    return broker.start_service()


def listen_to_keypress():
    while True:
        raw_input("Press Enter to create a new Release")
        app = wx.App(False)
        frame = ReleaseCreator(None)
        frame.Show(True)
        app.MainLoop()
        app.Destroy()


def start_packager_service():
    thread = Thread(target=listen_to_keypress, args=())
    thread.daemon = True
    thread.start()
    return thread


def main():
    release_dock, release_dock_thread = start_release_dock()
    broker_thread = start_broker()
    keyboard_listen = start_packager_service()
    # Subscribing to broker
    sub_dict = {"type": ["new", "change", "rapport"]}
    release_dock.connect_to_broker(sub_dict)

    # Waiting until threads are finished
    release_dock_thread.join()
    broker_thread.join()
    keyboard_listen.join()

if __name__ == "__main__":
    main()
