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
    normArray = {}
    uvArray = {}
    objectIndex = {}
    indArray = {}
    
    fShape = OpenMaya.MFnMesh()
    fPolygonSets = OpenMaya.MObjectArray()
    fPolygonComponents = OpenMaya.MObjectArray()
    
    UVSets = []
    
    allNormals = OpenMaya.MFloatVectorArray()

    def __init__(self, fileHandles, dagPath):
        self.dagPath = dagPath
        
        self.meshHandle, self.portalsHandle = fileHandles
        
        if dagPath.fullPathName().lower().find('portal') != -1:
            self.fileHandle = self.portalsHandle
            self.portalsMode = True
        else:
            self.fileHandle = self.meshHandle
            self.portalsMode = False
        
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
            self.normArray = {}
            self.uvArray = {}
            self.objectIndex = {}
            self.indArray = {}
            
            #---- start mesh iteration
            
            itMeshVerts = OpenMaya.MItMeshVertex(self.dagPath, self.fPolygonComponents[iSet])
            
            self.fShape.getNormals(self.allNormals)
            
            #uPt = OpenMaya.MScriptUtil().asFloatPtr()
            #vPt = OpenMaya.MScriptUtil().asFloatPtr()
            
            i=0
            while not itMeshVerts.isDone():
                cInd = itMeshVerts.index()
                vP = itMeshVerts.position()    
                self.vertArray[i] = vP
                
            #    uv = [uPt, vPt] #OpenMaya.MFloatArray(2, 0)
            #    itMeshVerts.getUV(uv, UVSets[0])
            #    uvArray[i] = [OpenMaya.MScriptUtil(uPt).asFloat(), OpenMaya.MScriptUtil(vPt).asFloat()]
                
            #    vN = OpenMaya.MVector()
            #    itMeshVerts.getNormal(vN)
            #    normArray[i] = vN
                
                self.objectIndex[cInd] = i
                i+=1
                itMeshVerts.next()
            
            itMeshPolys = OpenMaya.MItMeshPolygon(self.dagPath, self.fPolygonComponents[iSet])
            
            numTrianglesPx = OpenMaya.MScriptUtil()
            numTrianglesPx.createFromInt(0)
            numTrianglesPtr = numTrianglesPx.asIntPtr()
            
            j=0
            while not itMeshPolys.isDone():
                
                itMeshPolys.numTriangles(numTrianglesPtr)
                numTriangles = OpenMaya.MScriptUtil(numTrianglesPtr).asInt()
                while numTriangles!=0:
                    numTriangles -= 1
                    
                    nonTweaked = OpenMaya.MPointArray()
                    pVerts = OpenMaya.MIntArray()
                    
                    itMeshPolys.getTriangle( numTriangles, nonTweaked, pVerts, OpenMaya.MSpace.kObject )
                    
                    indCol = []
                    for pVert in pVerts:
                        indCol.append(self.objectIndex[pVert])
                    self.indArray[j] = indCol
                    j+=1
                    
                itMeshPolys.next()
            
            # ------ mesh iteration done, do output.

            self.addToOutput( '# Polygon Shape %s (set %i)' % (self.dagPath.fullPathName(), iSet) )
            self.addToOutput( 'AttributeBegin' )
            self.addToOutput( self.translationMatrix(self.dagPath) )
            
            # detect Material or AreaLight
            if not self.portalsMode:
                self.shadingGroup = self.findShadingGroup(self.instanceNum, iSet)
                self.addToOutput( self.findSurfaceShader( shadingGroup = self.shadingGroup ) )
                
                subPlug1 = self.fShape.findPlug('useMaxSubdivisions')
                useLoopSubdiv = subPlug1.asBool()
                if useLoopSubdiv:
                    subPlug2 = self.fShape.findPlug('maxSubd')
                    nlevels = subPlug2.asInt()
                    self.addToOutput( 'Shape "loopsubdiv"' )
                    self.addToOutput( '\t"integer nlevels" [%i]' % nlevels )
                    self.addToOutput( self.findDisplacementShader( self.shadingGroup ) )
                else:                
                    self.addToOutput( 'Shape "trianglemesh"' )
            else:
                self.addToOutput( 'PortalShape "trianglemesh"' )
                
            self.addToOutput( '\t"integer indices" [' )
            for k in self.indArray:
                self.addToOutput( '%i %i %i' % (self.indArray[k][0], self.indArray[k][1], self.indArray[k][2]) )
            self.addToOutput( '\t]' )
            
            self.addToOutput( '\t"point P" [' )
            for vP in self.vertArray:
                self.addToOutput( '%f %f %f' % (self.vertArray[vP].x, self.vertArray[vP].y, self.vertArray[vP].z) )
            self.addToOutput( '\t]' )
            
            # trianglemesh needs UV and Normals
            # loopsubdiv needs UV
            # portalshape needs Normals
            
#            self.addToOutput( '\t"normal N" [' )
#            self.addToOutput( '\t\t' + self.polygonSet.getNormals() )
#            # \t\t normal vectors float[3] on one line
#            self.addToOutput( '\t]' )
#            
#            if self.polygonSet.hasUVs and not self.portalsMode:
#                self.addToOutput( '\t"float uv" [' )
#                self.addToOutput( '\t\t' + self.polygonSet.getUVs() )
#                # \t\t vertex uv coords float[2] on one line
#                self.addToOutput( '\t]' )
                
            self.addToOutput( 'AttributeEnd' )
            self.addToOutput( '' )
            
            self.fileHandle.flush()

            #-------- debug output

            #print "VERTEX UVS"
            #for vUV in uvArray:
            #    print '%f %f' % (uvArray[vUV][0], uvArray[vUV][1])
            #
            #print "VERTEX NORMALS"
            #for vN in normArray:
            #    print '%f %f %f' % (normArray[vN].x, normArray[vN].y, normArray[vN].z)
            
