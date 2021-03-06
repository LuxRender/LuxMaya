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
# Blender Marble Texture node for Maya
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureIntegerAttribute
from Lux.LuxNodes.LuxNode import TextureFloatAttribute
from Lux.LuxNodes.LuxNode import TextureEnumAttribute
from Lux.LuxNodes.LuxNode import TextureColorAttribute
from Lux.LuxNodes.LuxNode import TextureVectorAttribute

## 3D Texture
class blenderMarbleTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Marble Texture node for Maya
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
    noisedepth       = OpenMaya.MObject()
    turbulance       = OpenMaya.MObject()
    
    type             = OpenMaya.MObject()
    aTypes = [
              'soft',
              'sharp',
              'sharper'
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
        return "blender_marble"

    def luxName(self):
        return "blender_marble"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757817) # 'lux' 23

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderMarbleTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['noisesize']  = TextureFloatAttribute('noisesize',  self.addToOutput, self.prependToOutput)
        self.attributes['noisedepth']  = TextureIntegerAttribute('noisedepth',  self.addToOutput, self.prependToOutput)
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
            blenderMarbleTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderMarbleTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderMarbleTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderMarbleTexture.makeInput(mAttr)
            
            blenderMarbleTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderMarbleTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderMarbleTexture.translate = nAttr.createPoint("translate", "t")
            blenderMarbleTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderMarbleTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderMarbleTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderMarbleTexture.scale = nAttr.createPoint("scale", "s")
            blenderMarbleTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderMarbleTexture.noisesize = blenderMarbleTexture.makeFloat("noisesize", "ns", 0.25)
            blenderMarbleTexture.noisedepth = blenderMarbleTexture.makeInteger("noisedepth", "nd", 2)
            blenderMarbleTexture.turbulance = blenderMarbleTexture.makeFloat("turbulance", "tu", 5.0)
            
            blenderMarbleTexture.type = enumAttr.create("type", "typ", 0)
            i=0
            for type in blenderMarbleTexture.aTypes:
                enumAttr.addField( type, i )
                i+=1
            
            blenderMarbleTexture.noisetype = enumAttr.create("noisetype", "nt", 0)
            i=0
            for noise in blenderMarbleTexture.aNoiseTypes:
                enumAttr.addField( noise, i )
                i+=1
            
            blenderMarbleTexture.noisebasis = enumAttr.create("noisebasis", "nb", 0)
            i=0
            for noise in blenderMarbleTexture.aNoises:
                enumAttr.addField( noise, i )
                i+=1
                
            blenderMarbleTexture.noisebasis2 = enumAttr.create("noisebasis2", "nb2", 0)
            i=0
            for noise in blenderMarbleTexture.aNoises2:
                enumAttr.addField( noise, i )
                i+=1
                            
            blenderMarbleTexture.bright = blenderMarbleTexture.makeFloat("bright", "br", 1.0)
            blenderMarbleTexture.contrast = blenderMarbleTexture.makeFloat("contrast", "co", 1.0)
            
            blenderMarbleTexture.tex1 = blenderMarbleTexture.makeColor("tex1", "t1", 0.0, 0.0, 0.0)
            blenderMarbleTexture.tex2 = blenderMarbleTexture.makeColor("tex2", "t2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderMarbleTexture attributes\n")
            raise
        
        try:
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.outColor)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.outAlpha)
            
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.placementMatrix)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.pointWorld)
            
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.translate)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.rotate)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.scale)


            blenderMarbleTexture.addAttribute(blenderMarbleTexture.noisesize)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.noisedepth)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.turbulance)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.type)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.noisetype)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.noisebasis)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.noisebasis2)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.bright)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.contrast)

            blenderMarbleTexture.addAttribute(blenderMarbleTexture.tex1)
            blenderMarbleTexture.addAttribute(blenderMarbleTexture.tex2)
                       
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
