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
from maya import cmds
from Lux.LuxNodes.luxshader import luxshader

from Lux import Registry as LR

class Importer:
    """
    Imports DB format dict (as string) to Maya nodes
    """
 
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
        new_shader = OpenMaya.MFnDependencyNode(new_shader)
        name = new_shader.name()
         
        shader_object = LR.Materials().alt_names[m['type']]()
        
        useable_attrs = {}
        for attr in m.keys():
            if attr[0] == ':':
                useable_attrs[attr[1:]] = m[attr]
        
        print 'material %s is a %s and has useable attributes:' % (name, shader_object.luxType)
        for attr in shader_object.attributes.keys():
            attr_l = attr.lower()
            if attr_l in useable_attrs.keys():
                print '\t%s: %s' % (shader_object.attributes[attr].plugName, useable_attrs[attr_l])
                Importer.DetectTexture(name, attr_l, useable_attrs, new_shader, shader_object.attributes[attr].plugName)
                
    @staticmethod
    def DetectTexture(name, attr, useable_attrs, dest_object, dest_attr):
        if attr+'.texture' in useable_attrs:
            print '\tTextured: %s' % useable_attrs[attr+'.texture']
            future_attrs = {}
            key_len = len(attr)+1
            for fattr in useable_attrs.keys():
                if fattr[:key_len] in [attr+':', attr+'.']:
                    future_attrs[fattr[key_len:]] = useable_attrs[fattr]
            Importer.ImportTexture(name+'_'+attr, useable_attrs[attr+'.texture'], future_attrs, dest_object, dest_attr)
        
    @staticmethod            
    def ImportTexture(name, type, m, connectFromNode = None, connectFromAttr = None):
        new_dagnode = OpenMaya.MFnDependencyNode()
        texture_object = LR.Textures().alt_names[type]()
        
        new_texture = new_dagnode.create(texture_object.nodeId(), name)
        new_texture = OpenMaya.MFnDependencyNode(new_texture)
        name = new_texture.name()
        
        if connectFromNode is not None and connectFromAttr is not None:
            try:
                cmds.connectAttr(name + '.outColor', connectFromNode.name() + '.' + connectFromAttr)
            except RuntimeError: # incompatible connection, possible trying to connect colour to float...
                try:
                    # ... so try to connect a float value ...
                    cmds.connectAttr(name + '.outAlpha', connectFromNode.name() + '.' + connectFromAttr)
                except:
                    # ... else fail
                    raise
        
        print '%s texture node %s (connect to %s.%s)' % (type, name, connectFromNode.name(), connectFromAttr)
        
        for attr in m.keys():
            print "\t%s: %s" % (attr, m[attr])

        print "\t-"
        for attr_m in texture_object.attributes.keys():
            attr = attr_m.lower()
            print "\t%s (%s): %s" % (attr, texture_object.attributes[attr_m].plugName, texture_object.attributes[attr_m])
            if attr in m.keys():
                print "\t -> attr also in m, setting value"
                texture_object.attributes[attr_m].setValue(name+'.'+attr, m[attr])
            
            Importer.DetectTexture(name, attr, m, new_texture, texture_object.attributes[attr_m].plugName)
        
    
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
    