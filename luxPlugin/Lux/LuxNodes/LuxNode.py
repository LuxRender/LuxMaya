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

import os, shutil
os.altsep = '/'
from maya import OpenMaya
from maya import cmds

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
	def makeFloat(longName, shortName, default = 0.0, input = False):
		nAttr = OpenMaya.MFnNumericAttribute()
		attrOut = nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kFloat)
		if input:
			LuxNode.makeInput( nAttr )
		else:
			LuxNode.makeOrdinary( nAttr )
		nAttr.setDefault( default )
		return attrOut
	
	@staticmethod
	def makeInteger(longName, shortName, default = 0, input = False):
		nAttr = OpenMaya.MFnNumericAttribute()
		attrOut = nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kInt)
		if input:
			LuxNode.makeInput( nAttr )
		else:
			LuxNode.makeOrdinary( nAttr )
		nAttr.setDefault( default )
		return attrOut
	
	@staticmethod
	def makeBoolean(longName, shortName, default = False, input = False):
		nAttr = OpenMaya.MFnNumericAttribute()
		attrOut = nAttr.create(longName, shortName, OpenMaya.MFnNumericData.kBoolean)
		if input:
			LuxNode.makeInput( nAttr )
		else:
			LuxNode.makeOrdinary( nAttr )
		# nAttr.setDefault( default )
		return attrOut

class FileCollector:
	"""
	Texture file collector for export process.
	Probably this should be in it's own	file.
	"""
	
	@staticmethod
	def collectTexture( texFile ):
		collectEnabled = cmds.getAttr( 'lux_settings.scene_collect_texture' )
		if collectEnabled:
			return FileCollector.doCollect( fileName = texFile, targetPath = 'textures' )
		else:
			return texFile
		
	@staticmethod
	def collectBumpmap( texFile ):
		collectEnabled = cmds.getAttr( 'lux_settings.scene_collect_bump' )
		if collectEnabled:
			return FileCollector.doCollect( fileName = texFile, targetPath = 'bumpmaps' )
		else:
			return texFile
		
	@staticmethod
	def collectHDRI( texFile ):
		collectEnabled = cmds.getAttr( 'lux_settings.scene_collect_hdri' )
		if collectEnabled:
			return FileCollector.doCollect( fileName = texFile, targetPath = 'environments' )
		else:
			return texFile
		
	@staticmethod
	def doCollect( fileName, targetPath ):
		
		if not os.path.exists( fileName ):
			OpenMaya.MGlobal.displayWarning( "File %s doesn't exist" % fileName )
		else:
			scenePath = cmds.getAttr( 'lux_settings.scene_path' )
			newFilePath = scenePath + os.altsep + targetPath + os.altsep
			if not os.path.exists( newFilePath ):
				os.mkdir( newFilePath )
			fileBaseName = os.path.basename( fileName )
			newFileName = newFilePath + fileBaseName
			if not os.path.exists( newFileName ):
				shutil.copyfile( fileName, newFileName )
			fileName = '..' + os.altsep + targetPath + os.altsep + fileBaseName
		
		return fileName
			
class NodeAttribute:
	"""
	Custom Lux node attribute base class
	"""
	
	plugName = str()
	
	luxName = str()
	shaderNode = OpenMaya.MFnDependencyNode()
	shaderName = str()
	
	inputFound = False
	
	outputString = str()
	
	exportName = str()
	
	def __init__(self, mayaAttrName, addTo, prependTo):
		self.addToOutput = addTo
		self.prependToOutput = prependTo
		self.plugName = mayaAttrName
	
	def addToOutput(self, string):
		if not string == '': 
			self.outputString += ( string + os.linesep )

	def prependToOutput(self, string):
		if not string == '':
			self.outputString = string + os.linesep + self.outputString 

	# THIS IS A TEXTURE FACTORY
	def detectInput(self, attrType):
		self.inputFound = False
		
		from TextureNodes.bilerpTexture import bilerpTexture
		from TextureNodes.blenderCloudsTexture import blenderCloudsTexture
		from TextureNodes.blenderMarbleTexture import blenderMarbleTexture
		from TextureNodes.blenderMusgraveTexture import blenderMusgraveTexture
		from TextureNodes.blenderWoodTexture import blenderWoodTexture
		from TextureNodes.bumpmapTexture import bumpmapTexture
		from TextureNodes.checkerboard2dTexture import checkerboard2dTexture
		from TextureNodes.checkerboard3dTexture import checkerboard3dTexture
		from TextureNodes.dotsTexture import dotsTexture
		from TextureNodes.fbmTexture import fbmTexture
		from TextureNodes.marbleTexture import marbleTexture
		from TextureNodes.mixTexture import mixTexture
		from TextureNodes.windyTexture import windyTexture
		from TextureNodes.wrinkledTexture import wrinkledTexture
		
		from TextureNodes.fileTexture import fileTexture
		
		onPlug = self.shaderNode.findPlug(self.plugName)
		inputPlugs = OpenMaya.MPlugArray()
		onPlug.connectedTo(inputPlugs, True, True)
		
		textureNode = False
		
		for ftIndex in range(0, inputPlugs.length()):
			inputNode = inputPlugs[ftIndex].node()
			iNFn = OpenMaya.MFnDependencyNode( inputNode )
			if inputNode.apiType() == OpenMaya.MFn.kBump:
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
		
class ShaderColorAttribute(NodeAttribute):
	"""
	Color Attribute for Shader nodes
	"""
	
	def __init__(self, mayaAttrName):
		self.plugName = mayaAttrName
		
	def getOutput(self, luxName, shaderNode, shaderName):
		self.luxName	= luxName
		self.shaderNode = shaderNode
		self.shaderName = shaderName
		
		texName, inputStr = self.detectInput('color')
		
		if self.inputFound:
			self.prependToOutput( inputStr )
			self.exportName = '%s.%s' % (texName, self.plugName)
		else:
			colorPlug = shaderNode.findPlug(self.plugName + "R")
			colorR = colorPlug.asFloat()
			
			colorPlug = shaderNode.findPlug(self.plugName + "G")
			colorG = colorPlug.asFloat()
			
			colorPlug = shaderNode.findPlug(self.plugName + "B")
			colorB = colorPlug.asFloat()
			
			self.addToOutput( 'Texture "%s.%s"' % (self.shaderName, self.luxName) )
			self.addToOutput( '\t"color" "constant"' )
			self.addToOutput( '\t\t"color value" [%f %f %f]' % (colorR, colorG, colorB) )
		
		return self.outputString
	
class ShaderFloatAttribute(NodeAttribute):
	"""
	Float Attribute for Shader nodes
	"""
	
	def __init__(self, mayaAttrName, preScale = 1, invert = False, postScale = 1):
		self.plugName = mayaAttrName
		
		self.aPreScale  = preScale
		self.aInvert	= invert
		self.aPostScale = postScale
		
	def getOutput(self, luxName, shaderNode, shaderName):
		self.luxName	= luxName
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
		
class TextureFloatAttribute(NodeAttribute):
	"""
	Float Attribute for Texture nodes
	"""
	
#	def __init__(self, mayaAttrName, addTo, prependTo):
#		self.addToOutput = addTo
#		self.prependToOutput = prependTo
#		self.plugName = mayaAttrName
		
	def getOutput(self, textureNode, textureName, luxName):
		cPlug = self.plugName
		self.shaderNode = textureNode
		
		texName, inputStr = self.detectInput( 'float' )
		
		if self.inputFound:
			self.prependToOutput(inputStr)
			nTextName = '%s.%s' % (texName, cPlug)
			self.addToOutput( '\t\t"texture %s" ["%s"]' % (cPlug, nTextName ))
		else:
			myPlug = textureNode.findPlug( cPlug  )
			value = myPlug.asFloat()
			self.addToOutput( '\t\t"float %s" [%f]' % (cPlug, value) )
		
		return self.outputString
	
class TextureColorAttribute(NodeAttribute):
	"""
	Color Attribute for Texture nodes
	"""
	
#	def __init__(self, mayaAttrName, addTo, prependTo):
#		self.addToOutput = addTo
#		self.prependToOutput = prependTo
#		self.plugName = mayaAttrName
		
	def getOutput(self, textureNode, textureName, luxName):
		cPlug = self.plugName
		self.shaderNode = textureNode
		
		texName, inputStr = self.detectInput( 'color' )
		
		if self.inputFound:
			self.prependToOutput(inputStr)
			nTextName = '%s.%s' % (texName, cPlug)
			self.addToOutput( '\t\t"texture %s" ["%s"]' % (cPlug, nTextName ))
		else:
			myPlugR = textureNode.findPlug( cPlug + 'R' )
			valueR = myPlugR.asFloat()
			myPlugG = textureNode.findPlug( cPlug + 'G' )
			valueG = myPlugG.asFloat()
			myPlugB = textureNode.findPlug( cPlug + 'B' )
			valueB = myPlugB.asFloat()
			self.addToOutput( '\t\t"color %s" [%f %f %f]' % (cPlug, valueR, valueG, valueB) )
		
		return self.outputString

class TextureVectorAttribute(NodeAttribute):
	"""
	Vector Attribute for Texture nodes
	"""
	
#	def __init__(self, mayaAttrName, addTo, prependTo):
#		self.addToOutput = addTo
#		self.prependToOutput = prependTo
#		self.plugName = mayaAttrName
		
	def getOutput(self, textureNode, textureName, luxName):
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
		
	def getOutput(self, textureNode, textureName, luxName):
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
	
#	def __init__(self, mayaAttrName, addTo, prependTo):
#		self.addToOutput = addTo
#		self.prependToOutput = prependTo
#		self.plugName = mayaAttrName
		
	def getOutput(self, textureNode, textureName, luxName):
		myPlug = textureNode.findPlug( self.plugName )
		value = myPlug.asInt()
		return '\t\t"integer %s" [%i]' % (self.plugName, value)
		
class TextureStringAttribute(NodeAttribute):
	"""
	String Attribute for Texture nodes
	"""
	
#	def __init__(self, mayaAttrName, addTo, prependTo):
#		self.addToOutput = addTo
#		self.prependToOutput = prependTo
#		self.plugName = mayaAttrName

	def getOutput(self, textureNode, textureName, luxName):
		myPlug = textureNode.findPlug( self.plugName )
		value = myPlug.asString()
		return '\t\t"string %s" ["%s"]' % (self.plugName, value)