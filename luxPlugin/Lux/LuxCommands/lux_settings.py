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
# lux_settings script node builder
#
# ------------------------------------------------------------------------------

import os
os.altsep = '/'
from maya import OpenMaya
from maya import cmds

class lux_settings:
    """
    Class to create the lux_settings scriptnode in the scene
    """

    # IMPORTANT!! Be sure to update this constant if you make changes to this file
    CURRENT_SC_VERSION = 12

    def addString(self, ln):
        """
        Add a string attribute to the sciptnode
        """
        
        cmds.addAttr( ln = ln, dt = "string" )
        
    def addEnum(self, ln, options, dv = 0):
        """
        Add an enum attribute to the scriptnode
        """
        
        cmds.addAttr( ln = ln, at = 'enum', enumName = options, dv = dv )
        
    def addShort(self, ln, dv = 0, min = 0, max = 32767):
        """
        Add a short (int16) attribute to the scriptnode
        """
        
        if min != 0 | max != 32767:
            cmds.addAttr( ln = ln, at = 'short', dv = dv, softMaxValue = max, softMinValue = min )
        else:
            cmds.addAttr( ln = ln, at = 'short', dv = dv )
        
    def addLong(self, ln, dv = 0):
        """
        Add a long (int32) attribute to the scriptnode
        """
        
        cmds.addAttr( ln = ln, at = 'long', dv = dv)

    def addFloat(self, ln, dv = 0):
        """
        Add a float attribute to the scripnode
        """
        
        cmds.addAttr( ln = ln, at = 'float', dv = dv)
        
    def addBool(self, ln, dv = 0):
        """
        Add a boolean attribute to the scriptnode
        """
        
        cmds.addAttr( ln = ln, at = 'bool', dv = dv)


    def doIt(self, args):
        """
        Class entry point.
        Detect if the node already exists:
            yes, then perform an upgrade, if necessary.
            no, then create a new scriptnode. 
        """
        
        if cmds.objExists('lux_settings'):
            old_lux_settings_version = cmds.getAttr( 'lux_settings.version' )
            
            # implement script node upgrade here:
            if old_lux_settings_version < self.CURRENT_SC_VERSION:
                
                OpenMaya.MGlobal.displayInfo( 'Lux: Settings node has changed, upgrading...' )

                # Rename the existing lux_settings to lux_settings_old or somethings,
                # create the new lux_settings, and then clone all the attribute
                # values from the old node into the new. :)
                # This way we don't even have to worry about what version they
                # are going from/to... effectively the upgrade from any version
                # happens all at once :)
                
                cmds.rename( 'lux_settings', 'lux_settings_v%i' % old_lux_settings_version )
                
                self.createNewScriptNode()
                
                newAttrs = cmds.listAttr( 'lux_settings' )
                
                for attr in cmds.listAttr( 'lux_settings_v%i' % old_lux_settings_version ):
                    if  attr not in ('message', 'caching', 'isHistoricallyInteresting', 'nodeState', 'binMembership', 'before', 'after', 'scriptType', 'version') \
                    and attr in newAttrs:
                        aType = cmds.getAttr( 'lux_settings_v%i.%s' % (old_lux_settings_version, attr) , type = True )
                        if aType in ('string'):
                            cmds.setAttr( 'lux_settings.%s' % attr, cmds.getAttr( 'lux_settings_v%i.%s' % (old_lux_settings_version,attr) ), type = aType )
                        else:
                            cmds.setAttr( 'lux_settings.%s' % attr, cmds.getAttr( 'lux_settings_v%i.%s' % (old_lux_settings_version,attr) ) )
                            
                        
                cmds.delete('lux_settings_v%i' % old_lux_settings_version )
            
            OpenMaya.MGlobal.executeCommand('updateAE lux_settings')
        else:
            OpenMaya.MGlobal.displayInfo( 'Lux: No settings node found, creating...' )
            self.createNewScriptNode()
            
    def createNewScriptNode(self):
        """
        Create a new lux_settings scriptnode
        """
        
        cmds.createNode( 'script', name = 'lux_settings' )
        
        # Keep a track of changes to lux_settings with a hidden version number
        cmds.addAttr( writable = False, hidden = True, ln = "version", at = "short", dv = self.CURRENT_SC_VERSION, min = 1 )
        
        # File paths / scene settings
        self.addString( ln = "lux_path" )
        self.addString( ln = "scene_path" )
        self.addString( ln = "scene_filename" )
        self.addBool  ( ln = "scene_collect_texture", dv = 0 )
        self.addBool  ( ln = "scene_collect_bump", dv = 0 )
        self.addBool  ( ln = "scene_collect_hdri", dv = 0 )
        
        # self.addBool(ln = 'scene_export_lights' , dv = 1)
        self.addBool(ln = 'scene_export_materials' , dv = 1)
        self.addBool(ln = 'scene_export_meshes' , dv = 1)
        self.addBool(ln = 'scene_export_nurbs' , dv = 0)
        self.addBool(ln = 'scene_export_volumes' , dv = 0)
        
        self.addBool(ln = 'scene_reverse_gamma', dv = 1)
        self.addBool(ln = 'scene_clamp_color', dv = 1)
        
        # Camera settings
        self.addFloat ( ln = 'camera_exposuretime', dv = 1 )
        self.addEnum  ( ln = 'camera_persptype', options = 'Perspective:Environment') #:Realistic' )
        self.addBool  ( ln = 'camera_autofocus', dv = 0 )
        
        # Renderer settings
        self.addEnum ( ln = 'pixel_sampler', options = 'Random:Low Discrepancy:Halton:Metropolis:erpt', dv = 1 )
        #  pixel sampler settings
        self.addShort( ln = 'pixel_sampler_xsamples', dv = 2 )
        self.addShort( ln = 'pixel_sampler_ysamples', dv = 2 )
        self.addEnum ( ln = 'pixel_sampler_pixelsampler', options = 'Linear:Vegas:Lowdiscrepancy:Tile:Random', dv = 2 )
        self.addShort( ln = 'pixel_sampler_pixelsamples', dv = 4 )
        self.addLong ( ln = 'pixel_sampler_initsamples', dv = 100000 )
        self.addLong ( ln = 'pixel_sampler_maxconsecrejects', dv = 128 )
        self.addFloat( ln = 'pixel_sampler_largemutationprob', dv = 0.25 )
        # disabled at request of radiance
        #self.addFloat( ln = 'pixel_sampler_mutationrange', dv = 43 )
        self.addLong ( ln = 'pixel_sampler_chainlength', dv = 2000 )
        self.addBool ( ln = 'pixel_sampler_usevariance', dv = 0 )
        
        self.addEnum ( ln = 'pixel_filter', options = 'Mitchell:Gaussian:Sinc:Triangle:Box', dv = 1 )
        #  pixel filter settings
        self.addFloat( ln = 'pixel_filter_xwidth', dv = 2 )
        self.addFloat( ln = 'pixel_filter_ywidth', dv = 2 )
        self.addFloat( ln = 'pixel_filter_alpha', dv = 2 )
        self.addFloat( ln = 'pixel_filter_b', dv = 0.333333 )
        self.addFloat( ln = 'pixel_filter_c', dv = 0.333333 )
        self.addFloat( ln = 'pixel_filter_tau', dv = 3 )
        
        self.addEnum ( ln = 'accelerator', options = 'Kdtree:Grid:Unsafekdtree:None' )
        #  accelerator settings
        self.addBool ( ln = 'accelerator_refineimmediately' )
        self.addShort( ln = 'accelerator_intersectcost', dv = 80 )
        self.addShort( ln = 'accelerator_traversalcost', dv = 1 )
        self.addFloat( ln = 'accelerator_emptybonus', dv = 0.2 )
        self.addLong ( ln = 'accelerator_maxprims', dv = 1 )
        self.addLong ( ln = 'accelerator_maxdepth', dv = -1 )
        
        self.addEnum ( ln = 'surface_integrator', options = 'Bidirectional:Directlighting:Particletracing:Path:Exphotonmap', dv = 3)
        #  Surface integrator settings
        self.addShort( ln = 'surface_integrator_eyemaxdepth', dv = 8 )
        self.addShort( ln = 'surface_integrator_lightmaxdepth', dv = 8 )
        self.addFloat( ln = 'surface_integrator_maxdepth', dv = 12 )
        self.addEnum ( ln = 'surface_integrator_strategy', options = 'All:One' )
        self.addFloat( ln = 'surface_integrator_rrcontinueprob', dv = 0.65 )
        self.addLong ( ln = 'surface_integrator_causticphotons', dv = 20000 )
        self.addLong ( ln = 'surface_integrator_indirectphotons', dv = 100000 )
        self.addLong ( ln = 'surface_integrator_nused', dv = 50 )
        self.addBool ( ln = 'surface_integrator_finalgather', dv = 1 )
        self.addLong ( ln = 'surface_integrator_finalgathersamples', dv = 32 )
        self.addFloat( ln = 'surface_integrator_maxdist', dv = 0.1 )
        # self.addFloat( ln = 'rrthreshold' ) # UNUSED ?!
        self.addFloat( ln = 'surface_integrator_gatherangle', dv = 10.0)
        
        self.addEnum ( ln = 'volume_integrator', options = 'Emission:Single', dv = 1 )
        #  volume integrator settings
        self.addFloat( ln = 'volume_integrator_stepsize', dv = 1 )
        
        
        # Film Settings
        self.addEnum ( ln = 'film', options = 'Fleximage' )
        #  fleximage settings
        # xresolution is set by exporter
        # yresolution is set by exporter
        # filename is set by exporter
        self.addFloat( ln = 'film_cropwindowXmin', dv = 0 )
        self.addFloat( ln = 'film_cropwindowXmax', dv = 1 )
        self.addFloat( ln = 'film_cropwindowYmin', dv = 0 )
        self.addFloat( ln = 'film_cropwindowYmax', dv = 1 )
        self.addFloat( ln = 'film_gamma', dv = 2.2 )
        self.addBool ( ln = 'film_premultiplyalpha', dv = 1 )
        self.addBool ( ln = 'film_write_tonemapped_exr', dv = 1 )
        self.addBool ( ln = 'film_write_tonemapped_igi' )
        self.addBool ( ln = 'film_write_tonemapped_tga', dv = 1 )
        self.addBool ( ln = 'film_write_untonemapped_exr' )
        self.addBool ( ln = 'film_write_untonemapped_igi' )
        self.addBool ( ln = 'film_write_resume_film' )
        self.addShort( ln = 'film_writeinterval', dv = 60 )
        self.addShort( ln = 'film_displayinterval', dv = 12 )
        self.addShort( ln = 'film_reject_warmup', dv = 12 )
        self.addFloat( ln = 'film_reinhard_prescale', dv = 1.0 )
        self.addFloat( ln = 'film_reinhard_postscale', dv = 1.0 )
        self.addFloat( ln = 'film_reinhard_burn', dv = 6.0 )
        
        # Process settings
        self.addBool ( ln = 'render_launch' )
        self.addBool ( ln = 'render_animation' )
        self.addEnum ( ln = 'render_interface', options = "GUI:Console" )
        self.addShort( ln = 'render_threads', min = 1, max = 32, dv = 1 )
        self.addEnum ( ln = 'render_priority', options = "REALTIME:HIGH:ABOVENORMAL:NORMAL:BELOWNORMAL:LOW", dv = 4 )
        
        lux_settings.setScriptNodeDefaultPaths()
        
    @staticmethod
    def setScriptNodeDefaultPaths(args = ''):
        """
        Set the default path values in the scriptnode
        """
        
        lsp = os.getenv('LUX_SEARCHPATH')
        cmds.setAttr( 'lux_settings.lux_path', lsp, type='string' )
        cmds.setAttr( 'lux_settings.scene_path', '%slux%s' % ( cmds.workspace( q = True, rootDirectory = True), os.altsep ), type='string' )
        cmds.setAttr( 'lux_settings.scene_filename', 'myScene', type='string' )