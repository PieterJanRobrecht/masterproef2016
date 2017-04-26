function Component()
{
    //Default component
	//Script van exe
}

Component.prototype.createOperations = function()
{
    // call default implementation to actually install README.txt!
    component.createOperations();

    if (systemInfo.productType === "windows") {
		component.addOperation("Execute"
		, "msiexec"
		, "/i"
		, "@TargetDir@\\python-2.7.3.msi"
		, "/quiet"
		, "UNDOEXECUTE"
		, "msiexec"
		, "/qb"
		, "/x"
		, "@TargetDir@\\python-2.7.3.msi")
    } else {
		component.addOperation("Execute"
		, "tar"
		, "-xvzf"
		, "@TargetDir@/Python-2.7.11.tgz"
		, "-C"
		, "@TargetDir@/"		
		)
		component.addOperation("Execute"
		, "@TargetDir@/Python-2.7.11/configure"
		)
		component.addOperation("Execute"
		, "make"
		)
		component.addOperation("Execute"
		, "make"
		, "install"
		)	
	}
}
