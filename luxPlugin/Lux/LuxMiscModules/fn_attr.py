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
# fn_attr: a class of static functions to list and apply AE presets to a node
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import cmds
from maya import mel
import os
os.altsep = '/'

class fn_attr:
    """
    Helper class for finding attribute presets and reading them
    """
    
    @staticmethod
    def applyAttrPreset(node, presetName, blend):
        """
        Apply the named preset to the given node.
        """
        
        gAEAttrPresetCurrentTarget = mel.eval('$tmpVar=$gAEAttrPresetCurrentTarget;')
        gAEAttrPresetBlend = mel.eval('$tmpVar=$gAEAttrPresetBlend;')
        
        ntype = cmds.nodeType( node )
        ppath = cmds.internalVar( userPrefDir = True )
        
        if presetName[-4:] == ".mel":
            ppath = presetName
        else:
            ppath = ppath.replace('prefs','presets/attrPresets')
            ppath = '%s%s%s%s.mel' % ( ppath, ntype, os.altsep, presetName )
            
        if os.path.exists(ppath):
            mel.eval('$gAEAttrPresetCurrentTarget = "%s"' % node)
            mel.eval('$gAEAttrPresetBlend = "%s"' % blend)
            mel.eval('source "%s"' % ppath)
        else:
            OpenMaya.MGlobal.displayWarning('No preset named %s for nodeType %s. Looked in: %s' % (presetName, ntype, ppath) )
            
    @staticmethod
    def findAttrPresets(node):
        """
        Build a list of attribute presets for the given node
        (the node's type is determined first)
        """
        
        attrList = []
        
        ntype = cmds.nodeType( node )
        ppath = cmds.internalVar( userPrefDir = True )
        ppath = ppath.replace('prefs','presets/attrPresets')
        ppath = ppath + ntype + "/"
            
        if os.path.exists(ppath):
            attrListT = os.listdir(ppath)
            for attr in attrListT:
                attrList.append(attr.replace('.mel',''))
        
        return attrList