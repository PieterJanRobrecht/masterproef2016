import mysql.connector
import pymysql as pymysql
import os

from distutils.dir_util import copy_tree
from dock import Dock
from message import Message
from component import Component
from tower import Tower


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


class ReleaseDock(Dock):
    database_user = 'root'
    database_password = 'root'
    database_host = 'localhost'
    database_name = 'mydb'

    current_release = None

    def __init__(self, host, port):
        super(ReleaseDock, self).__init__()
        self.host = host
        self.port = port
        self.cursor = None
        self.cnx = None
        self.actions = {}
        self.initiate_actions()

    def start_service(self):
        print("RELEASE DOCK -- Starting services")
        self.connect_to_database()
        thread = super(ReleaseDock, self).start_service()
        print("RELEASE DOCK -- Services started")
        return thread

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
                        " calibrationNumber, serialNumber, firmwareVersion) VALUES "\
                        + str(Component.to_tuple(id_tower, component)) + ";"
                self.cursor.execute(query)
                self.cnx.commit()
                print("RELEASE DOCK -- Added new component to database")

            print("RELEASE DOCK -- Writing complete")
        except mysql.connector.Error as err:
            print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
            self.cnx.rollback()

    @classmethod
    def notify_release(cls):
        release = ReleaseDock.current_release
        # Create folder structure
        package_dir = create_folder_structure(release)
        # Place every package in folder
        for package in release.packages:
            copy_package_to_release(package, package_dir)
        # Create message and send
