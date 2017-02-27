import mysql.connector
import pymysql as pymysql

from dock import Dock
from message import Message
from component import Component
from tower import Tower


# noinspection SqlDialectInspection
class ReleaseDock(Dock):
    database_user = 'root'
    database_password = 'root'
    database_host = 'localhost'
    database_name = 'mydb'

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

            for component in tower.components:
                query = "INSERT INTO hardware_component " \
                        "(Tower_idTower, manufacturer, productNumber," \
                        " calibrationNumber, serialNumber, firmwareVersion) VALUES "\
                        + str(Component.to_tuple(id_tower, component)) + ";"
                self.cursor.execute(query)
                self.cnx.commit()
                print("RELEASE DOCK -- Writing successful")
        except mysql.connector.Error as err:
            print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
            self.cnx.rollback()
