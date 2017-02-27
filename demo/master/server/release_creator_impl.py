import mysql.connector

import release_creator_gui
from server.installer import Installer
from server.package import Package
from server.release_dock import ReleaseDock


def write_to_database(installer):
    cnx = mysql.connector.connect(user=ReleaseDock.database_user, password=ReleaseDock.database_password,
                                  host=ReleaseDock.database_host,
                                  database=ReleaseDock.database_name)
    cursor = cnx.cursor(dictionary=True)
    # try:
    query = "INSERT INTO installer (name, installerVersion, diskLocation) VALUES " \
            + str(Installer.to_tuple(installer)) + ";"
    cursor.execute(query)
    cnx.commit()

    query = "SELECT idInstaller FROM installer ORDER BY idInstaller DESC LIMIT 1;"
    cursor.execute(query)
    for row in cursor:
        id_installer = row['idInstaller']

    for package in installer.packages:
        query = "INSERT INTO package " \
                "(name, version," \
                " description, type, priority, releaseDate, optional, framework) VALUES " \
                + str(Package.to_tuple(package)) + ";"
        cursor.execute(query)
        cnx.commit()

        query = "SELECT idPackage FROM package ORDER BY idPackage DESC LIMIT 1;"
        cursor.execute(query)
        for row in cursor:
            id_package = row['idPackage']

        query = "INSERT INTO installer_has_package (Installer_idInstaller, Package_idPackage) VALUES " \
                "(" + id_installer + ", " + id_package + ");"
        cursor.execute(query)
        cnx.commit()

        print("RELEASE DOCK -- Writing successful")
    # except mysql.connector.Error as err:
    #     print("RELEASE DOCK -- Something went wrong: \n\t\t " + str(err))
    #     cnx.rollback()
    cnx.close()


class ReleaseCreator(release_creator_gui.MyFrame1):
    def __init__(self, parent):
        release_creator_gui.MyFrame1.__init__(self, parent)
        self.root = self.m_treeCtrl1.AddRoot("Installer")
        self.installer = Installer()

    def select_installer(self, event):
        print "installer"

    def select_package(self, event):
        print "package"

    def release_installer(self, event):
        # Write to database
        self.installer.name = str(self.installer_name.GetValue())
        self.installer.version = str(self.installer_version.GetValue())
        self.installer.disk_location = str(self.installer_directory.GetTextCtrlValue())
        write_to_database(self.installer)

    def submit_package(self, event):
        package = Package()
        package.name = str(self.package_name.GetValue())
        package.description = str(self.package_description.GetValue())
        package.type = str(self.package_type.GetValue())
        package.version = str(self.package_version.GetValue())
        package.location = str(self.package_directory.GetTextCtrlValue())
        package.optional = str(self.is_optional_check.GetValue())
        package.is_framework = str(self.is_framework_check.GetValue())
        self.installer.packages.append(package)
        self.add_package_to_tree(package)

    def clear_installer(self, event):
        print "installer"

    def clear_package(self, event):
        self.package_name.SetValue("")
        self.package_directory.SetTextCtrlValue("")
        self.package_description.SetValue("")
        self.package_type.SetValue("")
        self.package_version.SetValue("")

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
