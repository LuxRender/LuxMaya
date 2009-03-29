# ------------------------------------------------------------------------------
# Custom Class Registry and Loader
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
# Once upon a time there were several files in LuxMaya that imported all of the
# custom node classes etc, and keeping them in sync was difficult when adding a
# new module/class or node or whatever.
#
# Registry holds all of the Lux imports and provides factories to use them.
#
# ------------------------------------------------------------------------------

import sys, types
from maya import OpenMayaMPx

class reg_factory:
    maya_type = None
    name_suffix = ''
    names = []
    
    def all(self):
        out = {}
        for item in self.names.values():
            out[item] = self.maya_type
        return out
    
    def list_all(self):
        return self.names.values()
    
    def alt_list_all(self):
        return self.alt_names.values()

class Textures(reg_factory):
    maya_type = OpenMayaMPx.MPxNode.kDependNode
    #name_suffix = 'Texture'
    
    def __init__(self):
        from Lux.LuxNodes.TextureNodes.bilerpTexture import bilerpTexture
        from Lux.LuxNodes.TextureNodes.blackbodyTexture import blackbodyTexture
        from Lux.LuxNodes.TextureNodes.blenderBlendTexture import blenderBlendTexture
        from Lux.LuxNodes.TextureNodes.blenderCloudsTexture import blenderCloudsTexture
        from Lux.LuxNodes.TextureNodes.blenderDistortednoiseTexture import blenderDistortednoiseTexture
        from Lux.LuxNodes.TextureNodes.blenderMagicTexture import blenderMagicTexture
        from Lux.LuxNodes.TextureNodes.blenderMarbleTexture import blenderMarbleTexture
        from Lux.LuxNodes.TextureNodes.blenderMusgraveTexture import blenderMusgraveTexture
        from Lux.LuxNodes.TextureNodes.blenderNoiseTexture import blenderNoiseTexture
        from Lux.LuxNodes.TextureNodes.blenderStucciTexture import blenderStucciTexture
        from Lux.LuxNodes.TextureNodes.blenderVoronoiTexture import blenderVoronoiTexture
        from Lux.LuxNodes.TextureNodes.blenderWoodTexture import blenderWoodTexture
        from Lux.LuxNodes.TextureNodes.brickTexture import brickTexture
        from Lux.LuxNodes.TextureNodes.checkerboard2dTexture import checkerboard2dTexture
        from Lux.LuxNodes.TextureNodes.checkerboard3dTexture import checkerboard3dTexture
        from Lux.LuxNodes.TextureNodes.constantTexture import constantTexture
        from Lux.LuxNodes.TextureNodes.dotsTexture import dotsTexture
        from Lux.LuxNodes.TextureNodes.equalenergyTexture import equalenergyTexture
        from Lux.LuxNodes.TextureNodes.fbmTexture import fbmTexture
        from Lux.LuxNodes.TextureNodes.frequencyTexture import frequencyTexture
        from Lux.LuxNodes.TextureNodes.gaussianTexture import gaussianTexture
        from Lux.LuxNodes.TextureNodes.marbleTexture import marbleTexture
        from Lux.LuxNodes.TextureNodes.mixTexture import mixTexture
        from Lux.LuxNodes.TextureNodes.scaleTexture import scaleTexture
        from Lux.LuxNodes.TextureNodes.windyTexture import windyTexture
        from Lux.LuxNodes.TextureNodes.wrinkledTexture import wrinkledTexture
        
        self.names = {
            'bilerp': bilerpTexture,
            'blackbody': blackbodyTexture,
            'blenderBlend': blenderBlendTexture,
            'blenderClouds': blenderCloudsTexture,
            'blenderDistortednoise': blenderDistortednoiseTexture,
            'blenderMagic': blenderMagicTexture,
            'blenderMarble': blenderMarbleTexture,
            'blenderMusgrave': blenderMusgraveTexture,
            'blenderNoise': blenderNoiseTexture,
            'blenderStucci': blenderStucciTexture,
            'blenderVoronoi': blenderVoronoiTexture,
            'blenderWood': blenderWoodTexture,
            'brick': brickTexture,
            # bumpmap
            'checkerboard2d': checkerboard2dTexture,
            'checkerboard3d': checkerboard3dTexture,
            'constant': constantTexture,
            'dots': dotsTexture,
            'equalenergy': equalenergyTexture,
            'fbm': fbmTexture,
            # file
            'frequency': frequencyTexture,
            'gaussian': gaussianTexture,
            'marble': marbleTexture,
            'mix': mixTexture,
            'scale': scaleTexture,
            'windy': windyTexture,
            'wrinkled': wrinkledTexture,
        }
        
        self.alt_names = self.names
        self.alt_names.update({
	        'blender_blend': blenderBlendTexture,
	        'blender_clouds': blenderCloudsTexture,
	        'blender_distortednoise': blenderDistortednoiseTexture,
	        'blender_magic': blenderMagicTexture,
	        'blender_marble': blenderMarbleTexture,
	        'blender_musgrave': blenderMusgraveTexture,
	        'blender_noise': blenderNoiseTexture,
	        'blender_stucci': blenderStucciTexture,
	        'blender_voronoi': blenderVoronoiTexture,
	        'blender_wood': blenderWoodTexture,
	    })


class Shaders(reg_factory):
    maya_type = OpenMayaMPx.MPxNode.kDependNode
    
    def __init__(self):
        from Lux.LuxNodes.luxshader import luxshader
        self.names = {
            'luxshader': luxshader
        }
    
class Locators(reg_factory):
    maya_type = OpenMayaMPx.MPxNode.kLocatorNode
    
    def __init__(self):
        from Lux.LuxNodes.luxObjectLocator import luxObjectLocator
        from Lux.LuxNodes.luxEnvironmentLight import luxEnvironmentLight
        from Lux.LuxNodes.luxSunsky import luxSunsky
        self.names = {
            'luxObjectLocator': luxObjectLocator,
            'luxEnvironmentLight': luxEnvironmentLight,
            'luxSunsky': luxSunsky,
        }

# this one is used differently. not used for module loading, but in Importer.
class Materials(reg_factory):
    #name_suffix = 'Shader'
    
    def __init__(self):
        from Lux.LuxNodes.ShaderNodes.carpaintShader import carpaintShader    
        from Lux.LuxNodes.ShaderNodes.glassShader import glassShader    
        from Lux.LuxNodes.ShaderNodes.glossyShader import glossyShader    
        from Lux.LuxNodes.ShaderNodes.matteShader import matteShader    
        from Lux.LuxNodes.ShaderNodes.mattetranslucentShader import mattetranslucentShader    
        from Lux.LuxNodes.ShaderNodes.metalShader import metalShader    
        from Lux.LuxNodes.ShaderNodes.mirrorShader import mirrorShader    
        from Lux.LuxNodes.ShaderNodes.mixShader import mixShader    
        from Lux.LuxNodes.ShaderNodes.nullShader import nullShader    
        from Lux.LuxNodes.ShaderNodes.roughglassShader import roughglassShader    
        from Lux.LuxNodes.ShaderNodes.shinymetalShader import shinymetalShader    
    
        self.names = {
            'carpaint': carpaintShader,
            'glass': glassShader,
            'glossy': glossyShader,
            'matte': matteShader,
            'mattetranslucent': mattetranslucentShader,
            'metal': metalShader,
            'mirror': mirrorShader,
            'mix': mixShader,
            'null': nullShader,
            'roughglass': roughglassShader,
            'shinymetal': shinymetalShader,
        }
        
        self.alt_names = self.names

    
    
# Experimental dynamic module importer, doesn't seem to work
#class dynload:
#    maya_type = None
#    name_suffix = ''
#    names = []
#    
#    @staticmethod
#    def get_mod(modulePath):
#        try:
#            aMod = sys.modules[modulePath]
#            if not isinstance(aMod, types.ModuleType):
#                raise KeyError
#        except KeyError:
#            # The last [''] is very important!
#            aMod = __import__(modulePath, globals(), locals(), [''])
#            sys.modules[modulePath] = aMod
#        return aMod
#    
#    @staticmethod
#    def get_func(fullFuncName):
#        """Retrieve a function object from a full dotted-package name."""
#        
#        # Parse out the path, module, and function
#        lastDot = fullFuncName.rfind(u".")
#        funcName = fullFuncName[lastDot + 1:]
#        modPath = fullFuncName[:lastDot]
#        
#        aMod = dynload.get_mod(modPath)
#        aFunc = getattr(aMod, funcName)
#        
#        # Assert that the function is a *callable* attribute.
#        assert callable(aFunc), u"%s is not callable." % fullFuncName
#        
#        # Return a reference to the function itself,
#        # not the results of the function.
#        return aFunc
#    
#    @staticmethod
#    def get_class(fullClassName, parentClass=None):
#        """Load a module and retrieve a class (NOT an instance).
#    
#       If the parentClass is supplied, className must be of parentClass
#       or a subclass of parentClass (or None is returned).
#       """
#        aClass = dynload.get_func(fullClassName)
#        
#        # Assert that the class is a subclass of parentClass.
#        if parentClass is not None:
#            if not issubclass(aClass, parentClass):
#                raise TypeError(u"%s is not a subclass of %s" %
#                    (fullClassName, parentClass))
#        
#        # Return a reference to the class itself, not an instantiated object.
#        return aClass
#    
#    def name_munge(name):
#        return name+self.name_suffix+'.'
#        #return '%s.%s' % (t_n, t_n)
#    
#    def instance(self, name):
#        if not name in self.names:
#            return None
#        else:
#            return dynload.get_class(self.name_munge(name))()
#
#    def all(self):
#        output = {}
#        for name in self.names:
#            output[dynload.get_class(self.name_munge(name))()] = self.maya_type 
 