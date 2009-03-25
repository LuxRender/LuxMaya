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
# Blender Wood Texture node for Maya
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureFloatAttribute

## Float Texture
class gaussianTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Gaussian Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
    # lux texture specific attributes
    
    wavelength  = OpenMaya.MObject()
    width       = OpenMaya.MObject()
    energy      = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_gaussian"

    def luxName(self):
        return "gaussian"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75781A) # 'lux' 26

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( gaussianTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/other"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['wavelength'] = TextureFloatAttribute('wavelength',  self.addToOutput, self.prependToOutput)
        self.attributes['width']      = TextureFloatAttribute('width',  self.addToOutput, self.prependToOutput)
        self.attributes['energy']     = TextureFloatAttribute('energy',  self.addToOutput, self.prependToOutput)
        
    
    def postConstructor(self):
        self._setMPSafe( True )
        self.setExistWithoutOutConnections( True )
        self.setExistWithoutInConnections( True )
    
    @staticmethod
    def nodeInitializer():
        nAttr = OpenMaya.MFnNumericAttribute()
        mAttr = OpenMaya.MFnMatrixAttribute()
        enumAttr = OpenMaya.MFnEnumAttribute()
        
        try:
            gaussianTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            gaussianTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            gaussianTexture.wavelength = gaussianTexture.makeFloat("wavelength", "wa", 550.0)
            gaussianTexture.width = gaussianTexture.makeFloat("width", "wi", 50.0)
            gaussianTexture.energy = gaussianTexture.makeFloat("energy", "en", 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create gaussianTexture attributes\n")
            raise
        
        try:
            gaussianTexture.addAttribute(gaussianTexture.outColor)
            gaussianTexture.addAttribute(gaussianTexture.outAlpha)

            gaussianTexture.addAttribute(gaussianTexture.wavelength)
            gaussianTexture.addAttribute(gaussianTexture.width)
            gaussianTexture.addAttribute(gaussianTexture.energy)
            
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
        