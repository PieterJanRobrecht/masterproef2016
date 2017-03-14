import cPickle as pickle
import mysql.connector
import pymysql as pymysql
import os
import zipfile
import socket
import threading
import time

from distutils.dir_util import copy_tree
from dock import Dock
from message import Message
from component import Component
from installer import Installer
from tower import Tower
from threading import Thread


def copy_package_to_release(package, destination):
    dir_name = package.name + package.version
    root = os.path.join(destination, dir_name)
    meta = os.path.join(root, "meta")
    data = os.path.join(root, "data")
    if not os.path.exists(meta):
        os.makedirs(meta)
    if not os.path.exists(data):
        os.makedirs(data)
    copy_tree(package.location, data)
    return root


def create_folder_structure(release):
    dir_name = release.name + release.version
    root = os.path.join(release.disk_location, dir_name)
    config = os.path.join(root, "config")
    package_dir = os.path.join(root, "packages")
    if not os.path.exists(config):
        os.makedirs(config)
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)

    print("RELEASE DOCK -- Folder structure created")
    return package_dir


def add_files_to_package_folder(package, meta_dir):
    meta_file = os.path.join(meta_dir, "metadata.json")
    json = open(meta_file, 'w+')
    json.write(str(package))
    meta_file = os.path.join(meta_dir, "install_script.py")
    open(meta_file, 'w+')


def copy_old_meta_folder(package, meta_dir):
    # Search old meta folder
    try:
        cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                      host=ReleaseDock.database_host,
                                      database=ReleaseDock.database_name)
        cursor = cnx.cursor(dictionary=True)

        query = "SELECT Installer_idInstaller FROM installer_has_package WHERE Package_idPackage = " \
                + str(package.id_package) + " ORDER BY Installer_idInstaller ASC LIMIT 1;"
        cursor.execute(query)

        for row in cursor:
            id_installer = row['Installer_idInstaller']

        query = "SELECT * FROM installer WHERE idInstaller = " + str(id_installer) + ";"
        cursor.execute(query)

        for row in cursor:
            installer = Installer()
            installer.disk_location = row["diskLocation"]
            installer.name = row["name"]
            installer.version = row["installerVersion"]

    except mysql.connector.Error as err:
        print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
        cnx.rollback()
    finally:
        cnx.close()
    # Copy tree to new dir
    installer_name = installer.name + installer.version
    package_name = package.name + package.version
    old_meta_folder = os.path.join(installer.disk_location, installer_name, "packages", package_name, "meta")
    copy_tree(old_meta_folder, meta_dir)


def zip_directory(directory, zipf):
    # zipf is zipfile handle
    for root, dirs, files in os.walk(directory):
        for file in files:
            zipf.write(os.path.join(root, file))


def send_file(conn, location):
    if type(location) is file:
        location = str(location.name)
    file_size = str(os.stat(location).st_size)
    conn.send(file_size)
    work_file = open(location, "rb")
    file_size = int(file_size)
    while file_size > 0:
        data = work_file.read(1024)
        conn.send(data)
        file_size -= len(data)


class ReleaseDock(Dock):
    database_user = 'root'
    database_password = 'root'
    database_host = 'localhost'
    database_name = 'mydb'

    def __init__(self, host, port):
        super(ReleaseDock, self).__init__()
        self.host = host
        self.port = port
        # Used for sending data directly to and from field docks
        self.data_host = None
        self.data_port = None
        self.data_socket = None
        # Used for database connection
        self.cursor = None
        self.cnx = None
        # Used for the current release
        self.current_release = None
        self.agents = []
        # Used for handling messages
        self.actions = {}
        self.initiate_actions()

    def start_service(self):
        print("RELEASE DOCK -- Starting services")
        self.connect_to_database()
        release_thread = self.open_release_socket("localhost", 12346)
        thread = super(ReleaseDock, self).start_service()
        print("RELEASE DOCK -- Services started")
        return thread, release_thread

    def connect_to_database(self):
        print("RELEASE DOCK -- Connecting to database")
        self.cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                           host=ReleaseDock.database_host,
                                           database=ReleaseDock.database_name)
        self.cursor = self.cnx.cursor(dictionary=True)
        print("RELEASE DOCK -- Connected to database")

    def check_database_connection(self):
        sq = "SELECT NOW()"
        try:
            self.cursor.execute(sq)
        except pymysql.Error as e:
            if e.errno == 2006:
                print("RELEASE DOCK -- Something went wrong with the database connection... Reconnecting")
                return self.connect_to_database()
            else:
                print ("RELEASE DOCK -- No connection with database")
                return False

    def connect_to_broker(self, sub_dict):
        print("RELEASE DOCK -- Connecting to Broker")
        super(ReleaseDock, self).connect_to_broker(sub_dict)
        print("RELEASE DOCK -- Subscribed and ready")

    def handle_message(self):
        while True:
            data = self.message_queue.get()
            if Message.check_format(data):
                # Unpack notification
                message = Message.convert_to_message(data)
                relayed_message = message.data
                # Convert to message
                relayed_message = Message.convert_to_message(relayed_message)
                self.actions[relayed_message.message_type](relayed_message)

    def save_new_tower(self, message):
        tower = Tower.convert_to_tower(message.data)
        self.write_tower(tower)

    def change_tower(self, message):
        # TODO
        print message.data

    def initiate_actions(self):
        self.actions["new"] = self.save_new_tower
        self.actions["change"] = self.change_tower

    def write_tower(self, tower):
        print("RELEASE DOCK -- Writing new tower to database")
        try:
            query = "INSERT INTO Tower (name, alias, geolocation, idInCompany, serialNumber) VALUES " \
                    + str(Tower.to_tuple(tower)) + ";"
            self.cursor.execute(query)
            self.cnx.commit()

            query = "SELECT idTower FROM tower ORDER BY idTower DESC LIMIT 1;"
            self.cursor.execute(query)
            for row in self.cursor:
                id_tower = row['idTower']

            print("RELEASE DOCK -- Added new tower to database")
            for component in tower.components:
                query = "INSERT INTO hardware_component " \
                        "(Tower_idTower, manufacturer, productNumber," \
                        " calibrationNumber, serialNumber, firmwareVersion) VALUES " \
                        + str(Component.to_tuple(id_tower, component)) + ";"
                self.cursor.execute(query)
                self.cnx.commit()
                print("RELEASE DOCK -- Added new component to database")

            print("RELEASE DOCK -- Writing complete")
        except mysql.connector.Error as err:
            print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
            self.cnx.rollback()

    def notify_release(self):
        # Zip folder
        self.zip_current_release()
        # Create release message
        release_message = Message()
        release_message.create_message(self.host, "release", str(self.current_release))
        # Send message
        self.send_message(release_message)

    def zip_current_release(self):
        zip_name = self.current_release.disk_location
        zip_name = os.path.join(zip_name, "release.zip")
        root = self.current_release.disk_location
        installer_folder_name = self.current_release.name + self.current_release.version
        folder_to_zip = os.path.join(root, installer_folder_name)
        zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
        zip_directory(folder_to_zip, zipf)
        zipf.close()

    def create_folders(self):
        release = self.current_release
        # Create folder structure and return "packages" folder
        packages_dir = create_folder_structure(release)
        # Place every package in folder
        for package in release.packages:
            current_dir = copy_package_to_release(package, packages_dir)
            meta_dir = os.path.join(current_dir, "meta")
            if package.new:
                add_files_to_package_folder(package, meta_dir)
            else:
                copy_old_meta_folder(package, meta_dir)

    def open_release_socket(self, host, port):
        self.data_host = host
        self.data_port = port
        # Queue a maximum connect requests
        max_connection_request = 1
        # print("Opening socket")
        self.data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.data_socket.bind((self.data_host, self.data_port))
        self.data_socket.listen(max_connection_request)

        thread = Thread(target=self.transfer_release, args=())
        thread.daemon = True
        thread.start()
        return thread

    def transfer_release(self):
        print("RELEASE DOCK -- Listening to port " + str(self.data_port) + " on interface " + self.data_host)
        # timeout in sec
        timeout = 3
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            conn, address = self.data_socket.accept()
            print("RELEASE DOCK -- Connected by \n\t\t" + str(address))

            # Sending zip file to field dock
            zip_location = os.path.join(self.current_release.disk_location, "release.zip")
            send_file(conn, zip_location)

            # Sending agents to release dock
            ready = conn.recv(1024)
            if str(ready) == "Ready":
                list_agents = pickle.dumps(self.agents)
                file_size = len(list_agents)
                conn.send(str(file_size))
                okay = conn.recv(1024)
                if str(okay) == "Received length":
                    conn.send(list_agents)
                # send_file(conn, pkl)
                print("RELEASE DOCK -- Done sending release to " + str(address))
            conn.close()
        print("RELEASE DOCK -- Closing listening thread")
