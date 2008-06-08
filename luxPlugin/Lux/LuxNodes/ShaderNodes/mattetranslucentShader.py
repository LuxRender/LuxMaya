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
# Lux material shader node for Maya ( mattetranslucent attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class mattetranslucentShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    MatteTranslucent fragment of luxshader
    """
    
    # mattetranslucent
    kr            =    OpenMaya.MObject()    # color
    kt            =    OpenMaya.MObject()    # color
    sigma         =    OpenMaya.MObject()    # float

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        
        # Export attributes
        self.attributes = {}
        self.luxType = "mattetranslucent"
        self.attributes['Kr']    = ShaderColorAttribute('mattetranslucentKr')
        self.attributes['Kt']    = ShaderColorAttribute('mattetranslucentKt')
        self.attributes['sigma'] = ShaderFloatAttribute('mattetranslucentSigma')

    @staticmethod
    def shaderInitializer():
        try:
            # diffuse reflectivity
            mattetranslucentShader.kr = mattetranslucentShader.makeColor("mattetranslucentKr", "mtkr")

            # diffuse transmissivity
            mattetranslucentShader.kt = mattetranslucentShader.makeColor("mattetranslucentKt", "mtkt")

            # Oren-Nayar sigma
            mattetranslucentShader.sigma = mattetranslucentShader.makeFloat("mattetranslucentSigma", "mts", 0.0)

        except:
            OpenMaya.MGlobal.displayError("Failed to create mattetranslucent attributes\n")
            raise