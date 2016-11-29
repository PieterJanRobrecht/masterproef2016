package Model;

import java.io.Serializable;

/**
 * Created by Pieter-Jan on 29/11/2016.
 */
public class Deployment implements Serializable {
    private static final long serialVersionUID = 1L;
    private Installer installer;

    public Deployment(Installer installer) {
        this.installer = installer;
    }

    public Installer getInstaller() {
        return installer;
    }

    public void setInstaller(Installer installer) {
        this.installer = installer;
    }
}
