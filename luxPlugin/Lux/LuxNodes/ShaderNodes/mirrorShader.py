# ------------------------------------------------------------------------------
# Lux material shader node for Maya
#
# by Doug Hammond 05/2008
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# Lux material shader node for Maya ( mirror attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderColorAttribute

class mirrorShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    Mirror fragment of luxshader
    """
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # mirror
        kr            =    OpenMaya.MObject()    # color
        
        # Export attributes
        self.attributes = {}
        self.luxType = "mirror"
        self.attributes['Kr'] = ShaderColorAttribute('mirrorKr')

    @staticmethod
    def shaderInitializer():
        try:
            # reflectiviy
            mirrorShader.kr = mirrorShader.makeColor("mirrorKr", "mikr")    # mkr is already in use ??!

        except:
            OpenMaya.MGlobal.displayError("Failed to create mirror attributes\n")
            raise
