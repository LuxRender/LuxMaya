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
# Lux material shader node for Maya ( substrate attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class substrateShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    Substrate fragment of luxshader
    """
    
    # substrate
    kd            =    OpenMaya.MObject()    # color
    ks            =    OpenMaya.MObject()    # color
    uroughness    =    OpenMaya.MObject()    # float
    vroughness    =    OpenMaya.MObject()    # float

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # Export attributes
        self.attributes = {}
        self.luxType = "substrate"
        self.attributes['Kd']         = ShaderColorAttribute('substrateKd')
        self.attributes['Ks']         = ShaderColorAttribute('substrateKs')
        self.attributes['uroughness'] = ShaderFloatAttribute('substrateURoughness')
        self.attributes['vroughness'] = ShaderFloatAttribute('substrateVRoughness')

    @staticmethod
    def shaderInitializer():
        try:
            # diffuse reflectivity
            substrateShader.kd = substrateShader.makeColor("substrateKd", "skd", 0.5, 0.5, 0.5)

            # specular reflectivity
            substrateShader.ks = substrateShader.makeColor("substrateKs", "sks", 0.5, 0.5, 0.5)

            # U roughness
            substrateShader.uroughness = substrateShader.makeFloat("substrateURoughness", "sur", 0.1)

            # V roughness
            substrateShader.vroughness = substrateShader.makeFloat("substrateVRoughness", "svr", 0.1)

        except:
            OpenMaya.MGlobal.displayError("Failed to create substrate attributes\n")
            raise