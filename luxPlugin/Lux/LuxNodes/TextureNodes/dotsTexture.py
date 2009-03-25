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
# Lux Dots Texture node for Maya
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureColorAttribute
from Lux.LuxNodes.LuxNode import TextureFloatAttribute
from Lux.LuxNodes.LuxNode import TextureEnumAttribute

# 3D Texture
class dotsTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Dots Texture node for Maya
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
    inside          = OpenMaya.MObject()
    outside         = OpenMaya.MObject() 
    
    @staticmethod
    def nodeName():
        return "lux_dots"
    
    def luxName(self):
        return "dots"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757809) # 'lux' 09

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( dotsTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/2d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
        self.attributes['inside']  = TextureColorAttribute('inside',  self.addToOutput, self.prependToOutput)
        self.attributes['outside'] = TextureColorAttribute('outside', self.addToOutput, self.prependToOutput)
        
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
            dotsTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            dotsTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)

            # 2D Params
            uvChild1 = nAttr.create( "uCoord", "u", OpenMaya.MFnNumericData.kFloat )
            uvChild2 = nAttr.create( "vCoord", "v", OpenMaya.MFnNumericData.kFloat )
            dotsTexture.UVCoord = nAttr.create( "uvCoord", "uv", uvChild1, uvChild2 )
            dotsTexture.makeInput( nAttr )
            nAttr.setHidden( True )
            
            uvChild3 = nAttr.create( "uvFilterSizeX", "fsx", OpenMaya.MFnNumericData.kFloat )
            uvChild4 = nAttr.create( "uvFilterSizeY", "fsy", OpenMaya.MFnNumericData.kFloat )
            dotsTexture.uvFilterSize = nAttr.create( "uvFilterSize", "fs", uvChild3, uvChild4 )
            dotsTexture.makeInput( nAttr )
            nAttr.setHidden( True )


            dotsTexture.mapping = enumAttr.create('mapping', 'mp', 0)
            i=0
            for type in dotsTexture.aMappings:
                enumAttr.addField( type, i )
                i+=1

            dotsTexture.uscale = dotsTexture.makeFloat('uscale', 'us', 1.0 )
            dotsTexture.vscale = dotsTexture.makeFloat('vscale', 'vs', 1.0 )

            dotsTexture.udelta = dotsTexture.makeFloat('udelta', 'ud', 1.0 )
            dotsTexture.vdelta = dotsTexture.makeFloat('vdelta', 'vd', 1.0 )

            dotsTexture.v1 = nAttr.createPoint("v1", "v1")
            dotsTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 0.0, 0.0 )
            dotsTexture.v2 = nAttr.createPoint("v2", "v2")
            dotsTexture.makeInput(nAttr)
            nAttr.setDefault( 0.0, 1.0, 0.0 )
            
            dotsTexture.inside = dotsTexture.makeColor("inside", "in")
            dotsTexture.outside = dotsTexture.makeColor("outside", "out")


        except:
            OpenMaya.MGlobal.displayError("Failed to create dotsTexture attributes\n")
            raise
        
        try:
            dotsTexture.addAttribute(dotsTexture.outColor)
            dotsTexture.addAttribute(dotsTexture.outAlpha)

            dotsTexture.addAttribute(dotsTexture.UVCoord)
            dotsTexture.addAttribute(dotsTexture.uvFilterSize)

            dotsTexture.addAttribute(dotsTexture.mapping)
            dotsTexture.addAttribute(dotsTexture.uscale)
            dotsTexture.addAttribute(dotsTexture.vscale)
            dotsTexture.addAttribute(dotsTexture.udelta)
            dotsTexture.addAttribute(dotsTexture.vdelta)
            dotsTexture.addAttribute(dotsTexture.v1)
            dotsTexture.addAttribute(dotsTexture.v2)
            
            dotsTexture.addAttribute(dotsTexture.inside)
            dotsTexture.addAttribute(dotsTexture.outside)
                        
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise