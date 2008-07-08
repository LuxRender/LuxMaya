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
from luxexport    import consoleProgress 

class luxbatch(OpenMayaMPx.MPxCommand):
    """
    Class to create a render batch script
    """

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
        
        self.startFrame = round( cmds.currentTime( query = True ) )
        
        if doAnimation:
            self.startFrame  = round( cmds.getAttr( 'defaultRenderGlobals.startFrame'  ) ) 
            self.endFrame    = round( cmds.getAttr( 'defaultRenderGlobals.endFrame'    ) )
            self.stepFrame   = round( cmds.getAttr( 'defaultRenderGlobals.byFrameStep' ) )
        else:
            self.endFrame = self.startFrame
        
        self.initProgressWindow()
        
        if doInSequence:
            self.startSequence()
        else:
            self.startBatch()
    
    def initProgressWindow(self):
        self.MayaGUIMode = OpenMaya.MGlobal.mayaState() == OpenMaya.MGlobal.kInteractive
        
        if self.MayaGUIMode:
            self.mProgress = OpenMayaUI.MProgressWindow()
        else:
            self.mProgress = consoleProgress()
            
    def showProgressWindow(self):
        if self.MayaGUIMode:
            self.mProgress.reserve()
            self.mProgress.setInterruptable(True)
            self.mProgress.setProgressRange(0, int(self.endFrame-self.startFrame)+1)
            self.mProgress.setProgress(0)
            self.mProgress.startProgress()
        else:
            self.mProgress.tProgress = int(self.endFrame-self.startFrame)+1
    
    def startSequence(self):
        """
        Start the sequential export process.
        1. for each frame to export, export it to a temp folder
        2. render it
        3. loop
        """
        
        self.showProgressWindow()
        
        if self.startFrame == self.endFrame:
            self.runProcess( self.exportFile(self.startFrame) )
            self.mProgress.advanceProgress(1)
        else:
            # frame range export
            ct = cmds.currentTime( query = True )
            for f in range(int(self.startFrame), int(self.endFrame)+1, int(self.stepFrame)): 
                self.mProgress.setTitle( 'Frames %i - %i: %i' % (int(self.startFrame), int(self.endFrame), f) )
                cmds.currentTime( f )
                self.runProcess( self.exportFile(f, tempExportPath = True) )
                self.mProgress.advanceProgress(1)
                if self.mProgress.isCancelled(): break
            
            cmds.currentTime( ct )
        
        OpenMaya.MGlobal.displayInfo( 'Lux Export Successful' )
        self.mProgress.endProgress()
    
    def startBatch(self):
        """
        Start the batch export process.
        1. For each frame to export, export it
        2. Append exported scene filename to fileList
        3. pass fileList to makeBatchFile()
        """
        
        fileList = []
        
        self.showProgressWindow()
        
        if self.startFrame == self.endFrame:
            # single frame export
            fileList.append( self.exportFile(self.startFrame) )
            self.mProgress.advanceProgress(1)
        else:
            # frame range export
            ct = cmds.currentTime( query = True )
            for f in range(int(self.startFrame), int(self.endFrame)+1, int(self.stepFrame)): 
                self.mProgress.setTitle( 'Frames %i - %i: %i' % (int(self.startFrame), int(self.endFrame), f) )
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
    
    def getNetworkServers(self):
        networking = cmds.getAttr( 'lux_settings.render_network' )
        serversList = cmds.getAttr( 'lux_settings.render_network_servers')
        
        if networking and serversList != None and len(serversList.strip()) > 0:
            serversList = serversList.strip().split(';')
            for item in serversList:
                if len(item.strip()) == 0: serversList.remove(item)
                
            if len(serversList) > 0:
                servers = str()
                for server in serversList:
                    servers += '-u %s ' % server

                networkinterval = cmds.getAttr( 'lux_settings.render_network_interval' )                
                servers += '-i %i ' % networkinterval
            
                return servers
            else:
                return ''
        else:
            return ''
    
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
        threads = cmds.getAttr( 'lux_settings.render_threads' )
        priority = cmds.getAttr( 'lux_settings.render_priority', asString = True )
        
        servers = self.getNetworkServers()
                
        # scale 0...5 to -9...6 - keeping normal at 0
        niceValue = (cmds.getAttr( 'lux_settings.render_priority' ) - 3) * 3
        
        if guiMode:
            luxPath += 'luxrender'
        else:
            luxPath += 'luxconsole'

        if os.name == 'nt':
            luxPath += '.exe'
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
                    ccmd = '%s %s -t %i %s"%s"' % ( cmdPrefix, luxPath, threads, servers, file )
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
                    fh.write( ('nice -n %i %s -t %i %s"%s"' % (niceValue, luxPath, threads, servers, file)) + os.linesep )
                fh.close()
            except:
                OpenMaya.MGlobal.displayError( 'Could not write render batch file' )
                raise
        
        if cmds.getAttr( 'lux_settings.render_launch' ) == 1:
            try:
                if os.name == 'nt':
                    # windows
                    #os.spawnv(os.P_NOWAIT, batchFileName, [batchFileName] )
                    os.system('start cmd /c "%s"' % batchFileName)
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
        
        servers = self.getNetworkServers()
        
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
                
                ccmd = '%s %s -t %i %s"%s"' % ( cmdPrefix, luxPath, threads, servers, sceneFile )
                os.system( ccmd )
                
            except:
                OpenMaya.MGlobal.displayError( 'Could not start lux' )
                raise
        else:
            try:
                cmdPrefix = 'nice -n %i %s -t %i %s"%s"' % (niceValue, luxPath, threads, servers, sceneFile)
                if guiMode:
                    ccmd = '(xterm -T "Lux Render" -e %s)' & cmdPrefix
                else:
                    ccmd = '(%s)' % cmdPrefix
                    
                os.system( ccmd )
            except:
                OpenMaya.MGlobal.displayError( 'Could not start lux' )
                raise
    