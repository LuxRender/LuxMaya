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
# Fluid volume -> volumegrid export module
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaFX

from ExportModule import ExportModule

class Volume(ExportModule):
    """
    Fluid volume export module
    """
    
    fFluid = OpenMayaFX.MFnFluid()
    
    def __init__(self, fileHandle, dagPath):
        """
        Set up the objects we're dealing with
        """
        
        self.fileHandle = fileHandle
        self.dagPath = dagPath
        
        self.fFluid = OpenMayaFX.MFnFluid( dagPath )
        
    def getOutput(self):
        """
        Read Fluid data and export as volumegrid
        """
    
        xPtr = OpenMaya.MScriptUtil().asDoublePtr()
        yPtr = OpenMaya.MScriptUtil().asDoublePtr()
        zPtr = OpenMaya.MScriptUtil().asDoublePtr()
        self.fFluid.getDimensions( xPtr, yPtr, zPtr )
        dimX = OpenMaya.MScriptUtil( xPtr ).asDouble() / 2
        dimY = OpenMaya.MScriptUtil( yPtr ).asDouble() / 2
        dimZ = OpenMaya.MScriptUtil( zPtr ).asDouble() / 2
        
        #xrPtr = OpenMaya.MScriptUtil().asIntPtr()
        #yrPtr = OpenMaya.MScriptUtil().asIntPtr()
        #zrPtr = OpenMaya.MScriptUtil().asIntPtr()
        #self.fFluid.getResolution( xrPtr, yrPtr, zrPtr )
        #xres = OpenMaya.MScriptUtil( xrPtr ).asInt()
        #yres = OpenMaya.MScriptUtil( yrPtr ).asInt()
        #zres = OpenMaya.MScriptUtil( zrPtr ).asInt()
        
        # getResolution is NOT IMPLEMENTED !!! ??!
        
        # therefore, assume equal res in every direction
        xres = yres = zres = round(self.fFluid.gridSize()**0.333333333333)
        
        self.addToOutput( 'AttributeBegin' )
        self.addToOutput( self.translationMatrix(self.dagPath) )
        
        self.addToOutput( '\tVolume "volumegrid"' )
        self.addToOutput( '\t\t"color sigma_a" [0.9 0.9 0.9]' )
        self.addToOutput( '\t\t"point p0" [%f %f %f]' % (-dimX, -dimY, -dimZ) )
        self.addToOutput( '\t\t"point p1" [%f %f %f]' % ( dimX,  dimY,  dimZ) )
        
        self.addToOutput( '\t\t"integer nx" [%i]' % xres )
        self.addToOutput( '\t\t"integer ny" [%i]' % yres )
        self.addToOutput( '\t\t"integer nz" [%i]' % zres )
        
        self.addToOutput( '\t\t"float density" [' )

        outStr = str()
        for i in range(0, self.fFluid.gridSize()):
            outStr += '%f ' % OpenMaya.MScriptUtil.getFloatArrayItem( self.fFluid.density(), i)
        
        self.addToOutput( '\t\t\t%s' % outStr )
        self.addToOutput( '\t\t]' )
    
        self.addToOutput( 'AttributeEnd' )
        self.addToOutput( '' )