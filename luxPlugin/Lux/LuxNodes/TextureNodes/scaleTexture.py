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

# 3D Texture
class scaleTexture(OpenMayaMPx.MPxNode, TextureNode):
    """
    Lux scale Texture node for Maya
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
        return "texture/3d"
    
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
            scaleTexture.placementMatrix = mAttr.create("placementMatrix", "pm")
            scaleTexture.makeInput(mAttr)
            
            scaleTexture.pointWorld = nAttr.createPoint("pointWorld", "pw")
            scaleTexture.makeInput(nAttr)
            nAttr.setHidden(True)
            
            scaleTexture.tex1 = scaleTexture.makeColor("tex1", "t1")
            scaleTexture.tex2 = scaleTexture.makeColor("tex2", "t2")


        except:
            OpenMaya.MGlobal.displayError("Failed to create scaleTexture attributes\n")
            raise
        
        try:
            scaleTexture.addAttribute(scaleTexture.outColor)
            scaleTexture.addAttribute(scaleTexture.outAlpha)
            scaleTexture.addAttribute(scaleTexture.placementMatrix)
            scaleTexture.addAttribute(scaleTexture.pointWorld)
            
            scaleTexture.addAttribute(scaleTexture.tex1)
            scaleTexture.addAttribute(scaleTexture.tex2)

            
#            scaleTexture.attributeAffects(scaleTexture.tex1, scaleTexture.outColor)
#            scaleTexture.attributeAffects(scaleTexture.tex2, scaleTexture.outColor)
#            scaleTexture.attributeAffects(scaleTexture.amount, scaleTexture.outColor)
#
#            scaleTexture.attributeAffects(scaleTexture.pointWorld, scaleTexture.outColor)
#            scaleTexture.attributeAffects(scaleTexture.placementMatrix, scaleTexture.outColor)
#            
#            scaleTexture.attributeAffects(scaleTexture.tex1, scaleTexture.outAlpha)
#            scaleTexture.attributeAffects(scaleTexture.tex2, scaleTexture.outAlpha)
#            scaleTexture.attributeAffects(scaleTexture.amount, scaleTexture.outAlpha)
#
#            scaleTexture.attributeAffects(scaleTexture.pointWorld, scaleTexture.outAlpha)
#            scaleTexture.attributeAffects(scaleTexture.placementMatrix, scaleTexture.outAlpha)
            
        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise
    
