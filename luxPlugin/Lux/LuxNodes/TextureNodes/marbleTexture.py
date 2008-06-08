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
# Lux Marble Texture node for Maya
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
class marbleTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Marble Texture node for Maya
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
    #scale           = OpenMaya.MObject()
    variation       = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_marble"
    
    def luxName(self):
        return "marble"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757810) # 'lux' 16

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( marbleTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
        self.attributes['octaves']   = TextureIntegerAttribute('octaves',  self.addToOutput, self.prependToOutput)
        self.attributes['roughness']   = TextureFloatAttribute('roughness',  self.addToOutput, self.prependToOutput)
        self.attributes['scale']   = TextureFloatAttribute('scale',  self.addToOutput, self.prependToOutput)
        self.attributes['variation']   = TextureFloatAttribute('variation',  self.addToOutput, self.prependToOutput)
        
        self.attributes['translate'] = TextureVectorAttribute('translate', self.addToOutput, self.prependToOutput)
        self.attributes['rotate'] = TextureVectorAttribute('rotate', self.addToOutput, self.prependToOutput)
        #self.attributes['scale'] = TextureVectorAttribute('scale', self.addToOutput, self.prependToOutput)
        
    def postConstructor(self):
        self._setMPSafe(True)
    
    @staticmethod
    def nodeInitializer():
        nAttr = OpenMaya.MFnNumericAttribute()
        mAttr = OpenMaya.MFnMatrixAttribute()
        
        try:
            marbleTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            marbleTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            marbleTexture.translate = nAttr.createPoint("translate", "t")
            marbleTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            marbleTexture.rotate = nAttr.createPoint("rotate", "r")
            marbleTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
#            marbleTexture.scale = nAttr.createPoint("scale", "s")
#            marbleTexture.makeInput(nAttr)
#            nAttr.setDefault( 1.0, 1.0, 1.0 )
#            #nAttr.setHidden(True)
            
            marbleTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            marbleTexture.makeInput(mAttr)
            
            marbleTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            marbleTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            marbleTexture.octaves = marbleTexture.makeInteger("octaves", "mmo", 8)
            marbleTexture.roughness = marbleTexture.makeFloat("roughness", "mmr", 0.5)
            marbleTexture.scale = marbleTexture.makeFloat("scale", "msc", 1.0)
            marbleTexture.variation = marbleTexture.makeFloat("variation", "mv", 0.2)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to create marbleTexture attributes\n")
            raise
        
        try:
            marbleTexture.addAttribute(marbleTexture.outColor)
            marbleTexture.addAttribute(marbleTexture.outAlpha)
            marbleTexture.addAttribute(marbleTexture.placementMatrix)
            marbleTexture.addAttribute(marbleTexture.pointWorld)
            
            marbleTexture.addAttribute(marbleTexture.translate)
            marbleTexture.addAttribute(marbleTexture.rotate)
            marbleTexture.addAttribute(marbleTexture.scale)

            marbleTexture.addAttribute(marbleTexture.octaves)
            marbleTexture.addAttribute(marbleTexture.roughness)
#            marbleTexture.addAttribute(marbleTexture.scale)
            marbleTexture.addAttribute(marbleTexture.variation)

#            marbleTexture.attributeAffects(marbleTexture.octaves, marbleTexture.outColor)
#            marbleTexture.attributeAffects(marbleTexture.roughness, marbleTexture.outColor)
#            marbleTexture.attributeAffects(marbleTexture.scale, marbleTexture.outColor)
#            marbleTexture.attributeAffects(marbleTexture.variation, marbleTexture.outColor)
#
#            marbleTexture.attributeAffects(marbleTexture.pointWorld, marbleTexture.outColor)
#            marbleTexture.attributeAffects(marbleTexture.placementMatrix, marbleTexture.outColor)
#            
#            marbleTexture.attributeAffects(marbleTexture.octaves, marbleTexture.outAlpha)
#            marbleTexture.attributeAffects(marbleTexture.roughness, marbleTexture.outAlpha)
#            marbleTexture.attributeAffects(marbleTexture.scale, marbleTexture.outAlpha)
#            marbleTexture.attributeAffects(marbleTexture.variation, marbleTexture.outAlpha)
#
#            marbleTexture.attributeAffects(marbleTexture.pointWorld, marbleTexture.outAlpha)
#            marbleTexture.attributeAffects(marbleTexture.placementMatrix, marbleTexture.outAlpha)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise