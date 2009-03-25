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
class brickTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Brick Texture node for Maya
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
    
    brickwidth         = OpenMaya.MObject()
    brickheight        = OpenMaya.MObject()
    brickdepth         = OpenMaya.MObject()
    mortarsize         = OpenMaya.MObject()
    
    # pseudo-mix
    bricktex             = OpenMaya.MObject()
    mortartex            = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_brick"

    def luxName(self):
        return "brick"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757819) # 'lux' 25

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( brickTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}

        self.attributes['brickwidth']  = TextureFloatAttribute('brickwidth',  self.addToOutput, self.prependToOutput)
        self.attributes['brickheight'] = TextureFloatAttribute('brickheight',  self.addToOutput, self.prependToOutput)
        self.attributes['brickdepth']  = TextureFloatAttribute('brickdepth',  self.addToOutput, self.prependToOutput)
        self.attributes['mortarsize']  = TextureFloatAttribute('mortarsize',  self.addToOutput, self.prependToOutput)
        
        self.attributes['bricktex']    = TextureColorAttribute('bricktex',  self.addToOutput, self.prependToOutput)
        self.attributes['mortartex']   = TextureColorAttribute('mortartex',  self.addToOutput, self.prependToOutput)
        
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
            brickTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            brickTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 3D Params
            brickTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            brickTexture.makeInput(mAttr)
            
            brickTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            brickTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            brickTexture.translate = nAttr.createPoint("translate", "t")
            brickTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            brickTexture.rotate = nAttr.createPoint("rotate", "r")
            brickTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            brickTexture.scale = nAttr.createPoint("scale", "s")
            brickTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            brickTexture.brickwidth = brickTexture.makeFloat("brickwidth", "bw", 0.3)
            brickTexture.brickheight = brickTexture.makeFloat("brickheight", "bh", 0.1)
            brickTexture.brickdepth = brickTexture.makeFloat("brickdepth", "bd", 0.15)
            brickTexture.mortarsize = brickTexture.makeFloat("mortarsize", "ms", 0.01)
            
            brickTexture.bricktex = brickTexture.makeColor("bricktex", "bt", 0.0, 0.0, 0.0)
            brickTexture.mortartex = brickTexture.makeColor("mortartex", "mt", 1.0, 1.0, 1.0)


        except:
            OpenMaya.MGlobal.displayError("Failed to create brickTexture attributes\n")
            raise
        
        try:
            brickTexture.addAttribute(brickTexture.outColor)
            brickTexture.addAttribute(brickTexture.outAlpha)
            
            brickTexture.addAttribute(brickTexture.placementMatrix)
            brickTexture.addAttribute(brickTexture.pointWorld)
            
            brickTexture.addAttribute(brickTexture.translate)
            brickTexture.addAttribute(brickTexture.rotate)
            brickTexture.addAttribute(brickTexture.scale)
            
            brickTexture.addAttribute(brickTexture.brickwidth)
            brickTexture.addAttribute(brickTexture.brickheight)
            brickTexture.addAttribute(brickTexture.brickdepth)
            brickTexture.addAttribute(brickTexture.mortarsize)
            
            brickTexture.addAttribute(brickTexture.bricktex)
            brickTexture.addAttribute(brickTexture.mortartex)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
