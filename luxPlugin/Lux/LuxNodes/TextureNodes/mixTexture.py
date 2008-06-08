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

# 3D Texture
class mixTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux Mix Texture node for Maya
    """
    
    outColor        = OpenMaya.MObject()
    outAlpha        = OpenMaya.MObject()
    
    # maya 3d common attributes
    placementMatrix = OpenMaya.MObject()
    pointWorld      = OpenMaya.MObject()

    # maya 2d common attributes
#    UVCoord         = OpenMaya.MObject()
#    uvFilterSize    = OpenMaya.MObject()
    
    # lux common 2D options attributes
#    mapping         = OpenMaya.MObject()
#    uscale          = OpenMaya.MObject()
#    vscale          = OpenMaya.MObject()
#    udelta          = OpenMaya.MObject()
#    vdelta          = OpenMaya.MObject()
#    v1              = OpenMaya.MObject()
#    v2              = OpenMaya.MObject()
    
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
        return "texture/3d"
    
    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # translation table for texture
        self.attributes = {}
        self.attributes['tex1']   = TextureColorAttribute('tex1',  self.addToOutput, self.prependToOutput)
        self.attributes['tex2']   = TextureColorAttribute('tex2',  self.addToOutput, self.prependToOutput)
        self.attributes['amount']   = TextureFloatAttribute('amount',  self.addToOutput, self.prependToOutput)
    
    def postConstructor(self):
        self._setMPSafe(True)
    
#    def compute(self, plug, block):
#        
#        if plug == self.outColor \
#        or plug == self.outAlpha:
#        #or plug.parent() == self.outColor \
#            worldPos = block.inputValue( self.pointWorld ).asFloatVector()
#            m = block.inputValue( self.placementMatrix ).asFloatMatrix()
#            
#            q = OpenMaya.MFloatPoint(worldPos[0] + m(3,0), worldPos[1] + m(3,1), worldPos[2] + m(3,2))
#            
#            #om = block.inputValue( self.roughness ).asFloat()
#            #oc = block.inputValue( self.octaves ).asInt()
#            
#            #fbm = self.FBm(q.x, q.y, q.z, om, oc)
#            
#            resultColor = OpenMaya.MFloatVector() #fbm, fbm, fbm)
#            
#            outColorHandle = block.outputValue( self.outColor )
#            outColorHandle.setMFloatVector(resultColor)
#            outColorHandle.setClean()
#            
#            outAlphaHandle = block.outputValue( self.outAlpha )
#            outAlphaHandle.setFloat( 0.0 )
#            outAlphaHandle.setClean()
#
#        else:
#            return OpenMaya.kUnknownParameter
    
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
            
            # 2D Params
#            uvChild1 = nAttr.create( "uCoord", "u", OpenMaya.MFnNumericData.kFloat )
#            uvChild2 = nAttr.create( "vCoord", "v", OpenMaya.MFnNumericData.kFloat )
#            bilerpTexture.UVCoord = nAttr.create( "uvCoord", "uv", uvChild1, uvChild2 )
#            bilerpTexture.makeInput( nAttr )
#            nAttr.setHidden( True )
#            
#            uvChild3 = nAttr.create( "uvFilterSizeX", "fsx", OpenMaya.MFnNumericData.kFloat )
#            uvChild4 = nAttr.create( "uvFilterSizeY", "fsy", OpenMaya.MFnNumericData.kFloat )
#            bilerpTexture.uvFilterSize = nAttr.create( "uvFilterSize", "fs", uvChild3, uvChild4 )
#            bilerpTexture.makeInput( nAttr )
#            nAttr.setHidden( True )
            
            # 3D Params
            mixTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            mixTexture.makeInput(mAttr)
            
            mixTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            mixTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            mixTexture.tex1 = mixTexture.makeColor("tex1", "t1")
            mixTexture.tex2 = mixTexture.makeColor("tex2", "t2")
            mixTexture.amount = mixTexture.makeFloat("amount", "am")


        except:
            OpenMaya.MGlobal.displayError("Failed to create mixTexture attributes\n")
            raise
        
        try:
            mixTexture.addAttribute(mixTexture.outColor)
            mixTexture.addAttribute(mixTexture.outAlpha)
            mixTexture.addAttribute(mixTexture.placementMatrix)
            mixTexture.addAttribute(mixTexture.pointWorld)
            
            mixTexture.addAttribute(mixTexture.tex1)
            mixTexture.addAttribute(mixTexture.tex2)
            mixTexture.addAttribute(mixTexture.amount)

            
#            mixTexture.attributeAffects(mixTexture.tex1, mixTexture.outColor)
#            mixTexture.attributeAffects(mixTexture.tex2, mixTexture.outColor)
#            mixTexture.attributeAffects(mixTexture.amount, mixTexture.outColor)
#
#            mixTexture.attributeAffects(mixTexture.pointWorld, mixTexture.outColor)
#            mixTexture.attributeAffects(mixTexture.placementMatrix, mixTexture.outColor)
#            
#            mixTexture.attributeAffects(mixTexture.tex1, mixTexture.outAlpha)
#            mixTexture.attributeAffects(mixTexture.tex2, mixTexture.outAlpha)
#            mixTexture.attributeAffects(mixTexture.amount, mixTexture.outAlpha)
#
#            mixTexture.attributeAffects(mixTexture.pointWorld, mixTexture.outAlpha)
#            mixTexture.attributeAffects(mixTexture.placementMatrix, mixTexture.outAlpha)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
