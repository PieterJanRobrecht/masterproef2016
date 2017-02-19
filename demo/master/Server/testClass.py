from subprocess import call


class Agent(object):
    def __init__(self, name):
        self.name = name

    def start(self):
        print('Print in Agent')


class InstallAgent(Agent):
    def __init__(self):
        super(InstallAgent, self).__init__("install")

    def start(self):
        # Don't use shell=True together with a command from external input, it will result in shell injection
        call(['docker build -t releasedock'], shell=True)
