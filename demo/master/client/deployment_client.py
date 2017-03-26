from threading import Thread

from wx import wx

from main_gui_impl import MainGui
from field_dock import FieldDock


def start_field_dock():
    print("FIELD DOCK -- initialisation")
    field_dock = FieldDock('localhost', 54321)
    return field_dock, field_dock.start_service()


def start_gui(field_dock, field_dock_thread):
    thread = Thread(target=field_gui, args=(field_dock, field_dock_thread))
    thread.daemon = True
    thread.start()


def field_gui(field_dock, field_dock_thread):
    while True:
        app = wx.App(False)
        frame = MainGui(None, field_dock, field_dock_thread)
        frame.Show(True)
        app.MainLoop()
        app.Destroy()


def main():
    field_dock, field_dock_thread = start_field_dock()
    # Subscribing to broker
    sub_dict = {"type": ["release", "update"]}
    field_dock.connect_to_broker(sub_dict)
    start_gui(field_dock, field_dock_thread)

    field_dock.kill_message_thread()
    field_dock_thread.do_run = False
    field_dock_thread.join()
    
if __name__ == "__main__":
    main()
