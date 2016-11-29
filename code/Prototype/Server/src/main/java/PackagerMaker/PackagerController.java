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
import javax.xml.bind.JAXBException;
import javax.xml.bind.Marshaller;
import java.io.File;
import java.io.IOException;
import java.io.PrintWriter;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;
import java.sql.Date;
import java.util.Calendar;

import static java.nio.file.Files.createDirectories;
import static java.nio.file.Files.write;

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
            newPackage.setDiskLocation(moduleBase.toPath().toString());
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
    }

    private void updateDatabase() {
        database.createPackage(newPackage);
    }

    private boolean setValues() {
        boolean alles = true;
        if (!packageName.getText().equals("")) {
            newPackage.setPackageName(packageName.getText());
        } else {
            createMessage("Gelieve een naam in te vullen");
            alles = false;
        }
        if (!description.getText().equals("")) {
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
        //TODO controleren dat er geen letters in zitten -> error in qt
        if (!version.getText().equals("")) {
            newPackage.setPackageVersionNumber(version.getText());
        } else {
            createMessage("Gelieve een version number in te vullen");
            alles = false;
        }
        newPackage.setReleaseDate(new Date(Calendar.getInstance().getTime().getTime()));
        return alles;
    }

    private void makeScript() {
        //TODO script maken (dikke miserie)
        try {
            File script = new File(meta, "installscript.qs");
            PrintWriter writer = new PrintWriter(script);
            writeFirstBlock(writer);

            String selected = moduleType.getSelectionModel().getSelectedItem();
            if (selected == null) {
                createMessage("Gelieve een type te selecteren");
            } else {
                writeActionWindows(writer, selected);
            }

            writeLastBlock(writer);
            writer.close();
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void writeLastBlock(PrintWriter writer) {
        writer.println("}");
    }

    private void writeActionWindows(PrintWriter writer, String selected) {
        String[] split = file.toPath().toString().split("\\\\");
        String name = split[split.length - 1];

        switch (selected) {
            case ".exe":
                writeExe(writer, name);
                break;
            case ".zip":
                writeZip(writer, name);
                break;
        }
    }

    private void writeZip(PrintWriter writer, String name) {
        writer.println(
                "if (systemInfo.productType === \"windows\") {\r\n" +
                        "\t\tcomponent.addOperation(\"Execute\"\r\n" +
                        "\t\t, \"cmd\"\r\n" +
                        "\t\t, \"/c\"\r\n" +
                        "\t\t, \"C:\\\\\\\"Program Files\\\"\\\\WinRAR\\\\WinRAR.exe\"\r\n" +
                        "\t\t, \"x\"\r\n" +
                        "\t\t, \"@TargetDir@\\\\" +
                        name + "\"\r\n" +
                        "\t\t, \"@TargetDir@\")\r\n" +
                        "\t\r\n" +
                        "\t\tcomponent.addOperation(\"Execute\"\r\n" +
                        "\t\t, \"cmd\"\t\r\n" +
                        "\t\t, \"/K\" \r\n" +
                        "\t\t, \"\\\"cd\" \r\n" +
                        "\t\t, \"@TargetDir@\\\\" +
                        name +
                        "\" \r\n" +
                        "\t\t, \"&&\" \r\n" +
                        "\t\t, \"C:\\\\Python27\\\\python.exe\" \r\n" +
                        "\t\t, \"setup.py\" \r\n" +
                        "\t\t, \"install\" \r\n" +
                        "\t\t, \"&&\" \r\n" +
                        "\t\t, \"exit\\\"\")\r\n" +
                        "\t}"
        );
    }

    private void writeExe(PrintWriter writer, String name) {
        writer.println(
                "\tif (systemInfo.productType === \"windows\") {\r\n" +
                        "\t\tcomponent.addOperation(\"Execute\"\r\n" +
                        "\t\t, \"msiexec\"\r\n" +
                        "\t\t, \"/i\"\r\n" +
                        "\t\t, \"@TargetDir@\\\\" +
                        name +
                        "\"\r\n" +
                        "\t\t, \"/quiet\"\r\n" +
                        "\t\t, \"UNDOEXECUTE\"\r\n" +
                        "\t\t, \"msiexec\"\r\n" +
                        "\t\t, \"/qb\"\r\n" +
                        "\t\t, \"/x\"\r\n" +
                        "\t\t, \"@TargetDir@\\\\" +
                        name +
                        "\")\r\n" +
                        "    } else {\r\n" +
                        "\t\t //Kijken wat de beste manier is voor linux\r\n" +
                        "\t}"
        );
    }

    private void writeFirstBlock(PrintWriter writer) {
        writer.println(
                "function Component()\r\n" +
                        "{\r\n" +
                        "}\r\n"
        );
        writer.println(
                "Component.prototype.createOperations = function()\r\n" +
                        "{\r\n" +
                        "\tcomponent.createOperations();\r\n" +
                        "\r\n"
        );
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

    public static void createMessage(String s) {
        Notifications.create()
                .title("Error")
                .text(s)
                .showWarning();
    }
}
