function Component()
{
    //Default component
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
		, "UNDOEXECUTE"
		, "msiexec"
		, "/qb"
		, "/x"
		, "@TargetDir@\\python-2.7.3.msi")
    }
}
