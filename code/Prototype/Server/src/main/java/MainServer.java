import Main.Database;
import Model.Deployment;
import RMI.ServerMethod;
import Server.ServerController;
import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;

import java.io.IOException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
public class MainServer extends Application{

    private static final int SERVERPOORT = 7854;

    public static void main(String[] args) {
        System.out.println("Booting Client");
        launch(args);
    }

    public void start(Stage primaryStage) throws Exception {
        Database data = new Database();

        try {
            //Laden van de fxml file waarin alle gui elementen zitten
            FXMLLoader loader = new FXMLLoader();
            Parent root = loader.load(getClass().getClassLoader().getResource("Server.fxml").openStream());

            //Setten van enkele elementen van het hoofdscherm
            primaryStage.setTitle("StatusServer");
            primaryStage.setScene(new Scene(root));
            primaryStage.show();

            //Ophalen van de controller horende bij de view klasse
            ServerController serverController = loader.<ServerController>getController();
            assert (serverController != null);

            startRegistry(data);
            serverController.setDatabase(data);
            serverController.initData();
            data.addObserver(serverController);

        } catch (IOException e) {
            e.printStackTrace();
        }

        primaryStage.setOnCloseRequest(new EventHandler<WindowEvent>() {
            @Override
            public void handle(WindowEvent event) {
                data.save();
                System.exit(0);
            }
        });
    }

    private void startRegistry(Database database) {
        try {
            Registry registry = LocateRegistry.createRegistry(SERVERPOORT);

            // create a new service named CounterService
            registry.rebind("ServerService", new ServerMethod(database));
        } catch (Exception e) {
            e.printStackTrace();
        }
    }
}
