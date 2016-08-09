function Component()
{
    //Default component
	//Script van zip
}

Component.prototype.createOperations = function()
{
    // call default implementation to actually install README.txt!
    component.createOperations();

    if (systemInfo.productType === "windows") {
		component.addOperation("Execute"
		, "cmd"
		, "/c"
		, "C:\\\"Program Files\"\\WinRAR\\WinRAR.exe"
		, "x"
		, "@TargetDir@\\scp.py-master.zip"
		, "@TargetDir@"
		, "UNDOEXECUTE"
		, "cmd"
		, "/c"
		, "rm"
		, "/f"
		, "@TargetDir@\\scp.py-master.zip")
	
		//component.addOperation("Execute"
		//, "msiexec"
		//, "/i"
		//, "@TargetDir@\\python-2.7.3.msi"
		//, "UNDOEXECUTE"
		//, "msiexec"
		//, "/qb"
		//, "/x"
		//, "@TargetDir@\\python-2.7.3.msi")
    }
}
