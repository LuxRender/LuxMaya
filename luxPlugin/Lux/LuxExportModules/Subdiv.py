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
# subdiv object exporter
#
# ------------------------------------------------------------------------------

import time, os
from maya import OpenMaya

from ExportModule import ExportModule

class Subdiv(ExportModule):
    
    dagPath = OpenMaya.MDagPath()
    fShape  = OpenMaya.MFnSubd()
    
    def __init__(self, fileHandles, dagPath):
        
        self.subdivHandle, self.portalsHandle = fileHandles
        
        self.fileHandle = self.subdivHandle
        
        self.fShape = OpenMaya.MFnSubd(dagPath)
        self.dagPath = dagPath
        
        
    def resetLists(self):
        self.vertArray = {}
        self.localIndex = {}
        self.indArray = {}
        self.normArray = {}
        self.i=0
        self.j=0
        
    def getOutput(self):
        
        self.resetLists()
    
        THEHIGHESTLEVEL = self.fShape.levelMaxCurrent()
    
        for THELEVEL in range(THEHIGHESTLEVEL, 0, -1):
            
            #THELEVEL = 1

            itSV = OpenMaya.MItSubdVertex(self.dagPath.node())
            itSV.setLevel( THELEVEL )
            
            while not itSV.isDone():
                cInd = itSV.index()

                if self.fShape.vertexIsValid(cInd):
                    vP = OpenMaya.MPoint()
                    self.fShape.vertexPositionGet(cInd, vP)
                    self.vertArray[self.i] = vP
                    
                    vN = OpenMaya.MVector()
                    self.fShape.vertexNormal(cInd, vN)
                    self.normArray[self.i] = vN
                    
                    self.localIndex[cInd] = self.i
                    self.i+=1
                itSV.next()
            
            itSF = OpenMaya.MItSubdFace(self.dagPath.node())
            itSF.setLevel( THELEVEL )
            
            while not itSF.isDone():
                fInd = itSF.index()
                
                if not self.fShape.polygonHasChildren(fInd):
                    pVerts = OpenMaya.MUint64Array()
                    self.fShape.polygonVertices(fInd, pVerts)
                    indCol = []
                    for pVert in pVerts:
                        indCol.append(self.localIndex[pVert])
                    self.indArray[self.j] = indCol
                self.j+=1
                itSF.next()
                    
           
        self.addToOutput( '# Subdiv Shape %s' % self.dagPath.fullPathName() )
        self.addToOutput( 'AttributeBegin' )
        self.addToOutput( self.translationMatrix(self.dagPath) )
        self.addToOutput( 'Shape "trianglemesh"' )
        
        #print "FACE VERTEX INDICES"
        self.addToOutput( '\t"integer indices" [' )
        for k in self.indArray:
            self.addToOutput( '%i %i %i' % (self.indArray[k][0], self.indArray[k][1], self.indArray[k][2]) )
            self.addToOutput( '%i %i %i ' % (self.indArray[k][0], self.indArray[k][2], self.indArray[k][3]) )
        self.addToOutput( '\t]' )
        
        
        self.addToOutput( '\t"point P" [' )
        for vP in self.vertArray:
            self.addToOutput( '%f %f %f ' % (self.vertArray[vP].x, self.vertArray[vP].y, self.vertArray[vP].z) )
        self.addToOutput( '\t]' )
        
        self.addToOutput( '\t"normal N" [' )
        for vN in self.normArray:
            self.addToOutput( '%f %f %f ' % (self.normArray[vN].x, self.normArray[vN].y, self.normArray[vN].z) )
        self.addToOutput( '\t]' )
        
        self.addToOutput( 'AttributeEnd' )
        self.addToOutput( '' )
        
        self.fileHandle.flush()