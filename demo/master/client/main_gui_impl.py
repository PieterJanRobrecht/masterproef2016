import sys

import description_file_gui


class MainGui(description_file_gui.MyFrame3):
    def __init__(self, parent, field_dock, field_dock_thread):
        description_file_gui.MyFrame3.__init__(self, parent)
        self.field_dock = field_dock
        self.field_dock_thread = field_dock_thread

    def close_action(self, event):
        print("FIELD DOCK -- Shutting down")
        # Send unsubcribe message
        unsub_dict = {"type": ["release", "update"]}
        self.field_dock.unsubscribe_to_messages(unsub_dict)
        # Kill GUI
        self.Destroy()
        sys.exit(0)
