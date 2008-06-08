# ------------------------------------------------------------------------------
# Lux exporter python script plugin for Maya
#
# Based on a translation of the c++ luxmaya exporter, in turn based on
# maya-pbrt by Mark Colbert
#
# Python translation by Doug Hammond 02/2008
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# lights export module
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from ExportModule import ExportModule

class Light(ExportModule):
	"""
	Light ExportModule base class. This is primarily a factory for returning
	various light types.
	"""
	
# 	def __init__(self):
# 		pass
	
	@staticmethod
	def LightFactory( fileHandle, dagPath ):
		"""
		Detect the given light type and return a corresponding light object
		"""
		
		nodeType = dagPath.node().apiType()
		
		if nodeType == OpenMaya.MFn.kSpotLight:
			#this is a spotlight
			return SpotLight( fileHandle, dagPath )
		elif nodeType == OpenMaya.MFn.kPointLight:
			#this is a pointlight
			return PointLight( fileHandle, dagPath )
		else:
			OpenMaya.MGlobal.displayWarning("Light type %i not supported" % nodeType)
			return False
	#end def LightFactory
	
	# TODO
	#  add support for:
	#	distant
	#	goniometric
	#	projection
	
	def getOutput(self):
		"""
		Nothing to do here, child classes output light type specific syntax.
		"""
		pass
	
#end class Light

class SpotLight(Light):
	"""
	Spot light type.
	"""

	light = OpenMaya.MFnSpotLight()
	
	def __init__( self, fileHandle, dagPath ):
		"""
		Constructor. Sets up this object's data.
		"""
		
		self.fileHandle = fileHandle
		self.dagPath = dagPath
		self.light = OpenMaya.MFnSpotLight( dagPath )
	#end def __init__
		
	def getOutput(self):
		"""
		Return lux LightSource "spot" from the given spotlight node.
		"""
		
		color = self.light.color()
		intensity = self.light.intensity()	
	
		self.addToOutput( '# Spot Light ' + self.dagPath.fullPathName() )
		self.addToOutput( 'TransformBegin' )
		self.addToOutput( self.translationMatrix( self.dagPath ) )
		self.addToOutput( '\tLightSource "spot"' )
		self.addToOutput( '\t\t"color I" [%f %f %f]' % (color.r*intensity, color.g*intensity, color.b*intensity) )
		self.addToOutput( '\t\t"point from" [0 0 0]')
		self.addToOutput( '\t\t"point to" [0 0 -1]' )
		self.addToOutput( '\t\t"float coneangle" [%f]' % ( self.light.coneAngle()*180/math.pi ) )
		self.addToOutput( '\t\t"float conedeltaangle" [%f]' % ( self.light.dropOff()*180/math.pi ) )
		self.addToOutput( 'TransformEnd' )
		self.addToOutput( '' )
		
		self.fileHandle.flush()
	#end def getOutput
		
#end class SpotLight

class PointLight(Light):
	"""
	Point light type.
	"""
	
	light = OpenMaya.MFnPointLight()

	def __init__( self, fileHandle, dagPath ):
		"""
		Constructor. Sets up this object's data.
		"""
		
		self.fileHandle = fileHandle
		self.dagPath = dagPath
		self.light = OpenMaya.MFnPointLight( dagPath )
	#end def __init__

	def getOutput(self):
		"""
		Return lux LightSource "point" from the given pointlight node.
		"""
		
		color = self.light.color()
		intensity = self.light.intensity()	
		
		self.addToOutput( '# Point Light ' + self.dagPath.fullPathName() )
		self.addToOutput( 'TransformBegin' )
		self.addToOutput( self.translationMatrix( self.dagPath ) )
		self.addToOutput( '\tLightSource "point"' )
		self.addToOutput( '\t\t"color I" [%f %f %f]' % (color.r*intensity, color.g*intensity, color.b*intensity) )
		self.addToOutput( 'TransformEnd' )
		self.addToOutput( '' )
	#end def getOutput
	
#end class PointLight