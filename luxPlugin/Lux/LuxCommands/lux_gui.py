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
# GUI builder command
#
# ------------------------------------------------------------------------------

import os
os.altsep = '/'
from maya import OpenMaya
from maya import OpenMayaMPx
from maya import cmds
from maya import mel

from Lux.LuxMiscModules.fn_attr import fn_attr

from lux_settings import lux_settings
from luxbatch     import luxbatch

class mMenu:
    """
    GUI helper class to construct window menus.
    """
    
    mName = str()
    def __init__(self, label, helpMenu = False, parent = False, tearOff = False ):
        """
        Start a new menu with the gIven options.
        """
        
        if parent == False:
            self.mName = cmds.menu( label = label, helpMenu = helpMenu, tearOff = tearOff )
        else:
            self.mName = cmds.menu( label = label, helpMenu = helpMenu, tearOff = tearOff, parent = parent )
    
    def getName(self):
        """
        Return the name of the created menu object
        """
        
        return self.mName
        
    def addItem(self, label, command, subMenu = False, divider = False, parent = False):
        """
        Add an item (or submenu) to this menu object.
        """
        
        if parent == False:
            return cmds.menuItem( label = label, command = command, parent = self.mName, divider = divider, subMenu = subMenu)
        else:
            return cmds.menuItem( label = label, command = command, divider = divider, subMenu = subMenu, parent = parent)
        
    def end(self):
        """
        End this menu object. No more items can be added.
        """
        
        cmds.setParent( '..', menu = True)
        
class mOptionMenu(mMenu):
    """
    GUI helper class to construct optionMenus
    """
    
    data = 0
    def __init__(self, parent, changeCommand = ''):
        """
        Start a new optionMenu
        """
        
        if changeCommand == '':
            self.mName = cmds.optionMenu( height = 24, parent = parent )
        else:
            self.mName = cmds.optionMenu( height = 24, parent = parent, changeCommand = changeCommand)
        
    def addItem(self, label):
        """
        Add an item to this optionMenu
        """
        
        itemName = cmds.menuItem( label = label, data = self.data, parent = self.mName)
        self.data += 1

class lux_gui(OpenMayaMPx.MPxCommand):
    """
    The Lux Exporter GUI Main class. This is huge, and could possibly be split up.
    """
    
    VERSION = '0.6.0'
    
    lux_GUI_height = 550       # Maya adds 20px to this
    lux_GUI_width  = 360       # this is the width of a column.
    lux_GUI_thirdWidth = 120
    lux_GUI_2thirdWidth = 240
    lux_GUI_scrollbar_width = 0 # no scrollbars anymore
    
    @staticmethod
    def commandName():
        return "lux_gui"
    
    @staticmethod
    def commandCreator():
        return OpenMayaMPx.asMPxPtr( lux_gui() )
    
#    def __init__(self):
#        pass
    
    def makeMainMenu(self):
        """
        Make the main Lux menu which resides in the Rendering menuSet
        """
        
        gMainWindow = mel.eval('$tmpVar=$gMainWindow')
        
        luxMenu = mMenu(label = 'Lux', parent = gMainWindow, tearOff = True )
        luxMenu.addItem( label = 'Show GUI', command = self.doIt )
        luxMenu.addItem( label = "Export" , command = self.goBatch )
        luxMenu.addItem( label = '', command = '', divider = True )
        luxCreateMenu = luxMenu.addItem( label = "Create", command = '', subMenu = True )
        luxMenu.addItem( label = 'PLY Object Locator', command = self.mnuObjectLocator, parent = luxCreateMenu )
        luxMenu.addItem( label = 'Environment Light', command = self.mnuEnvLight, parent = luxCreateMenu )
        luxMenu.addItem( label = 'Sun + Sky', command = self.mnuSunsky, parent = luxCreateMenu )
        luxMenu.end()
        
        renderMS = mel.eval('findMenuSetFromLabel("Rendering")')
        cmds.menuSet( currentMenuSet = renderMS )
        menuIndex  = cmds.menuSet( query = True, numberOfMenus = True)
        cmds.menuSet( insertMenu = (luxMenu.getName(), menuIndex) )
        luxMenu.end()
        
    # GUI Hierarchy construction methods
    
    def newFrame(self, label, parent = False, collapsable = False, collapsed = False):
        """
        Start a new frameLayout (and transparently add a columnLayout)
        """
        
        if parent == False:
            theFrame = cmds.frameLayout( label = label,
                                         collapsable = collapsable,
                                         collapse = collapsed,
                                         labelAlign = "top",
                                         borderStyle = "etchedOut" )
        else:
            theFrame = cmds.frameLayout( parent = parent,
                                         label = label,
                                         collapsable = collapsable,
                                         collapse = collapsed,
                                         labelAlign = "top",
                                         borderStyle = "etchedOut" )
        
        # LEVEL 3
        return cmds.columnLayout( rowSpacing = 3,
                                  columnAttach = ("both", 2),
                                  columnWidth = self.lux_GUI_width,
                                  parent = theFrame ), theFrame
    
    def endFrame(self):
        """
        End the frameLayout (and the transparent columnLayout)
        """
        
        cmds.setParent( '..', upLevel = True )
        cmds.setParent( '..', upLevel = True )
        
    def newRow(self, parent, numberOfColumns = 2, w1 = 0, w2 = 0):
        """
        Start a new rowLayout
        """
        
        if w1 == 0: w1 = self.lux_GUI_thirdWidth
        if w2 == 0: w2 = self.lux_GUI_2thirdWidth
        if numberOfColumns == 2:
            return cmds.rowLayout( numberOfColumns = numberOfColumns,
                                   columnWidth2 = (w1, w2),
                                   parent = parent )
        else:
            return cmds.rowLayout( numberOfColumns = numberOfColumns,
                                   columnWidth1 = self.lux_GUI_2thirdWidth,
                                   parent = parent )
    
    def endRow(self):
        """
        End a rowLayout
        """
        
        cmds.setParent( '..', upLevel = True )
    
    def newText(self, label, parent, addColon = True, width = False):
        """
        Insert a text control (ie, print text on the GUI)
        """
        
        if addColon:
            lString = '%s:'
        else:
            lString = '%s'
        
        if not width == False:
            cmds.text( label = lString % label,
                       parent = parent,
                       width = width )
        else:
            cmds.text( label = lString % label,
                       parent = parent )
    
    def startLevel(self):
        """
        Start a GUI sub-level (adds padding around controls)
        """
        
        return cmds.columnLayout( rowSpacing = 3,
                                  columnAttach = ("left", 4) )
    
    def endLevel(self):
        """
        End a GUI sub-level
        """
        
        self.endRow()
    
    def addTextField(self, parent ):
        """
        Add an editble text field to the GUI
        """
        
        return  cmds.textField( width = self.lux_GUI_2thirdWidth,
                                parent = parent )
    
    def addCheckBox(self, parent, label = '', value = False):
        """
        Add a labelled checkbox to the GUI 
        """
        
        return cmds.checkBox( parent = parent,
                              label = label,
                              value = value,
                              height = 12)
                              
    def addIntField(self, parent, min, max, value):
        """
        Add an integer input field to the GUI (not yet implemented)
        """
        
        pass
    
    def addFloatField(self, parent, min, max, value, changeCommand = False):
        """
        Add a float input field to the GUI
        """
        
        if not changeCommand:
            return cmds.floatField( parent = parent, min = min, max = max, value = value )
        else:
            return cmds.floatField( parent = parent, min = min, max = max, value = value, changeCommand = changeCommand )
        
    def makeTabs(self, inputDict):
        """
        Make a tabLayout set from the given dict of { controlGroup: 'tab label' }
        """
        
        tForm = cmds.formLayout()
        tTabs = cmds.tabLayout( parent = tForm, innerMarginWidth = 3, innerMarginHeight = 3 )
        cmds.formLayout( tForm, edit = True,  attachForm=((tTabs, 'top', 0), (tTabs, 'left', 0), (tTabs, 'bottom', 0), (tTabs, 'right', 0)) )
        
        tabLabels = []
        for controlGrp in inputDict:
            cGrp = controlGrp( parent = tTabs )
            tabLabels.append( (cGrp, inputDict[controlGrp]) )
        
        cmds.tabLayout( tTabs, edit = True, tabLabel = tabLabels )
        
    def doIt(self, args = OpenMaya.MArgList() ):
        """
        Start constructing the GUI, starting with the window itself, and then
        all child control groups.
        """
        
        # Check for script node and create/upgrade as necessary
        ls = lux_settings()
        ls.doIt(OpenMaya.MArgList())
        
        # Check for existing window and remove it
        if cmds.window('luxGuiMain', exists=True):
            cmds.deleteUI('luxGuiMain', window=True)
        
        if OpenMaya.MGlobal.mayaState() != OpenMaya.MGlobal.kInteractive:
            OpenMaya.MGlobal.displayInfo('LuxMaya: Running in console, not building GUI')
            return
        
        # Create a DB handler object
        from Lux.LuxMiscModules.lrmdb import lrmdb
        self.lrmdb = lrmdb()
        
        # Create window
        cmds.window('luxGuiMain', title="Lux Render Exporter",
                                  height = self.lux_GUI_height,
                                  width = ((self.lux_GUI_width) + self.lux_GUI_scrollbar_width),
                                  sizeable = True,
                                  resizeToFitChildren = True,
                                  menuBar = True,
                                  minimizeButton = True)
        
        self.makeGUIMenus()
        
        self.makeTabs({
                        self.fileFrame: 'Scene',
                        self.processFrame: 'Process',
                        self.filmFrame: 'Film',
                        self.cameraFrame: 'Camera',
                        self.renderFrame: 'Renderer',
                        self.databaseFrame: 'Database'
                     })
        self.endRow() # end the tabs
        
        # finally, show the window!
        cmds.showWindow( 'luxGuiMain' )
    
    def makeGUIMenus(self):
        """
        Make the menus on the GUI window
        """
        
        # Create menus
        fileMenu = mMenu( label = "File" )
        fileMenu.addItem( label = 'Export', command = self.goBatch )
        fileMenu.addItem( label = '', command = '', divider = True )
        fileMenu.addItem( label = "Close", command = self.mnuClose )
        fileMenu.end()
        
        createMenu = mMenu( label = 'Create' )
        createMenu.addItem( label = 'PLY Object Locator' , command = self.mnuObjectLocator )
        createMenu.addItem( label = 'Environment Light', command = self.mnuEnvLight )
        createMenu.addItem( label = 'Sun + Sky', command = self.mnuSunsky )
        createMenu.end()
        
        settingsMenu = mMenu( label = 'Settings' )
        settingsMenu.addItem( label = "Maya Preferences",  command = self.mnuPrefs )
        settingsMenu.addItem( label = "Show Lux settings", command = self.mnuLuxSettings )
        settingsMenu.addItem( label = '', command = '', divider = True )
        settingsMenu.addItem( label = "Restore default paths", command = lux_settings.setScriptNodeDefaultPaths )
        settingsMenu.addItem( label = '', command = '', divider = True )
        
        settingsRSMenu = settingsMenu.addItem( label = 'Render Presets', command = '', subMenu = True )
        presetList = fn_attr.findAttrPresets( 'lux_settings' )
        presetList.sort()
        for preset in presetList:
            if preset[0:4] == "lux_":
                niceName = preset.replace('lux_','')
                niceName = niceName.replace('_',' ')
                niceName = niceName.replace('-',' ')
                settingsMenu.addItem( label = niceName, command = "from Lux.LuxMiscModules.fn_attr import fn_attr\nfn_attr.applyAttrPreset( 'lux_settings', '%s', 100)" % preset, parent = settingsRSMenu)
        
        settingsCSMenu = settingsMenu.addItem( label = 'Colourspace Presets', command = '', subMenu = True )
        for preset in presetList:
            if preset[0:3] == "cs_":
                niceName = preset.replace('cs_','')
                niceName = niceName.replace('_',' ')
                #niceName = niceName.replace('-',' ')
                settingsMenu.addItem( label = niceName, command = "from Lux.LuxMiscModules.fn_attr import fn_attr\nfn_attr.applyAttrPreset( 'lux_settings', '%s', 100)" % preset, parent = settingsCSMenu)
        
        settingsWPMenu = settingsMenu.addItem( label = 'Whitepoint Presets', command = '', subMenu = True )
        for preset in presetList:
            if preset[0:3] == "wp_":
                niceName = preset.replace('wp_','')
                niceName = niceName.replace('_',' ')
                #niceName = niceName.replace('-',' ')
                settingsMenu.addItem( label = niceName, command = "from Lux.LuxMiscModules.fn_attr import fn_attr\nfn_attr.applyAttrPreset( 'lux_settings', '%s', 100)" % preset, parent = settingsWPMenu)
        
        settingsMenu.end()
        
        dbMenu = mMenu( label = 'Database' )
        dbMenu.addItem( label = 'TEST', command = self.mnuDbTEST )
        dbMenu.end()
        
        helpMenu = mMenu( label = 'Help', helpMenu = True )
        helpMenu.addItem( label = 'LuxRender website', command = self.mnuHelpWebsite )
        helpMenu.addItem( label = 'Documentation Wiki', command = self.mnuHelpWiki )
        helpMenu.addItem( label = 'Development Forum', command = self.mnuHelpDevForum )
        helpMenu.addItem( label = '', command = '', divider = True )
        helpMenu.addItem( label = 'About', command = self.mnuHelpAbout )
        helpMenu.end()
    
    # GUI Frames start here.
    # We can't indent the python code to show the GUI hierarchy, so instead
    # I'm using comment markers, like: #--
    
    def fileFrame(self, parent):
        """
        Make the frame for the 'Scene' window tab
        """
        
        #-
        # LEVEL 2 FILE PATH SETTINGS
        fileFrame, fileFrameContainer = self.newFrame( label = "Scene settings", parent = parent )
        #--
        fileRow1 = self.newRow( parent = fileFrame )
        #---
        self.newText( label = "Path to Lux", parent = fileRow1 )
        lux_file_luxpath = self.addTextField( parent = fileRow1 )
        cmds.connectControl( lux_file_luxpath, 'lux_settings.lux_path' )
        #---
        self.endRow()
        fileRow2 = self.newRow( parent = fileFrame )
        #---
        self.newText( label = "Scene export path", parent = fileRow2 )
        lux_file_scenepath = self.addTextField( parent = fileRow2 )
        cmds.connectControl( lux_file_scenepath, 'lux_settings.scene_path' )
        #---
        self.endRow()
        fileRow3 = self.newRow( parent = fileFrame )
        #---
        self.newText( label = "Scene name", parent = fileRow3 )
        lux_file_scenename = self.addTextField( parent = fileRow3 )
        cmds.connectControl( lux_file_scenename, 'lux_settings.scene_filename' )
        #---
        self.endRow()
        #--
        fileRow5 = self.newRow( parent = fileFrame )
        #---
        self.newText( label = 'Export' , parent = fileRow5 )
        fileExportRow = self.startLevel()
        #----
        matExportRow = self.newRow( parent = fileExportRow, numberOfColumns = 1)
        #-----
        lux_file_export_mats = self.addCheckBox( parent = matExportRow, label = 'Materials', value = True )
        cmds.connectControl( lux_file_export_mats, 'lux_settings.scene_export_materials' )
        #-----
        self.endRow()
        #----
        meshExportRow = self.newRow( parent = fileExportRow, numberOfColumns = 1)
        #-----
        lux_file_export_meshes = self.addCheckBox( parent = meshExportRow, label = 'Polygon Meshes', value = True )
        cmds.connectControl( lux_file_export_meshes, 'lux_settings.scene_export_meshes' )
        #-----
        self.endRow()
        #----
        nurbsExportRow = self.newRow( parent = fileExportRow, numberOfColumns = 1)
        #-----
        lux_file_export_nurbs = self.addCheckBox( parent = nurbsExportRow, label = 'NURBS Surfaces', value = False )
        cmds.connectControl( lux_file_export_nurbs, 'lux_settings.scene_export_nurbs' )
        #-----
        self.endRow()
        #----
        volsExportRow = self.newRow( parent = fileExportRow, numberOfColumns = 1)
        #-----
        lux_file_export_vols = self.addCheckBox( parent = volsExportRow, label = 'Fluid Volumes', value = False )
        cmds.connectControl( lux_file_export_vols, 'lux_settings.scene_export_volumes' )
        #-----
        self.endRow()
        #----
        self.endLevel()
        #---
        self.endRow()
        #--
        fileRow4 = self.newRow( parent = fileFrame )
        #---
        self.newText( label = 'Collect files', parent = fileRow4 )
        fileCollectRow = self.startLevel()
        #----
        texCollectRow = self.newRow( parent = fileCollectRow, numberOfColumns = 1)
        #-----
        lux_file_collect_tex = self.addCheckBox( parent = texCollectRow, label = 'Texture maps', value = False)
        cmds.connectControl( lux_file_collect_tex, 'lux_settings.scene_collect_texture' )
        #-----
        self.endRow() # texCollectRow
        #----
        bumpCollectRow = self.newRow( parent = fileCollectRow, numberOfColumns = 1)
        #-----
        lux_file_collect_bump = self.addCheckBox( parent = bumpCollectRow, label = 'Bump maps', value = False)
        cmds.connectControl( lux_file_collect_bump, 'lux_settings.scene_collect_bump' )
        #-----
        self.endRow() # bumpCollectRow
        #----
        hdriCollectRow = self.newRow( parent = fileCollectRow, numberOfColumns = 1)
        #-----
        lux_file_collect_hdri = self.addCheckBox( parent = hdriCollectRow, label = 'HDRI Enviroment maps', value = False)
        cmds.connectControl( lux_file_collect_hdri, 'lux_settings.scene_collect_hdri' )
        #-----
        self.endRow() # hdriCollectRow
        #----
        self.endLevel() # fileCollectRow
        #---
        self.endRow() # fileRow4
        #--
        
        fileRow6 = self.newRow( parent = fileFrame )
        #---
        self.newText( label = 'Animation Options', parent = fileRow6 )
        fileAnimLevel = self.startLevel()
        #----
        lux_file_anim_row1 = self.newRow( parent = fileAnimLevel, numberOfColumns = 1 )
        #-----
        lux_file_animation = self.addCheckBox( parent = lux_file_anim_row1, label = 'Export animation', value = False)
        cmds.connectControl( lux_file_animation, 'lux_settings.render_animation' )
        #-----
        self.endRow()
        #----
        lux_file_anim_row2 = self.newRow( parent = fileAnimLevel, numberOfColumns = 1 )
        #-----
        lux_file_animation_seq = self.addCheckBox( parent = lux_file_anim_row2, label = 'Export/Render in sequence', value = False)
        cmds.connectControl( lux_file_animation_seq, 'lux_settings.render_animation_sequence' )
        #-----
        self.endRow()
        #----
        self.endLevel()
        #---
        self.endRow()
        #--
        
        fileRow7 = self.newRow( parent = fileFrame )
        #---
        self.newText( label = 'Color Controls' , parent = fileRow7 )
        fileColorRow = self.startLevel()
        #----
        rgcRow = self.newRow( parent = fileColorRow, numberOfColumns = 1)
        #-----
        lux_file_rgc = self.addCheckBox( parent = rgcRow, label = 'Reverse Gamma Correction', value = True )
        cmds.connectControl( lux_file_rgc, 'lux_settings.scene_reverse_gamma' )
        #-----
        self.endRow()
        #----
        clampRow = self.newRow( parent = fileColorRow, numberOfColumns = 1)
        #-----
        lux_file_clamp = self.addCheckBox( parent = clampRow, label = 'Clamp: 0 <= c <= 0.9', value = True )
        cmds.connectControl( lux_file_clamp, 'lux_settings.scene_clamp_color' )
        #-----
        self.endRow()
        #----
        self.endLevel()
        #---
        self.endRow()
        #--
        
        # LEVEL 2 Add button and progress bar
        exportButton  = cmds.button( width = (self.lux_GUI_width),
                                      height = 30,
                                      label = "Export Scene",
                                      align = "center",
                                      command = self.goBatch )
        self.endFrame()
        #-
        
        return fileFrameContainer
    
    def processFrame(self, parent):
        """
        Make the frame for the 'Process' window tab
        """
        
        #-
        # LEVEL 2 PROCESS SETTINGS
        processFrame, processFrameContainer = self.newFrame( label = 'Process settings', parent = parent )
        #--
        process_row1 = self.newRow( parent = processFrame )
        #---
        self.newText( label = '' , parent = process_row1 )
        renderLaunchLevel = self.startLevel()
        lux_process_launch = self.addCheckBox( parent = renderLaunchLevel, label = 'Render after export' )
        cmds.connectControl( lux_process_launch, 'lux_settings.render_launch' )
        self.endLevel()
        #---
        self.endRow()
        #--
        process_row2 = self.newRow( parent = processFrame )
        #---
        self.newText( label = 'Render interface' , parent = process_row2 )
        lux_process_interface = mOptionMenu( parent = process_row2 )
        lux_process_interface.addItem( label = "GUI" )
        lux_process_interface.addItem( label = "Console" )
        lux_process_interface.end()
        cmds.connectControl( lux_process_interface.getName(), 'lux_settings.render_interface' )
        #---
        self.endRow()
        #--
        process_row3 = self.newRow( parent = processFrame )
        #---
        self.newText( label = 'Render threads' , parent = process_row3 )
        lux_render_threads = cmds.intField( parent = process_row3, min = 1, max = 64, value = 1)
        cmds.connectControl( lux_render_threads, 'lux_settings.render_threads' )
        #---
        self.endRow()
        #--
        process_row4 = self.newRow( parent = processFrame )
        #---
        self.newText( label = 'Render priority' , parent = process_row4 )
        lux_process_priority = mOptionMenu( parent = process_row4 )
        lux_process_priority.addItem( label = "Realtime" )
        lux_process_priority.addItem( label = "High" )
        lux_process_priority.addItem( label = "Above Normal" )
        lux_process_priority.addItem( label = "Normal" )
        lux_process_priority.addItem( label = "Below Normal" )
        lux_process_priority.addItem( label = "Low" )
        lux_process_priority.end()
        cmds.connectControl( lux_process_priority.getName(), 'lux_settings.render_priority' )
        #---
        self.endRow()
        #--
        self.endFrame()
        #-
        
        process_row5 = self.newRow( parent = processFrame )
        #--
        self.newText( label = '', parent = process_row5 )
        lux_render_network = self.addCheckBox( parent = process_row5, label = 'Network Render' )
        cmds.connectControl( lux_render_network, 'lux_settings.render_network' )
        #--
        self.endRow()
        #-
        
        process_row6 = self.newRow( parent = processFrame )
        #--
        self.newText( label = 'Server request interval', parent = process_row6 )
        lux_render_network_interval = cmds.intField( parent = process_row6, min = 1, value = 180 )
        cmds.connectControl( lux_render_network_interval, 'lux_settings.render_network_interval' )
        #--
        self.endRow()
        #-
        
        process_row7 = self.newRow( parent = processFrame )
        #--
        self.newText( label = 'Network servers', parent = process_row7 )
        lux_render_network_servers = self.addTextField( parent = process_row7 )
        cmds.connectControl( lux_render_network_servers, 'lux_settings.render_network_servers' )
        #--
        self.endRow()
        #-
        
        return processFrameContainer
    
    def cameraFrame(self, parent):
        """
        Make the frame for the 'Camera' window tab
        """
        
        #-
        # LEVEL 2 CAMERA SETTINGS
        cameraFrame, cameraFrameContainer = self.newFrame( label = 'Camera settings', parent = parent )
        #--
        camera_row1 = self.newRow( parent = cameraFrame )
        #---
        self.newText( label = 'Perspective camera type', parent = camera_row1 )
        lux_camera_persptype = mOptionMenu( parent = camera_row1 )
        lux_camera_persptype.addItem( label = 'Perspective' )
        lux_camera_persptype.addItem( label = 'Environment' )
        # lux_camera_persptype.addItem( label = 'Realistic' )
        lux_camera_persptype.end()
        cmds.connectControl( lux_camera_persptype.getName(), 'lux_settings.camera_persptype' )
        #---
        self.endRow()
        #--
        cameraFakeLevel = self.startLevel() # this is purely aesthetic
        camera_row2 = self.newRow( parent = cameraFakeLevel )
        #---
        self.newText( label = 'F Stop', parent = camera_row2 )
        lux_camera_fstop = self.addFloatField(parent = camera_row2, min = 1.0, max = 64.0, value = 5.6 )
        
        cams = []
        for cam in cmds.listCameras():
            cams.append( '%s.fStop' % cam )
        
        cmds.connectControl( lux_camera_fstop, (cams) )
        
        #---
        self.endRow()
        #--
        camera_row3 = self.newRow( parent = cameraFakeLevel )
        #---
        self.newText( label = 'Exposure time', parent = camera_row3 )
        lux_camera_exposure = self.addFloatField(parent = camera_row3, min = 0.0, max = 64.0, value = 1.0 )
        cmds.connectControl( lux_camera_exposure, 'lux_settings.camera_exposuretime' )
        #---
        self.endRow()
        #--
        camera_row4 = self.newRow( parent = cameraFakeLevel )
        #---
        self.newText( label = '', parent = camera_row4 )
        lux_camera_autofocus = self.addCheckBox( parent = camera_row4, label = 'Auto focus', value = False)
        cmds.connectControl( lux_camera_autofocus, 'lux_settings.camera_autofocus' )
        #---
        self.endRow()
        #--
        camera_row5 = self.newRow( parent = cameraFakeLevel )
        #---
        self.newText( label = '', parent = camera_row5 )
        lux_camera_infinite_focus = self.addCheckBox( parent = camera_row5, label = 'Infinite focus', value = False)
        cmds.connectControl( lux_camera_infinite_focus, 'lux_settings.camera_infinite_focus' )
        #---
        self.endRow()
        
        self.endLevel()
        #--
        self.endFrame()
        #-
        
        return cameraFrameContainer
        
    def filmFrame(self, parent):
        """
        Make the frame for the 'Film' window tab
        """
        
        #-
        # LEVEL 2 FILM SETTINGS
        filmFrame, filmFrameContainer = self.newFrame( label = "Film settings", parent = parent )
        
        self.makeTabs({
            self.filmFlexImageControls: 'FlexImage',
            self.filmFlexImageTonemapping: 'Tonemapping',
            self.filmFlexImageColourSpace: 'Colour Space',
        })
        
        #--
        self.endFrame()
        #-
        
        return filmFrameContainer
    
    def float_row(self, parent, label, min, max, default, lux_setting):
        #---
        ROW = self.newRow( parent = parent )
        #----
        self.newText(label = label, parent = ROW)
        FF = cmds.floatField( parent = ROW, min = min, max = max, value = default)
        cmds.connectControl( FF, lux_setting )
        #----
        self.endRow()
        #---
    
    def filmFlexImageColourSpace(self, parent):
        cs_controls, cs_frame_container = self.newFrame(label = 'Colour space settings', parent=parent)
        
        self.float_row(cs_controls, 'White X', 0.0, 1.0, 0.313, 'lux_settings.film_colourspace_white_x')
        self.float_row(cs_controls, 'White Y', 0.0, 1.0, 0.329, 'lux_settings.film_colourspace_white_y')
        self.float_row(cs_controls, 'Red X', 0.0, 1.0, 0.630, 'lux_settings.film_colourspace_red_x')
        self.float_row(cs_controls, 'Red Y', 0.0, 1.0, 0.340, 'lux_settings.film_colourspace_red_y')
        self.float_row(cs_controls, 'Green X', 0.0, 1.0, 0.310, 'lux_settings.film_colourspace_green_x')
        self.float_row(cs_controls, 'Green Y', 0.0, 1.0, 0.595, 'lux_settings.film_colourspace_green_y')
        self.float_row(cs_controls, 'Blue X', 0.0, 1.0, 0.155, 'lux_settings.film_colourspace_blue_x')
        self.float_row(cs_controls, 'Blue Y', 0.0, 1.0, 0.070, 'lux_settings.film_colourspace_blue_y')
        
        self.float_row(cs_controls, 'Gamma', 0.0, 4.0, 2.2, 'lux_settings.film_gamma')
        
        return cs_frame_container
    
    def filmFlexImageTonemapping(self, parent):
        tonemap_controls, tonemapFrameContainer = self.newFrame(label = 'Tonemapping settings', parent = parent)
        
        #---
        tm_row1 = self.newRow(parent=tonemap_controls)
        #----
        self.newText(label = "Tonemapping kernel", parent = tm_row1)
        lux_tm_type = mOptionMenu( parent = tm_row1 )
        lux_tm_type.addItem(label="Reinhard")
        lux_tm_type.addItem(label="Linear")
        lux_tm_type.addItem(label="Contrast")
        lux_tm_type.addItem(label="Maxwhite")
        lux_tm_type.end()
        cmds.connectControl(lux_tm_type.getName(), 'lux_settings.film_tonemapping')
        #----
        self.endRow()
        #---
        
        self.makeTabs({
            self.filmFlexReinhardControls: 'Reinhard',
            self.filmFlexLinearControls: 'Linear',
            self.filmFlexContrastControls: 'Contrast',
            #self.filmFlexMaxwhiteControls: 'Maxwhite',
        })
        
        return tonemapFrameContainer
    
    def filmFlexReinhardControls(self, parent):
        tonemap_controls, tonemapFrameContainer = self.newFrame(label = 'Reinhard settings', parent = parent)
        
        #---
        film_fleximage_row0 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'Auto Ywa', parent = film_fleximage_row0)
        lux_film_fleximage_reinhardautoywa = self.addCheckBox( parent = film_fleximage_row0, label = 'Auto Ywa', value = True)
        cmds.connectControl( lux_film_fleximage_reinhardautoywa, 'lux_settings.film_reinhard_autoywa' )
        #----
        self.endRow()
        #---
        film_fleximage_row4 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'Ywa', parent = film_fleximage_row4)
        lux_film_fleximage_reinhardywa = cmds.floatField( parent = film_fleximage_row4, min = 0.001, max = 1.0, value = 0.1)
        cmds.connectControl( lux_film_fleximage_reinhardywa, 'lux_settings.film_reinhard_ywa' )
        #----
        self.endRow()
        #---
        film_fleximage_row1 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'Prescale', parent = film_fleximage_row1)
        lux_film_fleximage_reinhardprescale = cmds.floatField( parent = film_fleximage_row1, min = 0, max = 30, value = 1.0)
        cmds.connectControl( lux_film_fleximage_reinhardprescale, 'lux_settings.film_reinhard_prescale' )
        #----
        self.endRow()
        #---
        film_fleximage_row2 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'Postscale', parent = film_fleximage_row2)
        lux_film_fleximage_reinhardpostscale = cmds.floatField( parent = film_fleximage_row2, min = 0, max = 30, value = 1.0)
        cmds.connectControl( lux_film_fleximage_reinhardpostscale, 'lux_settings.film_reinhard_postscale' )
        #----
        self.endRow()
        #---
        film_fleximage_row3 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'Burn', parent = film_fleximage_row3)
        lux_film_fleximage_reinhardburn = cmds.floatField( parent = film_fleximage_row3, min = 0, max = 30, value = 6.0)
        cmds.connectControl( lux_film_fleximage_reinhardburn, 'lux_settings.film_reinhard_burn' )
        #----
        self.endRow()
        #---
        
        return tonemapFrameContainer
    
    def filmFlexLinearControls(self, parent):
        tonemap_controls, tonemapFrameContainer = self.newFrame(label = 'Linear settings', parent = parent)
        
        #---
        film_fleximage_row1 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'Sensitivity', parent = film_fleximage_row1)
        lux_film_fleximage_linear_sensitivity = cmds.floatField( parent = film_fleximage_row1, min = 0, max = 100, value = 50.0)
        cmds.connectControl( lux_film_fleximage_linear_sensitivity, 'lux_settings.film_linear_sensitivity' )
        #----
        self.endRow()
        #---
        film_fleximage_row2 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'Exposure', parent = film_fleximage_row2)
        lux_film_fleximage_linear_exposure = cmds.floatField( parent = film_fleximage_row2, min = 0.001, max = 1.0, value = 1.0)
        cmds.connectControl( lux_film_fleximage_linear_exposure, 'lux_settings.film_linear_exposure' )
        #----
        self.endRow()
        #---
        film_fleximage_row3 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'f/Stop', parent = film_fleximage_row3)
        lux_film_fleximage_linear_fstop = cmds.floatField( parent = film_fleximage_row3, min = 0.1, max = 64.0, value = 2.8)
        cmds.connectControl( lux_film_fleximage_linear_fstop, 'lux_settings.film_linear_fstop' )
        #----
        self.endRow()
        #---
        film_fleximage_row4 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'Gamma', parent = film_fleximage_row4)
        lux_film_fleximage_linear_gamma = cmds.floatField( parent = film_fleximage_row4, min = 0.0, max = 8.0, value = 1.0)
        cmds.connectControl( lux_film_fleximage_linear_gamma, 'lux_settings.film_linear_gamma' )
        #----
        self.endRow()
        #---
        
        return tonemapFrameContainer
    
    def filmFlexContrastControls(self, parent):
        tonemap_controls, tonemapFrameContainer = self.newFrame(label = 'Contrast settings', parent = parent)
        
        #---
        film_fleximage_row1 = self.newRow( parent = tonemap_controls )
        #----
        self.newText(label = 'Ywa', parent = film_fleximage_row1)
        lux_film_fleximage_contrast_ywa = cmds.floatField( parent = film_fleximage_row1, min = 0.001, max = 1.0, value = 0.1)
        cmds.connectControl( lux_film_fleximage_contrast_ywa, 'lux_settings.film_contrast_ywa' )
        #----
        self.endRow()
        #---
        
        return tonemapFrameContainer
    
    def filmFlexImageControls(self, parent):
        """
        Make the frame for the 'Fleximage' film tab
        """
        
        fleximage_controls, flexImageFrameContainer = self.newFrame(label = 'Fleximage settings', parent = parent)
        
        #---
        film_fleximage_row5 = self.newRow( parent = fleximage_controls )
        #----
        self.newText( label = 'Pre-multiply Alpha' , parent = film_fleximage_row5 )
        lux_film_fleximage_premultiply = self.addCheckBox( parent = film_fleximage_row5, value = True )
        cmds.connectControl( lux_film_fleximage_premultiply, 'lux_settings.film_premultiplyalpha' )
        #----
        self.endRow()
        #---
        film_fleximage_row6 = self.newRow( parent = fleximage_controls )
        #----
        self.newText( label = 'Write' , parent = film_fleximage_row6 )
        lux_film_write_controls = self.startLevel()
        #-----
        lux_film_write_row1 = self.newRow( parent = lux_film_write_controls, numberOfColumns = 1 )
        #------
        lux_film_fleximage_write_tm_exr = self.addCheckBox( parent = lux_film_write_row1, label = 'Tonemapped EXR', value = True) 
        cmds.connectControl( lux_film_fleximage_write_tm_exr, 'lux_settings.film_write_tonemapped_exr' )
        #------
        self.endRow()
        #-----
        lux_film_write_row2 = self.newRow( parent = lux_film_write_controls, numberOfColumns = 1 )
        #------
        lux_film_fleximage_write_tm_igi = self.addCheckBox( parent = lux_film_write_row2, label = 'Tonemapped IGI', value = False )
        cmds.connectControl( lux_film_fleximage_write_tm_igi, 'lux_settings.film_write_tonemapped_igi' )
        #------
        self.endRow()
        #-----
        lux_film_write_row3 = self.newRow( parent = lux_film_write_controls, numberOfColumns = 1 )
        #------
        lux_film_fleximage_write_tm_tga = self.addCheckBox( parent = lux_film_write_row3, label = 'Tonemapped TGA', value = False )
        cmds.connectControl( lux_film_fleximage_write_tm_tga, 'lux_settings.film_write_tonemapped_tga' )
        #------
        self.endRow()
        #-----
        lux_film_write_row4 = self.newRow( parent = lux_film_write_controls, numberOfColumns = 1 )
        #------
        lux_film_fleximage_write_utm_exr = self.addCheckBox( parent = lux_film_write_row4, label = 'Untonemapped EXR' )
        cmds.connectControl( lux_film_fleximage_write_utm_exr, 'lux_settings.film_write_untonemapped_exr' )
        #------
        self.endRow()
        #-----
        lux_film_write_row5 = self.newRow( parent = lux_film_write_controls, numberOfColumns = 1 )
        #------
        lux_film_fleximage_write_utm_igi = self.addCheckBox( parent = lux_film_write_row5, label = 'Untonemapped IGI' )
        cmds.connectControl( lux_film_fleximage_write_utm_igi, 'lux_settings.film_write_untonemapped_igi' )
        #------
        self.endRow()
        #-----
        lux_film_write_row6A = self.newRow( parent = lux_film_write_controls, numberOfColumns = 1 )
        #------
        lux_film_fleximage_write_resume = self.addCheckBox( parent = lux_film_write_row6A, label = 'Resume Film' )
        cmds.connectControl( lux_film_fleximage_write_resume, 'lux_settings.film_write_resume_film' )
        #------
        self.endRow()
        #-----
        self.endRow()
        #-----
        lux_film_write_row6B = self.newRow( parent = lux_film_write_controls, numberOfColumns = 1 )
        #------
        lux_film_fleximage_restart_resume = self.addCheckBox( parent = lux_film_write_row6B, label = 'Restart Resume Film' )
        cmds.connectControl( lux_film_fleximage_restart_resume, 'lux_settings.film_restart_resume_film' )
        #------
        self.endRow()
        #-----
        
        self.endLevel()
        #----
        self.endRow()
        #---
        film_fleximage_row7 = self.newRow( parent = fleximage_controls )
        #----
        self.newText(label = 'Write interval', parent = film_fleximage_row7)
        lux_film_fleximage_writeinterval = cmds.intField( parent = film_fleximage_row7, min = 0, max = 12000, value = 60)
        cmds.connectControl( lux_film_fleximage_writeinterval, 'lux_settings.film_writeinterval' )
        #----
        self.endRow()
        #---
        film_fleximage_row8 = self.newRow( parent = fleximage_controls )
        #----
        self.newText(label = 'Display interval', parent = film_fleximage_row8)
        lux_film_fleximage_displayinterval = cmds.intField( parent = film_fleximage_row8, min = 0, max = 12000, value = 12)
        cmds.connectControl( lux_film_fleximage_displayinterval, 'lux_settings.film_displayinterval' )
        #----
        self.endRow()
        #---
        film_fleximage_row9 = self.newRow( parent = fleximage_controls )
        #----
        self.newText(label = 'Reject warmup', parent = film_fleximage_row9)
        lux_film_fleximage_rejectwarmup = cmds.intField( parent = film_fleximage_row9, min = 0, max = 12000, value = 12)
        cmds.connectControl( lux_film_fleximage_rejectwarmup, 'lux_settings.film_reject_warmup' )
        #----
        self.endRow()
        #---
        film_fleximage_row10 = self.newRow( parent = fleximage_controls )
        #----
        self.newText(label = 'Halt SPP', parent = film_fleximage_row10)
        lux_film_fleximage_haltspp = cmds.intField( parent = film_fleximage_row10, min = 0, value = 0)
        cmds.connectControl( lux_film_fleximage_haltspp, 'lux_settings.film_haltspp' )
        #----
        self.endRow()
        #---
        
        return flexImageFrameContainer
    
    def databaseFrame(self, parent):
        """
        Make the frame for the 'Database' window tab
        """
        
        #-
        # LEVEL 2 DATABASE CONTROLS
        dbFrame, dbFrameContainer = self.newFrame( label = "Database", parent = parent )
        #--
        
        #--
        self.endFrame()
        #-
        return dbFrameContainer
    
    def renderFrame(self, parent):
        """
        Make the frame for the 'Renderer' window tab
        """
        
        #-
        # LEVEL 2 RENDERER SETTINGS
        renderFrame, renderFrameContainer = self.newFrame( label = "Renderer Settings", parent = parent )
        #--
        # SAMPLERS
        SA_FRAME, SA_FRAME_CONTAINER = self.newFrame(label = 'Sampler' , parent = renderFrame, collapsable = True, collapsed = True)
        lux_render_row1 = self.newRow(parent = SA_FRAME)
        #---
        self.newText(label = "Sampler", parent = lux_render_row1)
        lux_render_sampler = mOptionMenu(parent = lux_render_row1)
        lux_render_sampler.addItem(label = "Random")
        lux_render_sampler.addItem(label = "Low discrepancy")
        lux_render_sampler.addItem(label = "Metropolis")
        lux_render_sampler.addItem(label = "erpt")
        lux_render_sampler.end()
        cmds.connectControl( lux_render_sampler.getName(), 'lux_settings.pixel_sampler' )
        #---
        self.endRow()
        #--
        self.makeTabs({
                       self.samplerRandom: 'Random',
                       self.samplerLowDiscrepancy: 'Low Discrepancy',
                       self.samplerMetropolis: 'Metropolis',
                       self.samplerErpt: 'ERPT'
                       })
        self.endRow()
        
        # FILTERS
        FI_FRAME, FI_FRAME_CONTAINER = self.newFrame(label = 'Filter' , parent = renderFrame, collapsable = True, collapsed = True)
        lux_render_row2 = self.newRow(parent = FI_FRAME)
        #---
        self.newText(label = "Pixel Filter", parent = lux_render_row2)
        lux_render_filter = mOptionMenu(parent = lux_render_row2)
        lux_render_filter.addItem(label = "Mitchell")
        lux_render_filter.addItem(label = "Gaussian")
        lux_render_filter.addItem(label = "Sinc")
        lux_render_filter.addItem(label = "Triangle")
        lux_render_filter.addItem(label = "Box")
        lux_render_filter.end()
        cmds.connectControl( lux_render_filter.getName(), 'lux_settings.pixel_filter' )
        #---
        self.endRow()
        #--
        self.makeTabs({
                       self.filterMitchell: 'Mitchell',
                       self.filterGaussian: 'Gaussian',
                       self.filterSinc: 'Sinc',
                       self.filterTriangle: 'Triangle',
                       self.filterBox: 'Box'
                       })
        self.endRow()
        
        # ACCELERATORS
        AC_FRAME, AC_FRAME_CONTAINER = self.newFrame(label = 'Accelerator', parent = renderFrame, collapsable = True, collapsed = True)
        lux_render_row3 = self.newRow(parent = AC_FRAME)
        #---
        self.newText(label = "Accelerator", parent = lux_render_row3)
        lux_render_accelerator = mOptionMenu(parent = lux_render_row3)
        lux_render_accelerator.addItem(label = "tabreckdtree")
        lux_render_accelerator.addItem(label = "Grid")
        lux_render_accelerator.addItem(label = "BVH")
        lux_render_accelerator.addItem(label = "None")
        lux_render_accelerator.end()
        cmds.connectControl( lux_render_accelerator.getName(), 'lux_settings.accelerator' )
        #---
        self.endRow()
        #--
        
        self.makeTabs({
            self.acceleratorKDtree: 'KD Tree',
            self.acceleratorGrid: 'Grid',
        })
        self.endRow()
        
        #--
        
        # SURFACE INTEGRATORS
        SI_FRAME, SI_FRAME_CONTAINER = self.newFrame(label = 'Surface Integrator', parent = renderFrame, collapsable = True, collapsed = True)
        lux_render_row4 = self.newRow(parent = SI_FRAME)
        #---
        self.newText(label = "Surface Integrator", parent = lux_render_row4)
        lux_render_surface_integrator = mOptionMenu(parent = lux_render_row4)
        lux_render_surface_integrator.addItem(label = "BiDirectional")
        lux_render_surface_integrator.addItem(label = "Direct Lighting")
        lux_render_surface_integrator.addItem(label = "Path")
        lux_render_surface_integrator.addItem(label = "Distributed Path")
        lux_render_surface_integrator.end()
        cmds.connectControl( lux_render_surface_integrator.getName(), 'lux_settings.surface_integrator' )
        #---
        self.endRow()
        #--
        
        self.makeTabs({
                       self.renderSurfaceIntegratorBiDir: 'BiDir',
                       self.renderSurfaceIntegratorDirectLighting: 'DirectLighting',
                       self.renderSurfaceIntegratorPath: 'Path',
                       self.renderSurfaceIntegratorDistributedPath: 'DistributedPath'
                       })
        self.endRow()
        
        # VOLUME INTEGRATORS
        VI_FRAME, VI_FRAME_CONTAINER = self.newFrame(label = 'Volume Integrator', parent = renderFrame, collapsable = True, collapsed = True)
        lux_render_row5 = self.newRow(parent = VI_FRAME)
        #---
        self.newText(label = "Volume Integrator", parent = lux_render_row5)
        lux_render_volume_integrator = mOptionMenu(parent = lux_render_row5 )
        lux_render_volume_integrator.addItem(label = "Emission")
        lux_render_volume_integrator.addItem(label = "Single")
        lux_render_volume_integrator.end()
        cmds.connectControl( lux_render_volume_integrator.getName(), 'lux_settings.volume_integrator' )
        #---
        self.endRow()
        #--
        self.makeTabs({
                       self.renderVolumeIntegrator: 'Emission && Single'
                       })
        self.endRow()
        
        self.endFrame()
        #-
        return renderFrameContainer
    
    def samplerRandom(self, parent):
        """
        Make the frame for the 'Sampler' renderer tab
        """
        
        fControls, fControlContainer = self.newFrame( label = 'Random Sampler Settings', parent = parent )
        
        lux_render_sampler_row1 = self.newRow( parent = fControls )
        #---
        self.newText( label = "xsamples", parent = lux_render_sampler_row1 )
        lux_render_sampler_xsamples = cmds.intField( parent = lux_render_sampler_row1, min = 1, max = 50000, value = 2)
        cmds.connectControl( lux_render_sampler_xsamples, 'lux_settings.pixel_sampler_xsamples' )
        #---
        self.endRow()
        #--
        lux_render_sampler_row2 = self.newRow( parent = fControls )
        #---
        self.newText( label = "ysamples", parent = lux_render_sampler_row2 )
        lux_render_sampler_ysamples = cmds.intField( parent = lux_render_sampler_row2, min = 1, max = 50000, value = 2)
        cmds.connectControl( lux_render_sampler_ysamples, 'lux_settings.pixel_sampler_ysamples' )
        #---
        self.endRow()
        #--
        self.samplerCTL_pixelsampler( parent = fControls )
        return fControlContainer
    
    def samplerLowDiscrepancy(self, parent):
        """
        Make the frame for the 'LowDiscrepancy' sampler tab
        """
        
        fControls, fControlContainer = self.newFrame( label = 'Low Discrepancy Sampler Settings', parent = parent )
        self.samplerCTL_pixelsamples( parent = fControls )
        self.samplerCTL_pixelsampler( parent = fControls )
        return fControlContainer
    
    def samplerMetropolis(self, parent):
        """
        Make the frame for the 'Metropolis' sampler tab
        """
        
        fControls, fControlContainer = self.newFrame( label = 'Metropolis Sampler Settings', parent = parent )
        self.samplerCTL_init_mutation( parent = fControls )
        
        lux_render_sampler_row3 = self.newRow( parent = fControls )
        #---
        self.newText( label = 'maxconsecrejects', parent = lux_render_sampler_row3 )
        lux_render_sampler_maxconsecrejects = cmds.intField( parent = lux_render_sampler_row3, min = 1, max = 32767, value = 512)
        cmds.connectControl( lux_render_sampler_maxconsecrejects, 'lux_settings.pixel_sampler_maxconsecrejects' )
        #---
        self.endRow()
        #--
        lux_render_sampler_row4 = self.newRow( parent = fControls )
        #---
        self.newText( label = 'largemutationprob', parent = lux_render_sampler_row4 )
        lux_render_sampler_largemutationprob = cmds.floatField( parent = lux_render_sampler_row4, min = 0, max = 1, value = 0.4)
        cmds.connectControl( lux_render_sampler_largemutationprob, 'lux_settings.pixel_sampler_largemutationprob' )
        #---
        self.endRow()
        #--
        lux_render_sampler_row5 = self.newRow( parent = fControls )
        #---
        self.newText( label = 'usevariance', parent = lux_render_sampler_row5 )
        lux_render_sampler_usevariance = self.addCheckBox( parent = lux_render_sampler_row5, label = '' )
        cmds.connectControl( lux_render_sampler_usevariance, 'lux_settings.pixel_sampler_usevariance' )
        #---
        self.endRow()
        #--
        return fControlContainer
    
    def samplerErpt(self, parent):
        """
        Make the frame for the 'ERPT' sampler tab
        """
        
        fControls, fControlContainer = self.newFrame( label = 'ERPT Sampler Settings', parent = parent )
        self.samplerCTL_init_mutation( parent = fControls )
        
        lux_render_sampler_row3 = self.newRow( parent = fControls )
        #---
        self.newText( label = 'chainlength', parent = lux_render_sampler_row3 )
        lux_render_sampler_chainlength = cmds.intField( parent = lux_render_sampler_row3, min = 1, max = 32767, value = 2000)
        cmds.connectControl( lux_render_sampler_chainlength, 'lux_settings.pixel_sampler_chainlength' )
        #---
        self.endRow()
        #--
        return fControlContainer
        
    def samplerCTL_init_mutation(self, parent):
        """
        Add the initsamples and mutationrange controls to the parent container
        """
        
        lux_render_sampler_row1 = self.newRow( parent = parent )
        #---
        self.newText( label = 'initsamples', parent = lux_render_sampler_row1 )
        lux_render_sampler_initsamples = cmds.intField( parent = lux_render_sampler_row1, min = 1, max = 10000000, value = 100000)
        cmds.connectControl( lux_render_sampler_initsamples, 'lux_settings.pixel_sampler_initsamples' )
        #---
        self.endRow()
        #--
        # disabled at request of Radiance
#        lux_render_sampler_row2 = self.newRow( parent = parent )
#        #---
#        self.newText( label = 'mutationrange', parent = lux_render_sampler_row2 )
#        lux_render_sampler_mutationrange = cmds.floatField( parent = lux_render_sampler_row2, min = 0, max = 10000, value = 45)
#        cmds.connectControl( lux_render_sampler_mutationrange, 'lux_settings.pixel_sampler_mutationrange' )
#        #---
#        self.endRow()
#        #--
    
    def samplerCTL_pixelsamples(self, parent):
        """
        Add the pixelsamples control to the parent container
        """
        
        lux_render_sampler_row1 = self.newRow( parent = parent )
        #---
        self.newText( label = 'pixelsamples', parent = lux_render_sampler_row1 )
        lux_render_sampler_pixelsamples = cmds.intField( parent = lux_render_sampler_row1, min = 1, max = 50000, value = 2)
        cmds.connectControl( lux_render_sampler_pixelsamples, 'lux_settings.pixel_sampler_pixelsamples' )
        #---
        self.endRow()
        #--
    
    def samplerCTL_pixelsampler(self, parent):
        """
        Add the pixelsampler controls to the parent container
        """
        
        lux_render_sampler_rowPS = self.newRow( parent = parent )
        #---
        self.newText( label = 'pixelsampler' , parent = lux_render_sampler_rowPS )
        lux_render_sampler_pixelsampler_select = mOptionMenu( parent = lux_render_sampler_rowPS )
        lux_render_sampler_pixelsampler_select.addItem( label = 'Linear' )
        lux_render_sampler_pixelsampler_select.addItem( label = 'Vegas' )
        lux_render_sampler_pixelsampler_select.addItem( label = 'Low Discrepancy' )
        lux_render_sampler_pixelsampler_select.addItem( label = 'Tile' )
        lux_render_sampler_pixelsampler_select.addItem( label = 'Random' )
        lux_render_sampler_pixelsampler_select.addItem( label = 'Hilbert' )
        lux_render_sampler_pixelsampler_select.end()
        cmds.connectControl( lux_render_sampler_pixelsampler_select.getName(), 'lux_settings.pixel_sampler_pixelsampler' )
        #---
        self.endRow()
        #--
    
    def filterMitchell(self, parent):
        """
        Make the Mitchell filter frame for the filters tabs
        """
        
        fControls, fControlContainer = self.newFrame( label = 'Mitchell Settings', parent = parent )
        self.filterCommonControls( parent = fControls )
        lux_render_filter_row3 = self.newRow( parent = fControls )
        #---
        self.newText( label = "B", parent = lux_render_filter_row3 )
        lux_render_filter_b = cmds.floatField( parent = lux_render_filter_row3, min = 0, max = 10000, value = 0.333)
        cmds.connectControl( lux_render_filter_b, 'lux_settings.pixel_filter_b' )
        #---
        self.endRow()
        #--
        lux_render_filter_row4 = self.newRow( parent = fControls )
        #---
        self.newText( label = "C", parent = lux_render_filter_row4 )
        lux_render_filter_c = cmds.floatField( parent = lux_render_filter_row4, min = 0, max = 10000, value = 0.333)
        cmds.connectControl( lux_render_filter_c, 'lux_settings.pixel_filter_c' )
        #---
        self.endRow()
        #--
        return fControlContainer
    
    def filterGaussian(self, parent):
        """
        Make the Gaussian filter frame for the filters tabs
        """
        
        fControls, fControlContainer = self.newFrame( label = 'Gaussian Settings', parent = parent )
        self.filterCommonControls( parent = fControls )
        
        lux_render_filter_row3 = self.newRow( parent = fControls )
        #---
        self.newText( label = "alpha", parent = lux_render_filter_row3 )
        lux_render_filter_alpha = cmds.floatField( parent = lux_render_filter_row3, min = 0, max = 10000, value = 2)
        cmds.connectControl( lux_render_filter_alpha, 'lux_settings.pixel_filter_alpha' )
        #---
        self.endRow()
        #--
        return fControlContainer
    
    def filterSinc(self, parent):
        """
        Make the Sinc filter frame for the filters tabs
        """
        
        fControls, fControlContainer = self.newFrame( label = 'Sinc Settings', parent = parent )
        self.filterCommonControls( parent = fControls )
        
        lux_render_filter_row3 = self.newRow( parent = fControls )
        #---
        self.newText( label = "tau", parent = lux_render_filter_row3 )
        lux_render_filter_tau = cmds.floatField( parent = lux_render_filter_row3, min = 0, max = 10000, value = 3)
        cmds.connectControl( lux_render_filter_tau, 'lux_settings.pixel_filter_tau' )
        #---
        self.endRow()
        #--
        return fControlContainer
    
    def filterTriangle(self, parent):
        """
        Make the Triangle filter frame for the filters tabs
        """
        
        fControls, fControlContainer = self.newFrame( label = 'Triangle Settings', parent = parent )
        self.filterCommonControls( parent = fControls )
        return fControlContainer
    
    def filterBox(self, parent):
        """
        Make the Box filter frame for the filters tabs
        """
        
        fControls, fControlContainer = self.newFrame( label = 'Box Settings', parent = parent )
        self.filterCommonControls( parent = fControls )
        return fControlContainer
    
    def filterCommonControls(self, parent):
        """
        Make the Common filter controls for the filters tabs
        """
        
        lux_render_filter_row1 = self.newRow( parent = parent )
        #---
        self.newText( label = "xwidth", parent = lux_render_filter_row1 )
        lux_render_filter_xwidth = cmds.floatField( parent = lux_render_filter_row1, min = 0, max = 10000, value = 2)
        cmds.connectControl( lux_render_filter_xwidth, 'lux_settings.pixel_filter_xwidth' )
        #---
        self.endRow()
        #--
        lux_render_filter_row2 = self.newRow( parent = parent )
        #---
        self.newText( label = "ywidth", parent = lux_render_filter_row2 )
        lux_render_filter_ywidth = cmds.floatField( parent = lux_render_filter_row2, min = 0, max = 10000, value = 2)
        cmds.connectControl( lux_render_filter_ywidth, 'lux_settings.pixel_filter_ywidth' )
        #---
        self.endRow()
        #--
    
    def acceleratorGrid(self, parent):
        """
        Make the Grid controls for the Accelerator tabs
        """
        
        acControls, acControlContainer = self.newFrame( label = 'Grid Accelerator Settings', parent = parent )
        
        lux_render_accelerator_row1 = self.newRow( parent = acControls )
        #---
        self.newText( label = 'refineimmediately' , parent = lux_render_accelerator_row1 )
        lux_render_accelerator_refineimmediately = self.addCheckBox( parent = lux_render_accelerator_row1 )
        cmds.connectControl( lux_render_accelerator_refineimmediately, 'lux_settings.accelerator_refineimmediately' )
        #---
        self.endRow()
        #--
        return acControlContainer
    
#    def acceleratorUnsafeKDtree(self, parent):
#        """
#        Clone the KDTree controls for the Accelerator tabs
#        """
#        
#        return self.acceleratorKDtree(parent)
    
    def acceleratorKDtree(self, parent):
        """
        Make the KDTree controls for the Accelerator tabs
        """
        
        acControls, acControlContainer = self.newFrame( label = 'KD Tree Accelerator Settings', parent = parent )
        
        lux_render_accelerator_row1 = self.newRow( parent = acControls )
        #---
        self.newText( label = 'intersectcost' , parent = lux_render_accelerator_row1 )
        lux_render_accelerator_intersectcost = cmds.intField( parent = lux_render_accelerator_row1, min = 0, max = 10000, value = 80)
        cmds.connectControl( lux_render_accelerator_intersectcost, 'lux_settings.accelerator_intersectcost' )
        #---
        self.endRow()
        #--
        lux_render_accelerator_row2 = self.newRow( parent = acControls )
        #---
        self.newText( label = 'traversalcost' , parent = lux_render_accelerator_row2 )
        lux_render_accelerator_traversalcost = cmds.intField( parent = lux_render_accelerator_row2, min = 0, max = 10000, value = 1)
        cmds.connectControl( lux_render_accelerator_traversalcost, 'lux_settings.accelerator_traversalcost' )
        #---
        self.endRow()
        #--
        lux_render_accelerator_row3 = self.newRow( parent = acControls )
        #---
        self.newText( label = 'emptybonus' , parent = lux_render_accelerator_row3 )
        lux_render_accelerator_emptybonus = cmds.floatField( parent = lux_render_accelerator_row3, min = 0, max = 10000, value = 0.5)
        cmds.connectControl( lux_render_accelerator_emptybonus, 'lux_settings.accelerator_emptybonus' )
        #---
        self.endRow()
        #--
        lux_render_accelerator_row4 = self.newRow( parent = acControls )
        #---
        self.newText( label = 'maxprims' , parent = lux_render_accelerator_row4 )
        lux_render_accelerator_maxprims = cmds.intField( parent = lux_render_accelerator_row4, min = 0, max = 10000, value = 1)
        cmds.connectControl( lux_render_accelerator_maxprims, 'lux_settings.accelerator_maxprims' )
        #---
        self.endRow()
        #--
        lux_render_accelerator_row5 = self.newRow( parent = acControls )
        #---
        self.newText( label = 'maxdepth' , parent = lux_render_accelerator_row5 )
        lux_render_accelerator_maxdepth = cmds.intField( parent = lux_render_accelerator_row5, min = 0, max = 10000, value = 1)
        cmds.connectControl( lux_render_accelerator_maxdepth, 'lux_settings.accelerator_maxdepth' )
        #---
        self.endRow()
        #--
        
        return acControlContainer
    
    def renderVolumeIntegrator(self, parent):
        """
        Make the Volume Integrator controls for the renderer frame
        """
        
        viControls, viControlContainer = self.newFrame( label = 'Volume Integrator Settings', parent = parent )
        
        lux_render_surface_integrator_row1 = self.newRow( parent = viControls )
        #----
        self.newText( label = 'stepsize' , parent = lux_render_surface_integrator_row1 )
        lux_render_surface_integrator_stepsize = cmds.floatField( parent = lux_render_surface_integrator_row1, min = 0, max = 10000, value = 1)
        cmds.connectControl( lux_render_surface_integrator_stepsize, 'lux_settings.volume_integrator_stepsize' )
        #----
        self.endRow()
        #---
        
        return viControlContainer
    
    def renderSurfaceIntegratorBiDir(self, parent):
        """
        Make the BiDir controls for the surface integrators tabs
        """
        
        siControls, siControlContainer = self.newFrame( label = 'BiDir Surface Integrator Settings', parent = parent )
        
        # rows
        
        lux_render_surface_integrator_row1 = self.newRow( parent = siControls )
        #---
        self.newText( label = 'eyedepth' , parent = lux_render_surface_integrator_row1 )
        lux_render_surface_integrator_eyedepth = cmds.intField( parent = lux_render_surface_integrator_row1, min = 0, max = 10000, value = 8)
        cmds.connectControl( lux_render_surface_integrator_eyedepth, 'lux_settings.surface_integrator_eyedepth' )
        #---
        self.endRow()
        #--
        lux_render_surface_integrator_row2 = self.newRow( parent = siControls )
        #---
        self.newText( label = 'lightdepth' , parent = lux_render_surface_integrator_row2 )
        lux_render_surface_integrator_lightdepth = cmds.intField( parent = lux_render_surface_integrator_row2, min = 0, max = 10000, value = 8)
        cmds.connectControl( lux_render_surface_integrator_lightdepth, 'lux_settings.surface_integrator_lightdepth' )
        #---
        self.endRow()
        #--
        
        return siControlContainer
    
    def renderSurfaceIntegratorDirectLighting(self, parent):
        """
        Make the Direct Lighting controls for the surface integrators tabs
        """
        
        siControls, siControlContainer = self.newFrame( label = 'Direct Lighting Integrator Settings', parent = parent )
        
        lux_render_surface_integrator_row1 = self.newRow( parent = siControls )
        #---
        self.newText( label = 'maxdepth' , parent = lux_render_surface_integrator_row1 )
        lux_render_surface_integrator_maxdepth = cmds.intField( parent = lux_render_surface_integrator_row1, min = 0, max = 10000, value = 32)
        cmds.connectControl( lux_render_surface_integrator_maxdepth, 'lux_settings.surface_integrator_maxdepth' )
        #---
        self.endRow()
        #--
        self.renderSurfaceIntegratorStrategy( siControls )
        
        return siControlContainer
    
    def renderSurfaceIntegratorStrategy(self, parent):
        lux_render_surface_integrator_row2 = self.newRow( parent = parent )
        #---
        self.newText( label = 'strategy' , parent = lux_render_surface_integrator_row2 )
        lux_render_surface_integrator_strategy = mOptionMenu(parent = lux_render_surface_integrator_row2 )
        lux_render_surface_integrator_strategy.addItem( label = 'All' )
        lux_render_surface_integrator_strategy.addItem( label = 'One' )
        lux_render_surface_integrator_strategy.addItem( label = 'Auto' )
        lux_render_surface_integrator_strategy.end()
        cmds.connectControl( lux_render_surface_integrator_strategy.getName(), 'lux_settings.surface_integrator_strategy' )
        #---
        self.endRow()
        #--
    
#    def renderSurfaceIntegratorParticleTracing(self, parent):
#        """
#        Make the Particle Tracing controls for the surface integrators tabs
#        """
#        
#        siControls, siControlContainer = self.newFrame( label = 'Particle Tracing Surface Integrator Settings', parent = parent )
#        
#        lux_render_surface_integrator_row1 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = 'maxdepth' , parent = lux_render_surface_integrator_row1 )
#        lux_render_surface_integrator_maxdepth = cmds.intField( parent = lux_render_surface_integrator_row1, min = 0, max = 10000, value = 32)
#        cmds.connectControl( lux_render_surface_integrator_maxdepth, 'lux_settings.surface_integrator_maxdepth' )
#        #---
#        self.endRow()
#        #--
#        
#        lux_render_surface_integrator_row2 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = 'rrcontinueprob' , parent = lux_render_surface_integrator_row2 )
#        lux_render_surface_integrator_rrcontinueprob = cmds.floatField( parent = lux_render_surface_integrator_row2, min = 0, max = 1, value = 0.65)
#        cmds.connectControl( lux_render_surface_integrator_rrcontinueprob, 'lux_settings.surface_integrator_rrcontinueprob' )
#        #---
#        self.endRow()
#        #--
#        
#        return siControlContainer
    
    def renderSurfaceIntegratorPath(self, parent):
        """
        Make the Path Tracing controls for the surface integrators tabs
        """
        
        siControls, siControlContainer = self.newFrame( label = 'Path Tracing Surface Integrator Settings', parent = parent )
        
        lux_render_surface_integrator_row1 = self.newRow( parent = siControls )
        #---
        self.newText( label = 'maxdepth' , parent = lux_render_surface_integrator_row1 )
        lux_render_surface_integrator_maxdepth = cmds.intField( parent = lux_render_surface_integrator_row1, min = 0, max = 10000, value = 32)
        cmds.connectControl( lux_render_surface_integrator_maxdepth, 'lux_settings.surface_integrator_maxdepth' )
        #---
        self.endRow()
        #--
        self.renderSurfaceIntegratorStrategy( siControls )
        
        return siControlContainer
    
#    def renderSurfaceIntegratorExPhotonMap(self, parent):
#        """
#        Make the ExPhotonMap controls for the surface integrators tabs
#        """
#        
#        siControls, siControlContainer = self.newFrame( label = 'ExPhotonMap Surface Integrator Settings', parent = parent )
#        
#        lux_render_surface_integrator_row1 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = 'causticphotons' , parent = lux_render_surface_integrator_row1 )
#        lux_render_surface_integrator_causticphotons = cmds.intField( parent = lux_render_surface_integrator_row1, min = 0, max = 1000000, value = 20000 )
#        cmds.connectControl( lux_render_surface_integrator_causticphotons, 'lux_settings.surface_integrator_causticphotons' )
#        #---
#        self.endRow()
#        #--
#        
#        lux_render_surface_integrator_row2 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = 'indirectphotons' , parent = lux_render_surface_integrator_row2 )
#        lux_render_surface_integrator_indirectphotons = cmds.intField( parent = lux_render_surface_integrator_row2, min = 0, max = 20000000, value = 100000)
#        cmds.connectControl( lux_render_surface_integrator_indirectphotons, 'lux_settings.surface_integrator_indirectphotons' )
#        #---
#        self.endRow()
#        #--
#        
#        lux_render_surface_integrator_row3 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = 'nused' , parent = lux_render_surface_integrator_row3 )
#        lux_render_surface_integrator_nused = cmds.intField( parent = lux_render_surface_integrator_row3, min = 0, max = 50000, value = 50 )
#        cmds.connectControl( lux_render_surface_integrator_nused, 'lux_settings.surface_integrator_nused' )
#        #---
#        self.endRow()
#        #--
#        
#        lux_render_surface_integrator_row4 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = 'maxdepth' , parent = lux_render_surface_integrator_row4 )
#        lux_render_surface_integrator_maxdepth = cmds.intField( parent = lux_render_surface_integrator_row4, min = 0, max = 10000, value = 5 )
#        cmds.connectControl( lux_render_surface_integrator_maxdepth, 'lux_settings.surface_integrator_maxdepth' )
#        #---
#        self.endRow()
#        #--
#        
#        lux_render_surface_integrator_row5 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = '' , parent = lux_render_surface_integrator_row5 )
#        lux_render_surface_integrator_finalgather = self.addCheckBox( parent = lux_render_surface_integrator_row5, label = 'finalgather', value = True)
#        cmds.connectControl( lux_render_surface_integrator_finalgather, 'lux_settings.surface_integrator_finalgather' )
#        #---
#        self.endRow()
#        #--
#        
#        lux_render_surface_integrator_row6 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = 'finalgathersamples' , parent = lux_render_surface_integrator_row6 )
#        lux_render_surface_integrator_finalgathersamples = cmds.intField( parent = lux_render_surface_integrator_row6, min = 0, max = 10000, value = 32 )
#        cmds.connectControl( lux_render_surface_integrator_finalgathersamples, 'lux_settings.surface_integrator_finalgathersamples' )
#        #---
#        self.endRow()
#        #--
#        
#        lux_render_surface_integrator_row7 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = 'maxdist' , parent = lux_render_surface_integrator_row7 )
#        lux_render_surface_integrator_maxdist = self.addFloatField( parent = lux_render_surface_integrator_row7, min = 0 , max = 20.0, value = 0.1)
#        cmds.connectControl( lux_render_surface_integrator_maxdist, 'lux_settings.surface_integrator_maxdist' )
#        #---
#        self.endRow()
#        #--
#        
#        # Reserved for rrthreshold (not used)
##        lux_render_surface_integrator_row8 = self.newRow( parent = siControls )
##        #---
##        self.newText( label = '' , parent = lux_render_surface_integrator_row8 )
##        lux_render_surface_integrator_ = cmds.intField( parent = lux_render_surface_integrator_row8, min = 0, max = , value = )
##        cmds.connectControl( lux_render_surface_integrator_, 'lux_settings.surface_integrator_' )
##        #---
##        self.endRow()
##        #--
#        
#        lux_render_surface_integrator_row9 = self.newRow( parent = siControls )
#        #---
#        self.newText( label = 'gatherangle' , parent = lux_render_surface_integrator_row9 )
#        lux_render_surface_integrator_gatherangle = self.addFloatField( parent = lux_render_surface_integrator_row9, min = 0 , max = 360.0, value = 10.0)
#        cmds.connectControl( lux_render_surface_integrator_gatherangle, 'lux_settings.surface_integrator_gatherangle' )
#        #---
#        self.endRow()
#        #--
#        self.renderSurfaceIntegratorStrategy( siControls )
#        
#        return siControlContainer
    
    def renderSurfaceIntegratorDistributedPath(self, parent):
        
        siControls, siControlContainer = self.newFrame( label = 'DistributedPath Surface Integrator Settings', parent = parent )
        
        lux_render_surface_integrator_row1 = self.newRow( parent = siControls )
        #---
        self.newText( label = 'Diffuse Depth' , parent = lux_render_surface_integrator_row1 )
        lux_render_surface_integrator_diffusedepth = cmds.intField( parent = lux_render_surface_integrator_row1, min = 0, max = 1000, value = 3 )
        cmds.connectControl( lux_render_surface_integrator_diffusedepth, 'lux_settings.surface_integrator_diffusedepth' )
        #---
        self.endRow()
        #--
        
        lux_render_surface_integrator_row2 = self.newRow( parent = siControls )
        #---
        self.newText( label = 'Glossy Depth' , parent = lux_render_surface_integrator_row2 )
        lux_render_surface_integrator_glossydepth = cmds.intField( parent = lux_render_surface_integrator_row2, min = 0, max = 1000, value = 2 )
        cmds.connectControl( lux_render_surface_integrator_glossydepth, 'lux_settings.surface_integrator_glossydepth' )
        #---
        self.endRow()
        #--
        
        lux_render_surface_integrator_row3 = self.newRow( parent = siControls )
        #---
        self.newText( label = 'Specular Depth' , parent = lux_render_surface_integrator_row3 )
        lux_render_surface_integrator_speculardepth = cmds.intField( parent = lux_render_surface_integrator_row3, min = 0, max = 1000, value = 5 )
        cmds.connectControl( lux_render_surface_integrator_speculardepth, 'lux_settings.surface_integrator_speculardepth' )
        #---
        self.endRow()
        #--
        
        self.renderSurfaceIntegratorStrategy( siControls )
        
        return siControlContainer
    
    # GUI Frames end here.
    
    # GUI callback functions follow... 
    
    # MENUS
    
    def mnuObjectLocator(self, *args):
        """
        Create a new luxObjectLocator
        """
        
        lol = OpenMaya.MFnDependencyNode().create( 'luxObjectLocator' )
    
    def mnuEnvLight(self, *args):
        """
        Create a new luxEnvironmentLight
        """
        
        lel = OpenMaya.MFnDependencyNode().create( 'luxEnvironmentLight' )
    
    def mnuSunsky(self, *args):
        """
        Create a new luxSunsky - TODO: detect if already present in scene. Scene should
        only need one.
        """
        
        lss = OpenMaya.MFnDependencyNode().create( 'luxSunsky' )
        
        # this is broken - causes C++ runtime error
        #from Lux.LuxMiscModules.geoSunData import updateSunNode
        #OpenMaya.MNodeMessage.addAttributeChangedCallback(lss, updateSunNode.doIt, lss )
    
    def mnuPrefs(self, *args):
        """
        Open the Maya Preferences window
        """
        
        OpenMaya.MGlobal.executeCommand('PreferencesWindow')
    
    def mnuLuxSettings(self, *args):
        """
        Load the lux_settings scriptnode into the AttributeEditor
        """
        
        OpenMaya.MGlobal.executeCommand('updateAE lux_settings')
    
    def mnuClose(self, *args):
        """
        Close (delete) the GUI window
        """
        
        cmds.deleteUI( 'luxGuiMain' )
        
    def mnuDbTEST(self, *args):
        # do something with self.lrmdb
        self.lrmdb.download(None, 60)
    
    def mnuHelpWebsite(self, *args):
        if os.name == 'nt':
            os.system('start http://www.luxrender.net/' )
    
    def mnuHelpWiki(self, *args):
        if os.name == 'nt':
            os.system('start http://www.luxrender.net/wiki/index.php/Main_Page' )
    
    def mnuHelpDevForum(self, *args):
        if os.name == 'nt':
            os.system('start http://www.luxrender.net/forum/viewforum.php?f=28' )
    
    def mnuHelpAbout(self, *args):
        if cmds.window('luxGuiAbout', exists=True):
            cmds.deleteUI('luxGuiAbout', window=True)
        
        # Create window
        abWin = cmds.window('luxGuiAbout', title="Lux Render Exporter",
                                  height = 128,
                                  width = ((self.lux_GUI_width) + self.lux_GUI_scrollbar_width),
                                  sizeable = False,
                                  resizeToFitChildren = True,
                                  menuBar = False,
                                  minimizeButton = False)
        
        tForm, tFormContainer = self.newFrame(label='About', parent = abWin, collapsable = False, collapsed = False)
        
        abStrings = [
                     'LuxMaya v%s By Doug Hammond' % self.VERSION,
                     '',
                     'Released under the GPLv3 License',
                     '',
                     'Check the LuxRender website for latest release info and support:',
                     '',
                     'http://www.luxrender.net/'
                     ]
        
        tRows = {}
        for i, string in enumerate(abStrings):
            tRows[i] = self.newRow(parent = tForm, numberOfColumns = 1)
            self.newText(label = string, parent = tRows[i], addColon = False, width = ((self.lux_GUI_width) + self.lux_GUI_scrollbar_width) )
            self.endRow()
        
        self.endFrame()
        cmds.showWindow( 'luxGuiAbout' )
    
    # OTHER COMMANDS
    
    def goBatch(self, *args):
        """
        Start the export process
        """
        
        lb = luxbatch()
        lb.doIt()
    
    # module debug command
    def dprint(self, str):
        if (self.debug):
            print str
