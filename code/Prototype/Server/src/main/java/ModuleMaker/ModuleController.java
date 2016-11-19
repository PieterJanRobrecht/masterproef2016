package ModuleMaker;

import Main.Database;
import javafx.application.Platform;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TextField;
import javafx.stage.FileChooser;
import org.apache.commons.io.FileUtils;
import org.controlsfx.control.Notifications;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.StandardCopyOption;

import static java.nio.file.Files.createDirectories;
import static java.nio.file.StandardCopyOption.*;

public class ModuleController {

    @FXML
    private ComboBox<String> moduleType;

    @FXML
    private TextField moduleName;

    @FXML
    private TextField fileLocation;

    private final String[] supportedTypes = {".exe", ".zip"};
    private Database database;
    private File folder;
    private File moduleBase;
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
        folder = new File(folder, "packages");
        //TODO beveiligen op niet invullen van gegevens
        if (file == null){
            File check =new File(fileLocation.getText());
            if(check.exists()){
                file = check;
            }else{
                Notifications.create()
                        .title("Error")
                        .text("File bestaat niet")
                        .showWarning();
            }
        }

        String name = moduleName.getText();
        //TODO kijken naar keuze voor het bepalen van handeling
        createModuleFolders(name);
        copyFile();
        makeMetaXml();
        makeScript();
    }

    private void makeScript() {
        //TODO script maken (dikke miserie)
    }

    private void makeMetaXml() {
        //TODO Meta XML schrijven
    }

    private void copyFile() {
        String[] split = file.toString().split("\\\\");
        String fileName = split[split.length-1];
        System.out.println(fileName);
        File file = new File(data, fileName);
        try {
            file.createNewFile();
            Files.copy(this.file.toPath(),file.toPath(),StandardCopyOption.REPLACE_EXISTING);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void createModuleFolders(String name) {
        moduleBase = new File(folder, name);
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

    public void initData() {
        for (int i = 0;i<supportedTypes.length;i++){
            moduleType.getItems().add(supportedTypes[i]);
        }
    }

    public void setDatabase(Database database) {
        this.database = database;
    }


    public void setFolder(File folder) {
        this.folder = folder;
    }
}
