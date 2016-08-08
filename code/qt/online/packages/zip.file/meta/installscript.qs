function Component()
{
    //Default component
}

Component.prototype.createOperations = function()
{
    // call default implementation to actually install README.txt!
    component.createOperations();

    if (systemInfo.productType === "windows") {
        component.addOperation("Extract", "@TargetDir@\\scp.py-master.zip", "/tmp");
		component.addOperation("Execute"
		, "msiexec"
		, "python"
		, "/i"
		, "@TargetDir@\\scp.py-maste\\setup.py"
		, "install"
		, "UNDOEXECUTE"
		, "msiexec"
		, "/qb"
		, "/x"
		, "@TargetDir@\\scp.py-maste\\setup.py");
    }
}
