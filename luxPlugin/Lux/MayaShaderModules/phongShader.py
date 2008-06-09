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
# Lambert shader node attributes translator
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class phongShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    This class provides an interface to translate Maya phong shaders
    into lux plastic materials.
    """
    
    def __init__(self):
        """
        phongShader constructor. Calls the parent OpenMayaMPx.MPxNode constructor
        and defines the Maya attribute -> lux material parameter mapping.
        """
        
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for shader
        self.attributes = {}
        self.luxType = "plastic"
        self.attributes['Kd']        = ShaderColorAttribute('color')
        self.attributes['Ks']        = ShaderColorAttribute('specularColor')
        self.attributes['uroughness'] = ShaderFloatAttribute('cosinePower', 0.01, True, 0.1)
        self.attributes['vroughness'] = ShaderFloatAttribute('cosinePower', 0.01, True, 0.1)
         