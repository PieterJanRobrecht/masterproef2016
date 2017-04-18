from threading import Thread

from wx import wx

from main_gui_impl import MainGui
from field_dock import FieldDock


def start_field_dock(interface, port, release_interface, release_port):
    """
        Initialisation of the field dock
        Will start field dock services
    :return field_dock: returns a FieldDock object
    :return service_thread: returns thread that handles the services
    """
    print("FIELD DOCK -- initialisation")
    field_dock = FieldDock(interface, port, release_interface, release_port)
    return field_dock, field_dock.start_service()


def start_gui(field_dock, field_dock_thread):
    """
        Start thread which will handle the GUI
    :param field_dock: FieldDock object
    :param field_dock_thread: thread which handles the services
    """
    thread = Thread(target=field_gui, args=(field_dock, field_dock_thread))
    thread.daemon = True
    thread.start()


def field_gui(field_dock, field_dock_thread):
    """
        Start wxPython GUI
    :param field_dock: FieldDock object
    :param field_dock_thread: thread which handles the services
    """
    while True:
        app = wx.App(False)
        frame = MainGui(None, field_dock, field_dock_thread)
        frame.Show(True)
        app.MainLoop()
        app.Destroy()


def main():
    """
        Create FieldDock object and service thread,
        Connect to broker,
        Start GUI,
        Wait until all threads are closed
    """
    field_dock_interface = "localhost"
    field_dock_port = 54321
    release_interface = "localhost"
    release_port = 12346
    broker_interface = "localhost"
    broker_port = 12347
    field_dock, field_dock_thread = start_field_dock(field_dock_interface, field_dock_port,
                                                     release_interface, release_port)
    # Subscribing to broker
    sub_dict = {"type": ["release", "update"]}
    field_dock.connect_to_broker(sub_dict, broker_interface, broker_port)
    start_gui(field_dock, field_dock_thread)

    field_dock.kill_message_thread()
    field_dock_thread.do_run = False
    field_dock_thread.join()

if __name__ == "__main__":
    main()
