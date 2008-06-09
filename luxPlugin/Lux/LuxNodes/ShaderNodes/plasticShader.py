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
# Lux material shader node for Maya ( plastic attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class plasticShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    Plastic fragment of luxshader
    """
    
    # plastic
    kd          =    OpenMaya.MObject()    # color
    ks          =    OpenMaya.MObject()    # color
    uroughness  =    OpenMaya.MObject()    # float
    vroughness  =    OpenMaya.MObject()    # float

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # Export attributes
        self.attributes = {}
        self.luxType = "plastic"
        self.attributes['Kd']        = ShaderColorAttribute('plasticKd')
        self.attributes['Ks']        = ShaderColorAttribute('plasticKs')
        self.attributes['uroughness'] = ShaderFloatAttribute('plasticURoughness')
        self.attributes['vroughness'] = ShaderFloatAttribute('plasticVRoughness')

    @staticmethod
    def shaderInitializer():
        try:
            # diffuse reflectivity
            plasticShader.kd = plasticShader.makeColor("plasticKd", "pkd")

            # specular reflectivity
            plasticShader.ks = plasticShader.makeColor("plasticKs", "pks")

            # surface roughness
            plasticShader.uroughness = plasticShader.makeFloat("plasticURoughness", "pur", 0.1)
            plasticShader.vroughness = plasticShader.makeFloat("plasticVRoughness", "pvr", 0.1)

        except:
            OpenMaya.MGlobal.displayError("Failed to create plastic attributes\n")
            raise