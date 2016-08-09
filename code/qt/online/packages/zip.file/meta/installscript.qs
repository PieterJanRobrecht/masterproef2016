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
		, "@TargetDir@\\pyusb-1.0.0a2.zip"
		, "@TargetDir@")
	
		component.addOperation("Execute"
		, "cmd"
		, "cd"
		, "@TargetDir@\\pyusb-1.0.0a2"
		, "&&"
		, "cmd"
		, "/c"
		, "C:\\Python27\\python.exe"
		, "setup.py"
		, "install")
    }
}
