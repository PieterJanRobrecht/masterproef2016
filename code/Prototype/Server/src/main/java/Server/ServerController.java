package Server;

import InstallerMaker.InstallerCreator;
import Main.Database;
import Model.Installer;
import Model.Server;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.DirectoryChooser;
import javafx.stage.Stage;
import org.controlsfx.control.Notifications;

import java.io.File;
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
    private TableView<Installer> versionTable;

    @FXML
    private TableColumn<Installer, String> version;

    private File folder = null;


    private Database database;
    private List<Server> servers;
    private List<Installer> installers;

    @FXML
    void createNewDeployment(ActionEvent event) {
        if (folder != null && folder.isDirectory()) {
            InstallerCreator p = new InstallerCreator((Stage) versionTable.getScene().getWindow(), database, folder);
        }else{
            Notifications.create()
                    .title("Select Folder")
                    .text("Must select a folder")
                    .showWarning();
        }
    }

    @FXML
    void setInstallFolder(ActionEvent event) {
        DirectoryChooser fileChooser = new DirectoryChooser();
        fileChooser.setTitle("Open Resource File");
        File file = fileChooser.showDialog(versionTable.getScene().getWindow());
        if (file != null) {
            folder = file;
        }
    }

    @FXML
    void deploy(ActionEvent event) {

    }

    @FXML
    public void initialize() {
        serverName.setCellValueFactory(new PropertyValueFactory<Server, String>("UID"));
        serverVersion.setCellValueFactory(new PropertyValueFactory<Server, String>("versionNumber"));
        serverStatus.setCellValueFactory(new PropertyValueFactory<Server, String>("status"));

        version.setCellValueFactory(new PropertyValueFactory<Installer, String>("versionNumber"));
    }

    public void initData() {
        installers = new ArrayList<>();
        servers = database.getServers();
        statusTable.getItems().setAll(servers);
        for (int i = 0; i < servers.size(); i++) {
            if (servers.get(i).getInstaller() != null)
                installers.add(servers.get(i).getInstaller());
        }
        versionTable.getItems().setAll(installers);
    }


    public void setDatabase(Database database) {
        this.database = database;
    }

    @Override
    public void update(Observable o, Object arg) {

    }

}
