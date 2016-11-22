package Main;

import Model.*;
import Model.Installer;
import Model.Package;
import javafx.collections.ObservableList;

import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Observable;

/**
 * Created by Pieter-Jan on 05/11/2016.
 */
public class Database extends Observable {
    private static final String DATBASELOCATION = "//localhost:3306/";
    private static final String DATABASENAME = "masterdb";

    private static final String USER = "root";
    private static final String PASS = "root";

    private Connection databaseConnection;

    public Database() {
        connectDatabase();
    }

    private void connectDatabase() {
        try {
            Class.forName("com.mysql.jdbc.Driver");
            databaseConnection = DriverManager.getConnection("jdbc:mysql:" + DATBASELOCATION + DATABASENAME + "?useSSL=false", USER, PASS);
        } catch (Exception e) {
            System.err.println(e.getClass().getName() + ": " + e.getMessage());
            System.exit(0);
        }
        System.out.println("Opened connection to database");
    }

    public List<Server> getServers() {
        List<Server> servers = new ArrayList<>();

        try {
            String query = "SELECT * FROM server";
            PreparedStatement pst = databaseConnection.prepareStatement(query);

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    int id = rs.getInt("idServer");
                    String serverUID = rs.getString("serverUID");
                    int versionId = rs.getInt("Installer_idInstaller");
                    Server s = new Server(id, serverUID, versionId);
                    Installer v = getVersion(versionId);
                    s.setInstaller(v);
                    servers.add(s);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return servers;
    }

    private Installer getVersion(int versionId) {
        try {
            String query = "SELECT * FROM installer WHERE idInstaller = ?";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, versionId + "");

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    int id = rs.getInt("idInstaller");
                    String version = rs.getString("installerVersionNumber");
                    String disk = rs.getString("diskLocation");
                    String name = rs.getString("installerName");
                    String exe = rs.getString("executableLocation");
                    return new Installer(id, version, disk,name,exe);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void addServer(Server server) {
        setChanged();
        notifyObservers();
    }

    public List<Package> getPackages() {
        List<Package> aPackages = new ArrayList<>();

        try {
            String query = "SELECT * FROM package";
            PreparedStatement pst = databaseConnection.prepareStatement(query);

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    int id = rs.getInt("idModule");
                    String number = rs.getString("packageVersionNumber");
                    String name = rs.getString("packageName");
                    String location = rs.getString("diskLocation");
                    int priority = rs.getInt("priority");
                    String description = rs.getString("description");

                    Package m = new Package(id, number, name, location, priority, description);
                    aPackages.add(m);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return aPackages;
    }

    public void createPackage(Package newPackage) {
        try {
            String query = "INSERT INTO package (packageName, description, packageVersionNumber, priority, diskLocation) VALUES (?,?,?,?,?)";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, newPackage.getPackageName());
            pst.setString(2, newPackage.getDescription());
            pst.setString(3, newPackage.getPackageVersionNumber());
            pst.setString(4, newPackage.getPriority() + "");
            pst.setString(5, newPackage.getDiskLocation());

            pst.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void saveData(Installer newInstaller, List<Package> geslecteerde) {
        createInstaller(newInstaller);
        linkPackagesToInstaller(newInstaller, geslecteerde);
    }

    private void linkPackagesToInstaller(Installer newInstaller, List<Package> geslecteerde) {
        int installerId = getInstallerId(newInstaller);
        if(installerId != -1){
            for (Package p : geslecteerde){
                setLink(installerId, p);
            }
        }
    }

    private void setLink(int installerId, Package p) {
        int packageId = getPackageId(p);
        if(packageId != -1) {
            try {
                String query = "INSERT INTO installer_has_package (Installer_idInstaller, Package_idPackage) VALUES (?,?)";
                PreparedStatement pst = databaseConnection.prepareStatement(query);
                pst.setString(1, installerId + "");
                pst.setString(2, packageId + "");

                pst.executeUpdate();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    private int getPackageId(Package p) {
        int id = -1;
        try {
            String query = "SELECT * FROM package WHERE packageName = ? AND packageVersionNumber = ?";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, p.getPackageName());
            pst.setString(2, p.getPackageVersionNumber());

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    id = rs.getInt("idModule");
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return id;
    }

    private int getInstallerId(Installer newInstaller) {
        int id = -1;
        try {
            String query = "SELECT * FROM installer WHERE installerName = ? AND installerVersionNumber = ?";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, newInstaller.getInstallerName());
            pst.setString(2,newInstaller.getInstallerVersion());

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    id = rs.getInt("idInstaller");
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return id;
    }

    private void createInstaller(Installer newInstaller) {
        try {
            String query = "INSERT INTO installer (installerName, diskLocation, installerVersionNumber) VALUES (?,?,?)";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, newInstaller.getInstallerName());
            pst.setString(2, newInstaller.getDiskLocation());
            pst.setString(3, newInstaller.getInstallerVersion());

            pst.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }
    }

    public void changeFolderNames(String installerLocation, ObservableList<Package> items) {
        for (Package p : items){
            try {
                String query = "UPDATE package SET diskLocation = ? WHERE packageName = ? AND packageVersionNumber = ?";
                PreparedStatement pst = databaseConnection.prepareStatement(query);
                String fullLocation = installerLocation +"\\packages\\"+p.getPackageName();
                pst.setString(1, fullLocation);
                pst.setString(2, p.getPackageName());
                pst.setString(3, p.getPackageVersionNumber());

                pst.executeUpdate();
            } catch (SQLException e) {
                e.printStackTrace();
            }
        }
    }

    public List<Installer> getInstallers() {
        List<Installer> installers = new ArrayList<>();

        try {
            String query = "SELECT * FROM installer";
            PreparedStatement pst = databaseConnection.prepareStatement(query);

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    int id = rs.getInt("idInstaller");
                    String version = rs.getString("installerVersionNumber");
                    String location = rs.getString("diskLocation");
                    String name = rs.getString("installerName");
                    String exe = rs.getString("executableLocation");
                    installers.add(new Installer(id,version,location,name,exe));
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return installers;
    }
}
