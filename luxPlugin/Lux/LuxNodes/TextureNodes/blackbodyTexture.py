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
class blackbodyTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Blackbody Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
#    # maya 3d common attributes
#    placementMatrix = OpenMaya.MObject()
    
    # lux texture specific attributes
    
    temperature      = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_blackbody"

    def luxName(self):
        return "blackbody"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75781E) # 'lux' 30

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blackbodyTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/other"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['temperature']  = TextureFloatAttribute('temperature',  self.addToOutput, self.prependToOutput)
    
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
            blackbodyTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blackbodyTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
#            # 3D Params
#            blackbodyTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
#            blackbodyTexture.makeInput(mAttr)

            blackbodyTexture.temperature = blackbodyTexture.makeFloat("temperature", "tm", 6500.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blackbodyTexture attributes\n")
            raise
        
        try:
            blackbodyTexture.addAttribute(blackbodyTexture.outColor)
            blackbodyTexture.addAttribute(blackbodyTexture.outAlpha)
            
#            blackbodyTexture.addAttribute(blackbodyTexture.placementMatrix)

            blackbodyTexture.addAttribute(blackbodyTexture.temperature)
            
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
