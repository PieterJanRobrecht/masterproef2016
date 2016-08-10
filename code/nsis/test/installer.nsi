# define installer name
OutFile "installer0.2.0.exe"
 
# set desktop as install directory
InstallDir $PROFILE\NsisExample
 
# default section start
Section
 
# define output path
SetOutPath $INSTDIR
 
# specify file to go in output path
File python-2.7.3.msi
File pyusb-1.0.0a2.zip
 
# define uninstaller name
WriteUninstaller $INSTDIR\uninstaller.exe
 
 
#-------
# default section end
SectionEnd

Section

ExecWait '"msiexec" /i "$INSTDIR\python-2.7.3.msi" /quiet'

SectionEnd

Section

ZipDLL::extractall "$INSTDIR\pyusb-1.0.0a2.zip" "$INSTDIR"

ExecWait 'cmd /K "cd "$INSTDIR\pyusb-1.0.0a2" && "C:\Python27\python.exe" "setup.py" install && exit"'

SectionEnd
 
# create a section to define what the uninstaller does.
# the section will always be named "Uninstall"
Section "Uninstall"
 
ExecWait '"msiexec" /i "$INSTDIR\python-2.7.3.msi"'
 
# Always delete uninstaller first
Delete $INSTDIR\uninstaller.exe
 
# now delete installed file
Delete $INSTDIR\python-2.7.3.msi
Delete $INSTDIR\pyusb-1.0.0a2.zip

RMDir /r $INSTDIR\pyusb-1.0.0a2
 
SectionEnd