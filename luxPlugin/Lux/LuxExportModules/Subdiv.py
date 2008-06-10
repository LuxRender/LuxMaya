# TODO: turn this into a proper ExportModule
# TODO: overcome problems relating to single/combined Level output
# TODO: implement creasing

from maya import OpenMaya
it = OpenMaya.MItDag( OpenMaya.MItDag.kDepthFirst, OpenMaya.MFn.kSubdiv)
tdp = OpenMaya.MDagPath()
# print it.isDone()
# Result: False # 
it.getPath(tdp)
fSD = OpenMaya.MFnSubd(tdp)

THEHIGHESTLEVEL = fSD.levelMaxCurrent()

i=0
j=0
vertArray = {}
localIndex = {}
indArray = {}

#for THELEVEL in range(fSD.levelMaxCurrent(), 0, -1):
    
THELEVEL = 1

itSV = OpenMaya.MItSubdVertex(tdp.node())
itSV.setLevel( THELEVEL )

while not itSV.isDone():
    cInd = itSV.index()
    #cIncEdg = OpenMaya.MUint64Array()
    #fSD.vertexIncidentEdges(cInd, cIncEdg)
    #if cIncEdg.length() > 0:
    vP = OpenMaya.MPoint()
    fSD.vertexPositionGet(cInd, vP)
    vertArray[i] = vP
    localIndex[cInd] = i
    i+=1
    itSV.next()

itSF = OpenMaya.MItSubdFace(tdp.node())
itSF.setLevel( THELEVEL )

while not itSF.isDone():
    fInd = itSF.index()
    
    if not fSD.polygonHasChildren(fInd):
        pVerts = OpenMaya.MUint64Array()
        fSD.polygonVertices(fInd, pVerts)
        indCol = []
        for pVert in pVerts:
            indCol.append(localIndex[pVert])
        indArray[j] = indCol
    j+=1
    itSF.next()
            
        
print "VERTEX POINTS"
#outStr = str()
for vP in vertArray:
    print '%f %f %f ' % (vertArray[vP].x, vertArray[vP].y, vertArray[vP].z)
#print outStr

print "FACE VERTEX INDICES"
#outStr = str()
for k in indArray:
    print '%i %i %i' % (indArray[k][0], indArray[k][1], indArray[k][2])
    print '%i %i %i ' % (indArray[k][0], indArray[k][2], indArray[k][3])
#print outStr
