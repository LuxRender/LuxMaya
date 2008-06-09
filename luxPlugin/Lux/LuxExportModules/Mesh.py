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
# trianglemesh geometry export module (un-optimised version)
#
# ------------------------------------------------------------------------------

from maya import OpenMaya

from ExportModule import ExportModule

class Mesh(ExportModule):
	"""
	Polygon mesh ExportModule.
	"""

	fPolygonSets = OpenMaya.MObjectArray()
	fPolygonComponents = OpenMaya.MObjectArray()
	fShape = OpenMaya.MFnMesh()
	
	def __init__(self, fileHandles, dagPath):
		"""
		Constructor. Initialises fileHandle, dagPath, polygon sets, polygon components,
		the mesh function set.
		"""
		self.dagPath = dagPath
		
		self.meshHandle, self.portalsHandle = fileHandles
		
		if dagPath.fullPathName().lower().find('portal') != -1:
			self.fileHandle = self.portalsHandle
			self.portalsMode = True
		else:
			self.fileHandle = self.meshHandle
			self.portalsMode = False
		
		self.fPolygonSets = OpenMaya.MObjectArray()
		self.fPolygonComponents = OpenMaya.MObjectArray()
		
		self.fShape = OpenMaya.MFnMesh( dagPath )
		
		dagPath.extendToShape()
		
		self.instanceNum = 0
		if dagPath.isInstanced():
			instanceNum = dagPath.instanceNumber()
		
		self.fShape.getConnectedSetsAndMembers(self.instanceNum, self.fPolygonSets, self.fPolygonComponents, True)
		
		self.setCount = self.fPolygonSets.length()
		
		if self.setCount > 1:
			self.setCount -= 1
		
	#end def __init__
	
	def getOutput(self):
		"""
		Get the lux trianglemesh Shape syntax. All mesh sets are iterated here. 
		"""
		
		for i in range(0, self.setCount):
			self.polygonSet = PolygonSet( self.fileHandle, self.dagPath, self.fPolygonComponents[i], self.fPolygonSets[i])
			
			try:
				polyOut = self.polygonSet.loadModule();
			except:
				OpenMaya.MGlobal.displayWarning('Invalid mesh: %s (set %i), skipping' % (self.dagPath.fullPathName(), i) )
				continue
			
			self.addToOutput( '# Polygon Shape %s (set %i)' % (self.dagPath.fullPathName(), i) )
			self.addToOutput( 'AttributeBegin' )
			self.addToOutput( self.translationMatrix(self.dagPath) )
			
			# detect Material or AreaLight
			if not self.portalsMode:
				self.shadingGroup = self.findShadingGroup(self.instanceNum, i)
				self.addToOutput( self.findSurfaceShader( shadingGroup = self.shadingGroup ) )
				self.addToOutput( 'Shape "trianglemesh"' )
				self.addToOutput( self.findDisplacementShader( self.shadingGroup ) )
			else:
				self.addToOutput( 'PortalShape "trianglemesh"' )
				
			self.addToOutput( '\t"integer indices" [' )
			self.addToOutput( '\t\t' + self.polygonSet.getIndices() )
			# \t\t vertex indices int[3] on one line
			self.addToOutput( '\t]' )
			self.addToOutput( '\t"point P" [' )
			self.addToOutput( '\t\t' + self.polygonSet.getPoints() )
			# \t\t vertex points float[3] on one line
			self.addToOutput( '\t]' )
			self.addToOutput( '\t"normal N" [' )
			self.addToOutput( '\t\t' + self.polygonSet.getNormals() )
			# \t\t normal vectors float[3] on one line
			self.addToOutput( '\t]' )
			
			if self.polygonSet.hasUVs and not self.portalsMode:
				self.addToOutput( '\t"float uv" [' )
				self.addToOutput( '\t\t' + self.polygonSet.getUVs() )
				# \t\t vertex uv coords float[2] on one line
				self.addToOutput( '\t]' )
				
			self.addToOutput( 'AttributeEnd' )
			self.addToOutput( '' )
			
			self.fileHandle.flush()
	#end def getOutput
	


class PolygonSet(ExportModule):
	"""
	The mesh polygon set class. This class iterates over a mesh's polygon set and collates
	and exports all face vertex indices, points, normals and uv coords.
	The class is responsible for a lot (nearly all) of the time and memory used by the exporter.
	If anywhere could do with a focus on optimisation, it's here.
	"""
	
	component = OpenMaya.MObject()
	
	indicesString = str()
	pointsString = str()
	normalsString = str()
	uvsString = str()
	
	hasUVs = True

	def __init__(self, fileHandle, dagPath, component, set):
		"""
		Constructor, initilises all the data and lists we need.
		"""
		
		self.fileHandle = fileHandle
		self.dagPath = dagPath
		self.component = component
		self.points = []
		self.normals = []
		self.uvs = []
		self.indices = []
		self.count = 0
	#end def __init__
	
	def addToIndicesOutput(self, string):
		"""
		Either write this polygon set's indices to file, or append to string.
		"""
		
		if not 'fileHandle' in vars(self):
			self.indicesString += ( string + " " )
		else:
			self.fileHandle.write( string + ' ' )
	#end def addToIndicesOutput
	
	def addToPointsOutput(self, string):
		"""
		Either write this polygon set's points to file, or append to string.
		"""
		
		if not 'fileHandle' in vars(self):
			self.pointsString += ( string + " " )
		else:
			self.fileHandle.write( string + ' ' )
	#end def addToPointsOutput
	
	def addToNormalsOutput(self, string):
		"""
		Either write this polygon set's normals to file, or append to string.
		"""
		
		if not 'fileHandle' in vars(self):
			self.normalsString += ( string + " " )
		else:
			self.fileHandle.write( string + ' ' )
	#end def addToNormalsOutput
	
	def addToUVsOutput(self, string):
		"""
		Either write this polygon set's uv coords to file, or append to string.
		"""
		
		if not 'fileHandle' in vars(self):
			self.uvsString += ( string + " " )
		else:
			self.fileHandle.write( string + ' ' )
	#end def addToUVsOutput

	def getIndices(self):
		"""
		Iterate the indices list into file or string
		"""
		
		for ind in range(0, self.count):
			self.addToIndicesOutput( str(ind) )
		return self.indicesString
	
	def getPoints(self):
		"""
		Iterate the points list into file or string
		"""
		
		for pt in self.points:
			self.addToPointsOutput( str(pt) )
		return self.pointsString
	
	def getNormals(self):
		"""
		Iterate the normals list into file or string
		"""
		
		for nm in self.normals:
			self.addToNormalsOutput( str(nm) )
		return self.normalsString
	
	def getUVs(self):
		"""
		Iterate the uv coords list into file or string
		"""
		
		for uvo in self.uvs:
			self.addToUVsOutput( str(uvo) )
		return self.uvsString
	
	def getOutput(self):
		"""
		Iterate ove the polygons and compile various lists. This is by far the
		"busiest" part of the exporter. Any optimisation here will speed up the 
		mesh export process.
		"""

		mesh = OpenMaya.MFnMesh( self.dagPath )
		itMeshPolygon = OpenMaya.MItMeshPolygon( self.dagPath, self.component )
		
		# cache the points
		meshPoints = OpenMaya.MPointArray()
		mesh.getPoints( meshPoints, OpenMaya.MSpace.kObject )
		
		#cache normals for each vtx
		meshNormals = OpenMaya.MFloatVectorArray()
		# normals are per-vertex per-face
		# use MtMeshPolygon.normalIndex() for index
		mesh.getNormals( meshNormals )
		
		#cache the UVs
		UVSets = []
		# Get UV sets for this mesh
		mesh.getUVSetNames( UVSets )
		
		# Get all UVs for the first set
		u = OpenMaya.MFloatArray()
		v = OpenMaya.MFloatArray()
		mesh.getUVs( u, v, UVSets[0] )
		
		# reset vertex count
		self.count = 0
		
		# Setup 'proxy' and pointer
		numTrianglesPx = OpenMaya.MScriptUtil()
		numTrianglesPx.createFromInt(0)
		numTrianglesPtr = numTrianglesPx.asIntPtr()
		
		uvIndexPx = OpenMaya.MScriptUtil()
		uvIndexPx.createFromInt(0)
		uvIndexPtr = uvIndexPx.asIntPtr()
		
		# get the indices for the tris in the mesh
		while not itMeshPolygon.isDone():
			if not itMeshPolygon.hasValidTriangulation():
				OpenMaya.MGlobal.displayWarning( "Mesh %s has invalid triangulation, skipping" % self.dagPath.fullPathName() )
				continue
			
			itMeshPolygon.numTriangles(numTrianglesPtr)
			# get real int value back from pointer
			numTriangles = OpenMaya.MScriptUtil(numTrianglesPtr).asInt()
			while numTriangles!=0:
				numTriangles -= 1
			
				#get object relative indices for verts in this face
				polygonVertices = OpenMaya.MIntArray()
				itMeshPolygon.getVertices( polygonVertices )
				
				nonTweaked = OpenMaya.MPointArray()
				 
				# obj-relative vert indices for each tri
				triangleVertices = OpenMaya.MIntArray()
				 
				# face-relative vert indices for each tri
				localIndex = OpenMaya.MIntArray
				
				itMeshPolygon.getTriangle( numTriangles, nonTweaked, triangleVertices, OpenMaya.MSpace.kObject )
				
				localIndex = self.GetLocalIndex( polygonVertices, triangleVertices )
				
				numVerts = triangleVertices.length()
				
				for i in range(0, numVerts):
					self.points.append( meshPoints[ triangleVertices[i] ].x )
					self.points.append( meshPoints[ triangleVertices[i] ].y )
					self.points.append( meshPoints[ triangleVertices[i] ].z )
				
					self.normals.append( meshNormals[ itMeshPolygon.normalIndex( localIndex[i] ) ].x )
					self.normals.append( meshNormals[ itMeshPolygon.normalIndex( localIndex[i] ) ].y )
					self.normals.append( meshNormals[ itMeshPolygon.normalIndex( localIndex[i] ) ].z )
					
					if self.hasUVs:
						try:
							itMeshPolygon.getUVIndex( localIndex[i], uvIndexPtr, UVSets[0] )
							uvIndex = OpenMaya.MScriptUtil(uvIndexPtr).asInt()
							
							self.uvs.append( u[uvIndex] )
							self.uvs.append( v[uvIndex] )
						except:
							OpenMaya.MGlobal.displayWarning('Mesh %s has no UV set' % self.dagPath.fullPathName() )
							self.hasUVs = False
							continue
	
	
				self.count += numVerts
			# end while

			itMeshPolygon.next()
		#end while
	#end def getOutput

	def GetLocalIndex(self, getVertices, getTriangle):
		"""
		To quote the C++ source:
			// MItMeshPolygon::getTriangle() returns object-relative vertex
			// indices; BUT MItMeshPolygon::normalIndex() and ::getNormal() need
			// face-relative vertex indices! This converts vertex indices from
			// object-relative to face-relative.
		"""
		
		localIndex = []
		
		for gt in range(0, getTriangle.length()):
			for gv in range(0, getVertices.length()):
				if getTriangle[gt] == getVertices[gv]:
					localIndex.append( gv )
					break
					
			if len(localIndex) == gt:
				localIndex.append( -1 )
				
		return localIndex
	#end def GetLocalIndex