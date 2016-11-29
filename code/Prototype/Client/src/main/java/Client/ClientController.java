package Client;

import Model.Deployment;
import Model.Installer;
import Model.Package;
import PackagerMaker.PackagerController;
import RMI.IServerMethod;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.scene.control.Label;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.cell.PropertyValueFactory;

import java.io.*;
import java.rmi.RemoteException;
import java.util.List;

public class ClientController {
    @FXML
    private Label currentNameLabel;

    @FXML
    private Label currentVersionLabel;

    @FXML
    private TableView<Package> currentTable;

    @FXML
    private TableColumn<Package, String> currentPackageName;

    @FXML
    private TableColumn<Package, String> currentPackageVersion;

    @FXML
    private Label newNameLabel;

    @FXML
    private Label newVersionLabel;

    @FXML
    private TableView<Package> newTable;

    @FXML
    private TableColumn<Package, String> newPackageName;

    @FXML
    private TableColumn<Package, String> newPackageVersion;
    private IServerMethod implementation;
    private State state;
    private Deployment newDeployment;

    @FXML
    void checkUpdate(ActionEvent event) {
        Deployment check = null;
        try {
            check = implementation.getLatestDeployment();
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        if (check !=null && check.getInstaller() == null) {
            PackagerController.createMessage("No installers available on the server");
        } else if (state.getCurrentDeployment() != null && state.getCurrentDeployment().getInstaller().getId() == check.getInstaller().getId()) {
            PackagerController.createMessage("No new version available");
        } else {
            PackagerController.createMessage("New version available");
            newDeployment = check;
            setNewData();
        }
    }

    @FXML
    void installNew(ActionEvent event) {
        try {
            implementation.setStatus(state.getClientID(), "Installing");
            //TODO effectief installeren van het programma
            Thread.sleep(3000);
        } catch (RemoteException e) {
            e.printStackTrace();
        } catch (InterruptedException e) {
            e.printStackTrace();
        }
        state.setCurrentDeployment(newDeployment);
        newDeployment = null;
        setNewData();
        setCurrentData();
        try {
            implementation.setStatus(state.getClientID(), "Running");
            implementation.setVersion(state.getClientID(), state.getCurrentDeployment().getInstaller().getId());
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }

    @FXML
    public void initialize() {
        currentPackageName.setCellValueFactory(new PropertyValueFactory<Package, String>("packageName"));
        currentPackageVersion.setCellValueFactory(new PropertyValueFactory<Package, String>("packageVersionNumber"));

        newPackageName.setCellValueFactory(new PropertyValueFactory<Package, String>("packageName"));
        newPackageVersion.setCellValueFactory(new PropertyValueFactory<Package, String>("packageVersionNumber"));
    }

    public void initData() {
        loadState();
        try {
            if (checkInstalled()) {
                setCurrentData();
            }
            implementation.setStatus(state.getClientID(), "Running");
        } catch (RemoteException e) {
            e.printStackTrace();
        }

    }

    private boolean checkInstalled() throws RemoteException {
        boolean firstBoot = true;
        if (state.getCurrentDeployment() != null) {
            Deployment check = null;
            check = implementation.getLatestDeployment();
            if (state.getCurrentDeployment().getInstaller().getId() == check.getInstaller().getId()) {
                PackagerController.createMessage("No new version available");
            } else {
                PackagerController.createMessage("New version available");
                setNewData();
            }
        } else {
            PackagerController.createMessage("No version installed");
            //TODO laatste versie downloaden en installeren
            //nu gedaan met fake
            newDeployment = implementation.getLatestDeployment();
            setNewData();
            firstBoot = false;
        }
        return firstBoot;
    }

    private void setNewData() {
        if (newDeployment != null && newDeployment.getInstaller() != null) {
            newNameLabel.setText(newDeployment.getInstaller().getInstallerName());
            newVersionLabel.setText(newDeployment.getInstaller().getInstallerVersion());

            List<Package> packageList = getPackages(newDeployment.getInstaller());
            newTable.getItems().addAll(packageList);
        } else {
            newNameLabel.setText("");
            newVersionLabel.setText("");

            newTable.getItems().clear();
        }
    }

    private void setCurrentData() {
        if (state != null) {
            Installer i = state.getCurrentDeployment().getInstaller();
            currentNameLabel.setText(i.getInstallerName());
            currentVersionLabel.setText(i.getInstallerVersion());

            List<Package> packageList = getPackages(i);
            currentTable.getItems().clear();
            currentTable.getItems().addAll(packageList);
        }
    }

    private List<Package> getPackages(Installer i) {
        List<Package> packages = null;
        try {
            packages = implementation.getPackages(i.getId());
        } catch (RemoteException e) {
            e.printStackTrace();
        }
        return packages;
    }

    public void saveState() {
        try {
            File file = new File(new File("."), "clientState.ser");
            file.createNewFile();
            FileOutputStream myFileOutputStream = new FileOutputStream(file);
            ObjectOutputStream myObjectOutputStream = new ObjectOutputStream(myFileOutputStream);
            myObjectOutputStream.writeObject(state);
            myObjectOutputStream.close();
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void loadState() {
        try {
            File file = new File(new File("."), "clientState.ser");
            if (file.exists()) {
                FileInputStream myFileInputStream = new FileInputStream(file);
                ObjectInputStream myObjectInputStream = new ObjectInputStream(myFileInputStream);
                state = (State) myObjectInputStream.readObject();
                myObjectInputStream.close();
            } else {
                makeNewClient();
            }
        } catch (Exception e) {
            e.printStackTrace();
        }
    }

    private void makeNewClient() {
        state = new State();
        try {
            implementation.createClient(state.getClientID());
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }

    public void setImplementation(IServerMethod implementation) {
        this.implementation = implementation;
    }

    public void setStatus(String s) {
        try {
            implementation.setStatus(state.getClientID(), s);
        } catch (RemoteException e) {
            e.printStackTrace();
        }
    }
}
