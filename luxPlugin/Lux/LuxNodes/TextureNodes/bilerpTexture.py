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
# Lux BiLerp Texture node for Maya
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode
from Lux.LuxNodes.LuxNode import TextureFloatAttribute
from Lux.LuxNodes.LuxNode import TextureColorAttribute
from Lux.LuxNodes.LuxNode import TextureEnumAttribute

# 2D Texture
class bilerpTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux BiLerp Texture node for Maya
    """

    # maya texture common attributes
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
    v00             = OpenMaya.MObject()
    v01             = OpenMaya.MObject()
    v10             = OpenMaya.MObject()
    v11             = OpenMaya.MObject()
    
    @staticmethod
    def nodeName():
        return "lux_bilerp"
    
    def luxName(self):
        return "bilerp"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757807) # 'lux' 07

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( bilerpTexture() )

    @staticmethod
    def nodeClassify():
        return "texture/2d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
        self.attributes['v00']   = TextureColorAttribute('v00',  self.addToOutput, self.prependToOutput)
        self.attributes['v01']   = TextureColorAttribute('v01',  self.addToOutput, self.prependToOutput)
        self.attributes['v10']   = TextureColorAttribute('v10',  self.addToOutput, self.prependToOutput)
        self.attributes['v11']   = TextureColorAttribute('v11',  self.addToOutput, self.prependToOutput)
        
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
            bilerpTexture.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            bilerpTexture.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)

            # 2D Params
            uvChild1 = nAttr.create( "uCoord", "u", OpenMaya.MFnNumericData.kFloat )
            uvChild2 = nAttr.create( "vCoord", "v", OpenMaya.MFnNumericData.kFloat )
            bilerpTexture.UVCoord = nAttr.create( "uvCoord", "uv", uvChild1, uvChild2 )
            bilerpTexture.makeInput( nAttr )
            nAttr.setHidden( True )
            
            uvChild3 = nAttr.create( "uvFilterSizeX", "fsx", OpenMaya.MFnNumericData.kFloat )
            uvChild4 = nAttr.create( "uvFilterSizeY", "fsy", OpenMaya.MFnNumericData.kFloat )
            bilerpTexture.uvFilterSize = nAttr.create( "uvFilterSize", "fs", uvChild3, uvChild4 )
            bilerpTexture.makeInput( nAttr )
            nAttr.setHidden( True )


            bilerpTexture.mapping = enumAttr.create('mapping', 'mp', 0)
            i=0
            for type in bilerpTexture.aMappings:
                enumAttr.addField( type, i )
                i+=1

            bilerpTexture.uscale = bilerpTexture.makeFloat('uscale', 'us', 1.0 )
            bilerpTexture.vscale = bilerpTexture.makeFloat('vscale', 'vs', 1.0 )

            bilerpTexture.udelta = bilerpTexture.makeFloat('udelta', 'ud', 1.0 )
            bilerpTexture.vdelta = bilerpTexture.makeFloat('vdelta', 'vd', 1.0 )
            
            bilerpTexture.v1 = nAttr.createPoint("v1", "v1")
            bilerpTexture.makeInput(nAttr)
            nAttr.setDefault( 1.0, 0.0, 0.0 )
            bilerpTexture.v2 = nAttr.createPoint("v2", "v2")
            bilerpTexture.makeInput(nAttr)
            nAttr.setDefault( 0.0, 1.0, 0.0 ) 
            
            bilerpTexture.v00 = bilerpTexture.makeColor("v00", "v00" )
            bilerpTexture.v01 = bilerpTexture.makeColor("v01", "v01" )
            bilerpTexture.v10 = bilerpTexture.makeColor("v10", "v10" )
            bilerpTexture.v11 = bilerpTexture.makeColor("v11", "v11" )


        except:
            OpenMaya.MGlobal.displayError("Failed to create bilerpTexture attributes\n")
            raise
        
        try:
            bilerpTexture.addAttribute(bilerpTexture.outColor)
            bilerpTexture.addAttribute(bilerpTexture.outAlpha)

            bilerpTexture.addAttribute(bilerpTexture.UVCoord)
            bilerpTexture.addAttribute(bilerpTexture.uvFilterSize)

            bilerpTexture.addAttribute(bilerpTexture.mapping)
            bilerpTexture.addAttribute(bilerpTexture.uscale)
            bilerpTexture.addAttribute(bilerpTexture.vscale)
            bilerpTexture.addAttribute(bilerpTexture.udelta)
            bilerpTexture.addAttribute(bilerpTexture.vdelta)
            bilerpTexture.addAttribute(bilerpTexture.v1)
            bilerpTexture.addAttribute(bilerpTexture.v2)
            
            bilerpTexture.addAttribute(bilerpTexture.v00)
            bilerpTexture.addAttribute(bilerpTexture.v01)
            bilerpTexture.addAttribute(bilerpTexture.v10)
            bilerpTexture.addAttribute(bilerpTexture.v11)

        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise