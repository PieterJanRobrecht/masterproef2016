function Component()
{
    //Default component
}

Component.prototype.createOperations = function()
{
    // call default implementation to actually install README.txt!
    component.createOperations();

    if (systemInfo.productType === "windows") {
        //component.addOperation("Extract", "@TargetDir@/scp.py-master.zip", "/tmp");
		//component.addOperation("Execute","python" ,"@TargetDir@/scp.py-master/setup.py")
    }
}
