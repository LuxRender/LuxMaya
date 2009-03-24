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
# Blender Distortednoise Texture node for Maya
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
class blenderDistortednoiseTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Distortednoise Texture node for Maya
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
    
    distamount       = OpenMaya.MObject()
    noisesize        = OpenMaya.MObject()
    nabla            = OpenMaya.MObject()
    
    type             = OpenMaya.MObject()
    noisebasis       = OpenMaya.MObject()
    aTypes = [
                'blender_original',
                'original_perlin',
                'improved_perlin',
                'voronoi_f1',
                'voronoi_f2',
                'voronoi_f3',
                'voronoi_f4',
                'voronoi_f2f1',
                'voronoi_crackle',
                'cell_noise'
               ]
    
    bright           = OpenMaya.MObject()
    contrast         = OpenMaya.MObject()
    
    # pseudo-mix
    tex1             = OpenMaya.MObject()
    tex2             = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "blender_distortednoise"

    def luxName(self):
        return "blender_distortednoise"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75780F) # 'lux' 15

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderDistortednoiseTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['distamount']  = TextureFloatAttribute('distamount',  self.addToOutput, self.prependToOutput)
        self.attributes['noisesize']  = TextureFloatAttribute('noisesize',  self.addToOutput, self.prependToOutput)
        self.attributes['nabla']  = TextureFloatAttribute('nabla',  self.addToOutput, self.prependToOutput)
        
        self.attributes['type']       = TextureEnumAttribute('type',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aTypes)
        self.attributes['noisebasis'] = TextureEnumAttribute('noisebasis',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aTypes)
        
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
            blenderDistortednoiseTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderDistortednoiseTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderDistortednoiseTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderDistortednoiseTexture.makeInput(mAttr)
            
            blenderDistortednoiseTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderDistortednoiseTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderDistortednoiseTexture.translate = nAttr.createPoint("translate", "t")
            blenderDistortednoiseTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderDistortednoiseTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderDistortednoiseTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderDistortednoiseTexture.scale = nAttr.createPoint("scale", "s")
            blenderDistortednoiseTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderDistortednoiseTexture.distamount = blenderDistortednoiseTexture.makeFloat("distamount", "dam", 1.0)
            blenderDistortednoiseTexture.noisesize = blenderDistortednoiseTexture.makeFloat("noisesize", "nos", 0.25)
            blenderDistortednoiseTexture.nabla = blenderDistortednoiseTexture.makeFloat("nabla", "nab", 5.0)
            
            blenderDistortednoiseTexture.type = enumAttr.create("type", "typ", 0)
            i=0
            for type in blenderDistortednoiseTexture.aTypes:
                enumAttr.addField( type, i )
                i+=1
            
            blenderDistortednoiseTexture.noisebasis = enumAttr.create("noisebasis", "nba", 0)
            i=0
            for noise in blenderDistortednoiseTexture.aTypes:
                enumAttr.addField( noise, i )
                i+=1
            
            blenderDistortednoiseTexture.bright = blenderDistortednoiseTexture.makeFloat("bright", "br", 1.0)
            blenderDistortednoiseTexture.contrast = blenderDistortednoiseTexture.makeFloat("contrast", "co", 1.0)
            
            blenderDistortednoiseTexture.tex1 = blenderDistortednoiseTexture.makeColor("tex1", "t1", 0.0, 0.0, 0.0)
            blenderDistortednoiseTexture.tex2 = blenderDistortednoiseTexture.makeColor("tex2", "t2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderDistortednoiseTexture attributes\n")
            raise
        
        try:
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.outColor)
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.outAlpha)
            
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.placementMatrix)
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.pointWorld)
            
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.translate)
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.rotate)
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.scale)

            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.distamount)
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.noisesize)
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.nabla)
            
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.type)
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.noisebasis)
            
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.bright)
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.contrast)

            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.tex1)
            blenderDistortednoiseTexture.addAttribute(blenderDistortednoiseTexture.tex2)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
