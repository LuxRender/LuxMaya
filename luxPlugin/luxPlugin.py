# ------------------------------------------------------------------------------
# Lux exporter python script plugin for Maya
#
# Based on a translation of the c++ luxmaya exporter, in turn based on
# maya-pbrt by Mark Colbert
#
# Python translation by Doug Hammond 02/2008
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# This script loads the various commands and nodes to allow lux integration into Maya.
# This file is purely a loader, all the real classes are in the Lux package. 
#
# ------------------------------------------------------------------------------

#Maya
from maya import OpenMaya
from maya import OpenMayaMPx
from maya import cmds
from maya import mel

#GUI/Commands
from Lux.LuxCommands.lux_gui import lux_gui
from Lux.LuxCommands.luxbatch import luxbatch
#from Lux.LuxMiscModules.geoSunData import updateSunNode

# ------------------------------------------------------------------------------

# Global list of commands that we want to register with Maya.
luxCommands = [
    lux_gui,
    luxbatch
]

# We need to know the node types when registering, so provide a dict
# of the nodes and their types.
luxNodes = {}

# This is now done 'dynamically' in the Registry. (ok, it's manual, the
# dynamic importer doesn't work, but at least all the imports are in one
# place now)
from Lux import Registry as LR
luxNodes.update(LR.Shaders().all())
luxNodes.update(LR.Locators().all())
luxNodes.update(LR.Textures().all())

# initialize the script plug-ins
def initializePlugin(mobject):
    """
    Start the plugin by registering all commands and nodes etc that this plugin provides
    """
    
    mplugin = OpenMayaMPx.MFnPlugin(mobject, "Lux (D Hammond)", "0.6", "Any")
    try:

        # Register commands
        for command in luxCommands:
            mplugin.registerCommand( command.commandName(), command.commandCreator )

        #Register nodes
        for node in luxNodes:
            mplugin.registerNode(
                node.nodeName(),
                node.nodeId(),
                node.nodeCreator,
                node.nodeInitializer,
                luxNodes[node],
                node.nodeClassify()
            )
        
        if OpenMaya.MGlobal.mayaState() == OpenMaya.MGlobal.kInteractive:
            # Create Lux menu
            lg = lux_gui()
            lg.makeMainMenu()
        else:
            OpenMaya.MGlobal.displayInfo('LuxMaya: Plugin loaded in console mode')

        # OpenMaya.MGlobal.displayInfo("Plugin Loaded OK.")
    except:
        OpenMaya.MGlobal.displayError( "Failed to register Lux Plugin" )
        raise

# uninitialize the script plug-in
def uninitializePlugin(mobject):
    """
    Unregister all commands and nodes etc that the initializePlugin() method registered with Maya
    """
     
    mplugin = OpenMayaMPx.MFnPlugin(mobject)
    try:
        # deregister commands
        for command in luxCommands:
            mplugin.deregisterCommand ( command.commandName() )
    
        # deregister nodes
        for node in luxNodes:
            mplugin.deregisterNode( node.nodeId() )

        # OpenMaya.MGlobal.displayInfo("Plugin Removed OK.")
    except:
        OpenMaya.MGlobal.displayError( "Failed to deregister plugin" )
        raise