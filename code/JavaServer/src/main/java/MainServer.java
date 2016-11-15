import Database.Database;
import Server.ServerController;
import javafx.application.Application;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;

import java.io.IOException;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
public class MainServer extends Application{
    public static void main(String[] args) {
        System.out.println("Booting Server");
        launch(args);
    }

    public void start(Stage primaryStage) throws Exception {
        try {
            //Laden van de fxml file waarin alle gui elementen zitten
            FXMLLoader loader = new FXMLLoader();
            Parent root = (Parent) loader.load(getClass().getClassLoader().getResource("Server.fxml").openStream());

            //Setten van enkele elementen van het hoofdscherm
            primaryStage.setTitle("StatusServer");
            primaryStage.setScene(new Scene(root));
            primaryStage.show();

            //Ophalen van de controller horende bij de view klasse
            ServerController serverController = loader.<ServerController>getController();
            assert (serverController != null);

            Database data = new Database();
            serverController.setDatabase(data);
            serverController.initData();
            data.addObserver(serverController);

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
