package Server;

import Database.Database;
import Model.Package;
import Packager.Packager;
import Model.Server;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.Stage;

import java.util.ArrayList;
import java.util.List;
import java.util.Observable;
import java.util.Observer;

public class ServerController implements Observer {

    @FXML
    private TableView<Server> statusTable;

    @FXML
    private TableColumn<Server, String> serverName;

    @FXML
    private TableColumn<Server, String> serverVersion;

    @FXML
    private TableColumn<Server, String> serverStatus;

    @FXML
    private TableView<Package> versionTable;

    @FXML
    private TableColumn<Package, String> version;


    private Database database;
    private List<Server> servers;
    private List<Package> aPackages;

    @FXML
    void createNewDeployment(ActionEvent event) {
        Packager p = new Packager((Stage) versionTable.getScene().getWindow(),database);
    }

    @FXML
    void deploy(ActionEvent event) {

    }

    @FXML
    public void initialize() {
        serverName.setCellValueFactory(new PropertyValueFactory<Server, String>("UID"));
        serverVersion.setCellValueFactory(new PropertyValueFactory<Server, String>("versionNumber"));
        serverStatus.setCellValueFactory(new PropertyValueFactory<Server, String>("status"));

        version.setCellValueFactory(new PropertyValueFactory<Package, String>("versionNumber"));
    }

    public void initData() {
        aPackages = new ArrayList<>();
        servers = database.getServers();
        statusTable.getItems().setAll(servers);
        for (int i = 0; i < servers.size(); i++) {
            if (servers.get(i).getaPackage() != null)
                aPackages.add(servers.get(i).getaPackage());
        }
        versionTable.getItems().setAll(aPackages);
    }

    public void setDatabase(Database database) {
        this.database = database;
    }

    @Override
    public void update(Observable o, Object arg) {

    }

}
