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
# Blender Voronoi Texture node for Maya
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
class blenderVoronoiTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Blender Voronoi Texture node for Maya
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
    distmetric       = OpenMaya.MObject()
    aDistmetrics = [
                'actual_distance',
                'distance_squared',
                'manhattan',
                'chebychev',
                'minkovsky_half',
                'minkovsky_four',
                'minkovsky',
               ]
    
    minkovsky_exp    = OpenMaya.MObject()
    outscale         = OpenMaya.MObject()
    noisesize        = OpenMaya.MObject()
    nabla            = OpenMaya.MObject()
    w1               = OpenMaya.MObject()
    w2               = OpenMaya.MObject()
    w3               = OpenMaya.MObject()
    w4               = OpenMaya.MObject()
    
    bright           = OpenMaya.MObject()
    contrast         = OpenMaya.MObject()
    
    # pseudo-mix
    tex1             = OpenMaya.MObject()
    tex2             = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "blender_voronoi"

    def luxName(self):
        return "blender_voronoi"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75780B) # 'lux' 11

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( blenderVoronoiTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['distmetric']     = TextureEnumAttribute('distmetric',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aDistmetrics)

        self.attributes['minkovsky_exp']  = TextureFloatAttribute('minkovsky_exp',  self.addToOutput, self.prependToOutput)
        self.attributes['outscale']       = TextureFloatAttribute('outscale',  self.addToOutput, self.prependToOutput)
        self.attributes['noisesize']      = TextureFloatAttribute('noisesize',  self.addToOutput, self.prependToOutput)
        self.attributes['nabla']          = TextureFloatAttribute('nabla',  self.addToOutput, self.prependToOutput)
        self.attributes['w1']             = TextureFloatAttribute('w1',  self.addToOutput, self.prependToOutput)
        self.attributes['w2']             = TextureFloatAttribute('w2',  self.addToOutput, self.prependToOutput)
        self.attributes['w3']             = TextureFloatAttribute('w3',  self.addToOutput, self.prependToOutput)
        self.attributes['w4']             = TextureFloatAttribute('w4',  self.addToOutput, self.prependToOutput)

        self.attributes['bright']         = TextureFloatAttribute('bright',  self.addToOutput, self.prependToOutput)
        self.attributes['contrast']       = TextureFloatAttribute('contrast',  self.addToOutput, self.prependToOutput)
        
        self.attributes['translate']      = TextureVectorAttribute('translate', self.addToOutput, self.prependToOutput)
        self.attributes['rotate']         = TextureVectorAttribute('rotate', self.addToOutput, self.prependToOutput)
        self.attributes['scale']          = TextureVectorAttribute('scale', self.addToOutput, self.prependToOutput)
        
        self.attributes['tex1']           = TextureColorAttribute('tex1',  self.addToOutput, self.prependToOutput)
        self.attributes['tex2']           = TextureColorAttribute('tex2',  self.addToOutput, self.prependToOutput)
    
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
            blenderVoronoiTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            blenderVoronoiTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            blenderVoronoiTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            blenderVoronoiTexture.makeInput(mAttr)
            
            blenderVoronoiTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            blenderVoronoiTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            blenderVoronoiTexture.translate = nAttr.createPoint("translate", "t")
            blenderVoronoiTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderVoronoiTexture.rotate = nAttr.createPoint("rotate", "r")
            blenderVoronoiTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            blenderVoronoiTexture.scale = nAttr.createPoint("scale", "s")
            blenderVoronoiTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            blenderVoronoiTexture.distmetric = enumAttr.create("distmetric", "dm", 0)
            i=0
            for dm in blenderVoronoiTexture.aDistmetrics:
                enumAttr.addField( dm, i )
                i+=1
            
            blenderVoronoiTexture.minkovsky_exp = blenderVoronoiTexture.makeFloat("minkovsky_exp", "me", 2.5)
            blenderVoronoiTexture.outscale = blenderVoronoiTexture.makeFloat("outscale", "os", 1.0)
            blenderVoronoiTexture.noisesize = blenderVoronoiTexture.makeFloat("noisesize", "ns", 0.25)
            blenderVoronoiTexture.nabla = blenderVoronoiTexture.makeFloat("nabla", "na", 0.025)
            blenderVoronoiTexture.w1 = blenderVoronoiTexture.makeFloat("w1", "w1", 1.0)
            blenderVoronoiTexture.w2 = blenderVoronoiTexture.makeFloat("w2", "w2", 0.0)
            blenderVoronoiTexture.w3 = blenderVoronoiTexture.makeFloat("w3", "w3", 0.0)
            blenderVoronoiTexture.w4 = blenderVoronoiTexture.makeFloat("w4", "w4", 0.0)
                            
            blenderVoronoiTexture.bright = blenderVoronoiTexture.makeFloat("bright", "br", 1.0)
            blenderVoronoiTexture.contrast = blenderVoronoiTexture.makeFloat("contrast", "co", 1.0)
            
            blenderVoronoiTexture.tex1 = blenderVoronoiTexture.makeColor("tex1", "t1", 0.0, 0.0, 0.0)
            blenderVoronoiTexture.tex2 = blenderVoronoiTexture.makeColor("tex2", "t2", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create blenderVoronoiTexture attributes\n")
            raise
        
        try:
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.outColor)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.outAlpha)
            
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.placementMatrix)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.pointWorld)
            
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.translate)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.rotate)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.scale)

            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.distmetric)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.minkovsky_exp)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.outscale)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.noisesize)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.nabla)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.w1)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.w2)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.w3)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.w4)
            
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.bright)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.contrast)

            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.tex1)
            blenderVoronoiTexture.addAttribute(blenderVoronoiTexture.tex2)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
