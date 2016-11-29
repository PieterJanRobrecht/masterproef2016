package InstallerMaker;

import Main.Database;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
public class InstallerCreator {
    private Stage lobbyStage;
    private Database database;
    private File installFolder;

    public InstallerCreator(Stage lobbyStage, Database database, File folder) {
        this.lobbyStage = lobbyStage;
        this.database = database;
        installFolder = folder;
        createTempFolder();
        setView("Installer.fxml");
    }

    private void createTempFolder() {
        File temp = new File(installFolder, "temp");
        installFolder = temp;
        File config = new File(temp, "config");
        File packages = new File(temp, "packages");
        try {
            Files.createDirectories(temp.toPath());
            Files.createDirectories(config.toPath());
            Files.createDirectories(packages.toPath());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private void setView(String s) {
        Stage stage;
        Parent root = null;

        //get reference to the button's stage
        stage = lobbyStage;
        stage.setTitle("New InstallerMaker");
        FXMLLoader loader = new FXMLLoader();

        try {
            //root = FXMLLoader.load(getClass().getResource("Lobby.fxml"));
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
        installerController.setFolder(installFolder);

    }

}
