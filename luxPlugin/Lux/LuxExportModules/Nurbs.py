# ------------------------------------------------------------------------------
# Lux exporter python script plugin for Maya
#
# by Doug Hammond 02/2008
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# NURBS geometry export module
#
# ------------------------------------------------------------------------------

from maya import OpenMaya

from ExportModule import ExportModule

class Nurbs(ExportModule):
    """
    NURBS object export module.
    """
    
    fShape = OpenMaya.MFnNurbsSurface()
    
    def __init__(self, fileHandles, dagPath):
        """
        Constructor, initialise various data
        """
        self.dagPath = dagPath
        
        self.nurbsHandle, self.portalsHandle = fileHandles
        
        if dagPath.fullPathName().lower().find('portal') != -1:
            self.fileHandle = self.portalsHandle
            self.portalsMode = True
        else:
            self.fileHandle = self.nurbsHandle
            self.portalsMode = False

        
        self.fShape = OpenMaya.MFnNurbsSurface( dagPath )
    
    def getOutput(self):
        """
        Get the lux syntax for the current NURBS object.
        """
        
        self.addToOutput( '# NURBS Shape ' + self.dagPath.fullPathName() )
        self.addToOutput( 'AttributeBegin' )
        self.addToOutput( self.translationMatrix(self.dagPath) )
        
        if not self.portalsMode:
            # detect Material or AreaLight
            self.addToOutput( self.findShader() )
            self.addToOutput( 'Shape "nurbs"' )
        else:
            self.addToOutput( 'PortalShape "nurbs"' )
        
        # U and V are REVERSED for nu, nv, uknots, vknots.
        # THIS IS NOT A BUG
        
        self.addToOutput( '\t"integer nv" [%i]' % self.fShape.numCVsInU() )
        self.addToOutput( '\t"integer nu" [%i]' % self.fShape.numCVsInV() )
        
        self.addToOutput( '\t"integer uorder" [%i]' % (self.fShape.degreeU()+1) )
        self.addToOutput( '\t"integer vorder" [%i]' % (self.fShape.degreeV()+1) )
        
        self.addToOutput( '\t"float vknots" [' )
        
        
        # not sure what all this logic is about - it seems to make the
        # module work, but is it causing any problems ?
        if abs(self.fShape.knotInU(0) - self.fShape.knotInU(1)) < 0.01:
            self.addToOutput( '\t\t' + str(self.fShape.knotInU(0) ) )
        else:
            self.addToOutput( '\t\t' + str(self.fShape.knotInU(0)-1 ) )
        
        for i in range(0, self.fShape.numKnotsInU()):
            self.addToOutput( '\t\t' + str(self.fShape.knotInU(i)) )
        
        if abs(self.fShape.knotInU(0) - self.fShape.knotInU(1)) < 0.01:
            self.addToOutput( '\t\t' + str( self.fShape.knotInU( self.fShape.numKnotsInU()-1 ) ) )
        else:
            self.addToOutput( '\t\t' + str( self.fShape.knotInU( self.fShape.numKnotsInU()-1 )+1 ) )
            
        self.addToOutput( '\t]' )
        
        self.addToOutput( '\t"float uknots" [' )
        
        if abs(self.fShape.knotInV(0) - self.fShape.knotInV(1)) < 0.01:
            self.addToOutput( '\t\t' + str(self.fShape.knotInV(0) ) )
        else:
            self.addToOutput( '\t\t' + str(self.fShape.knotInV(0)-1 ) )
        
        for i in range(0, self.fShape.numKnotsInV()):
            self.addToOutput( '\t\t' + str(self.fShape.knotInV(i)) )
        
        if abs(self.fShape.knotInV(0) - self.fShape.knotInV(1)) < 0.01:
            self.addToOutput( '\t\t' + str( self.fShape.knotInV( self.fShape.numKnotsInV()-1 ) ) )
        else:
            self.addToOutput( '\t\t' + str( self.fShape.knotInV( self.fShape.numKnotsInV()-1 )+1 ) )
            
        self.addToOutput( '\t]' )
        
        cvPoints = OpenMaya.MPointArray()
        self.fShape.getCVs(cvPoints, OpenMaya.MSpace.kObject)
        self.addToOutput( '\t"point P" [' )
        for i in range(0, cvPoints.length()):
            self.addToOutput( '\t\t' + str(cvPoints[i].x) + ' ' + str(cvPoints[i].y) + ' ' + str(cvPoints[i].z) ) #+ ' ' + str(cvPoints[i].w) )
        self.addToOutput( '\t]' )
        
        # u0 u1 v0 v1 are optional. not sure what Maya equivs are
        
        self.addToOutput( 'AttributeEnd' )
        self.addToOutput( '' )
        
        self.fileHandle.flush()
