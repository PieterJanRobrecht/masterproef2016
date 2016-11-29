package RMI;

import Main.Database;
import Model.Deployment;
import Model.Package;

import java.rmi.RemoteException;
import java.rmi.server.UnicastRemoteObject;
import java.util.List;
import java.util.UUID;

/**
 * Created by Pieter-Jan on 29/11/2016.
 */
public class ServerMethod extends UnicastRemoteObject implements IServerMethod {
    private Database database;

    public ServerMethod(Database database) throws RemoteException {
        this.database = database;
    }


    @Override
    public List<Package> getPackages(int id) throws RemoteException {
        return database.getPackages(id);
    }

    @Override
    public void setStatus(UUID clientID, String s) throws RemoteException {
        database.setStatus(clientID,s);
    }

    @Override
    public Deployment getLatestDeployment() throws RemoteException {
        return database.getActiveInstaller();
    }

    @Override
    public void createClient(UUID state) throws RemoteException {
        database.createClient(state);
    }

    @Override
    public void setVersion(UUID clientID, int installerId) throws RemoteException {
        database.setVersion(clientID,installerId);
    }

}
