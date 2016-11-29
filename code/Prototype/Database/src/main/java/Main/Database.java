package Main;

import Model.*;
import Model.Installer;
import Model.Package;
import javafx.collections.ObservableList;

import java.io.*;
import java.sql.*;
import java.util.ArrayList;
import java.util.List;
import java.util.Observable;
import java.util.UUID;

/**
 * Created by Pieter-Jan on 05/11/2016.
 */
public class Database extends Observable {
    private Deployment activeInstaller;

    private static final String DATBASELOCATION = "//localhost:3306/";
    private static final String DATABASENAME = "masterdb";

    private static final String USER = "root";
    private static final String PASS = "root";

    private Connection databaseConnection;

    public Database() {
        File file = new File(new File("."), "serverState.ser");
        activeInstaller = loadState(activeInstaller, file);
        connectDatabase();
    }

    public void save() {
        File file = new File(new File("."), "serverState.ser");
        saveState(activeInstaller, file);
    }

    public Deployment getActiveInstaller() {
        return activeInstaller;
    }

    public void setActiveInstaller(Deployment activeInstaller) {
        this.activeInstaller = activeInstaller;
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

    public List<Client> getClients() {
        List<Client> clients = new ArrayList<>();

        try {
            String query = "SELECT * FROM client";
            PreparedStatement pst = databaseConnection.prepareStatement(query);

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    int id = rs.getInt("idClient");
                    String serverUID = rs.getString("clientUUID");
                    int versionId = rs.getInt("Installer_idInstaller");
                    String status = rs.getString("status");
                    Client s = new Client(id, serverUID, versionId, status);
                    Installer v = getVersion(versionId);
                    s.setInstaller(v);
                    clients.add(s);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return clients;
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
                    Installer newInstaller = new Installer(id, version, disk, name, exe);
                    return newInstaller;
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void addServer(Client client) {
        setChanged();
        notifyObservers();
    }

    public List<Package> getAllPackages() {
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
                    Date date = rs.getDate("releaseDate");

                    Package m = new Package(id, number, name, location, priority, description, date);
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
            String query = "INSERT INTO package (packageName, description, packageVersionNumber, priority, diskLocation,releaseDate) VALUES (?,?,?,?,?,?)";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, newPackage.getPackageName());
            pst.setString(2, newPackage.getDescription());
            pst.setString(3, newPackage.getPackageVersionNumber());
            pst.setString(4, newPackage.getPriority() + "");
            pst.setString(5, newPackage.getDiskLocation());
            pst.setDate(6, newPackage.getReleaseDate());

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
        if (installerId != -1) {
            //TODO controleren of alle linken worden gelegd
            for (Package p : geslecteerde) {
                setLink(installerId, p);
            }
        }
    }

    private void setLink(int installerId, Package p) {
        int packageId = getPackageId(p);
        if (packageId != -1) {
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
            pst.setString(2, newInstaller.getInstallerVersion());

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
        for (Package p : items) {
            try {
                String query = "UPDATE package SET diskLocation = ? WHERE packageName = ? AND packageVersionNumber = ?";
                PreparedStatement pst = databaseConnection.prepareStatement(query);
                String fullLocation = installerLocation + "\\packages\\" + p.getPackageName();
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
                    Installer newInstaller = new Installer(id, version, location, name, exe);
                    installers.add(newInstaller);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return installers;
    }

    public static void saveState(Deployment activeInstaller, File file) {
        try {
            file.createNewFile();
            FileOutputStream myFileOutputStream = new FileOutputStream(file);
            ObjectOutputStream myObjectOutputStream = new ObjectOutputStream(myFileOutputStream);
            myObjectOutputStream.writeObject(activeInstaller);
            myObjectOutputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    public static Deployment loadState(Deployment currentDeployment, File file) {
        try {
            if(file.exists()){
                FileInputStream myFileInputStream = new FileInputStream(file);
                ObjectInputStream myObjectInputStream = new ObjectInputStream(myFileInputStream);
                currentDeployment = (Deployment) myObjectInputStream.readObject();
                myObjectInputStream.close();
            }else {
                currentDeployment = new Deployment(null);
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
        return currentDeployment;
    }

    public List<Package> getPackages(int id) {
        List<Package> packages = new ArrayList<>();
        List<Integer> idPackages = getPackageFromInstaller(id);
        for (Integer idPackage : idPackages) {
            Package p = getPackage(idPackage);
            packages.add(p);
        }
        return packages;
    }

    private Package getPackage(Integer idPackage) {
        Package p = null;
        try {
            String query = "SELECT * FROM package WHERE idModule = ?";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, idPackage + "");

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    int id = rs.getInt("idModule");
                    String number = rs.getString("packageVersionNumber");
                    String name = rs.getString("packageName");
                    String location = rs.getString("diskLocation");
                    int priority = rs.getInt("priority");
                    String description = rs.getString("description");
                    Date date = rs.getDate("releaseDate");

                    p = new Package(id, number, name, location, priority, description, date);

                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return p;
    }

    private List<Integer> getPackageFromInstaller(int id) {
        List<Integer> integers = new ArrayList<>();
        try {
            String query = "SELECT * FROM installer_has_package WHERE Installer_idInstaller = ?";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, id + "");

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    int packageId = rs.getInt("Package_idPackage");
                    integers.add(packageId);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return integers;
    }

    public void setStatus(UUID clientID, String s) {
        try {
            String query = "UPDATE client SET status = ? WHERE clientUUID = ?";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, s);
            pst.setString(2, clientID.toString());

            pst.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }

        setChanged();
        notifyObservers();
    }

    public void createClient(UUID state) {
        try {
            String query = "INSERT INTO client (clientUUID, status) VALUES (?,?)";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, state.toString());
            pst.setString(2, "New client");

            pst.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }

        setChanged();
        notifyObservers();
    }

    public void setVersion(UUID clientID, int installerVersion) {
        try {
            String query = "UPDATE client SET Installer_idInstaller = ? WHERE clientUUID = ?";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(2, clientID.toString());
            pst.setString(1, installerVersion+"");

            pst.executeUpdate();
        } catch (SQLException e) {
            e.printStackTrace();
        }

        setChanged();
        notifyObservers();
    }
}
