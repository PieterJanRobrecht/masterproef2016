import mysql.connector
import time
import release_creator_gui

from Queue import Queue
from installer import Installer
from package import Package
from release_dock import ReleaseDock


def write_to_database(installer):
    cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                  host=ReleaseDock.database_host,
                                  database=ReleaseDock.database_name)
    cursor = cnx.cursor(buffered=True, dictionary=True)
    try:
        query = "INSERT INTO installer (name, installerVersion, diskLocation) VALUES " \
                + str(Installer.to_tuple(installer)) + ";"
        cursor.execute(query)
        cnx.commit()

        query = "SELECT idInstaller FROM installer ORDER BY idInstaller DESC LIMIT 1;"
        cursor.execute(query)
        for row in cursor:
            id_installer = row['idInstaller']

        print("RELEASE DOCK -- Added new installer to database")

        for package in installer.packages:
            if package.id_package is -1:
                query = "INSERT INTO package " \
                        "(name, version," \
                        " description, location, type, priority, releaseDate, optional, framework) VALUES " \
                        + str(Package.to_tuple(package)) + ";"
                cursor.execute(query)
                cnx.commit()

                query = "SELECT idPackage FROM package ORDER BY idPackage DESC LIMIT 1;"
                cursor.execute(query)
                for row in cursor:
                    id_package = row['idPackage']

                print("RELEASE DOCK -- Added new package to database")
            else:
                id_package = package.id_package

            query = "INSERT INTO installer_has_package (Installer_idInstaller, Package_idPackage) VALUES " \
                    "(" + str(id_installer) + ", " + str(id_package) + ");"
            cursor.execute(query)
            cnx.commit()

            print("RELEASE DOCK -- Writing complete")
    except mysql.connector.Error as err:
        print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
        cnx.rollback()
    cnx.close()


def get_all_packages():
    cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                  host=ReleaseDock.database_host,
                                  database=ReleaseDock.database_name)
    cursor = cnx.cursor(buffered=True, dictionary=True)
    packages = []
    try:
        query = "SELECT * FROM (SELECT * FROM package ORDER BY idPackage DESC LIMIT 50) sub ORDER BY idPackage ASC"
        cursor.execute(query)
        for row in cursor:
            package = Package.convert_to_package(row)
            packages.append(package)

        print("RELEASE DOCK -- Collected all packages")
    except mysql.connector.Error as err:
        print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
        cnx.rollback()
    cnx.close()
    return packages


class ReleaseCreator(release_creator_gui.MyFrame1):
    queue = Queue()

    def __init__(self, parent, overview_gui):
        release_creator_gui.MyFrame1.__init__(self, parent)
        self.root = self.m_treeCtrl1.AddRoot("Installer")
        self.installer = Installer()
        # Used to transport the selected package between frames
        self.package_help = None
        self.frame = None
        self.overview_gui = overview_gui

    def select_installer(self, event):
        self.Hide()
        self.frame = SelectInstallerFrame(None, self)
        self.frame.Show(True)

    def select_package(self, event):
        self.Hide()
        self.frame = SelectPackageFrame(None, self)
        self.frame.Show(True)

    def add_selected(self):
        self.add_package_to_tree(self.package_help)
        self.installer.packages.append(self.package_help)

    def submit_installer(self, event):
        # Collect data
        self.installer.name = str(self.installer_name.GetValue())
        self.installer.version = str(self.installer_version.GetValue())
        self.installer.disk_location = str(self.installer_directory.GetTextCtrlValue())
        self.installer.new = True
        self.installer.id_installer = 0
        # Write to database
        write_to_database(self.installer)
        self.last_actions(True)

    def last_actions(self, make_folders):
        # Create file structure
        self.overview_gui.release_dock.current_release = self.installer
        if make_folders:
            self.overview_gui.release_dock.create_folders()
        self.overview_gui.set_release_field()
        self.Close()

    def submit_package(self, event):
        package = Package()
        package.name = str(self.package_name.GetValue())
        package.description = str(self.package_description.GetValue())
        package.type = str(self.package_type.GetValue())
        package.version = str(self.package_version.GetValue())
        package.location = str(self.package_directory.GetTextCtrlValue())
        package.optional = int(self.is_optional_check.GetValue() is True)
        package.is_framework = int(self.is_framework_check.GetValue() is True)
        package.release = time.strftime('%Y-%m-%d')
        package.priority = str(self.package_priority.GetValue())
        package.id_package = -1
        package.new = True
        self.installer.packages.append(package)
        self.add_package_to_tree(package)

    def clear_installer(self, event):
        # TODO
        print "installer"

    def clear_package(self, event):
        self.package_name.SetValue("")
        self.package_directory.SetPath("")
        self.package_description.SetValue("")
        self.package_type.SetValue("")
        self.package_version.SetValue("")
        self.package_priority.SetValue(50)

    def add_package_to_tree(self, package):
        tree = self.m_treeCtrl1
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

    def on_close(self, event):
        if self.frame is not None:
            self.frame.Destroy()
        self.Destroy()
        self.overview_gui.Show()


class SelectPackageFrame(release_creator_gui.MyFrame2):
    def __init__(self, parent, release_creator_frame):
        release_creator_gui.MyFrame2.__init__(self, parent)
        self.init_table()
        self.release_creator_frame = release_creator_frame
        self.selected_package = None
        self.row_dict = None
        self.fill_table_with_packages()

    def cancel(self, event):
        self.Hide()
        self.release_creator_frame.Show()

    def select(self, event):
        self.release_creator_frame.package_help = self.selected_package
        self.release_creator_frame.add_selected()
        self.cancel(event)

    def set_selected_package(self, event):
        current_item_id = event.m_itemIndex
        self.selected_package = self.row_dict[current_item_id]

    def fill_table_with_packages(self):
        packages = get_all_packages()
        i = 0
        self.row_dict = {}
        for package in packages:
            self.add_package_to_list(i, package)
            self.row_dict[i] = package
            i += 1

    def init_table(self):
        self.list_control.InsertColumn(0, "Name")
        self.list_control.InsertColumn(1, "Version")
        self.list_control.InsertColumn(2, "Description")
        self.list_control.InsertColumn(3, "Type")
        self.list_control.InsertColumn(4, "Priority")
        self.list_control.InsertColumn(5, "Optional")
        self.list_control.InsertColumn(6, "Framework")

    def add_package_to_list(self, i, package):
        self.list_control.InsertStringItem(i, str(package.id_package))
        self.list_control.SetStringItem(i, 0, str(package.name))
        self.list_control.SetStringItem(i, 1, str(package.version))
        self.list_control.SetStringItem(i, 2, str(package.description))
        self.list_control.SetStringItem(i, 3, str(package.type))
        self.list_control.SetStringItem(i, 4, str(package.priority))
        self.list_control.SetStringItem(i, 5, str(package.optional))
        self.list_control.SetStringItem(i, 6, str(package.is_framework))


def get_all_installers():
    cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                  host=ReleaseDock.database_host,
                                  database=ReleaseDock.database_name)
    cursor = cnx.cursor(buffered=True, dictionary=True)
    installers = []
    try:
        query = "SELECT * FROM (SELECT * FROM installer ORDER BY idInstaller DESC LIMIT 50)" \
                " sub ORDER BY idInstaller ASC"
        cursor.execute(query)
        for row in cursor:
            installer = Installer.convert_to_installer(row)
            installers.append(installer)

        print("RELEASE DOCK -- Collected all installers")
    except mysql.connector.Error as err:
        print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
        cnx.rollback()
    cnx.close()
    return installers


def get_package(id_package, cnx):
    cursor = cnx.cursor(buffered=True, dictionary=True)
    try:
        query = "SELECT * FROM package WHERE idPackage = " + str(id_package) + ";"
        cursor.execute(query)
        for row in cursor:
            package = Package.convert_to_package(row)

        print("RELEASE DOCK -- Collected package")
    except mysql.connector.Error as err:
        print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
        cnx.rollback()
    return package


def get_all_packages_with_installer(selected_installer):
    id = selected_installer.id_installer
    cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                  host=ReleaseDock.database_host,
                                  database=ReleaseDock.database_name)
    cursor = cnx.cursor(buffered=True, dictionary=True)
    try:
        query = "SELECT Package_idPackage FROM  installer_has_package WHERE Installer_idInstaller = " + str(id) + ";"
        cursor.execute(query)
        for row in cursor:
            package = get_package(row["Package_idPackage"], cnx)
            selected_installer.packages.append(package)

        print("RELEASE DOCK -- Collected packages for installer")
    except mysql.connector.Error as err:
        print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
        cnx.rollback()
    cnx.close()
    return selected_installer


class SelectInstallerFrame(release_creator_gui.MyFrame2):
    def __init__(self, parent, release_creator_frame):
        release_creator_gui.MyFrame2.__init__(self, parent)
        self.init_table()
        self.release_creator_frame = release_creator_frame
        self.selected_installer = None
        self.row_dict = None
        self.fill_table_with_installers()

    def cancel(self, event):
        self.Hide()
        self.release_creator_frame.Show()
        self.release_creator_frame.last_actions(False)

    def select(self, event):
        self.selected_installer = get_all_packages_with_installer(self.selected_installer)
        self.selected_installer.new = False
        self.release_creator_frame.installer = self.selected_installer
        self.cancel(event)

    def set_selected_package(self, event):
        current_item_id = event.m_itemIndex
        self.selected_installer = self.row_dict[current_item_id]

    def fill_table_with_installers(self):
        installers = get_all_installers()
        i = 0
        self.row_dict = {}
        for installer in installers:
            self.add_installer_to_list(i, installer)
            self.row_dict[i] = installer
            i += 1

    def init_table(self):
        self.list_control.InsertColumn(0, "Name")
        self.list_control.InsertColumn(1, "Version")
        self.list_control.InsertColumn(2, "Disk Location")

    def add_installer_to_list(self, i, installer):
        self.list_control.InsertStringItem(i, str(installer.id_installer))
        self.list_control.SetStringItem(i, 0, str(installer.name))
        self.list_control.SetStringItem(i, 1, str(installer.version))
        self.list_control.SetStringItem(i, 2, str(installer.disk_location))
