package PackagerMaker;

import Main.Database;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.File;
import java.io.IOException;

/**
 * Created by Pieter-Jan on 19/11/2016.
 */
public class PackagerCreator {
    private Stage stage;
    private Database database;
    private File installFolder;

    public PackagerCreator(Stage stage, Database database, File folder) {
        this.stage = stage;
        this.database = database;
        installFolder = folder;
        setViewModuleMaker();
    }

    private void setViewModuleMaker() {
        Parent root = null;

        //get reference to the button's stage
        stage.setTitle("New Package");
        FXMLLoader loader = new FXMLLoader();

        try {
            //root = FXMLLoader.load(getClass().getResource("Lobby.fxml"));
            root = (Parent) loader.load(getClass().getClassLoader().getResource("Package.fxml").openStream());
        } catch (IOException e) {
            e.printStackTrace();
        }

        //create a new scene with root and set the stage
        Scene scene = new Scene(root);
        stage.setScene(scene);
        stage.show();

        PackagerController packagerController = loader.getController();
        assert (packagerController != null);

        Database data = database;
        packagerController.setDatabase(data);
        packagerController.initData();
        packagerController.setFolder(installFolder);
    }
}
