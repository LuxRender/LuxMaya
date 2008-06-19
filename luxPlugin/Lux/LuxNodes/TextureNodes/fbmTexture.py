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
# Lux FBM Texture node for Maya
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
class fbmTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux FBM Texture node for Maya
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
        return "lux_fbm"

    def luxName(self):
        return "fbm"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757803) # 'lux' 03

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( fbmTexture() )

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
            fbmTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            fbmTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            fbmTexture.translate = nAttr.createPoint("translate", "t")
            fbmTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            fbmTexture.rotate = nAttr.createPoint("rotate", "r")
            fbmTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            fbmTexture.scale = nAttr.createPoint("scale", "s")
            fbmTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            fbmTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            fbmTexture.makeInput(mAttr)
            
            fbmTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            fbmTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            fbmTexture.octaves = fbmTexture.makeInteger("octaves", "fbmo", 8)
            fbmTexture.roughness = fbmTexture.makeFloat("roughness", "fbmr", 0.5)

        except:
            OpenMaya.MGlobal.displayError("Failed to create fbmtexture attributes\n")
            raise
        
        try:
            fbmTexture.addAttribute(fbmTexture.outColor)
            fbmTexture.addAttribute(fbmTexture.outAlpha)
            fbmTexture.addAttribute(fbmTexture.placementMatrix)
            fbmTexture.addAttribute(fbmTexture.pointWorld)
            
            fbmTexture.addAttribute(fbmTexture.translate)
            fbmTexture.addAttribute(fbmTexture.rotate)
            fbmTexture.addAttribute(fbmTexture.scale)

            fbmTexture.addAttribute(fbmTexture.octaves)
            fbmTexture.addAttribute(fbmTexture.roughness)
            
#            fbmTexture.attributeAffects(fbmTexture.octaves, fbmTexture.outColor)
#            fbmTexture.attributeAffects(fbmTexture.roughness, fbmTexture.outColor)
#            fbmTexture.attributeAffects(fbmTexture.pointWorld, fbmTexture.outColor)
#            fbmTexture.attributeAffects(fbmTexture.placementMatrix, fbmTexture.outColor)
#            
#            fbmTexture.attributeAffects(fbmTexture.octaves, fbmTexture.outAlpha)
#            fbmTexture.attributeAffects(fbmTexture.roughness, fbmTexture.outAlpha)
#            fbmTexture.attributeAffects(fbmTexture.pointWorld, fbmTexture.outAlpha)
#            fbmTexture.attributeAffects(fbmTexture.placementMatrix, fbmTexture.outAlpha)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
#    def FBm(self, Px, Py, Pz, omega, maxOctaves):
#
#        sum = 0.0
#        llambda = 1.0
#        o = 1.0
#        for i in range(0, maxOctaves):
#            sum += o * self.Noise(llambda*Px, llambda*Py, llambda*Pz)
#            llambda *= 1.99
#            o *= omega
#            
#        sum += o * self.SmoothStep(.3, .7, 0) * self.Noise(llambda*Px, llambda*Py, llambda*Pz)
#        
#        return sum