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
from Lux.LuxNodes.LuxNode import TextureFloatAttribute
from Lux.LuxNodes.LuxNode import TextureEnumAttribute
from Lux.LuxNodes.LuxNode import TextureVectorAttribute

## 3D Texture
class blenderWoodTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Wood Texture node for Maya
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
    
    noisesize        = OpenMaya.MObject()
    turbulance       = OpenMaya.MObject()
    
    type             = OpenMaya.MObject()
    aTypes = [
              'bands',
              'rings',
              'bandnoise',
              'ringnoise'
              ]
    
    noisetype        = OpenMaya.MObject()
    aNoiseTypes = [
              'soft_noise',
              'hard_noise'
              ]
    
    
    noisebasis       = OpenMaya.MObject()
    aNoises = [
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
    
    noisebasis2      = OpenMaya.MObject()
    aNoises2 = [
                'sin',
                'tri',
                'saw'
                ]
    
    bright           = OpenMaya.MObject()
    contrast         = OpenMaya.MObject()
    
    # pseudo-mix
    tex1             = OpenMaya.MObject()
    tex2             = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "blender_wood"

    def luxName(self):
        return "blender_wood"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757816) # 'lux' 22

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderWoodTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['noisesize']  = TextureFloatAttribute('noisesize',  self.addToOutput, self.prependToOutput)
        self.attributes['turbulance']  = TextureFloatAttribute('turbulance',  self.addToOutput, self.prependToOutput)
        
        self.attributes['type']       = TextureEnumAttribute('type',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aTypes)
        self.attributes['noisetype']  = TextureEnumAttribute('noisetype',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aNoiseTypes)
        self.attributes['noisebasis'] = TextureEnumAttribute('noisebasis',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aNoises)
        self.attributes['noisebasis2'] = TextureEnumAttribute('noisebasis2',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aNoises2)
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
            blenderWoodTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderWoodTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderWoodTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderWoodTexture.makeInput(mAttr)
            
            blenderWoodTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderWoodTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderWoodTexture.translate = nAttr.createPoint("translate", "t")
            blenderWoodTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderWoodTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderWoodTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderWoodTexture.scale = nAttr.createPoint("scale", "s")
            blenderWoodTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderWoodTexture.noisesize = blenderWoodTexture.makeFloat("noisesize", "ns", 0.25)
            blenderWoodTexture.turbulance = blenderWoodTexture.makeFloat("turbulance", "tu", 5.0)
            
            blenderWoodTexture.type = enumAttr.create("type", "typ", 0)
            i=0
            for type in blenderWoodTexture.aTypes:
                enumAttr.addField( type, i )
                i+=1
            
            blenderWoodTexture.noisetype = enumAttr.create("noisetype", "nt", 0)
            i=0
            for noise in blenderWoodTexture.aNoiseTypes:
                enumAttr.addField( noise, i )
                i+=1
            
            blenderWoodTexture.noisebasis = enumAttr.create("noisebasis", "nb", 0)
            i=0
            for noise in blenderWoodTexture.aNoises:
                enumAttr.addField( noise, i )
                i+=1
                
            blenderWoodTexture.noisebasis2 = enumAttr.create("noisebasis2", "nb2", 0)
            i=0
            for noise in blenderWoodTexture.aNoises2:
                enumAttr.addField( noise, i )
                i+=1
                            
            blenderWoodTexture.bright = blenderWoodTexture.makeFloat("bright", "br", 1.0)
            blenderWoodTexture.contrast = blenderWoodTexture.makeFloat("contrast", "co", 1.0)
            
            blenderWoodTexture.tex1 = blenderWoodTexture.makeColor("tex1", "t1", 0.0, 0.0, 0.0)
            blenderWoodTexture.tex2 = blenderWoodTexture.makeColor("tex2", "t2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderWoodTexture attributes\n")
            raise
        
        try:
            blenderWoodTexture.addAttribute(blenderWoodTexture.outColor)
            blenderWoodTexture.addAttribute(blenderWoodTexture.outAlpha)
            
            blenderWoodTexture.addAttribute(blenderWoodTexture.placementMatrix)
            blenderWoodTexture.addAttribute(blenderWoodTexture.pointWorld)
            
            blenderWoodTexture.addAttribute(blenderWoodTexture.translate)
            blenderWoodTexture.addAttribute(blenderWoodTexture.rotate)
            blenderWoodTexture.addAttribute(blenderWoodTexture.scale)


            blenderWoodTexture.addAttribute(blenderWoodTexture.noisesize)
            blenderWoodTexture.addAttribute(blenderWoodTexture.turbulance)
            blenderWoodTexture.addAttribute(blenderWoodTexture.type)
            blenderWoodTexture.addAttribute(blenderWoodTexture.noisetype)
            blenderWoodTexture.addAttribute(blenderWoodTexture.noisebasis)
            blenderWoodTexture.addAttribute(blenderWoodTexture.noisebasis2)
            blenderWoodTexture.addAttribute(blenderWoodTexture.bright)
            blenderWoodTexture.addAttribute(blenderWoodTexture.contrast)

            blenderWoodTexture.addAttribute(blenderWoodTexture.tex1)
            blenderWoodTexture.addAttribute(blenderWoodTexture.tex2)
                       
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
