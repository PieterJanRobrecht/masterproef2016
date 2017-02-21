import mysql.connector
import pymysql as pymysql

from dock import Dock


class ReleaseDock(Dock):
    def __init__(self, host, port, database_user, database_password, database_host, database_name):
        super(ReleaseDock, self).__init__()
        self.host = host
        self.port = port
        self.database_user = database_user
        self.database_password = database_password
        self.database_host = database_host
        self.database_name = database_name
        self.cursor = None
        self.cnx = None

    def start_service(self):
        print("RELEASE DOCK -- Starting services")
        self.connect_to_database()
        thread = super(ReleaseDock, self).start_service()
        print("RELEASE DOCK -- Services started")
        return thread

    def connect_to_database(self):
        print("RELEASE DOCK -- Connecting to database")
        self.cnx = mysql.connector.connect(user=self.database_user, password=self.database_password,
                                           host=self.database_host,
                                           database=self.database_name)
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
