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
# luxbatch: a command to render a set of lux renders (sequential, or network)
#
# ------------------------------------------------------------------------------

import os
os.altsep = '/'

from maya import cmds
from maya import OpenMaya
from maya import OpenMayaMPx
from maya import OpenMayaUI

from luxexport    import luxexport

class luxbatch(OpenMayaMPx.MPxCommand):
    """
    Class to create a render batch script
    """
    
    mProgress = OpenMayaUI.MProgressWindow()
    
    @staticmethod
    def commandName():
        return "lux_export"
    
    @staticmethod
    def commandCreator():
        return OpenMayaMPx.asMPxPtr( luxbatch() )
    
    def doIt(self, args = OpenMaya.MArgList() ):
        """
        Class entry point.
        1. Detect if lux_settings exists
        2. Detect if exporting an animation
        3. Determine start and end frame to export, and pass control to startBatch()
        """
        
        if not cmds.objExists('lux_settings'):
            OpenMaya.MGlobal.displayWarning('No Lux settings found for this scene, opening GUI...')
            from lux_gui import lux_gui
            lg = lux_gui()
            lg.doIt(OpenMaya.MArgList())
            return
        
        # here we go
        doAnimation  = cmds.getAttr( 'lux_settings.render_animation' )
        doInSequence = cmds.getAttr( 'lux_settings.render_animation_sequence' )
        
        startFrame = round( cmds.currentTime( query = True ) )
        
        if doAnimation:
            startFrame = round( cmds.playbackOptions( query = True, animationStartTime = True ) ) 
            endFrame =   round( cmds.playbackOptions( query = True, animationEndTime = True   ) )
        else:
            endFrame = startFrame
        
        if doInSequence:
            self.startSequence(startFrame, endFrame)
        else:
            self.startBatch(startFrame, endFrame)
    
    def startSequence(self, startFrame, endFrame):
        """
        Start the sequential export process.
        1. for each frame to export, export it to a temp folder
        2. render it
        3. loop
        """
        
        self.mProgress.reserve()
        self.mProgress.setInterruptable(True)
        self.mProgress.setProgressRange(0, int(endFrame-startFrame)+1)
        self.mProgress.setProgress(0)
        self.mProgress.startProgress()
        
        if startFrame == endFrame:
            self.runProcess( self.exportFile(startFrame) )
            self.mProgress.advanceProgress(1)
        else:
            # frame range export
            ct = cmds.currentTime( query = True )
            for f in range(int(startFrame), int(endFrame)+1): 
                self.mProgress.setTitle( 'Frames %i - %i: %i' % (int(startFrame), int(endFrame), f) )
                cmds.currentTime( f )
                self.runProcess( self.exportFile(f, tempExportPath = True) )
                self.mProgress.advanceProgress(1)
                if self.mProgress.isCancelled(): break
            
            cmds.currentTime( ct )
        
        OpenMaya.MGlobal.displayInfo( 'Lux Export Successful' )
        self.mProgress.endProgress()
    
    def startBatch(self, startFrame, endFrame):
        """
        Start the batch export process.
        1. For each frame to export, export it
        2. Append exported scene filename to fileList
        3. pass fileList to makeBatchFile()
        """
        
        fileList = []
        
        self.mProgress.reserve()
        self.mProgress.setInterruptable(True)
        self.mProgress.setProgressRange(0, int(endFrame-startFrame)+1)
        self.mProgress.setProgress(0)
        self.mProgress.startProgress()
        

        if startFrame == endFrame:
            # single frame export
            fileList.append( self.exportFile(startFrame) )
            self.mProgress.advanceProgress(1)
        else:
            # frame range export
            ct = cmds.currentTime( query = True )
            for f in range(int(startFrame), int(endFrame)+1): 
                self.mProgress.setTitle( 'Frames %i - %i: %i' % (int(startFrame), int(endFrame), f) )
                cmds.currentTime( f )
                fileList.append( self.exportFile(f) )
                self.mProgress.advanceProgress(1)
                if self.mProgress.isCancelled(): break
            
            cmds.currentTime( ct )
        
        self.makeBatchFile(fileList)
        OpenMaya.MGlobal.displayInfo( 'Lux Export Successful' )
        self.mProgress.endProgress()
            
    
    def exportFile(self, frameNumber = 1, tempExportPath = False):
        """
        Export a single frame, and return the name of the created scene file
        """

        render_cam = ''
        
        for cam in cmds.listCameras():
            renderable = cmds.getAttr( '%s.renderable' % cam )
            if renderable == 1:
                render_cam = cam
                break
            
        if render_cam == '':
            OpenMaya.MGlobal.displayError('No renderable camera in scene')

        
        saveFolder = cmds.getAttr( 'lux_settings.scene_path' )
        if not os.path.exists(saveFolder):
            os.mkdir( saveFolder )
            
        sceneFileBaseName = cmds.getAttr( 'lux_settings.scene_filename' ) + ('.%06i' % frameNumber)
            
        renderFolder = saveFolder + os.altsep + "renders" + os.altsep
        if not os.path.exists(renderFolder):
            os.mkdir(renderFolder)
            
        imageSaveName = renderFolder + sceneFileBaseName
        
        if tempExportPath:
            saveFolder += ('tmp') + os.altsep
            if not os.path.exists(saveFolder):
                os.mkdir( saveFolder )
            else:
                for file in os.listdir(saveFolder):
                    os.remove(saveFolder+file)
                os.rmdir( saveFolder )
                os.mkdir( saveFolder )
        else:
            saveFolder += ('%06i' % frameNumber) + os.altsep
            if not os.path.exists(saveFolder):
                os.mkdir( saveFolder )
                
        sceneFileName = saveFolder + sceneFileBaseName + '.lxs'
        
        renderWidth = cmds.getAttr( 'defaultResolution.width' )
        renderHeight = cmds.getAttr( 'defaultResolution.height' )
        
        # launch export proc here !
        le = luxexport()
        leArgs = OpenMaya.MArgList()
        leArgs.addArg( sceneFileName )
        leArgs.addArg( imageSaveName )
        leArgs.addArg( renderWidth )
        leArgs.addArg( renderHeight )
        leArgs.addArg( render_cam )
        
        try:
            le.doIt( leArgs )
        except:
            self.mProgress.endProgress()
            raise

        return sceneFileName
    
    def makeBatchFile(self, fileList):
        """
        Make batch render file, detecting appropriate type for the host OS.
        1. Add all given file names in fileList to the batch script
        2. Launch the script if told to. 
        """
        
        saveFolder = cmds.getAttr( 'lux_settings.scene_path' )
        sceneFileBaseName = cmds.getAttr( 'lux_settings.scene_filename' )
        
        batchFileName = saveFolder + sceneFileBaseName + '_render'
        
        luxPath = cmds.getAttr( 'lux_settings.lux_path' ) + os.altsep
        
        guiMode = cmds.getAttr( 'lux_settings.render_interface', asString = True ) == 'GUI'
        if guiMode:
            luxPath += 'luxrender'
        else:
            luxPath += 'luxconsole'
            
        if os.name == 'nt':
            luxPath += '.exe'
            
        threads = cmds.getAttr( 'lux_settings.render_threads' )
        
        priority = cmds.getAttr( 'lux_settings.render_priority', asString = True )
        
        # scale 0...5 to -9...6 - keeping normal at 0
        niceValue = (cmds.getAttr( 'lux_settings.render_priority' ) - 3) * 3
        
        if os.name == 'nt':
            # windows batch file
            batchFileName += '.bat'
            try:
                fh = open( batchFileName, 'wb')
                fh.write( ':: Lux batch render file generated by LuxMaya ' + cmds.date() + os.linesep )
                fh.write( '@Echo off' + os.linesep )
                
                cmdPrefix = str()
                if guiMode:
                    cmdPrefix = 'start /WAIT /%s' % priority
                else:
                    cmdPrefix = 'start /WAIT /MIN /%s' % priority
                
                for file in fileList:
                    ccmd = '%s %s -t %i "%s"' % ( cmdPrefix, luxPath, threads, file )
                    fh.write( ('echo Rendering file %s' % file) + os.linesep )
                    fh.write( ccmd + os.linesep )
                    
                fh.close()
            except:
                OpenMaya.MGlobal.displayError( 'Could not write render batch file' )
                raise
            
        else:
            #unix bash script
            batchFileName += '.sh'
            try:
                fh = open( batchFileName, 'wb')
                fh.write( '#!/bin/bash' + os.linesep)
                fh.write( '# Lux batch render file generated by LuxMaya ' + cmds.date() + os.linesep )
                for file in fileList:
                    fh.write( ('nice -n %i %s -t %i "%s"' % (niceValue, luxPath, threads, file)) + os.linesep )
                fh.close()
            except:
                OpenMaya.MGlobal.displayError( 'Could not write render batch file' )
                raise
        
        # launch process doesn't work on linux
        if cmds.getAttr( 'lux_settings.render_launch' ) == 1:
            try:
                if os.name == 'nt':
                    # windows
                    os.spawnv(os.P_NOWAIT, batchFileName, [batchFileName] )
                else:
                    # assuming linux, this probably won't work on OSX
                    os.system('(xterm -T "Lux Render" -e %s)&' % batchFileName)
            except:
                OpenMaya.MGlobal.displayError( "Failed to launch process\n" )
                raise
            
            
    def runProcess(self, sceneFile):
        self.mProgress.setProgressStatus( 'Rendering' )

        luxPath = cmds.getAttr( 'lux_settings.lux_path' ) + os.altsep
        guiMode = cmds.getAttr( 'lux_settings.render_interface', asString = True ) == 'GUI'
        threads = cmds.getAttr( 'lux_settings.render_threads' )
        priority = cmds.getAttr( 'lux_settings.render_priority', asString = True )
        # scale 0...5 to -9...6 - keeping normal at 0
        niceValue = (cmds.getAttr( 'lux_settings.render_priority' ) - 3) * 3
        
        if guiMode:
            luxPath += 'luxrender'
        else:
            luxPath += 'luxconsole'
            
        if os.name == 'nt':
            luxPath += '.exe'
            
        if os.name == 'nt':
            # windows batch file
            try:
                cmdPrefix = str()
                if guiMode:
                    cmdPrefix = 'start /WAIT /%s' % priority
                else:
                    cmdPrefix = 'start /WAIT /MIN /%s' % priority
                
                ccmd = '%s %s -t %i "%s"' % ( cmdPrefix, luxPath, threads, sceneFile )
                os.system( ccmd )
                
            except:
                OpenMaya.MGlobal.displayError( 'Could not start lux' )
                raise
    