package Packager;

import Main.Database;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
public class Packager {
    private Stage lobbyStage;
    private Database database;
    private File installFolder;

    public Packager(Stage lobbyStage, Database database, File folder) {
        this.lobbyStage = lobbyStage;
        this.database = database;
        installFolder = folder;
        createTempFolder();
        setView("Packager.fxml");
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
        stage.setTitle("New Package");
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

        PackagerController packagerController = loader.<PackagerController>getController();
        assert (packagerController != null);

        Database data = database;
        packagerController.setDatabase(data);
        packagerController.initData();
        packagerController.setFolder(installFolder);
        data.addObserver(packagerController);

    }

}
