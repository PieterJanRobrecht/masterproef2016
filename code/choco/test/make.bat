cd python
del *.nupkg
choco pack
cd ..\pyusb
del *.nupkg
choco pack
cd ..
@pause
cls