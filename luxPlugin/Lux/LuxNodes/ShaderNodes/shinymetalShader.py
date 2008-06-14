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
# Lux material shader node for Maya ( shinymetal attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class shinymetalShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    ShinyMetal fragment of luxshader
    """
    
    # shinymetal
    kr            =    OpenMaya.MObject()    # color
    ks            =    OpenMaya.MObject()    # color
    uroughness    =    OpenMaya.MObject()    # float
    vroughness    =    OpenMaya.MObject()    # float

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # Export attributes
        self.attributes = {}
        self.luxType = "shinymetal"
        self.attributes['Kr']        = ShaderColorAttribute('shinymetalKr')
        self.attributes['Ks']        = ShaderColorAttribute('shinymetalKs')
        self.attributes['uroughness'] = ShaderFloatAttribute('shinymetalURoughness', reciprocal = True)
        self.attributes['vroughness'] = ShaderFloatAttribute('shinymetalVRoughness', reciprocal = True)

    @staticmethod
    def shaderInitializer():
        try:
            # specular reflection
            shinymetalShader.kr = shinymetalShader.makeColor("shinymetalKr", "smkr")

            # glossy reflection
            shinymetalShader.ks = shinymetalShader.makeColor("shinymetalKs", "smks")

            # surface roughness
            shinymetalShader.uroughness = shinymetalShader.makeFloat("shinymetalURoughness", "smur", 500.0)
            shinymetalShader.vroughness = shinymetalShader.makeFloat("shinymetalVRoughness", "smvr", 500.0)

        except:
            OpenMaya.MGlobal.displayError("Failed to create shinymetal attributes\n")
            raise
        