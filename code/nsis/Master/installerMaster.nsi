; HM NIS Edit Wizard helper defines
!define PRODUCT_NAME "Framework_Installer"
!define PRODUCT_VERSION "0.1"
!define PRODUCT_PUBLISHER "PIETER-JAN ROBRECHT"
 
SetCompressor lzma
 
#!include "UserManagement.nsh"
 
 
; MUI 1.67 compatible ------
!include "MUI.nsh"
 
; MUI Settings
!define MUI_ABORTWARNING
!define MUI_ICON "${NSISDIR}\Contrib\Graphics\Icons\modern-install.ico"
 
; Welcome page
!insertmacro MUI_PAGE_WELCOME
; Components page
!insertmacro MUI_PAGE_COMPONENTS
; Instfiles page
!insertmacro MUI_PAGE_INSTFILES
; Finish page
!insertmacro MUI_PAGE_FINISH
 
; Language files
!insertmacro MUI_LANGUAGE "English"
 
; Reserve files
!insertmacro MUI_RESERVEFILE_INSTALLOPTIONS
 
; MUI end ------
	;Name "${PRODUCT_NAME} ${PRODUCT_VERSION}"
	OutFile "frameworkInstaller.exe"
	InstallDir "$PROGRAMFILES\Framework"
	ShowInstDetails show

	Section
	# create the uninstaller
	WriteUninstaller "$INSTDIR\uninstall.exe"

	# create a shortcut named "new shortcut" in the start menu programs directory
	# point the new shortcut at the program uninstaller
	CreateShortCut "$SMPROGRAMS\new shortcut.lnk" "$INSTDIR\uninstall.exe"
SectionEnd
	
Section -SETTINGS
  SetOutPath "$INSTDIR"
  SetOverwrite ifnewer
SectionEnd

Section "python" SEC01
  File "python libs\python-2.7.3.msi"
  ExecWait 'msiexec /i "$INSTDIR\python-2.7.3.msi" /passive '
SectionEnd

# uninstaller section start
Section "uninstall"
 
    # first, delete the uninstaller
    Delete "$INSTDIR\uninstall.exe"
 
    # second, remove the link from the start menu
    Delete "$SMPROGRAMS\new shortcut.lnk"
 
# uninstaller section end
SectionEnd