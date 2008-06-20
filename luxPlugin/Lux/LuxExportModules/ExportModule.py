# ------------------------------------------------------------------------------
# Lux exporter python script plugin for Maya
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
# Export module base class
#
# ------------------------------------------------------------------------------

import os, math
os.altsep = '/'
from maya import OpenMaya
from maya import cmds

class ExportModule:
    """
    The ExportModule base class. This base class holds various vars passed by
    DAG Path, Dependancy Node, and other MObject iterators so that the export
    of various scene elements can be handled in a uniform way.
    The methods of this base class provide I/O (OK, /O) functions to the scene
    file, and helper functions to do various things like find node connections,
    convert Y-Up transforms to Z-Up etc
    """
    
    outputString = str()
    moduleLoaded = False
    
    dagPath = OpenMaya.MDagPath()
    
    dpNode = OpenMaya.MFnDependencyNode()
    
    fShape = OpenMaya.MObject()
    
    plugName = str()
    inputFound = False
    
#    def __init__(self, dagPath):
#        pass

    @staticmethod
    def rgcAndClamp(colorValue):
        if cmds.getAttr( 'lux_settings.scene_reverse_gamma' ) == 1:
            gamma = cmds.getAttr( 'lux_settings.film_gamma' )
            colorValue = colorValue**gamma
            
        if cmds.getAttr( 'lux_settings.scene_clamp_color' ) == 1:
            colorValue *= 0.9
            if colorValue > 0.9: colorValue = 0.9
            if colorValue < 0.0: colorValue = 0.0
            
        return colorValue
    
    def intToBoolString(self, int):
        if int == 1: return 'true'
        else: return 'false'
    
    def writeTo(self, fout):
        """
        Write the accumulated outputString to the given file handle.
        """
        
        if not self.moduleLoaded:
            fout.write( self.loadModule() )
        else:
            fout.write( self.outputString )
    #end def write
    
    def addToOutput(self, string):
        """
        Accumulate the given string either to outputString, or direct to
        fileHandle if it exists.
        """
        
        if not 'fileHandle' in vars(self):
            self.outputString += (string + os.linesep)
        else:
            self.fileHandle.write( string + os.linesep )
            
    def prependToOutput(self, string):
        if not string == "":
            self.outputString = string + os.linesep + self.outputString
    
    def loadModule(self):
        """
        "Load" this module, ie. start it's main process. Returns the outputString
        if not writing direct to file.
        """
        
        self.getOutput()
        self.moduleLoaded = True
        return self.outputString
    #end def loadModule
    
    # THIS IS A TEXTURE FACTORY
    def detectInput(self, attrType):
        self.inputFound = False
        
        from Lux.LuxNodes.TextureNodes.bilerpTexture import bilerpTexture
        from Lux.LuxNodes.TextureNodes.blenderCloudsTexture import blenderCloudsTexture
        from Lux.LuxNodes.TextureNodes.blenderMarbleTexture import blenderMarbleTexture
        from Lux.LuxNodes.TextureNodes.blenderMusgraveTexture import blenderMusgraveTexture
        from Lux.LuxNodes.TextureNodes.blenderWoodTexture import blenderWoodTexture
        from Lux.LuxNodes.TextureNodes.checkerboard2dTexture import checkerboard2dTexture
        from Lux.LuxNodes.TextureNodes.checkerboard3dTexture import checkerboard3dTexture
        from Lux.LuxNodes.TextureNodes.dotsTexture import dotsTexture
        from Lux.LuxNodes.TextureNodes.fbmTexture import fbmTexture
        from Lux.LuxNodes.TextureNodes.marbleTexture import marbleTexture
        from Lux.LuxNodes.TextureNodes.mixTexture import mixTexture
        from Lux.LuxNodes.TextureNodes.scaleTexture import scaleTexture
        from Lux.LuxNodes.TextureNodes.windyTexture import windyTexture
        from Lux.LuxNodes.TextureNodes.wrinkledTexture import wrinkledTexture
        
        # psuedo-texture nodes
        from Lux.LuxNodes.TextureNodes.bumpmapTexture import bumpmapTexture
        from Lux.LuxNodes.TextureNodes.fileTexture import fileTexture
        
        onPlug = self.shaderNode.findPlug(self.plugName)
        inputPlugs = OpenMaya.MPlugArray()
        onPlug.connectedTo(inputPlugs, True, True)
        
        textureNode = False
        
        for ftIndex in range(0, inputPlugs.length()):
            inputNode = inputPlugs[ftIndex].node()
            iNFn = OpenMaya.MFnDependencyNode( inputNode )
            if inputNode.apiType() == OpenMaya.MFn.kBump \
            or inputNode.apiType() == OpenMaya.MFn.kBump3d:
                textureNode = bumpmapTexture()
                break
            if inputNode.apiType() == OpenMaya.MFn.kFileTexture:
                textureNode = fileTexture()
                break
            if iNFn.typeName() == bilerpTexture.nodeName():
                textureNode = bilerpTexture()
                break
            if iNFn.typeName() == blenderCloudsTexture.nodeName():
                textureNode = blenderCloudsTexture()
                break
            if iNFn.typeName() == blenderMarbleTexture.nodeName():
                textureNode = blenderMarbleTexture()
                break
            if iNFn.typeName() == blenderMusgraveTexture.nodeName():
                textureNode = blenderMusgraveTexture()
                break
            if iNFn.typeName() == blenderWoodTexture.nodeName():
                textureNode = blenderWoodTexture()
                break
            if iNFn.typeName() == checkerboard2dTexture.nodeName():
                textureNode = checkerboard2dTexture()
                break
            if iNFn.typeName() == checkerboard3dTexture.nodeName():
                textureNode = checkerboard3dTexture()
                break
            if iNFn.typeName() == dotsTexture.nodeName():
                textureNode = dotsTexture()
                break
            if iNFn.typeName() == fbmTexture.nodeName():
                textureNode = fbmTexture()
                break
            if iNFn.typeName() == marbleTexture.nodeName():
                textureNode = marbleTexture()
                break
            if iNFn.typeName() == mixTexture.nodeName():
                textureNode = mixTexture()
                break
            if iNFn.typeName() == scaleTexture.nodeName():
                textureNode = scaleTexture()
                break
            if iNFn.typeName() == windyTexture.nodeName():
                textureNode = windyTexture()
                break
            if iNFn.typeName() == fbmTexture.nodeName():
                textureNode = fbmTexture()
                break
            if iNFn.typeName() == wrinkledTexture.nodeName():
                textureNode = wrinkledTexture()
                break
            
        if not textureNode == False:
            self.inputFound = True
            #self.addToOutput(
            return iNFn.name(), textureNode.getTexture( self.plugName, iNFn, iNFn.name(), attrType )
        else:
            return '', ''
    
    
    def findShadingGroup(self, instanceNum = 0, setNumber = 0):
        if self.fShape.type() == OpenMaya.MFn.kMesh:
            try:
                shadingGroups = OpenMaya.MObjectArray()
                faceIndices = OpenMaya.MIntArray()
                self.fShape.getConnectedShaders(instanceNum, shadingGroups, faceIndices)
                # we return the material connected to the given setNumber
                theShadingGroup = OpenMaya.MFnDependencyNode( shadingGroups[setNumber] )
            except:
                OpenMaya.MGlobal.displayError("Could not find shading group")
                raise
        
        elif self.fShape.type() == OpenMaya.MFn.kNurbsSurface:
            plugs = OpenMaya.MPlugArray()
            self.fShape.getConnections(plugs)
            otherside = OpenMaya.MPlugArray()
            theShadingGroup = OpenMaya.MFnDependencyNode()
            for j in range(0, plugs.length()):
                plugs[j].connectedTo(otherside, False, True)
                for i in range(0, otherside.length()):
                    if otherside[i].node().hasFn(OpenMaya.MFn.kShadingEngine):
                        theShadingGroup = OpenMaya.MFnDependencyNode(otherside[i].node())
                        
        return theShadingGroup
    
    def findSurfaceShader(self, shadingGroup):
        """
        Find the surfaceShader node connected to this fShape's shadingGroup.
        """
                
        surfaceShader = shadingGroup.findPlug("surfaceShader")
        materials = OpenMaya.MPlugArray()
        surfaceShader.connectedTo(materials, True, True)
        
        if materials.length() > 0:
            matNode = materials[0].node()
            theMaterial = OpenMaya.MFnDependencyNode( matNode )
            
            if theMaterial.typeName() == "luxshader":
                materialTypePlug = theMaterial.findPlug( "material" )
                materialType = materialTypePlug.asInt()
            else:
                materialType = False
            
            if materialType == 10:
                return self.getAreaLight(theMaterial)
            else:
                return self.getNamedMaterial(theMaterial)
        else:
            return ''
        
    def findDisplacementShader(self, shadingGroup):
        """
        Find the displacementShader node connected to this fShape's shadingGroup.
        """
        
        displacementShader = shadingGroup.findPlug('displacementShader')
        dispNodes = OpenMaya.MPlugArray()
        displacementShader.connectedTo(dispNodes, True, True)
        
        if dispNodes.length() > 0:
            dispNode = dispNodes[0].node()
            theDisplacementShader = OpenMaya.MFnDependencyNode( dispNode )
            
            texPlug = theDisplacementShader.findPlug('displacement')
            dispInputPlugs = OpenMaya.MPlugArray()
            texPlug.connectedTo(dispInputPlugs, True, True)
            
            if dispInputPlugs.length() > 0:
                texNodeName = OpenMaya.MFnDependencyNode( dispInputPlugs[0].node() ).name()
                displacementMapName = texNodeName + ".displacement"
                return '\t"string displacementmap" ["%s"]' % displacementMapName
            else:
                return ''
        else:
            return ''
        
    
    def getNamedMaterial(self, shaderNode):
        """
        Return the NamedMaterial syntax with this class' shaderNode.name()
        """
        
        return '\tNamedMaterial "' + shaderNode.name() + '"' #theMaterial.name()
    
    def getAreaLight(self, shaderNode):
        """
        Return AreaLightSource syntax with this class' shaderNode's attributes
        """
        
        colorPlug = shaderNode.findPlug("arealightLR")
        colorR = self.rgcAndClamp( colorPlug.asFloat() )
        
        colorPlug = shaderNode.findPlug("arealightLG")
        colorG = self.rgcAndClamp( colorPlug.asFloat() )
        
        colorPlug = shaderNode.findPlug("arealightLB")
        colorB = self.rgcAndClamp( colorPlug.asFloat() )
        
        gainPlug = shaderNode.findPlug("arealightGain")
        gain = gainPlug.asFloat()
        
        nsPlug = shaderNode.findPlug("arealightNumsamples")
        numSamples = nsPlug.asInt()
        
        outStr  = '\tAreaLightSource "area"' + os.linesep
        outStr += ( '\t\t"integer nsamples" [%i]' % numSamples ) + os.linesep
        outStr += ( '\t\t"color L" [%f %f %f]' % (colorR, colorG, colorB) ) + os.linesep
        outStr += ( '\t\t"float gain" [%f]' % gain ) + os.linesep
        
        return outStr
    
    def translationMatrix(self, dagPath):
        """
        Convert this class' dagPath inclusive transformation matrix as ConcatTransform
        syntax. Y-Up to Z-Up and scale factor conversion is also performed.
        """
        
        matrix =  dagPath.inclusiveMatrix()
        
        matrix = self.checkUpAxis(matrix)

        strOut  = ( '\tConcatTransform [%f %f %f %f'  % (matrix(0,0), matrix(0,1), matrix(0,2), matrix(0,3)) ) + os.linesep
        strOut += ( '\t                 %f %f %f %f'  % (matrix(1,0), matrix(1,1), matrix(1,2), matrix(1,3)) ) + os.linesep
        strOut += ( '\t                 %f %f %f %f'  % (matrix(2,0), matrix(2,1), matrix(2,2), matrix(2,3)) ) + os.linesep
        strOut += ( '\t                 %f %f %f %f]' % (matrix(3,0), matrix(3,1), matrix(3,2), matrix(3,3)) )
        
        return strOut
    #end def translationMatrix
    
    def checkUpAxis(self, matrix):
        """
        Check the scene's up axis, and convert the given transform matrix if necessary.
        """
        
        if OpenMaya.MGlobal.isYAxisUp():
            tMatrix = OpenMaya.MTransformationMatrix( matrix )
            tMatrix.rotateBy( OpenMaya.MEulerRotation(math.radians(90), 0, 0), OpenMaya.MSpace.kTransform )
            oTrans = tMatrix.getTranslation(OpenMaya.MSpace.kTransform)
            oTrans = OpenMaya.MVector( oTrans[0], -oTrans[2], oTrans[1] )
            tMatrix.setTranslation(oTrans, OpenMaya.MSpace.kTransform)
            return self.checkScale( tMatrix.asMatrix() )
        else:
            return self.checkScale( matrix )
        
    def getSceneScaleFactor(self):
        cmdResult = OpenMaya.MCommandResult()
        sScale = OpenMaya.MGlobal.executeCommand('currentUnit -q -linear', cmdResult, False, False)
        sceneUnits = cmdResult.stringResult()
        
        #self.log('Found scene units: ' + sceneUnits )
        if sceneUnits == "cm":
            return 0.01
        elif sceneUnits == "mm":
            return 0.001
        elif sceneUnits == "in":
            return 0.0254
        elif sceneUnits == "ft":
            return 0.3048
        elif sceneUnits == "yd":
            return 0.9144
        else:
            return 1.0
            
    def checkScale(self, matrix):
        # Adjust scene scale
        scaleFactor = self.getSceneScaleFactor()
            
        scaleMatrix = OpenMaya.MMatrix()    
        OpenMaya.MScriptUtil.createMatrixFromList( (scaleFactor,0,0,0,
                                                    0,scaleFactor,0,0,
                                                    0,0,scaleFactor,0,
                                                    0,0,0,1),
                                                    scaleMatrix )
        matrix = matrix * scaleMatrix
        
        return matrix
    
    # This is the method that child classes should override,
    # calling addToOutput(<string>) to construct the output
    def getOutput(self):
        pass