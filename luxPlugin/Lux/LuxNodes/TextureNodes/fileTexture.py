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
# Lux File Texture expoter
#
# ------------------------------------------------------------------------------

import math, os
from maya import cmds
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureStringAttribute
# from Lux.LuxNodes.LuxNode import TextureFloatAttribute

from Lux.LuxMiscModules.FileCollector import FileCollector

# dummy Texture
class fileTexture(TextureNode):
    """
    File Texture node handler
    """
    
    @staticmethod
    def nodeName():
        return "fileTexture"
    
    def __init__(self):
        
        self.attributes = {}
        self.attributes['imagemap']   = TextureStringAttribute('fileTextureName',  self.addToOutput, self.prependToOutput)
        
    def getTexture(self, plugName, textureNode, textureName, attrType ):
        
    
        inputFileTexturePlug = textureNode.findPlug('fileTextureName')
        self.fileTextureFileName = inputFileTexturePlug.asString()
        
        inputFileTexturePlug = textureNode.findPlug('colorGainR')
        self.fileTextureScaleR =  inputFileTexturePlug.asFloat()
        inputFileTexturePlug = textureNode.findPlug('colorGainG')
        self.fileTextureScaleG =  inputFileTexturePlug.asFloat()
        inputFileTexturePlug = textureNode.findPlug('colorGainB')
        self.fileTextureScaleB =  inputFileTexturePlug.asFloat()
        
        #if attrType == "color":
        #    self.fileTextureScale = '%f %f %f' % ( self.fileTextureScaleR, self.fileTextureScaleG, self.fileTextureScaleB )
        #else:
        self.fileTextureScale = '%f' % ( self.fileTextureScaleR )
        
        self.addToOutput( 'Texture "%s.%s"' % (textureName, plugName) )
        self.addToOutput( '\t"%s" "imagemap"' % attrType )
        self.addToOutput( '\t\t"float vscale" [-1.0]' )
        self.addToOutput( '\t\t"string filename" ["%s"]' % FileCollector.collectTexture( self.fileTextureFileName ) )
        self.addToOutput( '\t\t"float gain" [%s]' % self.fileTextureScale )
        
        if cmds.getAttr( 'lux_settings.scene_reverse_gamma' ) == 1:
            self.addToOutput( '\t\t"float gamma" [%f]' % (cmds.getAttr( 'lux_settings.film_gamma' )) )


        return self.outputString