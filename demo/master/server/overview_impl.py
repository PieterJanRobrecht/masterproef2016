from server import release_creator_gui
from server.release_creator_impl import ReleaseCreator


class OverviewGui(release_creator_gui.MyFrame3):
    def __init__(self, parent, release_dock):
        release_creator_gui.MyFrame3.__init__(self, parent)
        self.frame = None
        self.release_dock = release_dock

    def release_current_installer(self, event):
        # TODO
        # create agents
        # send notification
        self.release_dock.notify_release()

    def create_installer(self, event):
        self.Hide()
        self.frame = ReleaseCreator(None, self)
        self.frame.Show(True)
