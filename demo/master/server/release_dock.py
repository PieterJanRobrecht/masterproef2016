import ast

import dill
import mysql.connector
import pymysql as pymysql
import os
import zipfile
import socket
import threading
import datetime

from distutils.dir_util import copy_tree
from dock import Dock
from message import Message
from component import Component
from installer import Installer
from tower import Tower
from threading import Thread


def copy_package_to_release(package, destination):
    """
        Create folders meta, incl and data
        Copy tree from old location
    :param package:
    :param destination:
    :return:
    """
    dir_name = package.name + package.version
    root = os.path.join(destination, dir_name)
    meta = os.path.join(root, "meta")
    incl = os.path.join(root, "incl")
    data = os.path.join(root, "data")
    if not os.path.exists(meta):
        os.makedirs(meta)
    if not os.path.exists(incl):
        os.makedirs(incl)
    if not os.path.exists(data):
        os.makedirs(data)
    copy_tree(package.location, data)
    return root


def create_folder_structure(release):
    """
        Create folders config, incl, packages
    :param release:
    :return:
    """
    dir_name = release.name + release.version
    root = os.path.join(release.disk_location, dir_name)
    config = os.path.join(root, "config")
    incl = os.path.join(root, "incl")
    package_dir = os.path.join(root, "packages")
    if not os.path.exists(config):
        os.makedirs(config)
    if not os.path.join(incl):
        os.makedirs(incl)
    if not os.path.exists(package_dir):
        os.makedirs(package_dir)

    print("RELEASE DOCK -- Folder structure created")
    return package_dir


def add_files_to_package_folder(package, meta_dir):
    """
        Add metadata, install and test script
        If framework package add start script
    :param package:
    :param meta_dir:
    :return:
    """
    meta_file = os.path.join(meta_dir, "metadata.json")
    json = open(meta_file, 'w+')
    json.write(str(package))
    meta_file = os.path.join(meta_dir, "install_script.py")
    open(meta_file, 'w+')
    meta_file = os.path.join(meta_dir, "test_script.py")
    open(meta_file, 'w+')
    if package.is_framework == 1:
        start_script = os.path.join(meta_dir, "start_script.py")
        open(start_script, 'w+')


def copy_old_meta_folder(package, meta_dir):
    """
        Search old meta folder
        Copy tree
    :param package:
    :param meta_dir:
    :return:
    """
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
    finally:
        cnx.close()
    # Copy tree to new dir
    installer_name = installer.name + installer.version
    package_name = package.name + package.version
    old_meta_folder = os.path.join(installer.disk_location, installer_name, "packages", package_name, "meta")
    copy_tree(old_meta_folder, meta_dir)


def zip_directory(directory, zipf):
    """
        Zip release directory
    :param directory:
    :param zipf:
    :return:
    """
    # zipf is zipfile handle
    for root, dirs, files in os.walk(directory):
        for file in files:
            zipf.write(os.path.join(root, file))


def send_file(conn, location):
    """
        Send file to connected dock
    :param conn:
    :param location:
    :return:
    """
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


def add_files_to_release(release, config):
    """
        Add dockerfile and meta data file from installer
    :param release:
    :param config:
    :return:
    """
    # Create Dockerfile
    docker_file_location = os.path.join(config, "Dockerfile")
    open(docker_file_location, "w+")
    # Create metadata.json
    meta_file_location = os.path.join(config, "metadata_installer.json")
    meta_file = open(meta_file_location, "w+")
    meta_file.write(str(release))


def get_tower_of_sender(cnx, sender):
    """
        Find the installer id of the sender
    :param cnx:
    :param sender:
    :return:
    """
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("""SELECT idTower FROM tower WHERE tower.hostname = %s""", (sender,))
    for row in cursor:
        id_tower = row['idTower']
    return id_tower


def change_tower_installer(cnx, id_tower, id_installer):
    """
        Change installer id of the tower
    :param cnx:
    :param id_tower:
    :param id_installer:
    :return:
    """
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("""UPDATE tower SET Installer_idInstaller = %s WHERE idTower = %s""", (id_installer, id_tower))
    cnx.commit()
    print("RELEASE DOCK -- Updated information of tower " + str(id_tower))


def get_installer_of_sender(cnx, name, version):
    """
        Get installer from database using name and version
    :param cnx:
    :param name:
    :param version:
    :return:
    """
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("""SELECT idInstaller FROM installer WHERE name = %s AND installerVersion = %s""", (name, version))
    for row in cursor:
        id_installer = row['idInstaller']
    return id_installer


def find_tower_of_sender(cnx, sender):
    """
        Get tower id from the sender
    :param cnx:
    :param sender:
    :return:
    """
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("""SELECT idTower FROM tower WHERE hostname = %s""", (sender,))
    for row in cursor:
        id_installer = row['idTower']
    return id_installer


def find_installer_of_sender(cnx, sender):
    """
        Get installer id using sender
    :param cnx:
    :param sender:
    :return:
    """
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("""SELECT Installer_idInstaller FROM tower WHERE hostname = %s""", (sender,))
    for row in cursor:
        id_installer = row['Installer_idInstaller']
    return id_installer


def find_package(cnx, id_installer, name, version):
    """
        Find package id using name and version
    :param cnx:
    :param id_installer:
    :param name:
    :param version:
    :return:
    """
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("""SELECT idPackage FROM package,
                      (SELECT * FROM installer_has_package WHERE Installer_idInstaller = %s) AS T
                      WHERE name = %s AND version = %s """, (id_installer, name, version))
    for row in cursor:
        id_package = row['idPackage']
    return id_package


def add_diagnostics(cnx, start, end, result, id_sender, id_installer, id_package):
    """
        Add rapport to database
    :param cnx:
    :param start:
    :param end:
    :param result:
    :param id_sender:
    :param id_installer:
    :param id_package:
    :return:
    """
    start = datetime.datetime.fromtimestamp(start).strftime('%Y-%m-%d %H:%M:%S')
    end = datetime.datetime.fromtimestamp(end).strftime('%Y-%m-%d %H:%M:%S')
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("""INSERT INTO diagnosticsCheck (startTime, endTime, endResult, tower_idTower,
                    installer_idInstaller, package_idPackage) VALUES (%s, %s, %s, %s, %s, %s);""",
                   (start, end, result, id_sender, id_installer, id_package))
    cnx.commit()


def change_tower_to_nullinstaller(cnx, id_tower):
    cursor = cnx.cursor(buffered=True, dictionary=True)
    cursor.execute("""UPDATE tower SET Installer_idInstaller = NULL WHERE idTower = %s""", (id_tower,))
    cnx.commit()
    print("RELEASE DOCK -- Updated information of tower null")


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

    def start_release_service(self, interface, port):
        """
            Open socket
            Start dock service
        :param interface:
        :param port:
        :return:
        """
        print("RELEASE DOCK -- Starting services")
        self.connect_to_database()
        release_thread = self.open_release_socket(interface, port)
        thread = super(ReleaseDock, self).start_service()
        print("RELEASE DOCK -- Services started")
        return thread, release_thread

    def connect_to_database(self):
        """
            Connect to database
        :return:
        """
        print("RELEASE DOCK -- Connecting to database")
        self.cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                           host=ReleaseDock.database_host,
                                           database=ReleaseDock.database_name)
        self.cursor = self.cnx.cursor(dictionary=True)
        print("RELEASE DOCK -- Connected to database")

    def check_database_connection(self):
        """
            Check if still connected with database
        :return:
        """
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

    def connect_to_broker(self, sub_dict, broker_interface, broker_port):
        """
            Connect to broker
        :param sub_dict:
        :param broker_interface:
        :param broker_port:
        :return:
        """
        print("RELEASE DOCK -- Connecting to Broker")
        super(ReleaseDock, self).connect_to_broker(sub_dict, broker_interface, broker_port)
        print("RELEASE DOCK -- Subscribed and ready")

    def handle_message(self):
        """
            Perform the appropriate action based on message type
        :return:
        """
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
        """
            Add tower to database
        :param message:
        :return:
        """
        tower = Tower.convert_to_tower(message.data)
        self.write_tower(tower, message.sender)

    def change_tower(self, message):
        """
            Change installer info of tower or component info
        :param message:
        :return:
        """
        # Convert to dictionary
        print("RELEASE DOCK -- Changing tower")
        if type(message.data) is not dict:
            d = ast.literal_eval(message.data)
        else:
            d = message.data
        sender = message.sender
        # Check if it is an installer change or a component change
        if "idInstaller" in d:
            self.update_installer_info(d, sender)
        else:
            self.update_component_info(d, sender)
        self.update_gui()

    def handle_rapport(self, message):
        """
            Add rapport to database
        :param message:
        :return:
        """
        print("RELEASE DOCK -- Handling rapport \n\t Rapport: " + str(message.data))
        # TODO only works for the rapport of a package
        if type(message.data) is not dict:
            d = ast.literal_eval(message.data)
        else:
            d = message.data
        sender = message.sender
        id_sender = find_tower_of_sender(self.cnx, sender)
        id_installer = find_installer_of_sender(self.cnx, sender)
        id_package = find_package(self.cnx, id_installer, d["name"], d["version"])
        add_diagnostics(self.cnx, d["start_time"], d["end_time"], d["result"], id_sender, id_installer, id_package)

    def initiate_actions(self):
        self.actions["new"] = self.save_new_tower
        self.actions["change"] = self.change_tower
        self.actions["rapport"] = self.handle_rapport

    def write_tower(self, tower, sender):
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

            self.cursor.execute("""UPDATE tower SET hostname = %s WHERE idTower = %s""",
                                (sender, id_tower))
            self.cnx.commit()

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

    def notify_release(self):
        """
            Create zip
            Send release message to broker
        :return:
        """
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
        """
            Create complete folder structure for release
        :return:
        """
        release = self.current_release
        # Create folder structure and return "packages" folder
        packages_dir = create_folder_structure(release)
        installer_dir = release.name + release.version
        config = os.path.join(release.disk_location, installer_dir, "config")
        if release.new:
            add_files_to_release(release, config)
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
        """
            Send zip file from local to connected dock
            Send agents to connected dock
        :return:
        """
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
            self.send_agents(conn, address)
        print("RELEASE DOCK -- Closing listening thread")

    def update_installer_info(self, d, sender):
        print("RELEASE DOCK -- Changing installer information")
        id_tower = get_tower_of_sender(self.cnx, sender)
        if d["idInstaller"] != "None":
            id_installer = get_installer_of_sender(self.cnx, d["name"], d["version"])
            change_tower_installer(self.cnx, id_tower, id_installer)
        else:
            change_tower_to_nullinstaller(self.cnx, id_tower)

    def update_component_info(self, d, sender):
        # TODO
        print("Still to do boys")

    def update_gui(self):
        # TODO
        pass

    def send_agents(self, conn, address):
        ready = conn.recv(1024)
        if str(ready) == "Ready":
            list_agents = dill.dumps(self.agents)
            file_size = len(list_agents)
            conn.send(str(file_size))
            okay = conn.recv(1024)
            if str(okay) == "Received length":
                conn.send(list_agents)
            # send_file(conn, pkl)
            print("RELEASE DOCK -- Done sending release to " + str(address))
        conn.close()
