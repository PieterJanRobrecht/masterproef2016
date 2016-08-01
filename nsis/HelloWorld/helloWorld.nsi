!include "MUI.nsh"

!insertmacro MUI_LANGUAGE "English"

Name "Hello world!" # Name of the installer.
OutFile "HelloWorld.exe" # Name of the installer's file.

Function .onInit # Function that will be executed on installer's start up.
  MessageBox MB_OK|MB_ICONINFORMATION "Hello world!" # Show a message that says "Hello world!".
  Quit # Close the installer because this is a simple "Hello world!" installer.
FunctionEnd

Section # Useless section because this is a simple "Hello world!" installer.
SectionEnd