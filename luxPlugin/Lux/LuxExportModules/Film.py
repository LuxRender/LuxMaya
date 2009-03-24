# ------------------------------------------------------------------------------
# Lux exporter python script plugin for Maya
#
# by Doug Hammond 05/2008
#
# This file is licensed under the GPL
# http://www.gnu.org/licenses/gpl-3.0.txt
#
# $Id$
#
# ------------------------------------------------------------------------------
#
# Film settings export module
#
# ------------------------------------------------------------------------------

from ExportModule import ExportModule

from maya import cmds

class Film(ExportModule):
    """
    Lux "Film" ExportModule. Responsible for getting the scene's Film settings.
    """
    
    def __init__(self, nWidth, nHeight, nImageName):
        """
        Constructor. Set's up this object with required data.
        """
        
        self.width = nWidth
        self.height = nHeight
        self.imageName = nImageName
        
    def getOutput(self):
        """
        Append this module's output to the scene file buffer.
        """
                
        # Get vars
        # TODO crop window could come from defaultRenderGlobals
        cx1             = cmds.getAttr( 'lux_settings.film_cropwindowXmin' )
        cx2             = cmds.getAttr( 'lux_settings.film_cropwindowXmax' )
        cy1             = cmds.getAttr( 'lux_settings.film_cropwindowYmin' )
        cy2             = cmds.getAttr( 'lux_settings.film_cropwindowYmax' )
        gamma           = cmds.getAttr( 'lux_settings.film_gamma' )
        prealpha        = self.intToBoolString( cmds.getAttr( 'lux_settings.film_premultiplyalpha' ) )
        
        tm_exr          = self.intToBoolString( cmds.getAttr( 'lux_settings.film_write_tonemapped_exr' ) )
        tm_igi          = self.intToBoolString( cmds.getAttr( 'lux_settings.film_write_tonemapped_igi' ) )
        tm_tga          = self.intToBoolString( cmds.getAttr( 'lux_settings.film_write_tonemapped_tga' ) )
        utm_exr         = self.intToBoolString( cmds.getAttr( 'lux_settings.film_write_untonemapped_exr' ) )
        utm_igi         = self.intToBoolString( cmds.getAttr( 'lux_settings.film_write_untonemapped_igi' ) )
        resume          = self.intToBoolString( cmds.getAttr( 'lux_settings.film_write_resume_film' ) )
        restart         = self.intToBoolString( cmds.getAttr( 'lux_settings.film_restart_resume_film' ) )
        
        tm              = cmds.getAttr( 'lux_settings.film_tonemapping', asString = True ).lower()
        
        r_autoywa       = self.intToBoolString( cmds.getAttr( 'lux_settings.film_reinhard_autoywa' ) )
        r_ywa           = cmds.getAttr( 'lux_settings.film_reinhard_ywa' )
        r_prescale      = cmds.getAttr( 'lux_settings.film_reinhard_prescale' )
        r_postscale     = cmds.getAttr( 'lux_settings.film_reinhard_postscale' )
        r_burn          = cmds.getAttr( 'lux_settings.film_reinhard_burn' )
        
        l_sensitivity   = cmds.getAttr( 'lux_settings.film_linear_sensitivity' )
        l_exposure      = cmds.getAttr( 'lux_settings.film_linear_exposure' )
        l_fstop         = cmds.getAttr( 'lux_settings.film_linear_fstop' )
        l_gamma         = cmds.getAttr( 'lux_settings.film_linear_gamma' )
        
        c_ywa           = cmds.getAttr( 'lux_settings.film_contrast_ywa' )
        
        writeinterval   = cmds.getAttr( 'lux_settings.film_writeinterval' )
        displayinterval = cmds.getAttr( 'lux_settings.film_displayinterval' )
        reject_warmup   = cmds.getAttr( 'lux_settings.film_reject_warmup' )
        
        haltspp         = cmds.getAttr( 'lux_settings.film_haltspp' )
        
        cs_wx           = cmds.getAttr( 'lux_settings.film_colourspace_white_x' )
        cs_wy           = cmds.getAttr( 'lux_settings.film_colourspace_white_y' )
        cs_rx           = cmds.getAttr( 'lux_settings.film_colourspace_red_x' )
        cs_ry           = cmds.getAttr( 'lux_settings.film_colourspace_red_y' )
        cs_gx           = cmds.getAttr( 'lux_settings.film_colourspace_green_x' )
        cs_gy           = cmds.getAttr( 'lux_settings.film_colourspace_green_y' )
        cs_bx           = cmds.getAttr( 'lux_settings.film_colourspace_blue_x' )
        cs_by           = cmds.getAttr( 'lux_settings.film_colourspace_blue_y' )
        
        # send to Film output
        self.addToOutput( 'Film "fleximage"' )
        self.addToOutput( '\t"integer xresolution" [%i]' % self.width )
        self.addToOutput( '\t"integer yresolution" [%i]' % self.height )
        self.addToOutput( '\t"string filename" ["%s"]' % self.imageName )
        
        self.addToOutput( '\t"float cropwindow" [%f %f %f %f]' % ( cx1, cx2, cy1, cy2 ) )
        self.addToOutput( '\t"bool premultiplyalpha" ["%s"]' % prealpha )
        
        self.addToOutput( '\t"bool write_tonemapped_exr" ["%s"]' % tm_exr )
        self.addToOutput( '\t"bool write_tonemapped_igi" ["%s"]' % tm_igi )
        self.addToOutput( '\t"bool write_tonemapped_tga" ["%s"]' % tm_tga )
        self.addToOutput( '\t"bool write_untonemapped_exr" ["%s"]' % utm_exr )
        self.addToOutput( '\t"bool write_untonemapped_igi" ["%s"]' % utm_igi )
        
        self.addToOutput( '\t"bool write_resume_flm" ["%s"]' % resume )
        self.addToOutput( '\t"bool restart_resume_flm" ["%s"]' % restart )
        
        if tm == 'reinhard':
            self.addToOutput( '\t"string tonemapkernel" ["reinhard"]' )
            
            if r_autoywa == 'false':
                self.addToOutput( '\t"float reinhard_ywa" [%f]'  % r_ywa )
            self.addToOutput( '\t"float reinhard_prescale" [%f]'  % r_prescale )
            self.addToOutput( '\t"float reinhard_postscale" [%f]' % r_postscale )
            self.addToOutput( '\t"float reinhard_burn" [%f]' % r_burn )
            
        elif tm == 'linear':
            self.addToOutput( '\t"string tonemapkernel" ["linear"]' )
            self.addToOutput( '\t"float linear_sensitivity" [%f]'  % l_sensitivity )
            self.addToOutput( '\t"float linear_exposure" [%f]'  % l_exposure )
            self.addToOutput( '\t"float linear_fstop" [%f]'  % l_fstop )
            self.addToOutput( '\t"float linear_gamma" [%f]'  % l_gamma )
            
        elif tm == 'contrast':
            self.addToOutput( '\t"string tonemapkernel" ["contrast"]' )
            self.addToOutput( '\t"float contrast_ywa" [%f]'  % c_ywa )
            
        elif tm == 'maxwhite':
            self.addToOutput( '\t"string tonemapkernel" ["maxwhite"]' )
        
        self.addToOutput( '\t"integer writeinterval" [%i]' % writeinterval )
        self.addToOutput( '\t"integer displayinterval" [%i]' % displayinterval )
        self.addToOutput( '\t"integer reject_warmup" [%i]' % reject_warmup )
        
        self.addToOutput( '\t"float colorspace_white" [%f %f]' % (cs_wx, cs_wy) )
        self.addToOutput( '\t"float colorspace_red" [%f %f]'   % (cs_rx, cs_ry) )
        self.addToOutput( '\t"float colorspace_green" [%f %f]' % (cs_gx, cs_gy) )
        self.addToOutput( '\t"float colorspace_blue" [%f %f]'  % (cs_bx, cs_by) )
        
        self.addToOutput( '\t"float gamma" [%f]' % gamma )
        
        self.addToOutput( '\t"integer haltspp" [%i]' % haltspp )
        
        self.addToOutput( '' )
    #end def getOutput