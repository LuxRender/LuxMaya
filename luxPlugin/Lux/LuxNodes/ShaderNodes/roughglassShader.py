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
# Lux material shader node for Maya ( roughglass attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class roughglassShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    RoughGlass fragment of luxshader
    """
    
    # roughglass
    kr            =    OpenMaya.MObject()    # color
    kt            =    OpenMaya.MObject()    # color
    uroughness    =    OpenMaya.MObject()    # float
    vroughness    =    OpenMaya.MObject()    # float
    index         =    OpenMaya.MObject()    # float
    cauchyb       =    OpenMaya.MObject()    # float

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # Export attributes
        self.attributes = {}
        self.luxType = "roughglass"
        self.attributes['Kr']         = ShaderColorAttribute('roughglassKr')
        self.attributes['Kt']         = ShaderColorAttribute('roughglassKt')
        self.attributes['uroughness'] = ShaderFloatAttribute('roughglassURoughness')
        self.attributes['vroughness'] = ShaderFloatAttribute('roughglassVRoughness')
        self.attributes['index']      = ShaderFloatAttribute('roughglassIndex')
        self.attributes['cauchyb']    = ShaderFloatAttribute('roughglassCauchyB')

    @staticmethod
    def shaderInitializer():
        try:
            # surface reflectivity
            roughglassShader.kr = roughglassShader.makeColor("roughglassKr", "rgkr")

            # surface transmissivity (is that even a word?)
            roughglassShader.kt = roughglassShader.makeColor("roughglassKt", "rgkt")

            # U roughness
            roughglassShader.uroughness = roughglassShader.makeFloat("roughglassURoughness", "rgur", 0.001)

            # V roughness
            roughglassShader.vroughness = roughglassShader.makeFloat("roughglassVRoughness", "rgvr", 0.001)

            # IOR
            roughglassShader.index = roughglassShader.makeFloat("roughglassIndex", "rgi", 1.5)

            # cauchy b
            roughglassShader.cauchyb = roughglassShader.makeFloat("roughglassCauchyB", "rgcb", 0.0)

        except:
            OpenMaya.MGlobal.displayError("Failed to create roughglass attributes\n")
            raise