import wx

from release_dock import ReleaseDock
from broker import Broker
from threading import Thread

from overview_impl import OverviewGui


def start_release_dock(interface, port, release_interface, release_port):
    print("RELEASE DOCK -- Initialisation")
    # '' = symbolic meaning for all interfaces
    release_dock = ReleaseDock(interface, port)
    # Starting broker
    thread, release_thread = release_dock.start_release_service(release_interface, release_port)
    return release_dock, thread, release_thread


def start_broker(interface, port):
    print("BROKER -- Initialisation")
    broker = Broker(interface, port)
    return broker.start_service()


def listen_to_keypress(release_dock):
    while True:
        raw_input("Press Enter to open the overview screen")
        app = wx.App(False)
        frame = OverviewGui(None, release_dock)
        frame.Show(True)
        if release_dock.current_release is not None:
            frame.set_release_field()
        app.MainLoop()
        app.Destroy()


def start_packager_service(release_dock):
    thread = Thread(target=listen_to_keypress, args=(release_dock,))
    thread.daemon = True
    thread.start()
    return thread


def main():
    broker_interface = "192.168.1.8"
    broker_port = 12347
    release_dock_interface = "192.168.1.8"
    release_dock_port = 12345
    release_interface = "192.168.1.8"
    release_port = 12346
    start_broker_boolean = True
    release_dock, release_dock_thread, release_thread = start_release_dock(release_dock_interface, release_dock_port,
                                                                           release_interface, release_port)
    if start_broker_boolean:
        broker_thread = start_broker(broker_interface, broker_port)
    keyboard_listen = start_packager_service(release_dock)
    # Subscribing to broker
    sub_dict = {"type": ["new", "change", "rapport"]}
    release_dock.connect_to_broker(sub_dict, broker_interface, broker_port)

    # Waiting until threads are finished
    release_dock_thread.join()
    release_thread.join()
    if start_broker_boolean:
        broker_thread.join()
    keyboard_listen.join()


if __name__ == "__main__":
    main()
