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
## Lux scale Texture node for Maya
##
## ------------------------------------------------------------------------------
#
import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureColorAttribute

# Float Texture
class scaleTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux scale Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
    # lux texture specific attributes
    tex1             = OpenMaya.MObject()
    tex2             = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_scale"
    
    def luxName(self):
        return "scale"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C75780A) # 'lux' 10

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( scaleTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/other"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
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
        
        try:
            scaleTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            scaleTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            scaleTexture.tex1 = scaleTexture.makeColor("tex1", "t1")
            scaleTexture.tex2 = scaleTexture.makeColor("tex2", "t2")


        except:
            OpenMaya.MGlobal.displayError("Failed to create scaleTexture attributes\n")
            raise
        
        try:
            scaleTexture.addAttribute(scaleTexture.outColor)
            scaleTexture.addAttribute(scaleTexture.outAlpha)
            
            scaleTexture.addAttribute(scaleTexture.tex1)
            scaleTexture.addAttribute(scaleTexture.tex2)
                      
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
