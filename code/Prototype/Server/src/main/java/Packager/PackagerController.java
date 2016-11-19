package Packager;

import Main.Database;
import Model.Module;
import ModuleMaker.ModuleController;
import ModuleMaker.ModuleCreator;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.stage.Stage;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Observable;
import java.util.Observer;

public class PackagerController implements Observer{

    @FXML
    private TableView<Module> allModulesTable;

    @FXML
    private TableColumn<Module, String> allName;

    @FXML
    private TableColumn<Module, String> allVersion;

    @FXML
    private TableView<Module> selectedModulesTable;

    @FXML
    private TableColumn<Module, String> selectedName;

    @FXML
    private TableColumn<Module, String> selectedVersion;

    private Database database;
    private List<Module> allModules;
    private List<Module> selectedModules;
    private File folder;


    @FXML
    void makeNewModule(ActionEvent event) {
        ModuleCreator m = new ModuleCreator((Stage) selectedModulesTable.getScene().getWindow(), database,folder);
    }

    @FXML
    void createPackage(ActionEvent event) {

    }

    @FXML
    public void initialize() {
        allName.setCellValueFactory(new PropertyValueFactory<>("moduleName"));
        allVersion.setCellValueFactory(new PropertyValueFactory<>("moduleNumber"));

        selectedName.setCellValueFactory(new PropertyValueFactory<>("moduleName"));
        selectedVersion.setCellValueFactory(new PropertyValueFactory<>("moduleNumber"));
    }

    public void initData() {
        allModules = database.getModules();
        allModulesTable.getItems().setAll(allModules);

        selectedModules = new ArrayList<>();
        selectedModulesTable.getItems().setAll(selectedModules);
    }

    @Override
    public void update(Observable o, Object arg) {

    }

    public void setDatabase(Database database) {
        this.database = database;
    }

    public void setFolder(File folder) {
        this.folder = folder;
    }
}
