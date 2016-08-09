!include ZipDLL.nsh

# define installer name
OutFile "installer0.0.5.exe"
 
# set desktop as install directory
InstallDir $PROFILE\NsisExample
 
!define TestDLL '"${NSISDIR}\Plugins\ZipDLL.dll"' 
 
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

#!insertmacro ZIPDLL_EXTRACT "$INSTDIR\pyusb-1.0.0a2.zip" "$INSTDIR" "<ALL>"
ZipDLL::extractall "$INSTDIR\pyusb-1.0.0a2.zip" "$INSTDIR"

nsExec::ExecToLog '"C:\Python27\python27" $INSTDIR\pyusb-1.0.0a2\setup.py install'
nsExec::ExecToLog 'ECHO hello'

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