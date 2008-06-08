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
# Lux material shader node for Maya ( carpaint attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderEnumAttribute
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute

class carpaintShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    CarPaint fragment of luxshader
    """
    
    # carpaint
    name    =    OpenMaya.MObject()    # enum
    kd      =    OpenMaya.MObject()    # color
    ks1     =    OpenMaya.MObject()    # color
    ks2     =    OpenMaya.MObject()    # color
    ks3     =    OpenMaya.MObject()    # color
    r1      =    OpenMaya.MObject()    # float
    r2      =    OpenMaya.MObject()    # float
    r3      =    OpenMaya.MObject()    # float
    m1      =    OpenMaya.MObject()    # float
    m2      =    OpenMaya.MObject()    # float
    m3      =    OpenMaya.MObject()    # float
    
    nameValues = {
                   0: "manual",
                   1: "ford f8",
                   2: "polaris silber",
                   3: "opel titan",
                   4: "bmw339",
                   5: "2k acrylack",
                   6: "white",
                   7: "blue",
                   8: "bluematte"
                  }

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)

        # Export attributes
        self.attributes = {}
        self.luxType = "carpaint"
        self.attributes['name'] = ShaderEnumAttribute('carpaintName', self.nameValues)
        self.attributes['Kd']   = ShaderColorAttribute('carpaintKd')
        self.attributes['Ks1']  = ShaderColorAttribute('carpaintKs1')
        self.attributes['Ks2']  = ShaderColorAttribute('carpaintKs2')
        self.attributes['Ks3']  = ShaderColorAttribute('carpaintKs3')
        self.attributes['R1']   = ShaderFloatAttribute('carpaintR1')
        self.attributes['R2']   = ShaderFloatAttribute('carpaintR2')
        self.attributes['R3']   = ShaderFloatAttribute('carpaintR3')
        self.attributes['M1']   = ShaderFloatAttribute('carpaintM1')
        self.attributes['M2']   = ShaderFloatAttribute('carpaintM2')
        self.attributes['M3']   = ShaderFloatAttribute('carpaintM3') 

    @staticmethod
    def shaderInitializer():
        enumAttr    = OpenMaya.MFnEnumAttribute()

        try:
            # preset name (or manual)
            carpaintShader.name = enumAttr.create("carpaintName", "cpn", 0)
            for ind in carpaintShader.nameValues:
                enumAttr.addField( carpaintShader.nameValues[ind], ind )

            # diffuse component
            carpaintShader.kd = carpaintShader.makeColor("carpaintKd", "cpkd")

            # specular layers
            carpaintShader.ks1 = carpaintShader.makeColor("carpaintKs1", "cpks1")
            carpaintShader.ks2 = carpaintShader.makeColor("carpaintKs2", "cpks2")
            carpaintShader.ks3 = carpaintShader.makeColor("carpaintKs3", "cpks3")

            # fresnel const layers
            carpaintShader.r1 = carpaintShader.makeFloat("carpaintR1", "cpr1")
            carpaintShader.r2 = carpaintShader.makeFloat("carpaintR2", "cpr2")
            carpaintShader.r3 = carpaintShader.makeFloat("carpaintR3", "cpr3")

            # microfacet roughness layers
            carpaintShader.m1 = carpaintShader.makeFloat("carpaintM1", "cpm1")
            carpaintShader.m2 = carpaintShader.makeFloat("carpaintM2", "cpm2")
            carpaintShader.m3 = carpaintShader.makeFloat("carpaintM3", "cpm3")

        except:
            OpenMaya.MGlobal.displayError("Failed to create carpaint attributes\n")
            raise