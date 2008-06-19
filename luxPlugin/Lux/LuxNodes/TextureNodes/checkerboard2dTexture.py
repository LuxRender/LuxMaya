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
# Lux CheckerBoard (2D version) Texture node for Maya
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

# 2D Texture
class checkerboard2dTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Checkerboard (2D) Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()

    # maya 2d common attributes
    UVCoord         = OpenMaya.MObject()
    uvFilterSize    = OpenMaya.MObject()
    
    # lux common 2D options attributes
    mapping         = OpenMaya.MObject()
    aMappings = [
                    "uv",
                    "spherical",
                    "cylindrical",
                    "planar"
                 ]
    
    
    uscale          = OpenMaya.MObject()
    vscale          = OpenMaya.MObject()
    udelta          = OpenMaya.MObject()
    vdelta          = OpenMaya.MObject()
    v1              = OpenMaya.MObject()
    v2              = OpenMaya.MObject()
    
    # lux texture specific attributes
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
        return "lux_checkerboard2d"
    
    def luxName(self):
        return "checkerboard"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757812) # 'lux' 18

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( checkerboard2dTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/2d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
        self.attributes['tex1']   = TextureColorAttribute('tex1',  self.addToOutput, self.prependToOutput)
        self.attributes['tex2']   = TextureColorAttribute('tex2',  self.addToOutput, self.prependToOutput)
        
        self.attributes['aamode'] = TextureEnumAttribute('aamode',  self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aAAModes)
        
        self.attributes['uscale']  = TextureFloatAttribute('uscale', self.addToOutput, self.prependToOutput)
        self.attributes['vscale']  = TextureFloatAttribute('vscale', self.addToOutput, self.prependToOutput)
        
        self.attributes['udelta']  = TextureFloatAttribute('udelta', self.addToOutput, self.prependToOutput)
        self.attributes['vdelta']  = TextureFloatAttribute('vdelta', self.addToOutput, self.prependToOutput)
        
        self.attributes['mapping']  = TextureEnumAttribute('mapping', self.addToOutput, self.prependToOutput, asString = True, nameValues = self.aMappings)
        #self.attributes['v1']  = TextureVectorAttribute('v1', self.addToOutput, self.prependToOutput)
        #self.attributes['v2']  = TextureVectorAttribute('v2', self.addToOutput, self.prependToOutput)
    
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
            checkerboard2dTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            checkerboard2dTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # 2D Params
            uvChild1 = nAttr.create( "uCoord", "u", OpenMaya.MFnNumericData.kFloat )
            uvChild2 = nAttr.create( "vCoord", "v", OpenMaya.MFnNumericData.kFloat )
            checkerboard2dTexture.UVCoord = nAttr.create( "uvCoord", "uv", uvChild1, uvChild2 )
            checkerboard2dTexture.makeInput( nAttr )
            nAttr.setHidden( True )
            
            uvChild3 = nAttr.create( "uvFilterSizeX", "fsx", OpenMaya.MFnNumericData.kFloat )
            uvChild4 = nAttr.create( "uvFilterSizeY", "fsy", OpenMaya.MFnNumericData.kFloat )
            checkerboard2dTexture.uvFilterSize = nAttr.create( "uvFilterSize", "fs", uvChild3, uvChild4 )
            checkerboard2dTexture.makeInput( nAttr )
            nAttr.setHidden( True )
            
            checkerboard2dTexture.mapping = enumAttr.create('mapping', 'mp', 0)
            i=0
            for type in checkerboard2dTexture.aMappings:
                enumAttr.addField( type, i )
                i+=1

            checkerboard2dTexture.uscale = checkerboard2dTexture.makeFloat('uscale', 'us', 1.0 )
            checkerboard2dTexture.vscale = checkerboard2dTexture.makeFloat('vscale', 'vs', 1.0 )

            checkerboard2dTexture.udelta = checkerboard2dTexture.makeFloat('udelta', 'ud', 1.0 )
            checkerboard2dTexture.vdelta = checkerboard2dTexture.makeFloat('vdelta', 'vd', 1.0 )
            
            checkerboard2dTexture.v1 = nAttr.createPoint("v1", "v1")
            checkerboard2dTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 0.0, 0.0 )
            checkerboard2dTexture.v2 = nAttr.createPoint("v2", "v2")
            checkerboard2dTexture.makeInput(nAttr)
            nAttr.setDefault( 0.0, 1.0, 0.0 ) 
            
            checkerboard2dTexture.tex1 = checkerboard2dTexture.makeColor("tex1", "t1")
            checkerboard2dTexture.tex2 = checkerboard2dTexture.makeColor("tex2", "t2")
            
            checkerboard2dTexture.aamode = enumAttr.create( 'aamode', 'aa', 0)
            i=0
            for mode in checkerboard2dTexture.aAAModes:
                enumAttr.addField( mode, i )
                i+=1
                
        except:
            OpenMaya.MGlobal.displayError("Failed to create checkerboard2dTexture attributes\n")
            raise
        
        try:
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.outColor)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.outAlpha)
            
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.UVCoord)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.uvFilterSize)

            checkerboard2dTexture.addAttribute(checkerboard2dTexture.mapping)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.uscale)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.vscale)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.udelta)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.vdelta)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.v1)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.v2)
            
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.tex1)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.tex2)
            checkerboard2dTexture.addAttribute(checkerboard2dTexture.aamode)
            
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.mapping, checkerboard2dTexture.outColor)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.uscale, checkerboard2dTexture.outColor)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.vscale, checkerboard2dTexture.outColor)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.udelta, checkerboard2dTexture.outColor)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.vdelta, checkerboard2dTexture.outColor)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.v1, checkerboard2dTexture.outColor)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.v2, checkerboard2dTexture.outColor)
#            
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.tex1, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.tex2, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.aamode, checkerboard2dTexture.outAlpha)
#            
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.mapping, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.uscale, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.vscale, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.udelta, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.vdelta, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.v1, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.v2, checkerboard2dTexture.outAlpha)
#            
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.tex1, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.tex2, checkerboard2dTexture.outAlpha)
#            checkerboard2dTexture.attributeAffects(checkerboard2dTexture.aamode, checkerboard2dTexture.outAlpha)

        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise