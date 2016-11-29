package RMI;

import Client.State;
import Model.Deployment;
import Model.Package;
import com.sun.org.apache.regexp.internal.RE;

import java.rmi.Remote;
import java.rmi.RemoteException;
import java.util.List;
import java.util.UUID;

/**
 * Created by Pieter-Jan on 29/11/2016.
 */
public interface IServerMethod extends Remote {
    List<Package> getPackages(int id) throws RemoteException;
    void setStatus(UUID clientID, String s) throws RemoteException;
    Deployment getLatestDeployment() throws RemoteException;
    void createClient(UUID state) throws RemoteException;
    void setVersion(UUID clientID, int installerVersion) throws RemoteException;
}
