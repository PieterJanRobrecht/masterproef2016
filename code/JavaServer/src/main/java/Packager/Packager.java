package Packager;

import Database.Database;
import Server.ServerController;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
public class Packager {
    private Stage lobbyStage;
    private Database database;

    public Packager(Stage lobbyStage, Database database) {
        this.lobbyStage = lobbyStage;
        this.database = database;
        setView("Packager.fxml");
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
        data.addObserver(packagerController);

    }

}
