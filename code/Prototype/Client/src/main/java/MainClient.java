import Client.ClientController;
import RMI.IServerMethod;
import javafx.application.Application;
import javafx.event.EventHandler;
import javafx.fxml.FXMLLoader;
import javafx.scene.Parent;
import javafx.scene.Scene;
import javafx.stage.Stage;
import javafx.stage.WindowEvent;

import java.io.IOException;
import java.rmi.NotBoundException;
import java.rmi.RemoteException;
import java.rmi.registry.LocateRegistry;
import java.rmi.registry.Registry;

/**
 * Created by Pieter-Jan on 29/11/2016.
 */
public class MainClient extends Application {
    private static final int SERVERPOORT = 7854;

    public static void main(String[] args) {
        launch(args);
    }

    @Override
    public void start(Stage primaryStage) throws Exception {
        try {
            //Laden van de fxml file waarin alle gui elementen zitten
            FXMLLoader loader = new FXMLLoader();
            Parent root = loader.load(getClass().getClassLoader().getResource("Client.fxml").openStream());

            //Setten van enkele elementen van het hoofdscherm
            primaryStage.setTitle("StatusServer");
            primaryStage.setScene(new Scene(root));
            primaryStage.show();

            //Ophalen van de controller horende bij de view klasse
            ClientController clientController = loader.<ClientController>getController();
            assert (clientController != null);

            IServerMethod impl = connectToRegistry();
            clientController.setImplementation(impl);
            clientController.initData();

            primaryStage.setOnCloseRequest(new EventHandler<WindowEvent>() {
                @Override
                public void handle(WindowEvent event) {
                    clientController.saveState();
                    clientController.setStatus("Not Connected");
                }
            });
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    private IServerMethod connectToRegistry() {
        IServerMethod impl = null;
        Registry myRegistry = null;
        try {
            myRegistry = LocateRegistry.getRegistry("localhost", SERVERPOORT);

            impl = (IServerMethod) myRegistry.lookup("ServerService");
        } catch (RemoteException | NotBoundException e) {
            e.printStackTrace();
        }
        return impl;
    }
}
