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
# Blender Noise Texture node for Maya
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureColorAttribute
from Lux.LuxNodes.LuxNode import TextureFloatAttribute
from Lux.LuxNodes.LuxNode import TextureEnumAttribute
from Lux.LuxNodes.LuxNode import TextureVectorAttribute

## 3D Texture
class blenderNoiseTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Noise Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
    # maya 3d common attributes
    placementMatrix = OpenMaya.MObject()
    pointWorld      = OpenMaya.MObject()
    
    translate       = OpenMaya.MObject()
    rotate          = OpenMaya.MObject()
    scale           = OpenMaya.MObject()
    
    # lux texture specific attributes
    
    bright           = OpenMaya.MObject()
    contrast         = OpenMaya.MObject()
    
    # pseudo-mix
    tex1             = OpenMaya.MObject()
    tex2             = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "blender_noise"

    def luxName(self):
        return "blender_noise"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75780E) # 'lux' 14

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderNoiseTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['bright']     = TextureFloatAttribute('bright',  self.addToOutput, self.prependToOutput)
        self.attributes['contrast']   = TextureFloatAttribute('contrast',  self.addToOutput, self.prependToOutput)
        
        self.attributes['translate'] = TextureVectorAttribute('translate', self.addToOutput, self.prependToOutput)
        self.attributes['rotate'] = TextureVectorAttribute('rotate', self.addToOutput, self.prependToOutput)
        self.attributes['scale'] = TextureVectorAttribute('scale', self.addToOutput, self.prependToOutput)
        
        self.attributes['tex1']   = TextureColorAttribute('tex1',  self.addToOutput, self.prependToOutput)
        self.attributes['tex2']   = TextureColorAttribute('tex2',  self.addToOutput, self.prependToOutput)
    
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
            blenderNoiseTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderNoiseTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderNoiseTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderNoiseTexture.makeInput(mAttr)
            
            blenderNoiseTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderNoiseTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderNoiseTexture.translate = nAttr.createPoint("translate", "t")
            blenderNoiseTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderNoiseTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderNoiseTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderNoiseTexture.scale = nAttr.createPoint("scale", "s")
            blenderNoiseTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderNoiseTexture.bright = blenderNoiseTexture.makeFloat("bright", "br", 1.0)
            blenderNoiseTexture.contrast = blenderNoiseTexture.makeFloat("contrast", "co", 1.0)
            
            blenderNoiseTexture.tex1 = blenderNoiseTexture.makeColor("tex1", "t1", 0.0, 0.0, 0.0)
            blenderNoiseTexture.tex2 = blenderNoiseTexture.makeColor("tex2", "t2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderNoiseTexture attributes\n")
            raise
        
        try:
            blenderNoiseTexture.addAttribute(blenderNoiseTexture.outColor)
            blenderNoiseTexture.addAttribute(blenderNoiseTexture.outAlpha)
            
            blenderNoiseTexture.addAttribute(blenderNoiseTexture.placementMatrix)
            blenderNoiseTexture.addAttribute(blenderNoiseTexture.pointWorld)
            
            blenderNoiseTexture.addAttribute(blenderNoiseTexture.translate)
            blenderNoiseTexture.addAttribute(blenderNoiseTexture.rotate)
            blenderNoiseTexture.addAttribute(blenderNoiseTexture.scale)

            blenderNoiseTexture.addAttribute(blenderNoiseTexture.bright)
            blenderNoiseTexture.addAttribute(blenderNoiseTexture.contrast)

            blenderNoiseTexture.addAttribute(blenderNoiseTexture.tex1)
            blenderNoiseTexture.addAttribute(blenderNoiseTexture.tex2)
           
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
