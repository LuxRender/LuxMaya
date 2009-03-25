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
# Lux Wrinkled Texture node for Maya
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
class wrinkledTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Wrinkled Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    placementMatrix = OpenMaya.MObject()
    pointWorld      = OpenMaya.MObject()
    
    translate       = OpenMaya.MObject()
    rotate          = OpenMaya.MObject()
    scale           = OpenMaya.MObject()
    
    octaves         = OpenMaya.MObject()
    roughness       = OpenMaya.MObject() 
    
    @staticmethod
    def nodeName():
        return "lux_wrinkled"

    def luxName(self):
        return "wrinkled"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757804) # 'lux' 03

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( wrinkledTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
        self.attributes['octaves']   = TextureIntegerAttribute('octaves',  self.addToOutput, self.prependToOutput)
        self.attributes['roughness'] = TextureFloatAttribute('roughness',  self.addToOutput, self.prependToOutput)
        
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
            wrinkledTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            wrinkledTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            wrinkledTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            wrinkledTexture.makeInput(mAttr)
            
            wrinkledTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            wrinkledTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            wrinkledTexture.translate = nAttr.createPoint("translate", "t")
            wrinkledTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            wrinkledTexture.rotate = nAttr.createPoint("rotate", "r")
            wrinkledTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            wrinkledTexture.scale = nAttr.createPoint("scale", "s")
            wrinkledTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            wrinkledTexture.octaves = wrinkledTexture.makeInteger("octaves", "fbmo", 8)
            wrinkledTexture.roughness = wrinkledTexture.makeFloat("roughness", "fbmr", 0.5)

        except:
            OpenMaya.MGlobal.displayError("Failed to create wrinkledTexture attributes\n")
            raise
        
        try:
            wrinkledTexture.addAttribute(wrinkledTexture.outColor)
            wrinkledTexture.addAttribute(wrinkledTexture.outAlpha)
            wrinkledTexture.addAttribute(wrinkledTexture.placementMatrix)
            wrinkledTexture.addAttribute(wrinkledTexture.pointWorld)
            
            wrinkledTexture.addAttribute(wrinkledTexture.translate)
            wrinkledTexture.addAttribute(wrinkledTexture.rotate)
            wrinkledTexture.addAttribute(wrinkledTexture.scale)

            wrinkledTexture.addAttribute(wrinkledTexture.octaves)
            wrinkledTexture.addAttribute(wrinkledTexture.roughness)
                     
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
        