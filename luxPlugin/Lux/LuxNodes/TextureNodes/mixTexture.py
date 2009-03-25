## ------------------------------------------------------------------------------
## Lux texture nodes for Maya
##
## by Doug Hammond 05/2008
##
## This file is licensed under the GPL
## http://www.gnu.org/licenses/gpl-3.0.txt
##
## $Id$
##
## ------------------------------------------------------------------------------
##
## Lux Mix Texture node for Maya
##
## ------------------------------------------------------------------------------
#
import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureColorAttribute
from Lux.LuxNodes.LuxNode import TextureFloatAttribute

# Float Texture
class mixTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Mix Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
    # lux texture specific attributes
    tex1             = OpenMaya.MObject()
    tex2             = OpenMaya.MObject()
    amount           = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_mix"
    
    def luxName(self):
        return "mix"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757813) # 'lux' 19

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( mixTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/other"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
        self.attributes['tex1']   = TextureColorAttribute('tex1',  self.addToOutput, self.prependToOutput)
        self.attributes['tex2']   = TextureColorAttribute('tex2',  self.addToOutput, self.prependToOutput)
        self.attributes['amount']   = TextureFloatAttribute('amount',  self.addToOutput, self.prependToOutput)
    
    def postConstructor(self):
        self._setMPSafe( True )
        self.setExistWithoutOutConnections( True )
        self.setExistWithoutInConnections( True )
    
    @staticmethod
    def nodeInitializer():
        nAttr = OpenMaya.MFnNumericAttribute()
        mAttr = OpenMaya.MFnMatrixAttribute()
        
        try:
            mixTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            mixTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            mixTexture.tex1 = mixTexture.makeColor("tex1", "t1")
            mixTexture.tex2 = mixTexture.makeColor("tex2", "t2")
            mixTexture.amount = mixTexture.makeFloat("amount", "am")


        except:
            OpenMaya.MGlobal.displayError("Failed to create mixTexture attributes\n")
            raise
        
        try:
            mixTexture.addAttribute(mixTexture.outColor)
            mixTexture.addAttribute(mixTexture.outAlpha)
            
            mixTexture.addAttribute(mixTexture.tex1)
            mixTexture.addAttribute(mixTexture.tex2)
            mixTexture.addAttribute(mixTexture.amount)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
