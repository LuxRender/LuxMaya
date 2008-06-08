# ------------------------------------------------------------------------------
# Lux exporter python script plugin for Maya
#
# by Doug Hammond 02/2008
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# material export class.
#
# ------------------------------------------------------------------------------

from maya import OpenMaya

from ExportModule import ExportModule

# Import all native material types...
from Lux.LuxNodes.ShaderNode                          import ShaderNode
from Lux.LuxNodes.ShaderNodes.carpaintShader          import carpaintShader
from Lux.LuxNodes.ShaderNodes.glassShader             import glassShader
from Lux.LuxNodes.ShaderNodes.matteShader             import matteShader
from Lux.LuxNodes.ShaderNodes.mattetranslucentShader  import mattetranslucentShader
from Lux.LuxNodes.ShaderNodes.metalShader             import metalShader
from Lux.LuxNodes.ShaderNodes.mirrorShader            import mirrorShader
from Lux.LuxNodes.ShaderNodes.mixShader               import mixShader
from Lux.LuxNodes.ShaderNodes.nullShader              import nullShader
from Lux.LuxNodes.ShaderNodes.plasticShader           import plasticShader
from Lux.LuxNodes.ShaderNodes.roughglassShader        import roughglassShader
from Lux.LuxNodes.ShaderNodes.shinymetalShader        import shinymetalShader
from Lux.LuxNodes.ShaderNodes.substrateShader         import substrateShader

# ...and the types that we can translate
from Lux.MayaShaderModules.lambertShader                import lambertShader
from Lux.MayaShaderModules.phongShader                  import phongShader

class MaterialBase:
    """
    Material type base class.
    """
    
    def __init__(self, shaderNode):
        """
        Set up the node that we're dealing with.
        """
        
        self.dpNode = shaderNode
        self.shaderName = self.dpNode.name()

# TODO global list of exported materials for duplicate detection doesn't work.
ExportedMaterials = []

class Material(ExportModule):
    """
    Material ExportModule. This acts as a factory to return a derived ExportModule
    for the given shader type.
    """
    
    @staticmethod
    def MaterialFactory( dpNode ):
        """
        The material factory.
        """
        
        nodeType = dpNode.typeName()
        
        nodeName = dpNode.name #OpenMaya.MFnDependencyNode( dpNode ).name()
        
        # TODO this doesn't work
        materialNotExported = not ExportedMaterials.__contains__(nodeName)
        
        if (dpNode.classification( nodeType ) == "shader/surface") and materialNotExported:
            ExportedMaterials.append( nodeName )
            
            if nodeType == "luxshader":
                # export lux material directly
                return MaterialLux( dpNode )
            elif nodeType == "lambert":
                # translate lambert -> matte
                return MaterialLambert( dpNode )
            elif nodeType == "phong":
                # translate phong -> plastic
                return MaterialPhong( dpNode )
            else:
                OpenMaya.MGlobal.displayWarning("Shader type %s not supported" % nodeType )
                return False
        else:
            return False
    #end def MaterialFactory
    
class MaterialLux(ExportModule, MaterialBase):
    """
    The native Lux material type. Responsible for detecting the lux material
    type and returning the syntax from that module's object.
    """
    
    def __init__(self, shaderNode):
        MaterialBase.__init__(self, shaderNode)
        
    def getOutput(self):
        """
        Essentially another factory method for all the lux material types.
        """
        
        # switch by lux material type
        materialTypePlug = self.dpNode.findPlug( "material" )
        materialType = materialTypePlug.asInt()
        
        validMaterial = True
        
        if materialType == 0:
            self.shaderSyntaxModule = carpaintShader()
        elif materialType == 1:
            self.shaderSyntaxModule = glassShader()
        elif materialType == 2:
            self.shaderSyntaxModule = roughglassShader()
        elif materialType == 3:
            self.shaderSyntaxModule = matteShader()
        elif materialType == 4:
            self.shaderSyntaxModule = mattetranslucentShader()
        elif materialType == 5:
            self.shaderSyntaxModule = metalShader()
        elif materialType == 6:
            self.shaderSyntaxModule = shinymetalShader()
        elif materialType == 7:
            self.shaderSyntaxModule = mirrorShader()
        elif materialType == 8:
            self.shaderSyntaxModule = plasticShader()
        elif materialType == 9:
            self.shaderSyntaxModule = substrateShader()
        # 10 is AreaLight, not a material
        elif materialType == 11:
            self.shaderSyntaxModule = mixShaderHandler( self.dpNode )
        elif materialType == 12:
            self.shaderSyntaxModule = nullShader()
        else:
            validMaterial = False
        
        if validMaterial:
            self.addToOutput( '# Lux Shader Material ' + self.dpNode.name() )
            self.addToOutput( self.shaderSyntaxModule.getMaterial( self.dpNode, self.shaderName ) )
    
# Lets do this one manually, because it's an exception
class mixShaderHandler(ExportModule, MaterialBase):
    
    #def __init___(self):
        
        
    def getMaterial(self, dpNode, shaderName):
        self.shaderSyntaxModule = mixShader()
        
        # TODO Fix Maya crash if either mixNamed1 or mixNamed2 are not connected 
        
        # OK, lets find the input connexions
        nm1Plug = dpNode.findPlug( 'mixNamed1' )
        inputPlugs1 = OpenMaya.MPlugArray()
        nm1Plug.connectedTo(inputPlugs1, True, True)
        
        nm2Plug = dpNode.findPlug( 'mixNamed2' )
        inputPlugs2 = OpenMaya.MPlugArray()
        nm2Plug.connectedTo(inputPlugs2, True, True)
        
        # if both are connected
        if inputPlugs1.length() > 0 and inputPlugs2.length() > 0:
            nmnode1 = inputPlugs1[0].node()
            nmnode2 = inputPlugs2[0].node()
            nm1 = OpenMaya.MFnDependencyNode( nmnode1 ).name()
            nm2 = OpenMaya.MFnDependencyNode( nmnode2 ).name()
            
            # This sets the material name, type and amount value/texture
            self.addToOutput( self.shaderSyntaxModule.getMaterial( dpNode, shaderName ) )
            
            # now just grab the names of the connected shaders
            self.addToOutput( '\t"string namedmaterial1" ["%s"]' % nm1 )
            self.addToOutput( '\t"string namedmaterial2" ["%s"]' % nm2 )
            
            # and output the dependent nodes before
            em1 = Material.MaterialFactory( OpenMaya.MFnDependencyNode( nmnode1 ) )
            self.prependToOutput( em1.loadModule() )
            
            em2 = Material.MaterialFactory( OpenMaya.MFnDependencyNode( nmnode2 ) )
            self.prependToOutput( em2.loadModule() )
            
        return self.outString


class MaterialLambert(ExportModule, MaterialBase):
    """
    A translatable Maya shader: Lambert
    """
    
    def __init__(self, shaderNode):
        MaterialBase.__init__(self, shaderNode)
        self.shaderSyntaxModule = lambertShader()
        
    def getOutput(self):
        """
        Get the syntax from the lambertShader module
        """
        
        self.addToOutput( '# Translated Lambert Material ' + self.shaderName )
        self.addToOutput( self.shaderSyntaxModule.getMaterial( self.dpNode, self.shaderName ) )

class MaterialPhong(ExportModule, MaterialBase):
    """
    A translatable Maya shader: Phong
    """
    
    def __init__(self, shaderNode):
        MaterialBase.__init__(self, shaderNode)
        self.shaderSyntaxModule = phongShader()
        
    def getOutput(self):
        """
        Get the syntax from the phongShader module.
        """
        
        self.addToOutput( '# Translated Phong Material ' + self.dpNode.name() )
        self.addToOutput( self.shaderSyntaxModule.getMaterial( self.dpNode, self.shaderName ) )