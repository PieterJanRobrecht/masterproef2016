from server import dock


class FieldDock(dock):
    def __init__(self, release_host, release_port):
        super(FieldDock, self).__init()
        self.release_host = release_host
        self.release_port = release_host
        print("New FieldDock made")

    def start_service(self):
        print("Starting FieldDock service")
        # check description file
        # start GUI
        # check messages
