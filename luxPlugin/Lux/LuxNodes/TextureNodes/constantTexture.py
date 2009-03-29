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
from Lux.LuxNodes.LuxNode import TextureColorAttribute

## Float Texture
class constantTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux constant Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
#    # maya 3d common attributes
#    placementMatrix = OpenMaya.MObject()
    
    # lux texture specific attributes
    
    value           = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_constant"

    def luxName(self):
        return "constant"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75781F) # 'lux' 31

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( constantTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/other"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['value']  = TextureColorAttribute('value',  self.addToOutput, self.prependToOutput)
    
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
            constantTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            constantTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
#            # 3D Params
#            constantTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
#            constantTexture.makeInput(mAttr)

            constantTexture.value = constantTexture.makeColor("value", "va")


        except:
            OpenMaya.MGlobal.displayError("Failed to create constantTexture attributes\n")
            raise
        
        try:
            constantTexture.addAttribute(constantTexture.outColor)
            constantTexture.addAttribute(constantTexture.outAlpha)
            
#            constantTexture.addAttribute(constantTexture.placementMatrix)

            constantTexture.addAttribute(constantTexture.value)
            
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
