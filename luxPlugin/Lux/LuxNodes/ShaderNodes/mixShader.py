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
# Lux material shader node for Maya ( mix attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class mixShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    Mix fragment of luxshader
    """
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # mix
        namedMaterial1            =    OpenMaya.MObject()    # color
        namedMaterial2            =    OpenMaya.MObject()    # color
        amount                    =    OpenMaya.MObject()    # float
        
        # Export attributes
        self.attributes = {}
        self.luxType = "mix"
        #self.attributes['namedmaterial1'] = ShaderColorAttribute('mixMat1')
        #self.attributes['namedmaterial2'] = ShaderColorAttribute('mixMat2')
        self.attributes['amount']         = ShaderFloatAttribute('mixAmount')

    @staticmethod
    def shaderInitializer():
        try:
            mixShader.namedMaterial1 = mixShader.makeColor("mixNamed1", "mn1" )
            mixShader.namedMaterial2 = mixShader.makeColor("mixNamed2", "mn2" )
            mixShader.amount         = mixShader.makeFloat("mixAmount", "ma" )

        except:
            OpenMaya.MGlobal.displayError("Failed to create mix attributes\n")
            raise

