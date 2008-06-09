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
# Lux material shader node for Maya ( attributes base class )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from LuxNode import LuxNode
from LuxNode import ShaderColorAttribute
from LuxNode import ShaderFloatAttribute
from LuxNode import ShaderEnumAttribute
#from Lux.LuxMiscModules.FileCollector import FileCollector

# ShaderModules serve dual purpose: Set up the custom shader in Maya
# AND provide attribute->parameter translation during export
class ShaderNode(LuxNode):
    """
    Lux custom shader base class. Each material type derives off this.
    """

    luxType = str()
    
    #attributes = {}
    
    def getMaterial(self, shaderNode, shaderName ):
        self.attributes['bumpmap'] = ShaderFloatAttribute('normalCamera')
        
        for attr in self.attributes:
            if not isinstance( self.attributes[attr], ShaderEnumAttribute ):
                self.addToOutput( self.attributes[attr].getOutput( attr, shaderNode, shaderName ) )
                
                
        self.addToOutput( 'MakeNamedMaterial "%s"' % shaderName )
        self.addToOutput( '\t"string type" ["%s"]' % self.luxType )
        
        for attr in self.attributes:
            if isinstance( self.attributes[attr], ShaderEnumAttribute ):
                self.addToOutput( self.attributes[attr].getOutput( attr, shaderNode, shaderName ) )
            else:
                if self.attributes[attr].exportName == '':
                    self.addToOutput( '\t"texture %s" ["%s.%s"]' % (attr, shaderName, attr) )
                else:
                    self.addToOutput( '\t"texture %s" ["%s"]' % (attr, self.attributes[attr].exportName) )
            

        self.addToOutput( '' )
        return self.outputString