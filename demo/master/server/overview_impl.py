import mysql.connector

import release_creator_gui
from server.install_agent import InstallAgent
from release_creator_impl import ReleaseCreator
from release_dock import ReleaseDock
from tower import Tower


def get_all_towers():
    """
        Collect all the tower information
    :return:
    """
    cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                  host=ReleaseDock.database_host,
                                  database=ReleaseDock.database_name)
    cursor = cnx.cursor(dictionary=True)
    towers = []
    try:
        query = "SELECT * FROM tower;"
        cursor.execute(query)
        for row in cursor:
            package = Tower.convert_to_tower(row)
            towers.append(package)

        print("RELEASE DOCK -- Collected all towers")
    except mysql.connector.Error as err:
        print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
    cnx.close()
    return towers


def get_installer_name(id_installer):
    """
        Collect name and installerversion using installerid
    :param id_installer:
    :return:
    """
    cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                  host=ReleaseDock.database_host,
                                  database=ReleaseDock.database_name)
    cursor = cnx.cursor(dictionary=True)
    try:
        query = "SELECT name, installerVersion FROM installer WHERE idInstaller = " + str(id_installer) + ";"
        cursor.execute(query)
        for row in cursor:
            name = row["name"] + row["installerVersion"]

    except mysql.connector.Error as err:
        print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
    cnx.close()
    return name


class OverviewGui(release_creator_gui.MyFrame3):
    def __init__(self, parent, release_dock):
        release_creator_gui.MyFrame3.__init__(self, parent)
        self.frame = None
        self.row_dict = None
        self.root = None
        self.release_dock = release_dock
        self.init_table()
        self.fill_table_with_towers()

    def release_current_installer(self, event):
        """
            Create install agent
            Notify broker of release
        :param event:
        :return:
        """
        # Create agents
        install_agent = InstallAgent()
        self.release_dock.agents.append(install_agent)
        # Send notification
        self.release_dock.notify_release()

    def create_installer(self, event):
        """
            Open release creator GUI
        :param event:
        :return:
        """
        self.Hide()
        self.frame = ReleaseCreator(None, self)
        self.frame.Show(True)

    def set_release_field(self):
        self.m_treeCtrl3.DeleteAllItems()
        text = "Installer: " + self.release_dock.current_release.name + self.release_dock.current_release.version
        self.root = self.m_treeCtrl3.AddRoot(text)
        for package in self.release_dock.current_release.packages:
            self.add_package_to_tree(package)

    def add_package_to_tree(self, package):
        tree = self.m_treeCtrl3
        text = "Package: " + package.name
        descr = "Description: " + package.description
        type = "Type: " + package.type
        version = "Version: " + package.version
        location = "Location: " + package.location
        opt = "Optional: " + str(package.optional)
        fram = "Is framework: " + str(package.is_framework)
        pack = tree.AppendItem(self.root, text)

        tree.AppendItem(pack, version)
        tree.AppendItem(pack, type)
        tree.AppendItem(pack, descr)
        tree.AppendItem(pack, location)
        tree.AppendItem(pack, opt)
        tree.AppendItem(pack, fram)

    def init_table(self):
        self.client_list.InsertColumn(0, "Alias")
        self.client_list.InsertColumn(1, "Geolocation")
        self.client_list.InsertColumn(2, "ID")
        self.client_list.InsertColumn(3, "Name")
        self.client_list.InsertColumn(4, "Serial Number")
        self.client_list.InsertColumn(5, "Installer")

    def fill_table_with_towers(self):
        towers = get_all_towers()
        i = 0
        self.row_dict = {}
        for tower in towers:
            self.add_tower_to_list(i, tower)
            self.row_dict[i] = tower
            i += 1

    def add_tower_to_list(self, i, tower):
        self.client_list.InsertStringItem(i, str(tower.id_tower))
        self.client_list.SetStringItem(i, 0, str(tower.alias))
        self.client_list.SetStringItem(i, 1, str(tower.location))
        self.client_list.SetStringItem(i, 2, str(tower.id_in_company))
        self.client_list.SetStringItem(i, 3, str(tower.name))
        self.client_list.SetStringItem(i, 4, str(tower.serial_number))
        if tower.id_installer is None:
            self.client_list.SetStringItem(i, 5, str("Non installed"))
        else:
            name_installer = get_installer_name(tower.id_installer)
            self.client_list.SetStringItem(i, 5, name_installer)
