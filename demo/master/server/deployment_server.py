from release_dock import ReleaseDock
from broker import Broker


def start_release_dock():
    print("RELEASE DOCK -- Initialisation")
    release_dock = ReleaseDock('localhost', 12345, 'root', 'root', 'localhost', 'mydb')
    # '' = symbolic meaning for all interfaces
    return release_dock.start_service()


def start_broker():
    print("BROKER -- Initialisation")
    broker = Broker('localhost', 12346)
    return broker.start_service()


def main():
    release_dock_thread = start_release_dock()
    broker_thread = start_broker()

    # Waiting until threads are finished
    release_dock_thread.join()
    broker_thread.join()

if __name__ == "__main__":
    main()
