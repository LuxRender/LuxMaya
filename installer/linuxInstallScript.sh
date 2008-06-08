#/bin/bash
#######################################
# Introduction
#######################################
echo LuxMaya Installer
echo

#######################################
# decompress the source
#######################################
echo Extracting source files...
tar -zxvf LuxMaya_src.tar.gz > /dev/null
echo ...done
echo

#######################################
# Define the functions
#######################################
# create directories
function lux_create_directories {

	echo Creating directories...
	mkdir -p "$HOME/maya/$MAYA_VER/scripts/LuxMaya/icons"
	mkdir -p "$HOME/maya/$MAYA_VER/scripts/LuxMaya/luxPlugin"
	echo ...done
}

# .mel script installer
function lux_install_scripts {
	echo Installing .mel Scripts...
	echo ... Copy files
	cp src/Mel/* "$HOME/maya/$MAYA_VER/scripts/LuxMaya/"

	if [ -e "$HOME/maya/$MAYA_VER/Maya.env" ]; then
		if grep MAYA_SCRIPT_PATH "$HOME/maya/$MAYA_VER/Maya.env"; then
			if [ ! -e "$HOME/maya/$MAYA_VER/Maya.env.luxbak" ]; then
				echo ... Backup Maya.env to Maya.env.luxbak
				cp "$HOME/maya/$MAYA_VER/Maya.env" "$HOME/maya/$MAYA_VER/Maya.env.luxbak"
			fi
			echo ... UPDATE MAYA_SCRIPT_PATH in Maya.env
			cp "$HOME/maya/$MAYA_VER/Maya.env" "$HOME/maya/$MAYA_VER/Maya.env.src"
			sed 's:^MAYA_SCRIPT_PATH\( *\)=\( *\)\(.*\)$:MAYA_SCRIPT_PATH = '"$HOME"'/maya/'"$MAYA_VER"'/scripts/LuxMaya\:\3:' < "$HOME/maya/$MAYA_VER/Maya.env.src" > "$HOME/maya/$MAYA_VER/Maya.env"
			rm "$HOME/maya/$MAYA_VER/Maya.env.src"
		else
			echo ... Append MAYA_SCRIPT_PATH to Maya.env
			echo "MAYA_SCRIPT_PATH = $HOME/maya/$MAYA_VER/scripts/LuxMaya/" >> "$HOME/maya/$MAYA_VER/Maya.env"
		fi
		
		if ! grep LUX_SEARCHPATH "$HOME/maya/$MAYA_VER/Maya.env"; then
			echo ... Add LUX_SEARCHPATH to Maya.env
			echo "LUX_SEARCHPATH = $LUX_DIR" >> "$HOME/maya/$MAYA_VER/Maya.env"
		fi
		
	else
		echo ... Create MAYA_SCRIPT_PATH and LUX_SEARCHPATH in Maya.env
		echo "MAYA_SCRIPT_PATH = $HOME/maya/$MAYA_VER/scripts/LuxMaya/" > "$HOME/maya/$MAYA_VER/Maya.env"
		echo "LUX_SEARCHPATH = $LUX_DIR" >> "$HOME/maya/$MAYA_VER/Maya.env"
	fi

}

# icons installer
function lux_install_icons {
	echo Installing GUI Icons...
	echo ... Copy files
	cp src/icons/*.xpm "$HOME/maya/$MAYA_VER/scripts/LuxMaya/icons/"

	if grep XBMLANGPATH "$HOME/maya/$MAYA_VER/Maya.env"; then
		echo ... Update XBMLANGPATH in Maya.env
		cp "$HOME/maya/$MAYA_VER/Maya.env" "$HOME/maya/$MAYA_VER/Maya.env.src"
		sed 's:^XBMLANGPATH\( *\)=\( *\)\(.*\)$:XBMLANGPATH = '"$HOME"'/maya/'"$MAYA_VER"'scripts/LuxMaya/icons%B\:\3:' < "$HOME/maya/$MAYA_VER/Maya.env.src" > "$HOME/maya/$MAYA_VER/Maya.env"
		rm "$HOME/maya/$MAYA_VER/Maya.env.src"
	else
		echo ... Append XBMLANGPATH to Maya.env
		echo "XBMLANGPATH = $HOME/maya/$MAYA_VER/scripts/LuxMaya/icons/%B" >> "$HOME/maya/$MAYA_VER/Maya.env"
	fi
	echo ...done
}

# presets installer
function lux_install_presets {
	echo Installing presets...
	echo ... Copy files
	cp -r src/attrPresets/* "$HOME/maya/$MAYA_VER/presets/attrPresets/"
	echo ...done
}

# plugin installer
function lux_install_plugin {
	echo Installing luxPlugin...
	echo ... Copy files

	cd luxPlugin/
	# recursive copy of only .py files !
	for i in `find . -name "*.py"`; do cp --parents $i "$HOME/maya/$MAYA_VER/scripts/LuxMaya/luxPlugin/"; done
	cd ../
	
	if grep MAYA_PLUG_IN_PATH "$HOME/maya/$MAYA_VER/Maya.env"; then
		cp "$HOME/maya/$MAYA_VER/Maya.env" "$HOME/maya/$MAYA_VER/Maya.env.src"
		echo ... UPDATE MAYA_PLUG_IN_PATH in Maya.env
		sed 's:^MAYA_PLUG_IN_PATH\( *\)=\( *\)\(.*\)$:MAYA_PLUG_IN_PATH = '"$HOME"'/maya/'"$MAYA_VER"'/scripts/LuxMaya/luxPlugin\:\3:' < "$HOME/maya/$MAYA_VER/Maya.env.src" > "$HOME/maya/$MAYA_VER/Maya.env"
		rm "$HOME/maya/$MAYA_VER/Maya.env.src"
	else
		echo ... Append MAYA_PLUG_IN_PATH to Maya.env
		echo "MAYA_PLUG_IN_PATH = $HOME/maya/$MAYA_VER/scripts/LuxMaya/luxPlugin/" >> "$HOME/maya/$MAYA_VER/Maya.env"
	fi

	# create entry in $HOME/maya/$MAYA_VER/prefs/pluginPrefs.mel
	if ! grep luxPlugin "$HOME/maya/$MAYA_VER/prefs/pluginPrefs.mel"; then
		echo ... Updating $HOME/maya/$MAYA_VER/prefs/pluginPrefs.mel
		echo 'evalDeferred("autoLoadPlugin(\"\", \"luxPlugin.py\", \"luxPlugin\")");' >> "$HOME/maya/$MAYA_VER/prefs/pluginPrefs.mel"
	else
		echo ... luxPlugin already set to autoload
	fi

	echo ...done
}

#######################################
# Ask for lux location
#######################################
while :
do
#  clear
  echo -n 'Please enter the full path where you installed lux: '
  read -e x
  if [ -e "$x/luxrender" -o -e "$x/luxconsole" ]; then
	LUX_DIR=$x
	echo Lux found in $LUX_DIR
	echo
	break
  else
	echo Lux not found there, try again
  fi
done

#######################################
# Execute the relevant functions
#######################################
MAYA_VERSIONS="8.5 8.5-x64 2008 2008-x64"
o_PS3=$PS3
PS3="Select your maya version: "
select mv in $MAYA_VERSIONS; do
	if [ "$mv" == "8.5" ]; then
		MAYA_VER="8.5"
		lux_create_directories
		lux_install_scripts
		lux_install_icons
		lux_install_presets
		lux_install_plugin
		break
	elif [ "$mv" == "8.5-x64" ]; then
		MAYA_VER="8.5-x64"
		lux_create_directories
		lux_install_scripts
		lux_install_icons
		lux_install_presets
		lux_install_plugin
		break
	elif [ "$mv" == "2008" ]; then
		MAYA_VER="2008"
		lux_create_directories
		lux_install_scripts
		lux_install_icons
		lux_install_presets
		lux_install_plugin
		break
	elif [ "$mv" == "2008-x64" ]; then
		MAYA_VER="2008-x64"
		lux_create_directories
		lux_install_scripts
		lux_install_icons
		lux_install_presets
		lux_install_plugin
		break
	else
		echo Bad option, try again.
	fi
done
PS3=$o_PS3

#######################################
# Done !
#######################################
echo
echo "All Done! You can now start Maya! Enjoy."
