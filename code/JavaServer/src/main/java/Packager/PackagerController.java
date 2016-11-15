package Packager;

import Database.Database;
import Model.Module;
import Model.Package;
import Model.Server;
import com.sun.org.apache.xpath.internal.operations.Mod;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;

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


    @FXML
    void makeNewModule(ActionEvent event) {

    }

    @FXML
    void createPackage(ActionEvent event) {
        
    }

    @FXML
    public void initialize() {
        allName.setCellValueFactory(new PropertyValueFactory<Module, String>("moduleName"));
        allVersion.setCellValueFactory(new PropertyValueFactory<Module, String>("moduleNumber"));

        selectedName.setCellValueFactory(new PropertyValueFactory<Module, String>("moduleName"));
        selectedVersion.setCellValueFactory(new PropertyValueFactory<Module, String>("moduleNumber"));
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

}
