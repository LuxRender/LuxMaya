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

#Commands
#from Lux.LuxMiscModules.geoSunData import updateSunNode

#Nodes
from Lux.LuxNodes.luxshader import luxshader
from Lux.LuxNodes.luxObjectLocator import luxObjectLocator
from Lux.LuxNodes.luxEnvironmentLight import luxEnvironmentLight
from Lux.LuxNodes.luxSunsky import luxSunsky

#Textures
from Lux.LuxNodes.TextureNodes.bilerpTexture import bilerpTexture
from Lux.LuxNodes.TextureNodes.blenderCloudsTexture import blenderCloudsTexture
from Lux.LuxNodes.TextureNodes.blenderMarbleTexture import blenderMarbleTexture
from Lux.LuxNodes.TextureNodes.blenderMusgraveTexture import blenderMusgraveTexture
from Lux.LuxNodes.TextureNodes.blenderWoodTexture import blenderWoodTexture
from Lux.LuxNodes.TextureNodes.checkerboard2dTexture import checkerboard2dTexture
from Lux.LuxNodes.TextureNodes.checkerboard3dTexture import checkerboard3dTexture
from Lux.LuxNodes.TextureNodes.dotsTexture import dotsTexture
from Lux.LuxNodes.TextureNodes.fbmTexture import fbmTexture
from Lux.LuxNodes.TextureNodes.marbleTexture import marbleTexture
from Lux.LuxNodes.TextureNodes.mixTexture import mixTexture
from Lux.LuxNodes.TextureNodes.scaleTexture import scaleTexture
from Lux.LuxNodes.TextureNodes.windyTexture import windyTexture
from Lux.LuxNodes.TextureNodes.wrinkledTexture import wrinkledTexture

#GUI/Commands
from Lux.LuxCommands.lux_gui    import lux_gui
from Lux.LuxCommands.luxbatch   import luxbatch

# ------------------------------------------------------------------------------

# Global list of commands that we want to register with Maya.
luxCommands= [
			  lux_gui,
			  luxbatch
			 ]

# We need to know the node types when registering, so provide a dict
# of the nodes and their types.
luxNodes = {
		    # shaders
			luxshader: OpenMayaMPx.MPxNode.kDependNode,
			
			# locators / lights
			luxObjectLocator: OpenMayaMPx.MPxNode.kLocatorNode,
			luxEnvironmentLight: OpenMayaMPx.MPxNode.kLocatorNode,
			luxSunsky: OpenMayaMPx.MPxNode.kLocatorNode,
			
			# textures
			bilerpTexture: OpenMayaMPx.MPxNode.kDependNode,
			blenderCloudsTexture: OpenMayaMPx.MPxNode.kDependNode,
			blenderMarbleTexture: OpenMayaMPx.MPxNode.kDependNode,
			blenderMusgraveTexture: OpenMayaMPx.MPxNode.kDependNode,
			blenderWoodTexture: OpenMayaMPx.MPxNode.kDependNode,
			checkerboard2dTexture: OpenMayaMPx.MPxNode.kDependNode,
			checkerboard3dTexture: OpenMayaMPx.MPxNode.kDependNode,
			dotsTexture: OpenMayaMPx.MPxNode.kDependNode,
			fbmTexture: OpenMayaMPx.MPxNode.kDependNode,
			marbleTexture: OpenMayaMPx.MPxNode.kDependNode,
			mixTexture: OpenMayaMPx.MPxNode.kDependNode,
			scaleTexture: OpenMayaMPx.MPxNode.kDependNode,
			windyTexture: OpenMayaMPx.MPxNode.kDependNode,
			wrinkledTexture: OpenMayaMPx.MPxNode.kDependNode
		   }

# initialize the script plug-ins
def initializePlugin(mobject):
	"""
	Start the plugin by registering all commands and nodes etc that this plugin provides
	"""
	
	mplugin = OpenMayaMPx.MFnPlugin(mobject, "Lux (D Hammond)", "1.0", "Any")
	try:

		# Register commands
		for command in luxCommands:
			mplugin.registerCommand( command.commandName(), command.commandCreator )

		#Register nodes
		for node in luxNodes:
			mplugin.registerNode( node.nodeName(),
								  node.nodeId(),
								  node.nodeCreator,
								  node.nodeInitializer,
								  luxNodes[node],
								  node.nodeClassify() )
		
		# Create Lux menu
		lg = lux_gui()
		lg.makeMainMenu()

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
		
		