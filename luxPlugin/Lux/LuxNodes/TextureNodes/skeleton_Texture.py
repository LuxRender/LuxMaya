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
## Lux {NODENAME} Texture node for Maya
##
## ------------------------------------------------------------------------------
#
#import math
#from maya import OpenMaya
#from maya import OpenMayaMPx
#
#from Lux.LuxNodes.TextureNode import TextureNode
#from Lux.LuxNodes.LuxNode import TextureIntegerAttribute
#from Lux.LuxNodes.LuxNode import TextureFloatAttribute
#from Lux.LuxNodes.LuxNode import TextureVectorAttribute
#
## 3D Texture
#class {CLASSNAME}(OpenMayaMPx.MPxNode, TextureNode):
#    
#    outColor        = OpenMaya.MObject()
#    outAlpha        = OpenMaya.MObject()
#    
#    # maya 3d common attributes
##    placementMatrix = OpenMaya.MObject()
##    pointWorld      = OpenMaya.MObject()
##    translate       = OpenMaya.MObject()
##    rotate          = OpenMaya.MObject()
##    scale           = OpenMaya.MObject()
#
#    # maya 2d common attributes
#    UVCoord         = OpenMaya.MObject()
#    uvFilterSize    = OpenMaya.MObject()
#    
#    # lux common 2D options attributes
#    mapping         = OpenMaya.MObject()
#    uscale          = OpenMaya.MObject()
#    vscale          = OpenMaya.MObject()
#    udelta          = OpenMaya.MObject()
#    vdelta          = OpenMaya.MObject()
#    v1              = OpenMaya.MObject()
#    v2              = OpenMaya.MObject()
#    
#    # lux texture specific attributes
#    
#    @staticmethod
#    def nodeName():
#        return "{NODENAME}"
#
#    def luxName(self):
#        return "{LUXNODENAME}"
#
#    @staticmethod
#    def nodeId():
#        return OpenMaya.MTypeId({NODEID}) # 'lux' ??
#
#    @staticmethod
#    def nodeCreator():
#        return OpenMayaMPx.asMPxPtr( {CLASSNAME}() )
#
#    @staticmethod
#    def nodeClassify():
#        return "texture/3d"
#    
#    def __init__(self):
#        OpenMayaMPx.MPxNode.__init__(self)
#
#        # translation table for texture
#        self.attributes = {}
##        self.attributes['octaves']   = TextureIntegerAttribute('octaves',  self.addToOutput, self.prependToOutput)
#    
##        self.attributes['translate'] = TextureVectorAttribute('translate', self.addToOutput, self.prependToOutput)
##        self.attributes['rotate'] = TextureVectorAttribute('rotate', self.addToOutput, self.prependToOutput)
##        self.attributes['scale'] = TextureVectorAttribute('scale', self.addToOutput, self.prependToOutput)
#
#
#    def postConstructor(self):
#        self._setMPSafe( True )
#        self.setExistWithoutOutConnections( True )
#        self.setExistWithoutInConnections( True )

#    
##    def compute(self, plug, block):
##        
##        if plug == self.outColor \
##        or plug == self.outAlpha:
##        #or plug.parent() == self.outColor \
##            worldPos = block.inputValue( self.pointWorld ).asFloatVector()
##            m = block.inputValue( self.placementMatrix ).asFloatMatrix()
##            
##            q = OpenMaya.MFloatPoint(worldPos[0] + m(3,0), worldPos[1] + m(3,1), worldPos[2] + m(3,2))
##            
##            #om = block.inputValue( self.roughness ).asFloat()
##            #oc = block.inputValue( self.octaves ).asInt()
##            
##            #fbm = self.FBm(q.x, q.y, q.z, om, oc)
##            
##            resultColor = OpenMaya.MFloatVector() #fbm, fbm, fbm)
##            
##            outColorHandle = block.outputValue( self.outColor )
##            outColorHandle.setMFloatVector(resultColor)
##            outColorHandle.setClean()
##            
##            outAlphaHandle = block.outputValue( self.outAlpha )
##            outAlphaHandle.setFloat( 0.0 )
##            outAlphaHandle.setClean()
##
##        else:
##            return OpenMaya.kUnknownParameter
#    
#    @staticmethod
#    def nodeInitializer():
#        nAttr = OpenMaya.MFnNumericAttribute()
#        mAttr = OpenMaya.MFnMatrixAttribute()
#        
#        try:
#            {CLASSNAME}.outColor = nAttr.createColor("outColor", "oc")
#            nAttr.setKeyable(0)
#            nAttr.setStorable(0)
#            nAttr.setReadable(1)
#            nAttr.setWritable(0)
#            
#            {CLASSNAME}.outAlpha = nAttr.create("outAlpha", "oa", OpenMaya.MFnNumericData.kFloat)
#            nAttr.setKeyable(0)
#            nAttr.setStorable(0)
#            nAttr.setReadable(1)
#            nAttr.setWritable(0)
#            
#            # 2D Params
##            uvChild1 = nAttr.create( "uCoord", "u", OpenMaya.MFnNumericData.kFloat )
##            uvChild2 = nAttr.create( "vCoord", "v", OpenMaya.MFnNumericData.kFloat )
##            bilerpTexture.UVCoord = nAttr.create( "uvCoord", "uv", uvChild1, uvChild2 )
##            bilerpTexture.makeInput( nAttr )
##            nAttr.setHidden( True )
##            
##            uvChild3 = nAttr.create( "uvFilterSizeX", "fsx", OpenMaya.MFnNumericData.kFloat )
##            uvChild4 = nAttr.create( "uvFilterSizeY", "fsy", OpenMaya.MFnNumericData.kFloat )
##            bilerpTexture.uvFilterSize = nAttr.create( "uvFilterSize", "fs", uvChild3, uvChild4 )
##            bilerpTexture.makeInput( nAttr )
##            nAttr.setHidden( True )
#            
#            # 3D Params
#            {CLASSNAME}.placementMatrix = mAttr.create("placementMatrix", "pm")
#            {CLASSNAME}.makeInput(mAttr)
#            
#            {CLASSNAME}.pointWorld = nAttr.createPoint("pointWorld", "pw")
#            {CLASSNAME}.makeInput(nAttr)
#            nAttr.setHidden(True)
#            

#            {CLASSNAME}.translate = nAttr.createPoint("translate", "t")
#            {CLASSNAME}.makeInput(nAttr)
#            #nAttr.setHidden(True)
#            
#            {CLASSNAME}.rotate = nAttr.createPoint("rotate", "r")
#            {CLASSNAME}.makeInput(nAttr)
#            #nAttr.setHidden(True)
#            
#            {CLASSNAME}.scale = nAttr.createPoint("scale", "s")
#            {CLASSNAME}.makeInput(nAttr)
#            nAttr.setDefault( 1.0, 1.0, 1.0 )
#            #nAttr.setHidden(True)

##            {CLASSNAME}.octaves = {CLASSNAME}.makeInteger("octaves", "fbmo", 8)
#
#
#        except:
#            OpenMaya.MGlobal.displayError("Failed to create {CLASSNAME} attributes\n")
#            raise
#        
#        try:
#            {CLASSNAME}.addAttribute({CLASSNAME}.outColor)
#            {CLASSNAME}.addAttribute({CLASSNAME}.outAlpha)
#            {CLASSNAME}.addAttribute({CLASSNAME}.placementMatrix)
#            {CLASSNAME}.addAttribute({CLASSNAME}.pointWorld)
#
#            {CLASSNAME}.addAttribute({CLASSNAME}.translate)
#            {CLASSNAME}.addAttribute({CLASSNAME}.rotate)
#            {CLASSNAME}.addAttribute({CLASSNAME}.scale)
#            
##            {CLASSNAME}.addAttribute({CLASSNAME}.octaves)
#
#            
##            {CLASSNAME}.attributeAffects({CLASSNAME}.octaves, {CLASSNAME}.outColor)
#
#            {CLASSNAME}.attributeAffects({CLASSNAME}.pointWorld, {CLASSNAME}.outColor)
#            {CLASSNAME}.attributeAffects({CLASSNAME}.placementMatrix, {CLASSNAME}.outColor)
#            
##            {CLASSNAME}.attributeAffects({CLASSNAME}.octaves, {CLASSNAME}.outAlpha)
#
#            {CLASSNAME}.attributeAffects({CLASSNAME}.pointWorld, {CLASSNAME}.outAlpha)
#            {CLASSNAME}.attributeAffects({CLASSNAME}.placementMatrix, {CLASSNAME}.outAlpha)
#            
#        except:
#            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
#            raise
#    
