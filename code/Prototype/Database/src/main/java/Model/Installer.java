package Model;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
@XmlRootElement(name = "Installer")
public class Installer {
    private String diskLocation;
    private int id;
    private String installerName;
    private String installerVersion;
    private String title;
    private String publisher;
    private String startMenuDir;
    private String targetDir;
    private String executableLocation;


    public Installer(int id, String version, String disk, String name,String exe) {
        this.id = id;
        this.installerVersion = version;
        this.diskLocation = disk;
        executableLocation = exe;
        installerName = name;
    }

    public Installer() {
        setPublisher("Pieter-Jan The Awesome");
        setTitle("Python Framework Installer");
        setStartMenuDir("InstallerFolder");
        setTargetDir("@HomeDir@/FrameWork/InstallFolder");
    }

    public String getDiskLocation() {
        return diskLocation;
    }

    @XmlTransient
    public void setDiskLocation(String diskLocation) {
        this.diskLocation = diskLocation;
    }

    public int getId() {
        return id;
    }

    @XmlTransient
    public void setId(int id){
        this.id = id;
    }

    public String getInstallerName() {
        return installerName;
    }

    @XmlElement(name = "Name")
    public void setInstallerName(String installerName) {
        this.installerName = installerName;
    }

    public String getInstallerVersion() {
        return installerVersion;
    }

    @XmlElement(name = "Version")
    public void setInstallerVersion(String installerVersion) {
        this.installerVersion = installerVersion;
    }

    public String getTitle() {
        return title;
    }

    @XmlElement(name = "Title")
    public void setTitle(String title) {
        this.title = title;
    }

    public String getPublisher() {
        return publisher;
    }

    @XmlElement(name = "Publisher")
    public void setPublisher(String publisher) {
        this.publisher = publisher;
    }

    public String getStartMenuDir() {
        return startMenuDir;
    }

    @XmlElement(name = "StartMenuDir")
    public void setStartMenuDir(String startMenuDir) {
        this.startMenuDir = startMenuDir;
    }

    public String getTargetDir() {
        return targetDir;
    }

    @XmlElement(name = "TargetDir")
    public void setTargetDir(String targetDir) {
        this.targetDir = targetDir;
    }

    public String getExecutableLocation() {
        return executableLocation;
    }

    @XmlTransient
    public void setExecutableLocation(String executableLocation) {
        this.executableLocation = executableLocation;
    }
}
