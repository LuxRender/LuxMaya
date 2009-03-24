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
# Lux material shader node for Maya ( glossy attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class glossyShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    Glossy fragment of luxshader
    """
    
    # glossy
    kd            =    OpenMaya.MObject()    # color
    ks            =    OpenMaya.MObject()    # color
    uroughness    =    OpenMaya.MObject()    # float
    vroughness    =    OpenMaya.MObject()    # float

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # Export attributes
        self.attributes = {}
        self.luxType = "glossy"
        self.attributes['Kd']         = ShaderColorAttribute('glossyKd')
        self.attributes['Ks']         = ShaderColorAttribute('glossyKs')
        self.attributes['uroughness'] = ShaderFloatAttribute('glossyURoughness', reciprocal = True)
        self.attributes['vroughness'] = ShaderFloatAttribute('glossyVRoughness', reciprocal = True)

    @staticmethod
    def shaderInitializer():
        try:
            # diffuse reflectivity
            glossyShader.kd = glossyShader.makeColor("glossyKd", "skd", 0.5, 0.5, 0.5)

            # specular reflectivity
            glossyShader.ks = glossyShader.makeColor("glossyKs", "sks", 0.5, 0.5, 0.5)

            # U roughness
            glossyShader.uroughness = glossyShader.makeFloat("glossyURoughness", "sur", 500.0)

            # V roughness
            glossyShader.vroughness = glossyShader.makeFloat("glossyVRoughness", "svr", 500.0)

        except:
            OpenMaya.MGlobal.displayError("Failed to create glossy attributes\n")
            raise