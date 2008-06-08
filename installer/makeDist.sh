#!/bin/bash

if [ ! $1 ]; then
	echo Usage: makeDish.sh version-number
	exit 1
fi

cp ../src/*.txt .

echo Making linux installer...
tar --exclude-vcs -cf - ../src/* ../luxPlugin | gzip -9 > LuxMaya_src.tar.gz
tar -cf - LuxMaya_src.tar.gz linuxInstallScript.sh | gzip -9 > payload.tar.gz

if [ -e "payload.tar.gz" ]; then
	cat linuxInstallerSrc.sh payload.tar.gz > LuxMayaInstaller.sh
else
	echo "payload.tar.gz does not exist"
	exit 1
fi
echo ...done.
echo Packaging linux installer...
zip -9 ../dist/LuxMaya-Installer-linux-$1.zip LuxMayaInstaller.sh README.txt LICENSE.txt CHANGELOG.txt
echo ...done.

echo Making windows installer...
makensis windowsInstaller.nsi > /dev/null
if [ ! -e "Setup-LuxMaya.exe" ]; then
	echo makensis failed.
	exit 1
fi
echo ...done.

echo Packaging windows installer...
zip -9 ../dist/LuxMaya-Installer-win-$1.zip Setup-LuxMaya.exe README.txt LICENSE.txt CHANGELOG.txt
echo ...done.

echo Making cross-platform .zip archive for manual install...
zip -9 -r ../dist/LuxMaya-ManualInstall-$1.zip *.txt `find ../luxPlugin -name "*.py"` `find ../src -name "*.mel"` `find ../src -name "*.xpm"`
echo ...done

rm LuxMaya_src.tar.gz payload.tar.gz LuxMayaInstaller.sh Setup-LuxMaya.exe
rm *.txt
exit 0
