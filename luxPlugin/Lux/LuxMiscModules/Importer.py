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
# Converter: Lux DB format data -> Maya converter
#
# ------------------------------------------------------------------------------
import types
from maya import OpenMaya
from Lux.LuxNodes.luxshader import luxshader
from Lux.LuxNodes.ShaderNodes import *
from Lux.LuxNodes.TextureNodes import *

class Importer:
    """
    Imports DB format dict (as string) to Maya nodes
    """
    
    shader_type_map = {
        'carpaint': carpaintShader.carpaintShader,
        'glass': glassShader.glassShader,
        'glossy': glossyShader.glossyShader,
        'matte': matteShader.matteShader,
        'mattetranslucent': mattetranslucentShader.mattetranslucentShader,
        'metal': metalShader.metalShader,
        'mirror': mirrorShader.mirrorShader,
        'mix': mixShader.mixShader,
        'null': nullShader.nullShader,
        'roughglass': roughglassShader.roughglassShader,
        'shinymetal': shinymetalShader.shinymetalShader,
    }
    
    texture_type_map = {
        'bilerp': bilerpTexture.bilerpTexture,
        'blackbody': blackbodyTexture.blackbodyTexture,
        'blenderBlend': blenderBlendTexture.blenderBlendTexture,
        'blender_clouds': blenderCloudsTexture.blenderCloudsTexture,
        'blenderDistortednoise': blenderDistortednoiseTexture.blenderDistortednoiseTexture,
        'blenderMagic': blenderMagicTexture.blenderMagicTexture,
        'blenderMarble': blenderMarbleTexture.blenderMarbleTexture,
        'blenderMusgrave': blenderMusgraveTexture.blenderMusgraveTexture,
        'blenderNoise': blenderNoiseTexture.blenderNoiseTexture,
        'blenderStucci': blenderStucciTexture.blenderStucciTexture,
        'blenderVoronoi': blenderVoronoiTexture.blenderVoronoiTexture,
        'blender_wood': blenderWoodTexture.blenderWoodTexture,
        #'brick': brickTexture.brickTexture,        # WTF is wrong with this ?
        'constant': constantTexture.constantTexture,
        'checkerboard2d': checkerboard2dTexture.checkerboard2dTexture,
        'checkerboard3d': checkerboard3dTexture.checkerboard3dTexture,
        'dots': dotsTexture.dotsTexture,
        'equalenergy': equalenergyTexture.equalenergyTexture,
        'fbm': fbmTexture.fbmTexture,
        'frequency': frequencyTexture.frequencyTexture,
        'gaussian': gaussianTexture.gaussianTexture,
        'marble': marbleTexture.marbleTexture,
        'mix': mixTexture.mixTexture,
        'scale': scaleTexture.scaleTexture,
        'windy': windyTexture.windyTexture,
        'wrinkled': wrinkledTexture.wrinkledTexture,
    }
    
    @staticmethod
    def getMatTex(mat, basekey, tex):
        pass
    
    @staticmethod
    def MatTex2dict(mattex, tex = False):
        pass
    
    @staticmethod
    def Import(str):
        dict_info = Importer.str2MatTex(str)
        if dict_info['type'] == 'material':
            Importer.ImportMaterial(dict_info['name'], dict_info['definition'])
    
    @staticmethod
    def ImportMaterial(name, m, connectTo = None, connectFrom = None):
        new_dagnode = OpenMaya.MFnDependencyNode()
        new_shader = new_dagnode.create(luxshader.nodeId(), name)
        name = OpenMaya.MFnDependencyNode(new_shader).name()
         
        shader_object = Importer.shader_type_map[m['type']]()
        
        useable_attrs = {}
        for attr in m.keys():
            if attr[0] == ':':
                useable_attrs[attr[1:]] = m[attr]
        
        print 'material %s is a %s and has useable attributes:' % (name, shader_object.luxType)
        for attr in shader_object.attributes.keys():
            attr = attr.lower()
            if attr in useable_attrs.keys():
                print '\t%s: %s' % (attr, useable_attrs[attr])
                Importer.DetectTexture(name, attr, useable_attrs)
                
    @staticmethod
    def DetectTexture(name, attr, useable_attrs):
        if attr+'.texture' in useable_attrs:
            print '\tTextured: %s' % useable_attrs[attr+'.texture']
            future_attrs = {}
            key_len = len(attr)+1
            for fattr in useable_attrs.keys():
                if fattr[:key_len] == attr+':':
                    future_attrs[fattr[key_len:]] = useable_attrs[fattr]
            Importer.ImportTexture(name+'-'+attr, useable_attrs[attr+'.texture'], future_attrs)
        
    @staticmethod            
    def ImportTexture(name, type, m, connectTo = None, connectFrom = None):
        print '%s texture node %s' % (type, name)
        
        texture_object = Importer.texture_type_map[type]()
        
        for attr in texture_object.attributes.keys():
            attr = attr.lower()
            #print '\t%s: %s' % (attr, m[attr])
            Importer.DetectTexture(name, attr, m)
        
    
    @staticmethod
    def str2MatTex(s):    # todo: this is not absolutely save from attacks!!!
        
        s = s.strip()
        if (s[0]=='{') and (s[-1]=='}'):
            d = eval(s, dict(__builtins__=None,True=True,False=False))
            if type(d)==types.DictType:
                    
                def lb_list_to_dict(list):
                    d = {}
                    for t, k, v in list:
                        if t == 'float':
                            v = float(v)
                            
                        d[k.lower()] = v
                    return d
                
                if   ('version' in d.keys() and d['version'] in ['0.6', '0.7']) \
                and  ('type' in d.keys() and d['type'] in ['material', 'texture']) \
                and  ('definition' in d.keys()):
                    try:
                        definition = d
                        definition['definition'] = lb_list_to_dict(d['definition'])
                        
                        if 'metadata' in d.keys():
                            definition['metadata'] = lb_list_to_dict(d['metadata'])
                        
                        return definition
                    except:
                        reason = 'Incorrect LBX definition data'
                else: 
                    reason = 'Missing/incorrect metadata'
            else:
                reason = 'Not a parsed dict'
        else:
            reason = 'Not a stored dict'
                
                
        print "ERROR: string to material/texture conversion failed: %s" % reason
        return None
    