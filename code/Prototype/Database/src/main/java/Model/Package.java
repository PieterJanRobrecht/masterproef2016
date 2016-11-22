package Model;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
@XmlRootElement(name = "Package")
public class Package {
    private int id;

    private String packageName;

    private String description;

    private String packageVersionNumber;

    private int priority;

    private String diskLocation;

    public Package() {
    }

    public Package(int id, String number, String name, String location, int priority, String description) {
        this.id = id;
        packageName = name;
        packageVersionNumber = number;
        diskLocation = location;
        this.priority = priority;
        this.description = description;
    }

    public int getId() {
        return id;
    }

    @XmlTransient
    public void setId(int id) {
        this.id = id;
    }

    public String getPackageName() {
        return packageName;
    }

    @XmlElement(name = "DisplayName")
    public void setPackageName(String packageName) {
        this.packageName = packageName;
    }

    public String getDescription() {
        return description;
    }

    @XmlElement(name = "Description")
    public void setDescription(String description) {
        this.description = description;
    }

    public String getPackageVersionNumber() {
        return packageVersionNumber;
    }

    @XmlElement(name = "Version")
    public void setPackageVersionNumber(String packageVersionNumber) {
        this.packageVersionNumber = packageVersionNumber;
    }

    public int getPriority() {
        return priority;
    }

    @XmlElement(name = "SortingPriority")
    public void setPriority(int priority) {
        this.priority = priority;
    }

    public String getDiskLocation() {
        return diskLocation;
    }

    @XmlTransient
    public void setDiskLocation(String diskLocation) {
        this.diskLocation = diskLocation;
    }
}
