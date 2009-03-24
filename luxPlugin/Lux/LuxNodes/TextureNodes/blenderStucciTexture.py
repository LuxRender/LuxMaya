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
# Blender Stucci Texture node for Maya
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
class blenderStucciTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Stucci Texture node for Maya
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
              'Plastic',
              'Wall In',
              'Wall Out',
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
        return "blender_stucci"

    def luxName(self):
        return "blender_stucci"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75780C) # 'lux' 12

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderStucciTexture() )

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
            blenderStucciTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderStucciTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderStucciTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderStucciTexture.makeInput(mAttr)
            
            blenderStucciTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderStucciTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderStucciTexture.translate = nAttr.createPoint("translate", "t")
            blenderStucciTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderStucciTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderStucciTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderStucciTexture.scale = nAttr.createPoint("scale", "s")
            blenderStucciTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderStucciTexture.noisesize = blenderStucciTexture.makeFloat("noisesize", "ns", 0.25)
            blenderStucciTexture.turbulance = blenderStucciTexture.makeFloat("turbulance", "tu", 5.0)
            
            blenderStucciTexture.type = enumAttr.create("type", "typ", 0)
            i=0
            for type in blenderStucciTexture.aTypes:
                enumAttr.addField( type, i )
                i+=1
            
            blenderStucciTexture.noisetype = enumAttr.create("noisetype", "nt", 0)
            i=0
            for noise in blenderStucciTexture.aNoiseTypes:
                enumAttr.addField( noise, i )
                i+=1
            
            blenderStucciTexture.noisebasis = enumAttr.create("noisebasis", "nb", 0)
            i=0
            for noise in blenderStucciTexture.aNoises:
                enumAttr.addField( noise, i )
                i+=1
                            
            blenderStucciTexture.bright = blenderStucciTexture.makeFloat("bright", "br", 1.0)
            blenderStucciTexture.contrast = blenderStucciTexture.makeFloat("contrast", "co", 1.0)
            
            blenderStucciTexture.tex1 = blenderStucciTexture.makeColor("tex1", "t1", 0.0, 0.0, 0.0)
            blenderStucciTexture.tex2 = blenderStucciTexture.makeColor("tex2", "t2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderStucciTexture attributes\n")
            raise
        
        try:
            blenderStucciTexture.addAttribute(blenderStucciTexture.outColor)
            blenderStucciTexture.addAttribute(blenderStucciTexture.outAlpha)
            
            blenderStucciTexture.addAttribute(blenderStucciTexture.placementMatrix)
            blenderStucciTexture.addAttribute(blenderStucciTexture.pointWorld)
            
            blenderStucciTexture.addAttribute(blenderStucciTexture.translate)
            blenderStucciTexture.addAttribute(blenderStucciTexture.rotate)
            blenderStucciTexture.addAttribute(blenderStucciTexture.scale)


            blenderStucciTexture.addAttribute(blenderStucciTexture.noisesize)
            blenderStucciTexture.addAttribute(blenderStucciTexture.turbulance)
            blenderStucciTexture.addAttribute(blenderStucciTexture.type)
            blenderStucciTexture.addAttribute(blenderStucciTexture.noisetype)
            blenderStucciTexture.addAttribute(blenderStucciTexture.noisebasis)
            blenderStucciTexture.addAttribute(blenderStucciTexture.bright)
            blenderStucciTexture.addAttribute(blenderStucciTexture.contrast)

            blenderStucciTexture.addAttribute(blenderStucciTexture.tex1)
            blenderStucciTexture.addAttribute(blenderStucciTexture.tex2)
           
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
