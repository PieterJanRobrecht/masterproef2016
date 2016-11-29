package Client;

import Model.Deployment;

import java.io.Serializable;
import java.util.UUID;

/**
 * Created by Pieter-Jan on 29/11/2016.
 */
public class State implements Serializable{
    private static final long serialVersionUID = 3L;
    private Deployment currentDeployment;

    private UUID clientID;

    public State() {
        clientID = UUID.randomUUID();
    }

    public Deployment getCurrentDeployment() {
        return currentDeployment;
    }

    public void setCurrentDeployment(Deployment currentDeployment) {
        this.currentDeployment = currentDeployment;
    }

    public UUID getClientID() {
        return clientID;
    }

    public void setClientID(UUID clientID) {
        this.clientID = clientID;
    }
}
