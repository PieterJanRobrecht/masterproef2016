package Model;

/**
 * Created by Pieter-Jan on 15/11/2016.
 */
public class Module {
    private int id;
    private String moduleNumber;
    private String moduleName;
    private String diskLocation;

    public Module(int id, String number, String name, String location) {
        this.id = id;
        moduleName = name;
        moduleNumber = number;
        diskLocation = location;
    }

    public int getId() {
        return id;
    }

    public void setId(int id) {
        this.id = id;
    }

    public String getModuleNumber() {
        return moduleNumber;
    }

    public void setModuleNumber(String moduleNumber) {
        this.moduleNumber = moduleNumber;
    }

    public String getModuleName() {
        return moduleName;
    }

    public void setModuleName(String moduleName) {
        this.moduleName = moduleName;
    }

    public String getDiskLocation() {
        return diskLocation;
    }

    public void setDiskLocation(String diskLocation) {
        this.diskLocation = diskLocation;
    }
}
