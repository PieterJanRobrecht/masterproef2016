package InstallerMaker;

import Main.Database;
import Model.Installer;
import Model.Package;
import PackagerMaker.PackagerController;
import PackagerMaker.PackagerCreator;
import Server.ServerController;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.MouseEvent;
import javafx.stage.Stage;

import java.io.File;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import java.util.Observable;
import java.util.Observer;

public class InstallerController implements Observer {

    @FXML
    private TableView<Package> allModulesTable;

    @FXML
    private TableColumn<Package, String> allName;

    @FXML
    private TableColumn<Package, String> allVersion;

    @FXML
    private TableView<Package> selectedModulesTable;

    @FXML
    private TableColumn<Package, String> selectedName;

    @FXML
    private TableColumn<Package, String> selectedVersion;

    @FXML
    private TextField installerVersion;

    @FXML
    private TextField installerName;

    private Database database;
    private File folder;
    private Installer newInstaller;


    @FXML
    void makeNewModule(ActionEvent event) {
        PackagerCreator m = new PackagerCreator((Stage) selectedModulesTable.getScene().getWindow(), database, folder);
    }

    @FXML
    void createPackage(ActionEvent event) {
        //Alle verschillende packages ophalen
        //In de juiste map plaatsen
        //Naam nemen en packages locatie updaten
        newInstaller = new Installer();
        List<Package> geslecteerde = selectedModulesTable.getItems();
        if(geslecteerde != null && geslecteerde.size() != 0){
            if(setValues()){
                //add installer to db
                //kopieer pakketen als dat nodig is + update die db
                //link leggen in db tussen pakket en installer
                //maken van effectieve installer
                changeFolderName(newInstaller.getInstallerName());
                database.saveData(newInstaller,geslecteerde);
                createExecutable();
                System.out.println("Klaar met exe maken");
                setView("Server.fxml");
            }
        }else {
            PackagerController.createMessage("Gelieve minstens 1 package te selecteren");
        }
    }

    private void setView(String s) {
        Stage stage = (Stage) installerVersion.getScene().getWindow();
        try {
            //Laden van de fxml file waarin alle gui elementen zitten
            FXMLLoader loader = new FXMLLoader();
            Parent root = (Parent) loader.load(getClass().getClassLoader().getResource(s).openStream());

            //Setten van enkele elementen van het hoofdscherm
            stage.setTitle("StatusServer");
            stage.setScene(new Scene(root));
            stage.show();

            //Ophalen van de controller horende bij de view klasse
            ServerController serverController = loader.<ServerController>getController();
            assert (serverController != null);

            serverController.setDatabase(database);
            serverController.initData();

        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void createExecutable() {
        //TODO qt gebruiken voor deze stap
    }

    private void changeFolderName(String installerName) {
        File parent = folder.getParentFile();
        File newName = new File(parent, installerName);
        folder.renameTo(newName);
        folder = newName;

        newInstaller.setDiskLocation(folder.toPath().toString());
        System.out.println("Klaar met het aanpassen van de folder naam");
        database.changeFolderNames(newInstaller.getDiskLocation(),selectedModulesTable.getItems());
    }

    private boolean setValues() {
        boolean alles = true;
        if(installerName.getText() != null){
            newInstaller.setInstallerName(installerName.getText());
        }else{
            PackagerController.createMessage("Gelieve een naam in te vullen");
            alles= false;
        }
        if (installerVersion.getText() != null){
            newInstaller.setInstallerVersion(installerVersion.getText());
        }else {
            PackagerController.createMessage("Gelieve een versie nummer in te vullen");
            alles=false;
        }
        newInstaller.setDiskLocation(folder.toPath().toString());
        return alles;
    }

    @FXML
    public void initialize() {
        allName.setCellValueFactory(new PropertyValueFactory<>("packageName"));
        allVersion.setCellValueFactory(new PropertyValueFactory<>("packageVersionNumber"));

        selectedName.setCellValueFactory(new PropertyValueFactory<>("packageName"));
        selectedVersion.setCellValueFactory(new PropertyValueFactory<>("packageVersionNumber"));

        allModulesTable.setOnMousePressed(new EventOnTable(allModulesTable, selectedModulesTable));

        selectedModulesTable.setOnMousePressed(new EventOnTable(selectedModulesTable, allModulesTable));
    }

    public void initData() {
        List<Package> allPackages = database.getPackages();
        allModulesTable.getItems().setAll(allPackages);

        List<Package> selectedPackages = new ArrayList<>();
        selectedModulesTable.getItems().setAll(selectedPackages);
    }

    @Override
    public void update(Observable o, Object arg) {

    }

    private void showInformation(Package selected) {
        //TODO details tonen van package
    }

    public void setDatabase(Database database) {
        this.database = database;
    }

    public void setFolder(File folder) {
        this.folder = folder;
    }

    private class EventOnTable implements EventHandler<MouseEvent> {
        private TableView<Package> from, to;

        public EventOnTable(TableView from, TableView to) {
            this.from = from;
            this.to = to;
        }

        @Override
        public void handle(MouseEvent event) {
            Package selected = from.getSelectionModel().getSelectedItem();
            if (event.isPrimaryButtonDown() && event.getClickCount() == 1) {
                showInformation(selected);
            }
            if (event.isPrimaryButtonDown() && event.getClickCount() == 2) {
                from.getItems().remove(selected);
                to.getItems().add(selected);
            }
        }
    }
}
