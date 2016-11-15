package Database;

import Model.Module;
import Model.Server;
import Model.Package;

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
                    int versionId = rs.getInt("Version_idVersion");
                    Server s = new Server(id, serverUID, versionId);
                    Package v = getVersion(versionId);
                    s.setaPackage(v);
                    servers.add(s);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return servers;
    }

    private Package getVersion(int versionId) {
        try {
            String query = "SELECT * FROM package WHERE idVersion = ?";
            PreparedStatement pst = databaseConnection.prepareStatement(query);
            pst.setString(1, versionId + "");

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    int id = rs.getInt("idVersion");
                    String version = rs.getString("versionNumber");
                    String disk = rs.getString("diskLocation");
                    return new Package(id, version, disk);
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

    public List<Module> getModules() {
        List<Module> modules = new ArrayList<>();

        try {
            String query = "SELECT * FROM MODULE";
            PreparedStatement pst = databaseConnection.prepareStatement(query);

            try (ResultSet rs = pst.executeQuery()) {
                while (rs.next()) {
                    int id = rs.getInt("idModule");
                    String number = rs.getString("moduleNumber");
                    String name = rs.getString("moduleName");
                    String location = rs.getString("diskLocation");

                    Module m = new Module(id,number,name,location);
                    modules.add(m);
                }
            }
        } catch (SQLException e) {
            e.printStackTrace();
        }
        return modules;
    }
}
