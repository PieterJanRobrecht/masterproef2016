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
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.MouseEvent;
import javafx.scene.text.TextAlignment;
import javafx.stage.Stage;
import org.apache.commons.io.FileUtils;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import java.io.BufferedReader;
import java.io.File;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

public class InstallerController {

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

    @FXML
    private Label locationLabel;

    @FXML
    private Label descriptionLabel;

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
        List<Package> geselecteerde = selectedModulesTable.getItems();
        if(geselecteerde != null && geselecteerde.size() != 0){
            if(setValues()){
                //add installer to db
                //kopieer pakketen als dat nodig is + update die db
                //link leggen in db tussen pakket en installer
                //maken van effectieve installer
                transportPackages(geselecteerde);
                changeFolderName(newInstaller.getInstallerName());
                makeXml();
                database.saveData(newInstaller, geselecteerde);
                createExecutable();
                setView("Server.fxml");
            }
        }else {
            PackagerController.createMessage("Gelieve minstens 1 package te selecteren");
        }
    }

    private void transportPackages(List<Package> geslecteerde) {
        for (Package p : geslecteerde){
            if(!p.getDiskLocation().contains(newInstaller.getDiskLocation())){
                File hulp = new File(newInstaller.getDiskLocation(), "packages");
                File dest = new File(hulp, p.getPackageName());
                try {
                    FileUtils.copyDirectory(new File(p.getDiskLocation()), dest);
                } catch (IOException e) {
                    e.printStackTrace();
                }
            }
        }
    }

    private void makeXml() {
        try {
            //print XML string representation of Student object
            File metaXml = new File(new File(folder, "config"), "config.xml");
            JAXBContext jaxbContext = JAXBContext.newInstance(Installer.class);
            Marshaller jaxbMarshaller = jaxbContext.createMarshaller();

            // output pretty printed
            jaxbMarshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);

            jaxbMarshaller.marshal(newInstaller, metaXml);

        } catch (JAXBException e) {
            e.printStackTrace();
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
        String command = "cd "+folder.toPath()+" && binarycreator --offline-only -c config/config.xml -p packages PythonFrameworkInstaller";
        ProcessBuilder builder = new ProcessBuilder(
                "cmd.exe", "/c", command);
        builder.redirectErrorStream(true);
        try {
            Process p = builder.start();
            BufferedReader r = new BufferedReader(new InputStreamReader(p.getInputStream()));
            String line;
            while (true) {
                line = r.readLine();
                if (line == null) { break; }
                System.out.println(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void changeFolderName(String installerName) {
        File parent = folder.getParentFile();
        File newName = new File(parent, installerName);
        folder.renameTo(newName);
        folder = newName;

        newInstaller.setDiskLocation(folder.toPath().toString());
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
        List<Package> allPackages = database.getAllPackages();
        allModulesTable.getItems().setAll(allPackages);

        List<Package> selectedPackages = new ArrayList<>();
        selectedModulesTable.getItems().setAll(selectedPackages);
    }

    private void showInformation(Package selected) {
        descriptionLabel.setText(selected.getDescription());
        descriptionLabel.setWrapText(true);
        descriptionLabel.setTextAlignment(TextAlignment.JUSTIFY);
        locationLabel.setText(selected.getDiskLocation());
        locationLabel.setWrapText(true);
        locationLabel.setTextAlignment(TextAlignment.JUSTIFY);
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
