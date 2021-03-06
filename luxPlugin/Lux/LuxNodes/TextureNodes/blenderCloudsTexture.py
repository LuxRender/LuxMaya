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
# Blender Clouds Texture node for Maya
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
class blenderCloudsTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Clouds Texture node for Maya
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
    
    type             = OpenMaya.MObject()
    aTypes = [
              'default',
              'color'
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
    
    bright           = OpenMaya.MObject()
    contrast         = OpenMaya.MObject()
    
    # pseudo-mix
    tex1             = OpenMaya.MObject()
    tex2             = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "blender_clouds"

    def luxName(self):
        return "blender_clouds"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757815) # 'lux' 21

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderCloudsTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['noisesize']  = TextureFloatAttribute('noisesize',  self.addToOutput, self.prependToOutput)
        self.attributes['noisedepth'] = TextureFloatAttribute('noisedepth',  self.addToOutput, self.prependToOutput)
        self.attributes['type']       = TextureEnumAttribute('type',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aTypes)
        self.attributes['noisetype']  = TextureEnumAttribute('noisetype',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aNoiseTypes)
        self.attributes['noisebasis'] = TextureEnumAttribute('noisebasis',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aNoises)
        
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
            blenderCloudsTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderCloudsTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderCloudsTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderCloudsTexture.makeInput(mAttr)
            
            blenderCloudsTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderCloudsTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderCloudsTexture.translate = nAttr.createPoint("translate", "t")
            blenderCloudsTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderCloudsTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderCloudsTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderCloudsTexture.scale = nAttr.createPoint("scale", "s")
            blenderCloudsTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderCloudsTexture.noisesize = blenderCloudsTexture.makeFloat("noisesize", "ns", 0.25)
            blenderCloudsTexture.noisedepth = blenderCloudsTexture.makeFloat("noisedepth", "nd", 2.0)
            
            blenderCloudsTexture.type = enumAttr.create("type", "typ", 0)
            i=0
            for type in blenderCloudsTexture.aTypes:
                enumAttr.addField( type, i )
                i+=1
            
            blenderCloudsTexture.noisetype = enumAttr.create("noisetype", "nt", 0)
            i=0
            for noise in blenderCloudsTexture.aNoiseTypes:
                enumAttr.addField( noise, i )
                i+=1
            
            blenderCloudsTexture.noisebasis = enumAttr.create("noisebasis", "nb", 0)
            i=0
            for noise in blenderCloudsTexture.aNoises:
                enumAttr.addField( noise, i )
                i+=1
                            
            blenderCloudsTexture.bright = blenderCloudsTexture.makeFloat("bright", "br", 1.0)
            blenderCloudsTexture.contrast = blenderCloudsTexture.makeFloat("contrast", "co", 1.0)
            
            blenderCloudsTexture.tex1 = blenderCloudsTexture.makeColor("tex1", "t1", 0.0, 0.0, 0.0)
            blenderCloudsTexture.tex2 = blenderCloudsTexture.makeColor("tex2", "t2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderCloudsTexture attributes\n")
            raise
        
        try:
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.outColor)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.outAlpha)
            
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.placementMatrix)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.pointWorld)
            
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.translate)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.rotate)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.scale)


            blenderCloudsTexture.addAttribute(blenderCloudsTexture.noisesize)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.noisedepth)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.type)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.noisetype)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.noisebasis)
            
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.bright)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.contrast)
            
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.tex1)
            blenderCloudsTexture.addAttribute(blenderCloudsTexture.tex2)
                       
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
