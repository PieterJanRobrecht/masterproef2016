package Model;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
public class Installer {
    private String diskLocation;
    private final int id;
    private String versionNumber;

    public Installer(int id, String version, String disk) {
        this.id = id;
        this.versionNumber = version;
        this.diskLocation = disk;
    }

    public String getDiskLocation() {
        return diskLocation;
    }

    public void setDiskLocation(String diskLocation) {
        this.diskLocation = diskLocation;
    }

    public int getId() {
        return id;
    }

    public String getVersionNumber() {
        return versionNumber;
    }

    public void setVersionNumber(String versionNumber) {
        this.versionNumber = versionNumber;
    }
}
