# TODO: turn this into a proper ExportModule

#This file won't work with either the UVs or Normals bits enabled.

# Error: No matching function for overloaded 'MItMeshVertex_getUV'
# Traceback (most recent call last):
#   File "<maya console>", line 52, in ?
#   File "C:\engserv\rbuild\164\build\wrk\optim\runTime\Python\Lib\site-packages\maya\OpenMaya.py", line 7310, in getUV
# NotImplementedError: No matching function for overloaded 'MItMeshVertex_getUV' # 

# For fucks sake.
# TODO: there must be another way

from maya import OpenMaya
it = OpenMaya.MItDag( OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kMesh)
tdp = OpenMaya.MDagPath()
# print it.isDone()
# Result: False # 
it.getPath(tdp)
fSD = OpenMaya.MFnMesh(tdp)

i=0
vertArray = {}
normArray = {}
uvArray = {}
localIndex = {}
j=0
indArray = {}


fPolygonSets = OpenMaya.MObjectArray()
fPolygonComponents = OpenMaya.MObjectArray()

tdp.extendToShape()

instanceNum = 0
if tdp.isInstanced():
    instanceNum = tdp.instanceNumber()

fSD.getConnectedSetsAndMembers(instanceNum, fPolygonSets, fPolygonComponents, True)

setCount = fPolygonSets.length()
if setCount > 1:
    setCount -= 1


#UVSets = []
## Get UV sets for this mesh
#fSD.getUVSetNames( UVSets )

itSV = OpenMaya.MItMeshVertex(tdp.node())

#allNormals = OpenMaya.MFloatVectorArray()
#fSD.getNormals(allNormals)

#uPt = OpenMaya.MScriptUtil().asFloatPtr()
#vPt = OpenMaya.MScriptUtil().asFloatPtr()

while not itSV.isDone():
    cInd = itSV.index()
    vP = itSV.position()    
    vertArray[i] = vP
    
#    uv = [uPt, vPt] #OpenMaya.MFloatArray(2, 0)
#    itSV.getUV(uv, UVSets[0])
#    uvArray[i] = [OpenMaya.MScriptUtil(uPt).asFloat(), OpenMaya.MScriptUtil(vPt).asFloat()]
    
#    vN = OpenMaya.MVector()
#    itSV.getNormal(vN)
#    normArray[i] = vN
    
    localIndex[cInd] = i
    i+=1
    itSV.next()


itSF = OpenMaya.MItMeshPolygon(tdp.node())

numTrianglesPx = OpenMaya.MScriptUtil()
numTrianglesPx.createFromInt(0)
numTrianglesPtr = numTrianglesPx.asIntPtr()

while not itSF.isDone():
    
    itSF.numTriangles(numTrianglesPtr)
    numTriangles = OpenMaya.MScriptUtil(numTrianglesPtr).asInt()
    while numTriangles!=0:
        numTriangles -= 1
        
        
        nonTweaked = OpenMaya.MPointArray()
        pVerts = OpenMaya.MIntArray()
        
        itSF.getTriangle( numTriangles, nonTweaked, pVerts, OpenMaya.MSpace.kObject )
        
        
        indCol = []
        for pVert in pVerts:
            indCol.append(localIndex[pVert])
        indArray[j] = indCol
        j+=1
        
    itSF.next()
            
        
print "VERTEX POINTS"
for vP in vertArray:
    print '%f %f %f' % (vertArray[vP].x, vertArray[vP].y, vertArray[vP].z)

#print "VERTEX UVS"
#for vUV in uvArray:
#    print '%f %f' % (uvArray[vUV][0], uvArray[vUV][1])
#
#print "VERTEX NORMALS"
#for vN in normArray:
#    print '%f %f %f' % (normArray[vN].x, normArray[vN].y, normArray[vN].z)

print "FACE VERTEX INDICES"
for k in indArray:
    print '%i %i %i' % (indArray[k][0], indArray[k][1], indArray[k][2])
