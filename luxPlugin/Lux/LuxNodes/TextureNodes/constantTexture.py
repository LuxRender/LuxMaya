# ------------------------------------------------------------------------------
# Lux texture nodes for Maya
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
# Lux Constant Texture node for Maya
#
# ------------------------------------------------------------------------------

import math
from maya import OpenMaya
from maya import OpenMayaMPx

from Lux.LuxNodes.TextureNode import TextureNode


# This is here just so that the importer works or now,
# but it needs to be developed into a proper node
class constantTexture(OpenMayaMPx.MPxNode, TextureNode):
    def __init__(self):
        self.attributes = {}
        self.attributes['value'] = None