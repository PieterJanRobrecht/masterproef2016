import wx

from release_dock import ReleaseDock
from broker import Broker
from threading import Thread

from server.overview_impl import OverviewGui


def start_release_dock():
    print("RELEASE DOCK -- Initialisation")
    # '' = symbolic meaning for all interfaces
    release_dock = ReleaseDock('localhost', 12345)
    thread, release_thread = release_dock.start_service()
    return release_dock, thread, release_thread


def start_broker():
    print("BROKER -- Initialisation")
    broker = Broker('localhost', 12347)
    return broker.start_service()


def listen_to_keypress(release_dock):
    while True:
        raw_input("Press Enter to open the overview screen")
        app = wx.App(False)
        frame = OverviewGui(None, release_dock)
        frame.Show(True)
        app.MainLoop()
        app.Destroy()


def start_packager_service(release_dock):
    thread = Thread(target=listen_to_keypress, args=(release_dock,))
    thread.daemon = True
    thread.start()
    return thread


def main():
    release_dock, release_dock_thread, release_thread = start_release_dock()
    broker_thread = start_broker()
    keyboard_listen = start_packager_service(release_dock)
    # Subscribing to broker
    sub_dict = {"type": ["new", "change", "rapport"]}
    release_dock.connect_to_broker(sub_dict)

    # Waiting until threads are finished
    release_dock_thread.join()
    release_thread.join()
    broker_thread.join()
    keyboard_listen.join()


if __name__ == "__main__":
    main()
