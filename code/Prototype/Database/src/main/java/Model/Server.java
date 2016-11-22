package Model;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
public class Server {
    private int id;
    private String UID;
    private Installer installer;
    private int versionId;
    private String versionNumber;
    private String status;

    public Server(int id, String serverUID, int versionId) {
        this.id = id;
        this.UID = serverUID;
        this.versionId = versionId;
        status = "Not Connected";
    }

    public Installer getInstaller() {
        return installer;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getUID() {
        return UID;
    }

    public void setUID(String UID) {
        this.UID = UID;
    }

    public int getVersionId() {
        return versionId;
    }

    public void setVersionId(int versionId) {
        this.versionId = versionId;
    }

    public String getStatus() {
        return status;
    }

    public void setStatus(String status) {

        this.status = status;
    }

    public String getVersionNumber() {
        if(installer !=null){
            versionNumber = installer.getInstallerVersion();
        }
        return versionNumber;
    }

    public void setInstaller(Installer v) {
        this.installer = v;
    }
}
