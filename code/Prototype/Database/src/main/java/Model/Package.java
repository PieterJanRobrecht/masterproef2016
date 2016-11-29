package Model;

import XmlAdapter.DateAdapter;

import javax.xml.bind.annotation.XmlElement;
import javax.xml.bind.annotation.XmlRootElement;
import javax.xml.bind.annotation.XmlTransient;
import javax.xml.bind.annotation.adapters.XmlJavaTypeAdapter;
import java.io.Serializable;
import java.sql.Date;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
@XmlRootElement(name = "Package")
public class Package implements Serializable {
    private int id;

    private String packageName;

    private String description;

    private String packageVersionNumber;

    private int priority;

    private String diskLocation;

    private Date releaseDate;

    private String script;

    public Package() {
        setScript("installscript.qs");
    }

    public Package(int id, String number, String name, String location, int priority, String description, Date releaseDate) {
        this.id = id;
        packageName = name;
        packageVersionNumber = number;
        diskLocation = location;
        this.priority = priority;
        this.description = description;
        this.releaseDate = releaseDate;
        setScript("installscript.qs");
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

    public Date getReleaseDate() {
        return releaseDate;
    }

    @XmlElement(name = "ReleaseDate")
    @XmlJavaTypeAdapter(DateAdapter.class)
    public void setReleaseDate(Date releaseDate) {
        this.releaseDate = releaseDate;
    }

    public int getPriority() {
        return priority;
    }

    @XmlElement(name = "SortingPriority")
    public void setPriority(int priority) {
        this.priority = priority;
    }

    public String getScript() {
        return script;
    }

    @XmlElement(name = "Script")
    public void setScript(String script) {
        this.script = script;
    }

    public String getDiskLocation() {
        return diskLocation;
    }

    @XmlTransient
    public void setDiskLocation(String diskLocation) {
        this.diskLocation = diskLocation;
    }
}
