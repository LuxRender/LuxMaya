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
# Displacement shader node attributes translator
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class displacementShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    This class provides an interface to Maya displacement shaders.
    We don't actually need any material output here, but we need to
    maked references to all downstream textures.
    """

    def __init__(self):
        """
        lambertShader constructor. Calls the parent OpenMayaMPx.MPxNode constructor
        and defines the Maya attribute -> lux material parameter mapping.
        """
        
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for shader
        self.attributes = {}
        self.luxType = "null"
        #self.attributes['Kd']    = ShaderColorAttribute('color')
        #self.attributes['sigma'] = ShaderFloatAttribute('translucence')
        self.attributes['null'] = ShaderFloatAttribute('displacement')
        
    def getMaterial(self, shaderNode, shaderName ):
        
        for attr in self.attributes:
            #if not isinstance( self.attributes[attr], ShaderEnumAttribute ):
            self.addToOutput( self.attributes[attr].getOutput( attr, shaderNode, shaderName ) )
                
                
#        self.addToOutput( 'MakeNamedMaterial "%s"' % shaderName )
#        self.addToOutput( '\t"string type" ["%s"]' % self.luxType )
#        
#        for attr in self.attributes:
#            if isinstance( self.attributes[attr], ShaderEnumAttribute ):
#                self.addToOutput( self.attributes[attr].getOutput( attr, shaderNode, shaderName ) )
#            else:
#                if self.attributes[attr].exportName == '':
#                    self.addToOutput( '\t"texture %s" ["%s.%s"]' % (attr, shaderName, attr) )
#                else:
#                    self.addToOutput( '\t"texture %s" ["%s"]' % (attr, self.attributes[attr].exportName) )
            

        self.addToOutput( '' )
        return self.outputString
         