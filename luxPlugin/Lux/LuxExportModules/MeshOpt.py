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

from maya import OpenMaya

from ExportModule import ExportModule

class MeshOpt(ExportModule):
    """
    Polygon mesh ExportModule (Optimised)
    """

    vertArray = []
#    uCoords = []
#    vCoords = []
#    vNormals = []
    objectIndex = {}
    indArray = []
    
    fShape = OpenMaya.MFnMesh()
    fPolygonSets = OpenMaya.MObjectArray()
    fPolygonComponents = OpenMaya.MObjectArray()
    
#    UVSets = []
    
    # used to determine appropriate UV and Normals output
    mode = 'trianglemesh' # or loopsubdiv
    type = 'geom' # or portal

    def __init__(self, fileHandles, dagPath):
        self.dagPath = dagPath
        
        self.meshHandle, self.portalsHandle = fileHandles
        
        if dagPath.fullPathName().lower().find('portal') != -1:
            self.fileHandle = self.portalsHandle
            self.type = 'portal'
        else:
            self.fileHandle = self.meshHandle
            self.type = 'geom'
        
        self.fShape = OpenMaya.MFnMesh( dagPath )

        dagPath.extendToShape()

        self.instanceNum = 0
        if dagPath.isInstanced():
            self.instanceNum = dagPath.instanceNumber()
        
        self.fShape.getConnectedSetsAndMembers(self.instanceNum, self.fPolygonSets, self.fPolygonComponents, True)
        
        self.setCount = self.fPolygonSets.length()
        
        if self.setCount > 1:
            self.setCount -= 1

    def getOutput(self):
        
        # Get UV sets for this mesh
#        self.fShape.getUVSetNames( self.UVSets )
        
        for iSet in range(0, 1): #self.setCount):
            # reset lists
            self.vertArray = []
#            self.uCoords = []
#            self.vCoords = []
#            self.vNormals = []
            self.objectIndex = {}
            self.indArray = []
            
            self.addToOutput( '# Polygon Shape %s (set %i)' % (self.dagPath.fullPathName(), iSet) )
            self.addToOutput( 'AttributeBegin' )
            self.addToOutput( self.translationMatrix(self.dagPath) )
            
            
            # detect Material or AreaLight
            if self.type == 'geom':
                self.shadingGroup = self.findShadingGroup(self.instanceNum, iSet)
                self.addToOutput( self.findSurfaceShader( shadingGroup = self.shadingGroup ) )
                
                subPlug1 = self.fShape.findPlug('useMaxSubdivisions')
                useLoopSubdiv = subPlug1.asBool()
                if useLoopSubdiv:
                    self.mode = 'loopsubdiv'
                    subPlug2 = self.fShape.findPlug('maxSubd')
                    nlevels = subPlug2.asInt()
                    self.addToOutput( '\tShape "loopsubdiv"' )
                    self.addToOutput( '\t\t"integer nlevels" [%i]' % nlevels )
                    self.addToOutput( self.findDisplacementShader( self.shadingGroup ) )
                else:
                    self.mode = 'trianglemesh'                
                    self.addToOutput( '\tShape "trianglemesh"' )
            else:
                self.addToOutput( '\tPortalShape "trianglemesh"' )
            
            
            #---- start mesh iteration
            
            itMeshVerts = OpenMaya.MItMeshVertex(self.dagPath, self.fPolygonComponents[iSet])
            
#            meshNormals = OpenMaya.MFloatVectorArray()
#            self.fShape.getNormals( meshNormals )

            objectVertCount = 0
            while not itMeshVerts.isDone():
                
                self.vertArray.append( itMeshVerts.position() )
                
#                normalIndices = OpenMaya.MIntArray()
#                itMeshVerts.getNormalIndices(normalIndices)
                
                cInd = itMeshVerts.index()
                
#                for normalIndex in normalIndices:
#                self.vNormals.append( meshNormals[ normalIndex ] )
                #self.objectIndex[cInd, normalIndex] = objectVertCount
                self.objectIndex[cInd] = objectVertCount
                objectVertCount+=1
                    
                itMeshVerts.next()

            # this is a nice list
            # (objVertID, normalID): luxVertID

#            {
#            
#            (0, 0): 1,
#            (0, 21): 0,
#            (0, 15): 2,
#            
#            (1, 1): 4,
#            (1, 16): 5,
#            (1, 14): 3,
#            
#            (2, 3): 7,
#            (2, 4): 6,
#            (2, 22): 8,
#            
#            (3, 2): 10,
#            (3, 5): 11,
#            (3, 19): 9,
#            
#            (4, 23): 14,
#            (4, 7): 13,
#            (4, 8): 12,
#            
#            (5, 6): 16,
#            (5, 9): 17,
#            (5, 18): 15,
#            
#            (6, 11): 19,
#            (6, 12): 18,
#            (6, 20): 20,
#            
#            (7, 10): 22,
#            (7, 13): 23,
#            (7, 17): 21
#            
#            
#            }


#            self.uCoords = [0] * objectVertCount
#            self.vCoords = [0] * objectVertCount

            numTrianglesPx = OpenMaya.MScriptUtil()
            numTrianglesPx.createFromInt(0)
            numTrianglesPtr = numTrianglesPx.asIntPtr()
            
            itMeshPolys = OpenMaya.MItMeshPolygon(self.dagPath, self.fPolygonComponents[iSet])
            # each face
            while not itMeshPolys.isDone():
                
                itMeshPolys.numTriangles(numTrianglesPtr)
                numTriangles = OpenMaya.MScriptUtil(numTrianglesPtr).asInt()
                
                # each triangle in each face
                for currentTriangle in range(0, numTriangles):
                    
                    nonTweaked = OpenMaya.MPointArray()
                    pVerts = OpenMaya.MIntArray()
                    
                    itMeshPolys.getTriangle( currentTriangle, nonTweaked, pVerts, OpenMaya.MSpace.kObject )
                    
#                    uArray = OpenMaya.MFloatArray()
#                    vArray = OpenMaya.MFloatArray()
#                    itMeshPolys.getUVs(uArray, vArray, self.UVSets[0])
                    
#                    polyNormalIds = OpenMaya.MIntArray()
#                    itMeshPolys.getFaceNormalIds(polyNormalIds)
                    
                    for pVert, localVertIndex in zip( pVerts, range(0, uArray.length()) ):
                        
#                        normalIndex = polyNormalIds(localVertIndex)
#                        print '(%i, %i)' % (pVert, normalIndex)
                        
                        objVertIndex = self.objectIndex[pVert] #, normalIndex]
                        
                        self.indArray.append(objVertIndex)
#                        self.uCoords[objVertIndex] = uArray[localVertIndex]
#                        self.vCoords[objVertIndex] = vArray[localVertIndex]
                        
                itMeshPolys.next()
            
            # ------ mesh iteration done, do output.

            self.addToOutput( '\t"integer indices" [' )
            self.addToOutput( '\t\t' + ' '.join(map(str,self.indArray)) )
            self.addToOutput( '\t]' )
            
            self.addToOutput( '\t"point P" [' )
            for vP in self.vertArray:
                self.addToOutput( '\t\t%f %f %f' % (vP.x, vP.y, vP.z) )
            self.addToOutput( '\t]' )
            
            # add UVs for trianglemesh and loopsubdiv, but not for portals
#            if self.type == 'geom':
#                self.addToOutput( '\t"float uv" [' )
#                for uv in zip(self.uCoords, self.vCoords):
#                    self.addToOutput( '\t\t%f %f' % uv )
#                self.addToOutput( '\t]' )
            
            # Add normals to trianglemesh
#            if self.mode == 'trianglemesh':
#                self.addToOutput( '\t"normal N" [' )
#                for vN in self.vNormals:
#                    self.addToOutput( '\t\t%f %f %f' % (vN.x, vN.y, vN.z) )
#                self.addToOutput( '\t]' )

            self.addToOutput( 'AttributeEnd' )
            self.addToOutput( '' )
            
            self.fileHandle.flush()
