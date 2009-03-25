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
# Lux Windy Texture node for Maya
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureIntegerAttribute
from Lux.LuxNodes.LuxNode import TextureFloatAttribute
from Lux.LuxNodes.LuxNode import TextureVectorAttribute

# 3D Texture
class windyTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Windy Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
    placementMatrix = OpenMaya.MObject()
    pointWorld      = OpenMaya.MObject()
    
    translate       = OpenMaya.MObject()
    rotate          = OpenMaya.MObject()
    scale           = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_windy"
    
    def luxName(self):
        return "windy"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757811) # 'lux' 17

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( windyTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
                
        self.attributes['translate'] = TextureVectorAttribute('translate', self.addToOutput, self.prependToOutput)
        self.attributes['rotate'] = TextureVectorAttribute('rotate', self.addToOutput, self.prependToOutput)
        self.attributes['scale'] = TextureVectorAttribute('scale', self.addToOutput, self.prependToOutput)
        
    
    def postConstructor(self):
        self._setMPSafe( True )
        self.setExistWithoutOutConnections( True )
        self.setExistWithoutInConnections( True )

    
    @staticmethod
    def nodeInitializer():
        nAttr = OpenMaya.MFnNumericAttribute()
        mAttr = OpenMaya.MFnMatrixAttribute()
        
        try:
            windyTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            windyTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            windyTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            windyTexture.makeInput(mAttr)
            
            windyTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            windyTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            windyTexture.translate = nAttr.createPoint("translate", "t")
            windyTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            windyTexture.rotate = nAttr.createPoint("rotate", "r")
            windyTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            windyTexture.scale = nAttr.createPoint("scale", "s")
            windyTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to create windyTexture attributes\n")
            raise
        
        try:
            windyTexture.addAttribute(windyTexture.outColor)
            windyTexture.addAttribute(windyTexture.outAlpha)
            
            windyTexture.addAttribute(windyTexture.placementMatrix)
            windyTexture.addAttribute(windyTexture.pointWorld)
            
            windyTexture.addAttribute(windyTexture.translate)
            windyTexture.addAttribute(windyTexture.rotate)
            windyTexture.addAttribute(windyTexture.scale)
                       
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise