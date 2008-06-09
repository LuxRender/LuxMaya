# ------------------------------------------------------------------------------
# Lux texture nodes for Maya
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
# Lux Texture node base class
#
# ------------------------------------------------------------------------------

import math

from maya import OpenMaya

from LuxNode import LuxNode

class TextureNode(LuxNode):
    """
    Lux custom texture node base class
    """
    
    def getTexture(self, plugName, textureNode, textureName, attrType ):
        nTextName = '%s.%s' % (textureName, plugName)
        self.addToOutput( 'Texture "%s"' % nTextName )
        self.addToOutput( '\t"%s" "%s"' % ( attrType, self.luxName() ) )
        
        for attr in self.attributes:
            self.addToOutput( self.attributes[attr].getOutput(attr, textureNode, textureName, self.luxName() ) )

        return self.outputString
    