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
# Blender Magic Texture node for Maya
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
class blenderMagicTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Magic Texture node for Maya
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
    
    noisedepth       = OpenMaya.MObject()
    turbulance       = OpenMaya.MObject()
    
    bright           = OpenMaya.MObject()
    contrast         = OpenMaya.MObject()
    
    # pseudo-mix
    tex1             = OpenMaya.MObject()
    tex2             = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "blender_magic"

    def luxName(self):
        return "blender_magic"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75780D) # 'lux' 13

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderMagicTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['noisedepth']  = TextureFloatAttribute('noisedepth',  self.addToOutput, self.prependToOutput)
        self.attributes['turbulance']  = TextureFloatAttribute('turbulance',  self.addToOutput, self.prependToOutput)
        
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
            blenderMagicTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderMagicTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderMagicTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderMagicTexture.makeInput(mAttr)
            
            blenderMagicTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderMagicTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderMagicTexture.translate = nAttr.createPoint("translate", "t")
            blenderMagicTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderMagicTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderMagicTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderMagicTexture.scale = nAttr.createPoint("scale", "s")
            blenderMagicTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderMagicTexture.noisedepth = blenderMagicTexture.makeFloat("noisedepth", "nd", 0.25)
            blenderMagicTexture.turbulance = blenderMagicTexture.makeFloat("turbulance", "tu", 5.0)
            
            blenderMagicTexture.bright = blenderMagicTexture.makeFloat("bright", "br", 1.0)
            blenderMagicTexture.contrast = blenderMagicTexture.makeFloat("contrast", "co", 1.0)
            
            blenderMagicTexture.tex1 = blenderMagicTexture.makeColor("tex1", "t1", 0.0, 0.0, 0.0)
            blenderMagicTexture.tex2 = blenderMagicTexture.makeColor("tex2", "t2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderMagicTexture attributes\n")
            raise
        
        try:
            blenderMagicTexture.addAttribute(blenderMagicTexture.outColor)
            blenderMagicTexture.addAttribute(blenderMagicTexture.outAlpha)
            
            blenderMagicTexture.addAttribute(blenderMagicTexture.placementMatrix)
            blenderMagicTexture.addAttribute(blenderMagicTexture.pointWorld)
            
            blenderMagicTexture.addAttribute(blenderMagicTexture.translate)
            blenderMagicTexture.addAttribute(blenderMagicTexture.rotate)
            blenderMagicTexture.addAttribute(blenderMagicTexture.scale)


            blenderMagicTexture.addAttribute(blenderMagicTexture.noisedepth)
            blenderMagicTexture.addAttribute(blenderMagicTexture.turbulance)
            
            blenderMagicTexture.addAttribute(blenderMagicTexture.bright)
            blenderMagicTexture.addAttribute(blenderMagicTexture.contrast)

            blenderMagicTexture.addAttribute(blenderMagicTexture.tex1)
            blenderMagicTexture.addAttribute(blenderMagicTexture.tex2)
           
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
