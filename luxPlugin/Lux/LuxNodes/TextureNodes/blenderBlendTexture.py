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
# Blender Blend Texture node for Maya
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode

from Lux.LuxNodes.LuxNode import TextureBoolAttribute
from Lux.LuxNodes.LuxNode import TextureColorAttribute
from Lux.LuxNodes.LuxNode import TextureFloatAttribute
from Lux.LuxNodes.LuxNode import TextureEnumAttribute
from Lux.LuxNodes.LuxNode import TextureVectorAttribute

## 3D Texture
class blenderBlendTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Blend Texture node for Maya
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
    flipxy           = OpenMaya.MObject()
    
    type             = OpenMaya.MObject()
    aTypes = [
              'lin',
              'quad',
              'ease',
              'diag',
              'sphere',
              'halo',
              'radial'
              ]
    
    bright           = OpenMaya.MObject()
    contrast         = OpenMaya.MObject()
    
    # pseudo-mix
    tex1             = OpenMaya.MObject()
    tex2             = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "blender_blend"

    def luxName(self):
        return "blender_blend"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757818) # 'lux' 24

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderBlendTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['flipxy'] = TextureBoolAttribute('flipxy',  self.addToOutput, self.prependToOutput)
        
        self.attributes['type'] = TextureEnumAttribute('type',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aTypes)
        
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
            blenderBlendTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderBlendTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderBlendTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderBlendTexture.makeInput(mAttr)
            
            blenderBlendTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderBlendTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderBlendTexture.translate = nAttr.createPoint("translate", "t")
            blenderBlendTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderBlendTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderBlendTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderBlendTexture.scale = nAttr.createPoint("scale", "s")
            blenderBlendTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderBlendTexture.flipxy = blenderBlendTexture.makeBoolean("flipxy", "fxy", False)
            
            blenderBlendTexture.type = enumAttr.create("type", "typ", 0)
            i=0
            for type in blenderBlendTexture.aTypes:
                enumAttr.addField( type, i )
                i+=1
                   
            blenderBlendTexture.bright = blenderBlendTexture.makeFloat("bright", "br", 1.0)
            blenderBlendTexture.contrast = blenderBlendTexture.makeFloat("contrast", "co", 1.0)
            
            blenderBlendTexture.tex1 = blenderBlendTexture.makeColor("tex1", "t1", 0.0, 0.0, 0.0)
            blenderBlendTexture.tex2 = blenderBlendTexture.makeColor("tex2", "t2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderBlendTexture attributes\n")
            raise
        
        try:
            blenderBlendTexture.addAttribute(blenderBlendTexture.outColor)
            blenderBlendTexture.addAttribute(blenderBlendTexture.outAlpha)
            
            blenderBlendTexture.addAttribute(blenderBlendTexture.placementMatrix)
            blenderBlendTexture.addAttribute(blenderBlendTexture.pointWorld)
            
            blenderBlendTexture.addAttribute(blenderBlendTexture.translate)
            blenderBlendTexture.addAttribute(blenderBlendTexture.rotate)
            blenderBlendTexture.addAttribute(blenderBlendTexture.scale)

            blenderBlendTexture.addAttribute(blenderBlendTexture.flipxy)
            blenderBlendTexture.addAttribute(blenderBlendTexture.type)

            blenderBlendTexture.addAttribute(blenderBlendTexture.tex1)
            blenderBlendTexture.addAttribute(blenderBlendTexture.tex2)
        
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
