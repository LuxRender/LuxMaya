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
# Blender Musgrave Texture node for Maya
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
class blenderMusgraveTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Musgrave Texture node for Maya
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
    h                = OpenMaya.MObject()
    lacu             = OpenMaya.MObject()
    octs             = OpenMaya.MObject()
    gain             = OpenMaya.MObject()
    offset           = OpenMaya.MObject()
    noisesize        = OpenMaya.MObject()
    outscale         = OpenMaya.MObject()
    type             = OpenMaya.MObject()
    aTypes = [
              'multifractal',
              'ridged_multifractal',
              'hybrid_multifractal',
              'hetero_terrain',
              'fbm'
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
        return "blender_musgrave"

    def luxName(self):
        return "blender_musgrave"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757814) # 'lux' 20

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderMusgraveTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
        self.attributes['h']          = TextureFloatAttribute('h',  self.addToOutput, self.prependToOutput)
        self.attributes['lacu']       = TextureFloatAttribute('lacu',  self.addToOutput, self.prependToOutput)
        self.attributes['octs']       = TextureFloatAttribute('octs',  self.addToOutput, self.prependToOutput)
        self.attributes['gain']       = TextureFloatAttribute('gain',  self.addToOutput, self.prependToOutput)
        self.attributes['offset']     = TextureFloatAttribute('offset',  self.addToOutput, self.prependToOutput)
        self.attributes['noisesize']  = TextureFloatAttribute('noisesize',  self.addToOutput, self.prependToOutput)
        self.attributes['outscale']   = TextureFloatAttribute('outscale',  self.addToOutput, self.prependToOutput)
        self.attributes['type']       = TextureEnumAttribute('type',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aTypes)
        self.attributes['noisebasis'] = TextureEnumAttribute('noisebasis',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aNoises)
        self.attributes['bright']     = TextureFloatAttribute('bright',  self.addToOutput, self.prependToOutput)
        self.attributes['contrast']   = TextureFloatAttribute('contrast',  self.addToOutput, self.prependToOutput)
        
        self.attributes['tex1']   = TextureColorAttribute('tex1', self.addToOutput, self.prependToOutput)
        self.attributes['tex2']   = TextureColorAttribute('tex2', self.addToOutput, self.prependToOutput)
        
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
        enumAttr = OpenMaya.MFnEnumAttribute()
        
        try:
            blenderMusgraveTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderMusgraveTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderMusgraveTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderMusgraveTexture.makeInput(mAttr)
            
            blenderMusgraveTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderMusgraveTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderMusgraveTexture.translate = nAttr.createPoint("translate", "t")
            blenderMusgraveTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderMusgraveTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderMusgraveTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderMusgraveTexture.scale = nAttr.createPoint("scale", "s")
            blenderMusgraveTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderMusgraveTexture.h = blenderMusgraveTexture.makeFloat("h", "h", 1.00)
            blenderMusgraveTexture.lacu = blenderMusgraveTexture.makeFloat("lacu", "la", 2.0)
            blenderMusgraveTexture.octs = blenderMusgraveTexture.makeFloat("octs", "oct", 2.0)
            blenderMusgraveTexture.gain = blenderMusgraveTexture.makeFloat("gain", "ga", 1.0)
            blenderMusgraveTexture.offset = blenderMusgraveTexture.makeFloat("offset", "of", 1.0)
            blenderMusgraveTexture.noisesize = blenderMusgraveTexture.makeFloat("noisesize", "ns", 0.25)
            blenderMusgraveTexture.outscale = blenderMusgraveTexture.makeFloat("outscale", "os", 1.0)
            
            blenderMusgraveTexture.type = enumAttr.create("type", "typ", 0)
            i=0
            for type in blenderMusgraveTexture.aTypes:
                enumAttr.addField( type, i )
                i+=1
            
            blenderMusgraveTexture.noisebasis = enumAttr.create("noisebasis", "nb", 0)
            i=0
            for noise in blenderMusgraveTexture.aNoises:
                enumAttr.addField( noise, i )
                i+=1
                            
            blenderMusgraveTexture.bright = blenderMusgraveTexture.makeFloat("bright", "br", 1.0)
            blenderMusgraveTexture.contrast = blenderMusgraveTexture.makeFloat("contrast", "co", 1.0)
            
            blenderMusgraveTexture.tex1 = blenderMusgraveTexture.makeColor("tex1", "te1", 0.0, 0.0, 0.0)
            blenderMusgraveTexture.tex2 = blenderMusgraveTexture.makeColor("tex2", "te2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderMusgraveTexture attributes\n")
            raise
        
        try:
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.outColor)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.outAlpha)
            
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.placementMatrix)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.pointWorld)
            
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.h)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.lacu)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.octs)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.gain)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.offset)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.noisesize)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.outscale)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.type)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.noisebasis)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.bright)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.contrast)

            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.tex1)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.tex2)
            
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.translate)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.rotate)
            blenderMusgraveTexture.addAttribute(blenderMusgraveTexture.scale)
                       
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
