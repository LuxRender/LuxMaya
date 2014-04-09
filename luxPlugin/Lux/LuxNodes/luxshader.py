# ------------------------------------------------------------------------------
# Lux material shader node for Maya
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
# luxshader: a shader node for Maya which defines all available lux materal types
# and their available parameters
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from ShaderNode                            import ShaderNode

from ShaderNodes.carpaintShader            import carpaintShader
from ShaderNodes.glassShader               import glassShader
from ShaderNodes.matteShader               import matteShader
from ShaderNodes.mattetranslucentShader    import mattetranslucentShader
from ShaderNodes.metalShader               import metalShader
from ShaderNodes.mixShader                 import mixShader
from ShaderNodes.mirrorShader              import mirrorShader
from ShaderNodes.roughglassShader          import roughglassShader
from ShaderNodes.shinymetalShader          import shinymetalShader
from ShaderNodes.glossyShader              import glossyShader

from ShaderNodes.arealightShader           import arealightShader

class luxshader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    Custom lux material shader for Maya.
    This is a single node that contains all material types, although
    the attributes for each type are split into different modules.
    (Also inluded here is AreaLight even though it's not a material)
    
    Each of these modules has two purposes:
    1. Provide attributes for Maya to use
    2. Provide a mapping of Maya attributes -> Lux parameters to be read
       at export time. 
    """
    
    colorTable = {}

    @staticmethod
    def nodeName():
        return "luxshader"

    @staticmethod
    def nodeId():
        return OpenMaya.MTypeId(0x6C757801) # 'lux' 01

    @staticmethod
    def nodeCreator():
        return OpenMayaMPx.asMPxPtr( luxshader() )

    @staticmethod
    def nodeClassify():
        return "shader/surface"

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # 4 generic attributes to set up the shader's internal operation
        iMaterialType       =  OpenMaya.MObject()    # enum
        bumpMap             =  OpenMaya.MObject()    # point
        outColor            =  OpenMaya.MObject()    # color
        transparency        =  OpenMaya.MObject()    # transparency
        
        # instances of shader types
        carpaint            = carpaintShader()
        glass               = glassShader()
        roughglass          = roughglassShader()
        matte               = matteShader()
        mattetranslucent    = mattetranslucentShader()
        metal               = metalShader()
        mix                 = mixShader()
        shinymetal          = shinymetalShader()
        mirror              = mirrorShader
        glossy              = glossyShader()
        
        arealight           = arealightShader()        # not technically a shader
        

    def postConstructor(self):
        self._setMPSafe( True )
        self.setExistWithoutOutConnections( True )
        self.setExistWithoutInConnections( True )
        
        self.colorTable = {
                      0: self.carpaint.kd,
                      1: self.glass.kt,
                      2: self.roughglass.kt,
                      3: self.matte.kd,
                      4: self.mattetranslucent.kt,
                      #5: self.metal.n,
                      6: self.shinymetal.ks,
                      7: self.mirror.kr,
                      9: self.glossy.kd,
                      10: self.arealight.L
                      }

    def compute(self, plug, block):
        if plug == self.outColor or plug.parent() == self.outColor:
            # THIS IS A VERY SIMPLE FLAT COLOUR SHADER.
            # I CAN'T GET THE LAMBERTIAN BIT TO WORK
            
            matType = block.inputValue( self.iMaterialType ).asInt()
            
            # choose the appropriate color
            if matType in self.colorTable:
                resultColor = block.inputValue( self.colorTable[matType] ).asFloatVector()
            else:
                resultColor = OpenMaya.MFloatVector(0.0, 0.0, 0.0)
            

            # set the output as a flat color
            outColorHandle = block.outputValue( self.outColor )
            outColorHandle.setMFloatVector(resultColor)
            outColorHandle.setClean()
            return True #povman: OpenMaya.MStatus.kSuccess
        else:
            return OpenMaya.kUnknownParameter

    @staticmethod
    def nodeInitializer():
        nAttr        = OpenMaya.MFnNumericAttribute()
        enumAttr    = OpenMaya.MFnEnumAttribute()

        # reference instances of shader types
        luxshader.carpaint          = carpaintShader()
        luxshader.glass             = glassShader()
        luxshader.roughglass        = roughglassShader()
        luxshader.matte             = matteShader()
        luxshader.mattetranslucent  = mattetranslucentShader()
        luxshader.metal             = metalShader()
        luxshader.mix               = mixShader()
        luxshader.shinymetal        = shinymetalShader()
        luxshader.mirror            = mirrorShader()
        luxshader.glossy            = glossyShader()

        luxshader.arealight         = arealightShader()

        try:
            # set up the base attributes

            # the different material types available herewithin
            luxshader.iMaterialType = enumAttr.create("material", "mat",    3)
            enumAttr.addField( "Carpaint",                                  0)
            enumAttr.addField( "Glass",                                     1)
            enumAttr.addField( "Rough Glass",                               2)
            enumAttr.addField( "Matte",                                     3)
            enumAttr.addField( "Matte Translucent",                         4)
            enumAttr.addField( "Metal",                                     5)
            # hmm out of sequence Enum values have no effect
            enumAttr.addField( "Mix",                                      11)
            enumAttr.addField( "Null",                                     12)
            enumAttr.addField( "Shiny Metal",                               6)
            enumAttr.addField( "Mirror",                                    7)
            enumAttr.addField( "Glossy",                                    9)
            enumAttr.addField( "Area Light",                               10)

            # hidden attribute to allow attaching bump maps, relevant to every material type
            luxshader.bumpMap = nAttr.createPoint("normalCamera","n")
            luxshader.makeInput( nAttr )
            nAttr.setHidden(1)
            nAttr.setDefault(0.0, 0.0, 0.0)

            # a special color attribute for shading purposes
            luxshader.outColor = nAttr.createColor("outColor", "oc")
            nAttr.setKeyable(0)
            nAttr.setStorable(0)
            nAttr.setReadable(1)
            nAttr.setWritable(0)
            
            # this is set by luxshader itself, not the user, according to the material type.
            # the actual setting of this parameter is done in the AETemplate.
            # (I'm using this to make AreaLight objects 50% transparent in the viewport)
            luxshader.transparency = nAttr.createColor("transparency", "t")
            luxshader.makeInput( nAttr )
            nAttr.setHidden(1)
            nAttr.setDefault(0.5, 0.5, 0.5)
            
            # init all the shader attributes
            luxshader.carpaint.shaderInitializer()
            luxshader.glass.shaderInitializer()
            luxshader.roughglass.shaderInitializer()
            luxshader.matte.shaderInitializer()
            luxshader.mattetranslucent.shaderInitializer()
            luxshader.metal.shaderInitializer()
            luxshader.mix.shaderInitializer()
            luxshader.shinymetal.shaderInitializer()
            luxshader.mirror.shaderInitializer()
            luxshader.glossy.shaderInitializer()

            luxshader.arealight.shaderInitializer()

        except:
            OpenMaya.MGlobal.displayError("Failed to create attributes\n")
            raise

        try:
            # base attributes
            luxshader.addAttribute(luxshader.iMaterialType)
            luxshader.addAttribute(luxshader.bumpMap)
            luxshader.addAttribute(luxshader.outColor)
            luxshader.addAttribute(luxshader.transparency)

            ####
            # can we defer all the below into the child/sibling classes ?

            # carpaint
            luxshader.addAttribute(luxshader.carpaint.name)
            luxshader.addAttribute(luxshader.carpaint.kd)
            luxshader.addAttribute(luxshader.carpaint.ks1)
            luxshader.addAttribute(luxshader.carpaint.ks2)
            luxshader.addAttribute(luxshader.carpaint.ks3)
            luxshader.addAttribute(luxshader.carpaint.r1)
            luxshader.addAttribute(luxshader.carpaint.r2)
            luxshader.addAttribute(luxshader.carpaint.r3)
            luxshader.addAttribute(luxshader.carpaint.m1)
            luxshader.addAttribute(luxshader.carpaint.m2)
            luxshader.addAttribute(luxshader.carpaint.m3)

            # glass
            luxshader.addAttribute(luxshader.glass.kr)
            luxshader.addAttribute(luxshader.glass.kt)
            luxshader.addAttribute(luxshader.glass.index)
            luxshader.addAttribute(luxshader.glass.cauchyb)
            luxshader.addAttribute(luxshader.glass.architectural)

            # roughglass
            luxshader.addAttribute(luxshader.roughglass.kr)
            luxshader.addAttribute(luxshader.roughglass.kt)
            luxshader.addAttribute(luxshader.roughglass.uroughness)
            luxshader.addAttribute(luxshader.roughglass.vroughness)
            luxshader.addAttribute(luxshader.roughglass.index)
            luxshader.addAttribute(luxshader.roughglass.cauchyb)

            # matte
            luxshader.addAttribute(luxshader.matte.kd)
            luxshader.addAttribute(luxshader.matte.sigma)

            # mattetranslucent
            luxshader.addAttribute(luxshader.mattetranslucent.kr)
            luxshader.addAttribute(luxshader.mattetranslucent.kt)
            luxshader.addAttribute(luxshader.mattetranslucent.sigma)

            # metal
            luxshader.addAttribute(luxshader.metal.name)
            #luxshader.addAttribute(luxshader.metal.n)
            #luxshader.addAttribute(luxshader.metal.k)
            luxshader.addAttribute(luxshader.metal.uroughness)
            luxshader.addAttribute(luxshader.metal.vroughness)
            luxshader.addAttribute(luxshader.metal.nkFile)

            # shinymetal
            luxshader.addAttribute(luxshader.shinymetal.kr)
            luxshader.addAttribute(luxshader.shinymetal.ks)
            luxshader.addAttribute(luxshader.shinymetal.uroughness)
            luxshader.addAttribute(luxshader.shinymetal.vroughness)

            # mirror
            luxshader.addAttribute(luxshader.mirror.kr)
            
            # mix
            luxshader.addAttribute(luxshader.mix.namedMaterial1)
            luxshader.addAttribute(luxshader.mix.namedMaterial2)
            luxshader.addAttribute(luxshader.mix.amount)

            # glossy
            luxshader.addAttribute(luxshader.glossy.kd)
            luxshader.addAttribute(luxshader.glossy.ks)
            luxshader.addAttribute(luxshader.glossy.uroughness)
            luxshader.addAttribute(luxshader.glossy.vroughness)

            # arealight
            luxshader.addAttribute(luxshader.arealight.L)
            luxshader.addAttribute(luxshader.arealight.gain)
            luxshader.addAttribute(luxshader.arealight.numsamples)
            luxshader.addAttribute(luxshader.arealight.lightGroup)
            

        except:
            OpenMaya.MGlobal.displayError("Failed to add attributes\n")
            raise

        try:
            luxshader.attributeAffects(luxshader.bumpMap,                   luxshader.outColor)
            # and these are the attributes that we use in compute
            luxshader.attributeAffects(luxshader.carpaint.kd,               luxshader.outColor)
            luxshader.attributeAffects(luxshader.glass.kt,                  luxshader.outColor)
            luxshader.attributeAffects(luxshader.roughglass.kt,             luxshader.outColor)
            luxshader.attributeAffects(luxshader.matte.kd,                  luxshader.outColor)
            luxshader.attributeAffects(luxshader.mattetranslucent.kt,       luxshader.outColor)
            #luxshader.attributeAffects(luxshader.metal.n,                   luxshader.outColor)
            luxshader.attributeAffects(luxshader.shinymetal.kr,             luxshader.outColor)
            luxshader.attributeAffects(luxshader.mirror.kr,                 luxshader.outColor)
            luxshader.attributeAffects(luxshader.glossy.kd,                 luxshader.outColor)
            # arealight doesn't affect, values are hardcoded

        except:
            OpenMaya.MGlobal.displayError("Failed in setting attributeAffects\n")
            raise
