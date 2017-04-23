import sys
import wx

from release_dock import ReleaseDock
from broker import Broker
from threading import Thread

from overview_impl import OverviewGui


def start_release_dock(interface, port, release_interface, release_port):
    """
        Create ReleaseDock object and start the services
    :param interface:
    :param port:
    :param release_interface:
    :param release_port:
    :return:
    """
    print("RELEASE DOCK -- Initialisation")
    release_dock = ReleaseDock(interface, port)
    thread, release_thread = release_dock.start_release_service(release_interface, release_port)
    return release_dock, thread, release_thread


def start_broker(interface, port):
    """
        Create Broker and start the services
    :param interface:
    :param port:
    :return:
    """
    print("BROKER -- Initialisation")
    broker = Broker(interface, port)
    return broker.start_service()


def listen_to_keypress(release_dock):
    """
        Listen to keyboard
        When enter is pressed start GUI
    :param release_dock:
    :return:
    """
    while True:
        try:
            raw_input("Press Enter to open the overview screen")
            app = wx.App(False)
            frame = OverviewGui(None, release_dock)
            frame.Show(True)
            if release_dock.current_release is not None:
                frame.set_release_field()
            app.MainLoop()
            app.Destroy()
        except KeyboardInterrupt:
            sys.exit()


def start_packager_service(release_dock):
    thread = Thread(target=listen_to_keypress, args=(release_dock,))
    thread.daemon = True
    thread.start()
    return thread


def main():
    """
        Start release dock
        Start broker
        Subscribe to broker
    :return:
    """
    broker_interface = "localhost"
    broker_port = 12347
    release_dock_interface = "localhost"
    release_dock_port = 12345
    release_interface = "localhost"
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
