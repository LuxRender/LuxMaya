# ------------------------------------------------------------------------------
# Lux exporter python script plugin for Maya
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# trianglemesh/loopsubdiv geometry export module (optimised version)
#
# ------------------------------------------------------------------------------

import time, os
from maya import OpenMaya

from ExportModule import ExportModule

class MeshOpt(ExportModule):
    """
    Polygon mesh ExportModule (Optimised)
    """

    doBenchmark = False

    fShape = OpenMaya.MFnMesh()
    fPolygonSets = OpenMaya.MObjectArray()
    fPolygonComponents = OpenMaya.MObjectArray()
    
    UVSets = []
    currentUVSet = 0
    
    vertNormUVList = []
    vertIndexList = []
    vertPointList = []
    vertNormList = []
    vertUVList = []
    
    fileHandle = int()
    
    # used to determine appropriate UV and Normals output
    mode = 'trianglemesh' # or loopsubdiv
    type = 'geom' # or portal

    def __init__(self, fileHandles, dagPath):
        self.dagPath = dagPath
        self.fShape = OpenMaya.MFnMesh( dagPath )
        
        meshHandle, portalsHandle = fileHandles
        
        if dagPath.fullPathName().lower().find('portal') != -1:
            self.fileHandle = portalsHandle
            self.type = 'portal'
        else:
            self.fileHandle = meshHandle
            self.type = 'geom'
        
        dagPath.extendToShape()

        self.instanceNum = 0
        if dagPath.isInstanced():
            self.instanceNum = dagPath.instanceNumber()
        
        self.fShape.getConnectedSetsAndMembers(self.instanceNum, self.fPolygonSets, self.fPolygonComponents, True)
        
        shaderArray = OpenMaya.MObjectArray()
        polyShaderIdx = OpenMaya.MIntArray()
        
        try:
            # try to establish nimber of mesh sets through shader conections,
            self.fShape.getConnectedShaders(self.instanceNum, shaderArray, polyShaderIdx)
            self.setCount = shaderArray.length()
        except:
            # skip all sets in this mesh if no shaders assigned
            self.setCount = 0
            
        if self.fShape.numUVSets() > 0:
            # Get UV sets for this mesh
            self.fShape.getUVSetNames( self.UVSets )
        
           
    def resetLists(self):
        # reset lists
        self.vertNormUVList = []
        self.vertIndexList = []
        self.vertPointList = []
        self.vertNormList = []
        self.vertUVList = []

    def getOutput(self):
        
        # get all object verts
        meshPoints = OpenMaya.MPointArray()
        self.fShape.getPoints(meshPoints)
        
        # get all object normals
        meshNormals = OpenMaya.MFloatVectorArray()
        self.fShape.getNormals(meshNormals)
        
        # get all object UVs, if any
        if self.fShape.numUVSets() > 0:
            meshUArray = OpenMaya.MFloatArray()
            meshVArray = OpenMaya.MFloatArray()
            self.fShape.getUVs(meshUArray, meshVArray, self.UVSets[self.currentUVSet])
        
        # set up some scripting junk
        numTrianglesPx = OpenMaya.MScriptUtil()
        numTrianglesPx.createFromInt(0)
        numTrianglesPtr = numTrianglesPx.asIntPtr()
        uvIdxPx = OpenMaya.MScriptUtil()
        uvIdxPx.createFromInt(0)
        uvIdxPtr = uvIdxPx.asIntPtr()
        
        # each set/shader on this object
        for iSet in range(0, self.setCount):
            
            # start afresh for this set
            self.resetLists()
            
            # start shape syntax
            self.addToOutput( '# Polygon Shape %s (set %i)' % (self.dagPath.fullPathName(), iSet) )
            self.addToOutput( 'AttributeBegin' )
            self.addToOutput( self.translationMatrix(self.dagPath) )
            
            # set syntax for trianglemesh/loopsubdiv or portalshape
            if self.type == 'geom':
                # detect Material or AreaLight
                self.shadingGroup = self.findShadingGroup(self.instanceNum, iSet)
                self.addToOutput( self.findSurfaceShader( shadingGroup = self.shadingGroup ) )
                
                # detect trianglemesh/loopsubdiv
                subPlug1 = self.fShape.findPlug('useMaxSubdivisions')
                useLoopSubdiv = subPlug1.asBool()
                if useLoopSubdiv:
                    self.mode = 'loopsubdiv'
                    subPlug2 = self.fShape.findPlug('maxSubd')
                    nlevels = subPlug2.asInt()
                    self.addToOutput( '\tShape "loopsubdiv"' )
                    self.addToOutput( '\t\t"integer nlevels" [%i]' % nlevels )
                    # find displacement, if any
                    self.addToOutput( self.findDisplacementShader( self.shadingGroup ) )
                else:
                    self.mode = 'trianglemesh'                
                    self.addToOutput( '\tShape "trianglemesh"' )
            else:
                self.addToOutput( '\tPortalShape "trianglemesh"' )
            
            # start mesh face iteration            
            itMeshPolys = OpenMaya.MItMeshPolygon(self.dagPath, self.fPolygonComponents[iSet])
            
            # storage for obj-relative vert indices in a face
            polygonVertices = OpenMaya.MIntArray()
            
            # storage for the face vert points
            vertPoints = OpenMaya.MPointArray()
                        
            # storage for the face vert indices
            vertIndices = OpenMaya.MIntArray()
            
            startTime = time.clock()
            
            # each face
            while not itMeshPolys.isDone():
                
                # get nuber of triangles in face
                itMeshPolys.numTriangles(numTrianglesPtr)
                numTriangles = OpenMaya.MScriptUtil(numTrianglesPtr).asInt()

                #get object relative indices for verts in this face
                itMeshPolys.getVertices( polygonVertices )

                # each triangle in each face
                for currentTriangle in range(0, numTriangles):

                    # get the triangle points and indices
                    itMeshPolys.getTriangle( currentTriangle, vertPoints, vertIndices, OpenMaya.MSpace.kObject )
                    
                    # get a list of local indices
                    localIndex = self.GetLocalIndex( polygonVertices, vertIndices )
                    
                    # each vert in this triangle
                    #for vertIndex, i in zip( vertIndices, range(0, vertIndices.length()) ):
                    for i in range(0, vertIndices.length()):
                        
                        # get indices to points/normals/uvs
                        vertIndex = vertIndices[i]
                        vertNormalIndex = itMeshPolys.normalIndex( localIndex[i] )
                        
                        if itMeshPolys.hasUVs():
                            itMeshPolys.getUVIndex( localIndex[i], uvIdxPtr, self.UVSets[self.currentUVSet] )
                            vertUVIndex = OpenMaya.MScriptUtil( uvIdxPtr ).asInt()
                        else:
                            vertUVIndex = 0
                        
                        # if we've not seen this combo yet,
                        #if not (vertIndex, vertNormalIndex, vertUVIndex) in self.vertNormUVList:
                        testVal = (vertIndex, vertNormalIndex, vertUVIndex) 
                        if not testVal in self.vertNormUVList:
                            # add it to the lists
                            self.vertPointList.append( meshPoints[vertIndex] )
                            self.vertNormList.append( meshNormals[vertNormalIndex] )
                            if itMeshPolys.hasUVs():
                                self.vertUVList.append( ( meshUArray[vertUVIndex], meshVArray[vertUVIndex] ) )
                            
                            # and keep track of what we've seen
                            self.vertNormUVList.append( testVal )
                            # and use the most recent idx value
                            useVertIndex = len(self.vertNormUVList) - 1
                        else:
                            useVertIndex = self.vertNormUVList.index( testVal )
                        
                        # use the appropriate vert index
                        self.vertIndexList.append( useVertIndex )
                        
                itMeshPolys.next()
                
            procTime = time.clock()
            procDuration = procTime - startTime
            
            
            # mesh iteration done, do output.

            self.addToOutput( '\t"integer indices" [' )
            self.addToOutput( '\t\t' + ' '.join(map(str,self.vertIndexList)) )
            self.addToOutput( '\t]' )
            
            self.fileHandle.flush()
            
            self.addToOutput( '\t"point P" [' )
            for vP in self.vertPointList:
                self.addToOutput( '\t\t%f %f %f' % (vP.x, vP.y, vP.z) )
            self.addToOutput( '\t]' )
            
            self.fileHandle.flush()
            
            # add UVs for trianglemesh and loopsubdiv, but not for portals and only if the shape has uvs
            if self.type == 'geom' and len(self.vertUVList) > 0:
                self.addToOutput( '\t"float uv" [' )
                for uv in self.vertUVList:
                    self.addToOutput( '\t\t%f %f' % uv )
                self.addToOutput( '\t]' )
            
            self.fileHandle.flush()
            
            # Add normals to trianglemesh
            if self.mode == 'trianglemesh':
                self.addToOutput( '\t"normal N" [' )
                for vN in self.vertNormList:
                    self.addToOutput( '\t\t%f %f %f' % (vN.x, vN.y, vN.z) )
                self.addToOutput( '\t]' )

            self.addToOutput( 'AttributeEnd' )
            self.addToOutput( '' )
            
            self.fileHandle.flush()
            
            outTime = time.clock()
            writeDuration = outTime - procTime
            
            
            if self.doBenchmark:
                vLen = len(self.vertNormUVList)
                pSpeed = vLen/procDuration
                wSpeed = vLen/writeDuration
                print "%i verts processed in %f seconds: %f verts/sec" % (vLen, procDuration, pSpeed)
                print " -> written in %f seconds: %f verts/sec" % (writeDuration, wSpeed)
                
                sf = open("e:\meshopt_stats.csv", "a")
                sf.write ( ( '%i,%f,%f' % (vLen, pSpeed, wSpeed) ) + os.linesep )
                sf.close()
            
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
