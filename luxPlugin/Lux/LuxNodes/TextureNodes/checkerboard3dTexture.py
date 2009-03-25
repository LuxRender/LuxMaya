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
# Lux CheckerBoard (3D version) Texture node for Maya
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureIntegerAttribute
from Lux.LuxNodes.LuxNode import TextureFloatAttribute
from Lux.LuxNodes.LuxNode import TextureColorAttribute
from Lux.LuxNodes.LuxNode import TextureEnumAttribute
from Lux.LuxNodes.LuxNode import TextureVectorAttribute

# 3D Texture
class checkerboard3dTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Checkerboard (3D) Texture node for Maya
    """

    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    placementMatrix = OpenMaya.MObject()
    pointWorld      = OpenMaya.MObject()
    
    translate       = OpenMaya.MObject()
    rotate          = OpenMaya.MObject()
    scale           = OpenMaya.MObject()
    
    #dimension       = OpenMaya.MObject()
    tex1            = OpenMaya.MObject()
    tex2            = OpenMaya.MObject()
    aamode          = OpenMaya.MObject()
    aAAModes = [
                    'closedform',
                    'supersample',
                    'none'
                ]
    
    @staticmethod
    def nodeName():
        return "lux_checkerboard3d"
    
    def luxName(self):
        return "checkerboard"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757808) # 'lux' 08

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( checkerboard3dTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
        self.attributes['tex1']   = TextureColorAttribute('tex1',  self.addToOutput, self.prependToOutput)
        self.attributes['tex2']   = TextureColorAttribute('tex2',  self.addToOutput, self.prependToOutput)
        self.attributes['aamode'] = TextureEnumAttribute('aamode',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aAAModes)
        
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
            checkerboard3dTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            checkerboard3dTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            checkerboard3dTexture.translate = nAttr.createPoint("translate", "t")
            checkerboard3dTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            checkerboard3dTexture.rotate = nAttr.createPoint("rotate", "r")
            checkerboard3dTexture.makeInput(nAttr)
            #nAttr.setHidden(True)
            
            checkerboard3dTexture.scale = nAttr.createPoint("scale", "s")
            checkerboard3dTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 1.0, 1.0 )
            #nAttr.setHidden(True)
            
            checkerboard3dTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            checkerboard3dTexture.makeInput(mAttr)
            
            checkerboard3dTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            checkerboard3dTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            checkerboard3dTexture.tex1 = checkerboard3dTexture.makeColor("tex1", "t1")
            checkerboard3dTexture.tex2 = checkerboard3dTexture.makeColor("tex2", "t2")
            
            checkerboard3dTexture.aamode = enumAttr.create( 'aamode', 'aa', 0)
            i=0
            for mode in checkerboard3dTexture.aAAModes:
                enumAttr.addField( mode, i )
                i+=1

        except:
            OpenMaya.MGlobal.displayError("Failed to create checkerboard3dTexture attributes\n")
            raise
        
        try:
            checkerboard3dTexture.addAttribute(checkerboard3dTexture.outColor)
            checkerboard3dTexture.addAttribute(checkerboard3dTexture.outAlpha)
            checkerboard3dTexture.addAttribute(checkerboard3dTexture.placementMatrix)
            checkerboard3dTexture.addAttribute(checkerboard3dTexture.pointWorld)
            
            checkerboard3dTexture.addAttribute(checkerboard3dTexture.translate)
            checkerboard3dTexture.addAttribute(checkerboard3dTexture.rotate)
            checkerboard3dTexture.addAttribute(checkerboard3dTexture.scale)

            checkerboard3dTexture.addAttribute(checkerboard3dTexture.tex1)
            checkerboard3dTexture.addAttribute(checkerboard3dTexture.tex2)
            checkerboard3dTexture.addAttribute(checkerboard3dTexture.aamode)
                        
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise