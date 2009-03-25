# ------------------------------------------------------------------------------
# Lux nodes for Maya
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
# Lux nodes and attributes for Maya ( base class )
#
# ------------------------------------------------------------------------------

import os
os.altsep = '/'
from maya import OpenMaya
from maya import cmds

from Lux.LuxExportModules.ExportModule import ExportModule

class LuxNode:
    """
    Custom Lux node base class
    """
    
    attributes = {}    
    outputString = str()
    
    def addToOutput(self, string):
        if not string == '': 
            self.outputString += ( string + os.linesep )
            
    def prependToOutput(self, string):
        if not string == '':
            self.outputString = string + os.linesep + self.outputString 

    # node attribute setup helper functions
    @staticmethod
    def makeInput(attr):
        attr.setKeyable(1)
        attr.setStorable(1)
        attr.setReadable(1)
        attr.setWritable(1)

    @staticmethod
    def makeOrdinary(attr):
        attr.setKeyable(1)
        attr.setStorable(1)
        attr.setReadable(0)
        attr.setWritable(1)

    @staticmethod
    def makeColor(longName, shortName, defaultR = 1.0, defaultG = 1.0, defaultB = 1.0):
        nAttr = OpenMaya.MFnNumericAttribute()
        attrOut = nAttr.createColor(longName, shortName)
        LuxNode.makeInput( nAttr )
        nAttr.setUsedAsColor(1)
        nAttr.setDefault(defaultR, defaultG, defaultB)
        return attrOut

    @staticmethod
    def makeFloat(longName, shortName, default = 0.0, input = True):
        nAttr = OpenMaya.MFnNumericAttribute()
        attrOut = nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kFloat)
        if input:
            LuxNode.makeInput( nAttr )
        else:
            LuxNode.makeOrdinary( nAttr )
        nAttr.setDefault( default )
        return attrOut
    
    @staticmethod
    def makeInteger(longName, shortName, default = 0, input = True):
        nAttr = OpenMaya.MFnNumericAttribute()
        attrOut = nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kInt)
        if input:
            LuxNode.makeInput( nAttr )
        else:
            LuxNode.makeOrdinary( nAttr )
        nAttr.setDefault( default )
        return attrOut
    
    @staticmethod
    def makeBoolean(longName, shortName, default = False, input = True):
        nAttr = OpenMaya.MFnNumericAttribute()
        attrOut = nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kBoolean)
        if input:
            LuxNode.makeInput( nAttr )
        else:
            LuxNode.makeOrdinary( nAttr )
        # nAttr.setDefault( default )
        return attrOut


            
class NodeAttribute(ExportModule):
    """
    Custom Lux node attribute base class
    """
    
    luxName = str()
    shaderNode = OpenMaya.MFnDependencyNode()
    shaderName = str()
    
    exportName = str()
    
    def __init__(self, mayaAttrName, addTo, prependTo):
        self.addToOutput = addTo
        self.prependToOutput = prependTo
        self.plugName = mayaAttrName

    
        
class ShaderColorAttribute(NodeAttribute):
    """
    Color Attribute for Shader nodes
    """
    
    def __init__(self, mayaAttrName):
        self.plugName = mayaAttrName
        
    def getOutput(self, luxName, shaderNode, shaderName):
        self.luxName    = luxName
        self.shaderNode = shaderNode
        self.shaderName = shaderName
        
        texName, inputStr = self.detectInput('color')
        
        if self.inputFound:
            self.prependToOutput( inputStr )
            self.exportName = '%s.%s' % (texName, self.plugName)
        else:
            colorPlug = shaderNode.findPlug(self.plugName + "R")
            colorR = self.rgcAndClamp( colorPlug.asFloat() )
            
            colorPlug = shaderNode.findPlug(self.plugName + "G")
            colorG = self.rgcAndClamp( colorPlug.asFloat() )
            
            colorPlug = shaderNode.findPlug(self.plugName + "B")
            colorB = self.rgcAndClamp( colorPlug.asFloat() )
            
            self.addToOutput( 'Texture "%s.%s"' % (self.shaderName, self.luxName) )
            self.addToOutput( '\t"color" "constant"' )
            self.addToOutput( '\t\t"color value" [%f %f %f]' % (colorR, colorG, colorB) )
        
        return self.outputString
    
class ShaderFloatAttribute(NodeAttribute):
    """
    Float Attribute for Shader nodes
    """
    
    def __init__(self, mayaAttrName, preScale = 1, invert = False, reciprocal = False, postScale = 1):
        self.plugName = mayaAttrName
        
        self.aPreScale  = preScale
        self.aInvert    = invert
        self.aRecip     = reciprocal
        self.aPostScale = postScale
        
    def getOutput(self, luxName, shaderNode, shaderName):
        self.luxName    = luxName
        self.shaderNode = shaderNode
        self.shaderName = shaderName
        
        texName, inputStr = self.detectInput('float')
        
        if self.inputFound:
            self.prependToOutput( inputStr )
            self.exportName = '%s.%s' % (texName, self.plugName)
        else:
            floatPlug = shaderNode.findPlug(self.plugName)
            floatValue = floatPlug.asFloat() * self.aPreScale
            
            if self.aInvert:
                floatValue = 1 - floatValue
                
            if self.aRecip:
                floatValue = 1.0/floatValue
                
            floatValue *= self.aPostScale
    
            self.addToOutput( 'Texture "%s.%s"' % (self.shaderName, self.luxName) )
            self.addToOutput( '\t"float" "constant"' )
            self.addToOutput( '\t\t"float value" [%f]' % floatValue )
        
        return self.outputString    
    
class ShaderEnumAttribute(NodeAttribute):
    """
    Enum Attribute for Shader nodes
    """
    
    def __init__(self, mayaAttrName, nameValues):
        self.plugName = mayaAttrName
        self.nameValues = nameValues
        
    def getOutput(self, luxName, shaderNode, shaderName):
        
        ePlug = shaderNode.findPlug(self.plugName)
        eValue = ePlug.asInt()
        eValue = self.nameValues[eValue]
        
        if not eValue == "manual":
            return '\t"string %s" ["%s"]' % (luxName, eValue)
        else:
            return ''
        
class ShaderStringAttribute(NodeAttribute):
    """
    String Attribute for Shader nodes
    """
    
    def __init__(self, mayaAttrName):
        self.plugName = mayaAttrName
        
    def getOutput(self, luxName, shaderNode, shaderName):
        plug = shaderNode.findPlug(self.plugName)
        self.rawValue = plug.asString()
        return '\t"string %s" ["%s"]' % (luxName, self.rawValue)
    
class ShaderBoolAttribute(NodeAttribute):
    """
    Bool Attribute for Shader nodes
    """
    
    def __init__(self, mayaAttrName):
        self.plugName = mayaAttrName
        
    def getOutput(self, luxName, shaderNode, shaderName):
        plug = shaderNode.findPlug(self.plugName)
        self.rawValue = self.intToBoolString( plug.asInt() )
        return '\t"bool %s" ["%s"]' % (luxName, self.rawValue)
    
class TextureBoolAttribute(NodeAttribute):
    """
    Boolean Attribute for Texture nodes
    """
    
#   def __init__(self, mayaAttrName, addTo, prependTo):
#       self.addToOutput = addTo
#       self.prependToOutput = prependTo
#       self.plugName = mayaAttrName
        
    def getOutput(self, luxParamName, textureNode, textureName, luxName):
        myPlug = textureNode.findPlug( self.plugName )
        value = self.intToBoolString( myPlug.asInt() )
        return '\t\t"bool %s" ["%s"]' % (self.plugName, value)
        
class TextureFloatAttribute(NodeAttribute):
    """
    Float Attribute for Texture nodes
    """
    
#    def __init__(self, mayaAttrName, addTo, prependTo):
#        self.addToOutput = addTo
#        self.prependToOutput = prependTo
#        self.plugName = mayaAttrName
        
    def getOutput(self, luxParamName, textureNode, textureName, luxName):
        cPlug = self.plugName
        self.shaderNode = textureNode
        
        texName, inputStr = self.detectInput( 'float' )
        
        if self.inputFound:
            self.prependToOutput(inputStr)
            nTextName = '%s.%s' % (texName, cPlug)
            self.addToOutput( '\t\t"texture %s" ["%s"]' % (luxParamName, nTextName ))
        else:
            myPlug = textureNode.findPlug( cPlug  )
            value = myPlug.asFloat()
            self.addToOutput( '\t\t"float %s" [%f]' % (luxParamName, value) )
        
        return self.outputString
    
class TextureColorAttribute(NodeAttribute):
    """
    Color Attribute for Texture nodes
    """
    
#    def __init__(self, mayaAttrName, addTo, prependTo):
#        self.addToOutput = addTo
#        self.prependToOutput = prependTo
#        self.plugName = mayaAttrName
        
    def getOutput(self, luxParamName, textureNode, textureName, luxName):
        cPlug = self.plugName
        self.shaderNode = textureNode
        
        texName, inputStr = self.detectInput( 'color' )
        
        if self.inputFound:
            self.prependToOutput(inputStr)
            nTextName = '%s.%s' % (texName, cPlug)
            self.addToOutput( '\t\t"texture %s" ["%s"]' % (cPlug, nTextName ))
        else:
            myPlugR = textureNode.findPlug( cPlug + 'R' )
            valueR = self.rgcAndClamp( myPlugR.asFloat() )
            myPlugG = textureNode.findPlug( cPlug + 'G' )
            valueG = self.rgcAndClamp( myPlugG.asFloat() )
            myPlugB = textureNode.findPlug( cPlug + 'B' )
            valueB = self.rgcAndClamp( myPlugB.asFloat() )
            
            self.addToOutput( '\t\t"color %s" [%f %f %f]' % (cPlug, valueR, valueG, valueB) )
        
        return self.outputString

class TextureVectorAttribute(NodeAttribute):
    """
    Vector Attribute for Texture nodes
    """
    
#    def __init__(self, mayaAttrName, addTo, prependTo):
#        self.addToOutput = addTo
#        self.prependToOutput = prependTo
#        self.plugName = mayaAttrName
        
    def getOutput(self, luxParamName, textureNode, textureName, luxName):
        cPlug = self.plugName
        self.shaderNode = textureNode
        
        myPlugX = textureNode.findPlug( cPlug + 'X' )
        valueX = myPlugX.asFloat()
        myPlugY = textureNode.findPlug( cPlug + 'Y' )
        valueY = myPlugY.asFloat()
        myPlugZ = textureNode.findPlug( cPlug + 'Z' )
        valueZ = myPlugZ.asFloat()
        self.addToOutput( '\t\t"vector %s" [%f %f %f]' % (cPlug, valueX, valueY, valueZ) )
        
        return self.outputString


class TextureEnumAttribute(NodeAttribute):
    """
    Enum Attribute for Texture nodes
    """
    
    def __init__(self, mayaAttrName, addTo, prependTo, asString = False, nameValues = []):
        self.addToOutput = addTo
        self.prependToOutput = prependTo
        self.plugName = mayaAttrName
        self.asString = asString
        self.nameValues = nameValues
        
    def getOutput(self, luxParamName, textureNode, textureName, luxName):
        myPlug = textureNode.findPlug( self.plugName )
        value = myPlug.asInt()
        if self.asString:
            eValue = self.nameValues[value]
            return '\t\t"string %s" ["%s"]' % (self.plugName, eValue)
        else:
            return '\t\t"integer %s" [%i]' % (self.plugName, value)

class TextureIntegerAttribute(NodeAttribute):
    """
    Integer Attribute for Texture nodes
    """
    
#    def __init__(self, mayaAttrName, addTo, prependTo):
#        self.addToOutput = addTo
#        self.prependToOutput = prependTo
#        self.plugName = mayaAttrName
        
    def getOutput(self, luxParamName, textureNode, textureName, luxName):
        myPlug = textureNode.findPlug( self.plugName )
        value = myPlug.asInt()
        return '\t\t"integer %s" [%i]' % (self.plugName, value)
        
class TextureStringAttribute(NodeAttribute):
    """
    String Attribute for Texture nodes
    """
    
#    def __init__(self, mayaAttrName, addTo, prependTo):
#        self.addToOutput = addTo
#        self.prependToOutput = prependTo
#        self.plugName = mayaAttrName

    def getOutput(self, luxParamName, textureNode, textureName, luxName):
        myPlug = textureNode.findPlug( self.plugName )
        value = myPlug.asString()
        return '\t\t"string %s" ["%s"]' % (self.plugName, value)