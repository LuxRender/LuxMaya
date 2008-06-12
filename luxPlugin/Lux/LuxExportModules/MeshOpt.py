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

    vertArray = {}
    uCoords = []
    vCoords = []
    vNormals = []
    objectIndex = {}
    indArray = []
    
    fShape = OpenMaya.MFnMesh()
    fPolygonSets = OpenMaya.MObjectArray()
    fPolygonComponents = OpenMaya.MObjectArray()
    
    UVSets = []
    
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
        self.fShape.getUVSetNames( self.UVSets )
        
        for iSet in range(0, 1): #self.setCount):
            # reset lists
            self.vertArray = {}
            self.uCoords = []
            self.vCoords = []
            self.vNormals = []
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
                    self.addToOutput( 'Shape "loopsubdiv"' )
                    self.addToOutput( '\t"integer nlevels" [%i]' % nlevels )
                    self.addToOutput( self.findDisplacementShader( self.shadingGroup ) )
                else:                
                    self.addToOutput( 'Shape "trianglemesh"' )
            else:
                self.mode = 'trianglemesh'
                self.addToOutput( 'PortalShape "trianglemesh"' )
            
            
            #---- start mesh iteration
            
            itMeshVerts = OpenMaya.MItMeshVertex(self.dagPath, self.fPolygonComponents[iSet])

            i=0
            while not itMeshVerts.isDone():
                cInd = itMeshVerts.index()
                vP = itMeshVerts.position()    
                self.vertArray[i] = vP
                
                self.objectIndex[cInd] = i
                i+=1
                itMeshVerts.next()

            self.uCoords = [0] * i
            self.vCoords = [0] * i
            self.vNormals = [0] * i

            numTrianglesPx = OpenMaya.MScriptUtil()
            numTrianglesPx.createFromInt(0)
            numTrianglesPtr = numTrianglesPx.asIntPtr()
            
            itMeshPolys = OpenMaya.MItMeshPolygon(self.dagPath, self.fPolygonComponents[iSet])
            while not itMeshPolys.isDone():
                
                itMeshPolys.numTriangles(numTrianglesPtr)
                numTriangles = OpenMaya.MScriptUtil(numTrianglesPtr).asInt()
                for currentTriangle in range(0, numTriangles):
                    
                    nonTweaked = OpenMaya.MPointArray()
                    pVerts = OpenMaya.MIntArray()
                    
                    itMeshPolys.getTriangle( currentTriangle, nonTweaked, pVerts, OpenMaya.MSpace.kObject )
                    
                    uArray = OpenMaya.MFloatArray()
                    vArray = OpenMaya.MFloatArray()
                    itMeshPolys.getUVs(uArray, vArray, self.UVSets[0])
                    
                    polyNormals = OpenMaya.MVectorArray()
                    itMeshPolys.getNormals(polyNormals, OpenMaya.MSpace.kObject)
                    
                    j=0
                    for pVert in pVerts:
                        self.indArray.append(self.objectIndex[pVert])
                        self.uCoords[self.objectIndex[pVert]] = uArray[j]
                        self.vCoords[self.objectIndex[pVert]] = vArray[j]
                        self.vNormals[self.objectIndex[pVert]] = polyNormals[j]
                        j+=1
                        
                itMeshPolys.next()
            
            # ------ mesh iteration done, do output.

            self.addToOutput( '\t"integer indices" [' )
            self.addToOutput( '\t\t' + ' '.join(map(str,self.indArray)) )
            self.addToOutput( '\t]' )
            
            self.addToOutput( '\t"point P" [' )
            for vP in self.vertArray:
                self.addToOutput( '\t\t%f %f %f' % (self.vertArray[vP].x, self.vertArray[vP].y, self.vertArray[vP].z) )
            self.addToOutput( '\t]' )
            
            # add UVs for trianglemesh and loopsubdiv, but not for portals
            if self.type == 'geom':
                self.addToOutput( '\t"float uv" [' )
                for uv in zip(self.uCoords, self.vCoords):
                    self.addToOutput( '\t\t%f %f' % uv )
                self.addToOutput( '\t]' )
            
            # Add normals to trianglemesh
            if self.mode == 'trianglemesh':
                self.addToOutput( '\t"normal N" [' )
                for normal in self.vNormals:
                    self.addToOutput( '\t\t%f %f %f' % (normal.x, normal.y, normal.z) )
                self.addToOutput( '\t]' )

            self.addToOutput( 'AttributeEnd' )
            self.addToOutput( '' )
            
            self.fileHandle.flush()
