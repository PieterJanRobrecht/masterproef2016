package InstallerMaker;

import Main.Database;
import Model.Package;
import PackagerMaker.PackagerCreator;
import com.sun.glass.ui.Accessible;
import javafx.event.ActionEvent;
import javafx.event.EventHandler;
import javafx.fxml.FXML;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextField;
import javafx.scene.control.cell.PropertyValueFactory;
import javafx.scene.input.MouseEvent;
import javafx.stage.Stage;

import java.io.File;
import java.util.ArrayList;
import java.util.List;
import java.util.Observable;
import java.util.Observer;

import static com.sun.xml.internal.fastinfoset.alphabet.BuiltInRestrictedAlphabets.table;

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
    private List<Package> allPackages;
    private List<Package> selectedPackages;
    private File folder;


    @FXML
    void makeNewModule(ActionEvent event) {
        PackagerCreator m = new PackagerCreator((Stage) selectedModulesTable.getScene().getWindow(), database, folder);
    }

    @FXML
    void createPackage(ActionEvent event) {

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
        allPackages = database.getPackages();
        allModulesTable.getItems().setAll(allPackages);

        selectedPackages = new ArrayList<>();
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
