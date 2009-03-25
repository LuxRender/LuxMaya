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
class equalenergyTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Equalenergy Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
    # lux texture specific attributes
    
    energy      = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_equalenergy"

    def luxName(self):
        return "equalenergy"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75781C) # 'lux' 28

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( equalenergyTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/other"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['energy']  = TextureFloatAttribute('energy',  self.addToOutput, self.prependToOutput)
    
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
            equalenergyTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            equalenergyTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)

            equalenergyTexture.energy = equalenergyTexture.makeFloat("energy", "en", 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create equalenergyTexture attributes\n")
            raise
        
        try:
            equalenergyTexture.addAttribute(equalenergyTexture.outColor)
            equalenergyTexture.addAttribute(equalenergyTexture.outAlpha)

            equalenergyTexture.addAttribute(equalenergyTexture.energy)
            
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
