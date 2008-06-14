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
# Lux material shader node for Maya ( metal attributes )
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.ShaderNode import ShaderNode
from Lux.LuxNodes.LuxNode import ShaderEnumAttribute
from Lux.LuxNodes.LuxNode import ShaderColorAttribute
from Lux.LuxNodes.LuxNode import ShaderFloatAttribute
from Lux.LuxNodes.LuxNode import ShaderStringAttribute

class metalShader(OpenMayaMPx.MPxNode, ShaderNode):
    """
    Metal fragment of luxshader
    """
    
    # metal
    name        =    OpenMaya.MObject()    # enum
    n           =    OpenMaya.MObject()    # color
    k           =    OpenMaya.MObject()    # color
    uroughness  =    OpenMaya.MObject()    # float
    vroughness  =    OpenMaya.MObject()    # float
    
    nameValues  = {
                    0: "manual",
                    1: "nickel",
                    2: "potassium",
                    3: "platinum",
                    4: "iridium",
                    5: "silicon",
                    6: "amorphous silicon",
                    7: "sodium",
                    8: "rhodium",
                    9: "tungsten",
                    10: "vanadium",
                    11: "aluminium",
                    12: "amorphous carbon",
                    13: "silver",
                    14: "gold",
                    15: "cobalt",
                    16: "copper",
                    17: "chromium",
                    18: "lithium",
                    19: "mercury"
                   }
    
    nkFile      = OpenMaya.MObject()

    def __init__(self):
        OpenMayaMPx.MPxNode.__init__(self)
        
        # Export attributes
        self.attributes = {}
        self.luxType = "metal"
        self.attributes['name']         = ShaderEnumAttribute('metalName', self.nameValues)
        self.attributes['n']            = ShaderColorAttribute('metalN')
        self.attributes['k']            = ShaderColorAttribute('metalK')
        self.attributes['uroughness']   = ShaderFloatAttribute('metalURoughness', reciprocal = True)
        self.attributes['vroughness']   = ShaderFloatAttribute('metalVRoughness', reciprocal = True)


    # override
    def getMaterial(self, shaderNode, shaderName):
        # Make the material as normal, with all regular attributes.
        ShaderNode.getMaterial( self, shaderNode, shaderName )
        
        # Then add the nk data if it exists, overriding name parameter
        nkAttr = ShaderStringAttribute('metalNkFile')
        nkParameter = nkAttr.getOutput( 'name', shaderNode, shaderName )
        if nkAttr.rawValue.strip() != '':
            self.addToOutput( nkParameter )
        
        self.addToOutput( '' )
        return self.outputString

    @staticmethod
    def shaderInitializer():
        enumAttr    = OpenMaya.MFnEnumAttribute()
        tAttr       = OpenMaya.MFnTypedAttribute()

        try:
            metalShader.name = enumAttr.create("metalName", "mname", 0)
            for ind in metalShader.nameValues:
                enumAttr.addField( metalShader.nameValues[ind], ind )

            # n and k components of complex IOR for manual type
            metalShader.n = metalShader.makeColor("metalN", "mn")
            metalShader.k = metalShader.makeColor("metalK", "mk")

            # surface roughness
            metalShader.uroughness = metalShader.makeFloat("metalURoughness", "mur", 500.0)
            metalShader.vroughness = metalShader.makeFloat("metalVRoughness", "mvr", 500.0)
            
            # external NK file
            metalShader.nkFile = tAttr.create("metalNkFile", "nk", OpenMaya.MFnData.kString)
            tAttr.setKeyable(1)
            tAttr.setStorable(1)
            tAttr.setReadable(1)
            tAttr.setWritable(1)

        except:
            OpenMaya.MGlobal.displayError("Failed to create metal attributes\n")
            raise