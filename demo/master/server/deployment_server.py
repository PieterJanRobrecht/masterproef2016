from release_dock import ReleaseDock

release_dock = ReleaseDock('localhost', 12345, 'root', 'root', 'localhost', 'mydb')
# '' = symbolic meaning for all interfaces
thread = release_dock.start_service()
print("ReleaseDock ready to do stuff")
thread.join()
