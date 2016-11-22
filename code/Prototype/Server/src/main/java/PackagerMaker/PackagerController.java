package PackagerMaker;

import InstallerMaker.InstallerController;
import Main.Database;
import Model.Package;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import javafx.stage.FileChooser;
import javafx.stage.Stage;
import org.controlsfx.control.Notifications;

import javax.xml.bind.JAXBContext;
import javax.xml.bind.JAXBElement;
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import javax.xml.namespace.QName;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.io.StringWriter;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;

import static java.nio.file.Files.createDirectories;
import static java.nio.file.Files.setOwner;

public class PackagerController {

    @FXML
    private ComboBox<String> moduleType;

    @FXML
    private TextField packageName;

    @FXML
    private TextField description;

    @FXML
    private TextField priority;

    @FXML
    private TextField version;

    @FXML
    private TextField fileLocation;

    private Package newPackage;

    private final String[] supportedTypes = {".exe", ".zip"};
    private Database database;
    private File folder;
    private File moduleBase;
    private File packages;
    private File data;
    private File meta;
    private File file;

    @FXML
    void choseFile(ActionEvent event) {
        FileChooser fileChooser = new FileChooser();
        fileChooser.setTitle("Open Resource File");
        File file = fileChooser.showOpenDialog(moduleType.getScene().getWindow());
        if (file != null) {
            this.file = file;
            fileLocation.setText(file.getPath());
        }
    }

    @FXML
    void makeModule(ActionEvent event) {
        newPackage = new Package();
        packages = new File(folder, "packages");

        if (file == null) {
            File check = new File(fileLocation.getText());
            if (check.exists()) {
                file = check;
            } else {
                createMessage("File bestaat niet");
            }
        }

        if (setValues()) {
            String name = packageName.getText();
            //TODO kijken naar keuze voor het bepalen van handeling
            createModuleFolders(name);
            copyFile();
            makeMetaXml();
            makeScript();
            updateDatabase();
            setView("Installer.fxml");
        }
    }

    private void setView(String s) {

        Stage stage;
        Parent root = null;

        //get reference to the button's stage
        stage = (Stage) packageName.getScene().getWindow();
        stage.setTitle("New InstallerMaker");
        FXMLLoader loader = new FXMLLoader();

        try {
            root = (Parent) loader.load(getClass().getClassLoader().getResource(s).openStream());
        } catch (IOException e) {
            e.printStackTrace();
        }

        //create a new scene with root and set the stage
        Scene scene = new Scene(root);
        stage.setScene(scene);
        stage.show();

        InstallerController installerController = loader.<InstallerController>getController();
        assert (installerController != null);

        Database data = database;
        installerController.setDatabase(data);
        installerController.initData();
        installerController.setFolder(folder);
        data.addObserver(installerController);
    }

    private void updateDatabase() {
        database.createPackage(newPackage);
    }

    private boolean setValues() {
        boolean alles = true;
        if (fileLocation.getText() != null) {
            newPackage.setDiskLocation(fileLocation.getText());
        } else {
            createMessage("Geen geldig pad");
            alles = false;
        }
        if (packageName.getText() != null) {
            newPackage.setPackageName(packageName.getText());
        } else {
            createMessage("Gelieve een naam in te vullen");
            alles = false;
        }
        if (description.getText() != null) {
            newPackage.setDescription(description.getText());
        } else {
            createMessage("Een description moet ingevuld worden");
            alles = false;
        }
        try {
            int prio = Integer.parseInt(priority.getText());
            if (prio > 100 || prio < 1) {
                createMessage("Gelieve een getal tussen 0 en 100 te nemen");
                alles = false;
            } else {
                newPackage.setPriority(prio);
            }
        } catch (Exception e) {
            createMessage("Gelieve een getal in te vullen");
            alles = false;
        }
        if (version.getText() != null) {
            newPackage.setPackageVersionNumber(version.getText());
        } else {
            createMessage("Gelieve een version number in te vullen");
            alles = false;
        }
        return alles;
    }

    private void makeScript() {
        //TODO script maken (dikke miserie)
    }

    private void makeMetaXml() {
        try {
            //print XML string representation of Student object
            File metaXml = new File(meta, "package.xml");
            JAXBContext jaxbContext = JAXBContext.newInstance(Package.class);
            Marshaller jaxbMarshaller = jaxbContext.createMarshaller();

            // output pretty printed
            jaxbMarshaller.setProperty(Marshaller.JAXB_FORMATTED_OUTPUT, true);

            jaxbMarshaller.marshal(newPackage, metaXml);

        } catch (JAXBException e) {
            e.printStackTrace();
        }
    }

    private void copyFile() {
        String[] split = file.toString().split("\\\\");
        String fileName = split[split.length - 1];
        System.out.println(fileName);
        File file = new File(data, fileName);
        try {
            file.createNewFile();
            Files.copy(this.file.toPath(), file.toPath(), StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void createModuleFolders(String name) {
        moduleBase = new File(packages, name);
        data = new File(moduleBase, "data");
        meta = new File(moduleBase, "meta");
        try {
            createDirectories(moduleBase.toPath());
            createDirectories(data.toPath());
            createDirectories(meta.toPath());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    void initData() {
        for (String supportedType : supportedTypes) {
            moduleType.getItems().add(supportedType);
        }
    }

    void setDatabase(Database database) {
        this.database = database;
    }


    void setFolder(File folder) {
        this.folder = folder;
    }

    void createMessage(String s) {
        Notifications.create()
                .title("Error")
                .text(s)
                .showWarning();
    }
}
