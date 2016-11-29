package Server;

import InstallerMaker.InstallerCreator;
import Main.Database;
import Model.Client;
import Model.Deployment;
import Model.Installer;
import javafx.application.Platform;
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
    private TableView<Client> statusTable;

    @FXML
    private TableColumn<Client, String> clientName;

    @FXML
    private TableColumn<Client, String> clientVersion;

    @FXML
    private TableColumn<Client, String> clientStatus;

    @FXML
    private TableView<Installer> versionTable;

    @FXML
    private TableColumn<Installer, String> version;

    private File folder = null;

    private Database database;
    private List<Client> clients;
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
        Installer selected = versionTable.getSelectionModel().getSelectedItem();
        Deployment newDeployment = new Deployment(selected);
        database.setActiveInstaller(newDeployment);
    }

    @FXML
    public void initialize() {
        clientName.setCellValueFactory(new PropertyValueFactory<Client, String>("UID"));
        clientVersion.setCellValueFactory(new PropertyValueFactory<Client, String>("versionNumber"));
        clientStatus.setCellValueFactory(new PropertyValueFactory<Client, String>("status"));

        version.setCellValueFactory(new PropertyValueFactory<Installer, String>("installerVersion"));
        clients = new ArrayList<>();
    }

    public void initData() {
        clients = database.getClients();
        statusTable.getItems().setAll(clients);

        installers = database.getInstallers();
        versionTable.getItems().setAll(installers);
    }


    public void setDatabase(Database database) {
        this.database = database;
    }

    @Override
    public void update(Observable o, Object arg) {
        clients = database.getClients();
        statusTable.getItems().clear();
        Platform.runLater(() -> statusTable.getItems().setAll(clients));
    }

}
