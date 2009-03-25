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
class frequencyTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Frequency Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
    # lux texture specific attributes
    
    frequency   = OpenMaya.MObject()
    phase       = OpenMaya.MObject()
    energy      = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_frequency"

    def luxName(self):
        return "frequency"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75781B) # 'lux' 27

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( frequencyTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/other"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['frequency']  = TextureFloatAttribute('frequency',  self.addToOutput, self.prependToOutput)
        self.attributes['phase']      = TextureFloatAttribute('phase',  self.addToOutput, self.prependToOutput)
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
            frequencyTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            frequencyTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            frequencyTexture.frequency = frequencyTexture.makeFloat("frequency", "fr", 0.03)
            frequencyTexture.phase = frequencyTexture.makeFloat("phase", "ph", 0.5)
            frequencyTexture.energy = frequencyTexture.makeFloat("energy", "en", 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create frequencyTexture attributes\n")
            raise
        
        try:
            frequencyTexture.addAttribute(frequencyTexture.outColor)
            frequencyTexture.addAttribute(frequencyTexture.outAlpha)

            frequencyTexture.addAttribute(frequencyTexture.frequency)
            frequencyTexture.addAttribute(frequencyTexture.phase)
            frequencyTexture.addAttribute(frequencyTexture.energy)
            
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
        