# ------------------------------------------------------------------------------
# Lux material shader node for Maya
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
# luxshader: a shader node for Maya which defines all available lux materal types
# and their available parameters
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx

from ShaderNode						 import ShaderNode

from ShaderNodes.carpaintShader		 import carpaintShader
from ShaderNodes.glassShader			import glassShader
from ShaderNodes.matteShader			import matteShader
from ShaderNodes.mattetranslucentShader import mattetranslucentShader
from ShaderNodes.metalShader			import metalShader
from ShaderNodes.mixShader			  import mixShader
from ShaderNodes.mirrorShader		   import mirrorShader
from ShaderNodes.plasticShader		  import plasticShader
from ShaderNodes.roughglassShader	   import roughglassShader
from ShaderNodes.shinymetalShader	   import shinymetalShader
from ShaderNodes.substrateShader		import substrateShader

from ShaderNodes.arealightShader		import arealightShader

class luxshader(OpenMayaMPx.MPxNode, ShaderNode):
	"""
	Custom lux material shader for Maya.
	This is a single node that contains all material types, although
	the attributes for each type are split into different modules.
	(Also inluded here is AreaLight even though it's not a material)
	
	Each of these modules has two purposes:
	1. Provide attributes for Maya to use
	2. Provide a mapping of Maya attributes -> Lux parameters to be read
	   at export time. 
	"""

	@staticmethod
	def nodeName():
		return "luxshader"

	@staticmethod
	def nodeId():
		return OpenMaya.MTypeId(0x6C757801) # 'lux' 01

	@staticmethod
	def nodeCreator():
		return OpenMayaMPx.asMPxPtr( luxshader() )

	@staticmethod
	def nodeClassify():
		return "shader/surface"

	def __init__(self):
		OpenMayaMPx.MPxNode.__init__(self)

		# 4 generic attributes to set up the shader's internal operation
		iMaterialType		=	OpenMaya.MObject()	# enum
		bumpMap 			=	OpenMaya.MObject()	# point
		outColor			=	OpenMaya.MObject()	# color
		transparency		=   OpenMaya.MObject()	# transparency
		
		# instances of shader types
		carpaint			= carpaintShader()
		glass				= glassShader()
		roughglass			= roughglassShader()
		matte				= matteShader()
		mattetranslucent	= mattetranslucentShader()
		metal				= metalShader()
		mix   				= mixShader()
		shinymetal			= shinymetalShader()
		mirror				= mirrorShader
		plastic 			= plasticShader()
		substrate			= substrateShader()
		
		arealight			= arealightShader()		# not technically a shader


	def compute(self, plug, block):
		if plug == self.outColor or plug.parent() == self.outColor:
			# THIS IS A VERY SIMPLE FLAT COLOUR SHADER.
			# I CAN'T GET THE LAMBERTIAN BIT TO WORK
			
			# THIS IS ALSO VERY SLOW AND MAY BE REMOVED
			
			# choose the appropriate color
			if	 block.inputValue( self.iMaterialType ).asInt() == 0:
				 # carpaint
				 resultColor = block.inputValue( self.carpaint.kd ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 1:
				 # glass
				 resultColor = block.inputValue( self.glass.kt ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 2:
				 # roughglass
				 resultColor = block.inputValue( self.roughglass.kt ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 3:
				 # matte
				 resultColor = block.inputValue( self.matte.kd ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 4:
				 # mattetranslucent
				 resultColor = block.inputValue( self.mattetranslucent.kt ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 5:
				 # metal
				 resultColor = block.inputValue( self.metal.n ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 6:
				 # shinymetal
				 resultColor = block.inputValue( self.shinymetal.ks ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 7:
				 # mirror
				 resultColor = block.inputValue( self.mirror.kr ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 8:
				 # plastic
				 resultColor = block.inputValue( self.plastic.kd ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 9:
				 # substrate
				 resultColor = block.inputValue( self.substrate.kd ).asFloatVector()
			elif block.inputValue( self.iMaterialType ).asInt() == 10:
				 # arealight
				 resultColor = block.inputValue( self.arealight.L ).asFloatVector() # all arealights are 50% transparent
			else:
				resultColor = OpenMaya.MFloatVector(0.0, 0.0, 0.0)

			# set the output as a flat color
			outColorHandle = block.outputValue( self.outColor )
			outColorHandle.setMFloatVector(resultColor)
			outColorHandle.setClean()
		else:
			return OpenMaya.kUnknownParameter

	@staticmethod
	def nodeInitializer():
		nAttr		= OpenMaya.MFnNumericAttribute()
		enumAttr	= OpenMaya.MFnEnumAttribute()

		# reference instances of shader types
		luxshader.carpaint			= carpaintShader()
		luxshader.glass 			= glassShader()
		luxshader.roughglass		= roughglassShader()
		luxshader.matte 			= matteShader()
		luxshader.mattetranslucent	= mattetranslucentShader()
		luxshader.metal 			= metalShader()
		luxshader.mix	 			= mixShader()
		luxshader.shinymetal		= shinymetalShader()
		luxshader.mirror			= mirrorShader()
		luxshader.plastic			= plasticShader()
		luxshader.substrate 		= substrateShader()

		luxshader.arealight			= arealightShader()

		try:
			# set up the base attributes

			# the different material types available herewithin
			luxshader.iMaterialType = enumAttr.create("material", "mat",	0)
			enumAttr.addField( "Carpaint",									0)
			enumAttr.addField( "Glass", 									1)
			enumAttr.addField( "Rough Glass",								2)
			enumAttr.addField( "Matte", 									3)
			enumAttr.addField( "Matte Translucent", 						4)
			enumAttr.addField( "Metal", 									5)
			# hmm out of sequence Enum values have no effect
			enumAttr.addField( "Mix",										11)
			enumAttr.addField( "Null",									  12)
			enumAttr.addField( "Shiny Metal",								6)
			enumAttr.addField( "Mirror",									7)
			enumAttr.addField( "Plastic",									8)
			enumAttr.addField( "Substrate", 								9)
			enumAttr.addField( "Area Light",								10)

			# hidden attribute to allow attaching bump maps, relevant to every material type
			luxshader.bumpMap = nAttr.createPoint("normalCamera","n")
			luxshader.makeInput( nAttr )
			nAttr.setHidden(1)
			nAttr.setDefault(0.0, 0.0, 0.0)

			# a special color attribute for shading purposes
			luxshader.outColor = nAttr.createColor("outColor", "oc")
			nAttr.setKeyable(0)
			nAttr.setStorable(0)
			nAttr.setReadable(1)
			nAttr.setWritable(0)
			
			# this is set by luxshader itself, not the user, according to the material type.
			# the actual setting of this parameter is done in the AETemplate.
			# (I'm using this to make AreaLight objects 50% transparent in the viewport)
			luxshader.transparency = nAttr.createColor("transparency", "t")
			luxshader.makeInput( nAttr )
			nAttr.setHidden(1)
			nAttr.setDefault(0.5, 0.5, 0.5)
			
			# init all the shader attributes
			luxshader.carpaint.shaderInitializer()
			luxshader.glass.shaderInitializer()
			luxshader.roughglass.shaderInitializer()
			luxshader.matte.shaderInitializer()
			luxshader.mattetranslucent.shaderInitializer()
			luxshader.metal.shaderInitializer()
			luxshader.mix.shaderInitializer()
			luxshader.shinymetal.shaderInitializer()
			luxshader.mirror.shaderInitializer()
			luxshader.plastic.shaderInitializer()
			luxshader.substrate.shaderInitializer()

			luxshader.arealight.shaderInitializer()

		except:
			OpenMaya.MGlobal.displayError("Failed to create attributes\n")
			raise

		try:
			# base attributes
			luxshader.addAttribute(luxshader.iMaterialType)
			luxshader.addAttribute(luxshader.bumpMap)
			luxshader.addAttribute(luxshader.outColor)
			luxshader.addAttribute(luxshader.transparency)

			####
			# can we defer all the below into the child/sibling classes ?

			# carpaint
			luxshader.addAttribute(luxshader.carpaint.name)
			luxshader.addAttribute(luxshader.carpaint.kd)
			luxshader.addAttribute(luxshader.carpaint.ks1)
			luxshader.addAttribute(luxshader.carpaint.ks2)
			luxshader.addAttribute(luxshader.carpaint.ks3)
			luxshader.addAttribute(luxshader.carpaint.r1)
			luxshader.addAttribute(luxshader.carpaint.r2)
			luxshader.addAttribute(luxshader.carpaint.r3)
			luxshader.addAttribute(luxshader.carpaint.m1)
			luxshader.addAttribute(luxshader.carpaint.m2)
			luxshader.addAttribute(luxshader.carpaint.m3)

			# glass
			luxshader.addAttribute(luxshader.glass.kr)
			luxshader.addAttribute(luxshader.glass.kt)
			luxshader.addAttribute(luxshader.glass.index)
			luxshader.addAttribute(luxshader.glass.cauchyb)

			# roughglass
			luxshader.addAttribute(luxshader.roughglass.kr)
			luxshader.addAttribute(luxshader.roughglass.kt)
			luxshader.addAttribute(luxshader.roughglass.uroughness)
			luxshader.addAttribute(luxshader.roughglass.vroughness)
			luxshader.addAttribute(luxshader.roughglass.index)
			luxshader.addAttribute(luxshader.roughglass.cauchyb)

			# matte
			luxshader.addAttribute(luxshader.matte.kd)
			luxshader.addAttribute(luxshader.matte.sigma)

			# mattetranslucent
			luxshader.addAttribute(luxshader.mattetranslucent.kr)
			luxshader.addAttribute(luxshader.mattetranslucent.kt)
			luxshader.addAttribute(luxshader.mattetranslucent.sigma)

			# metal
			luxshader.addAttribute(luxshader.metal.name)
			luxshader.addAttribute(luxshader.metal.n)
			luxshader.addAttribute(luxshader.metal.k)
			luxshader.addAttribute(luxshader.metal.uroughness)
			luxshader.addAttribute(luxshader.metal.vroughness)
			luxshader.addAttribute(luxshader.metal.nkFile)

			# shinymetal
			luxshader.addAttribute(luxshader.shinymetal.kr)
			luxshader.addAttribute(luxshader.shinymetal.ks)
			luxshader.addAttribute(luxshader.shinymetal.uroughness)
			luxshader.addAttribute(luxshader.shinymetal.vroughness)

			# mirror
			luxshader.addAttribute(luxshader.mirror.kr)
			
			# mix
			luxshader.addAttribute(luxshader.mix.namedMaterial1)
			luxshader.addAttribute(luxshader.mix.namedMaterial2)
			luxshader.addAttribute(luxshader.mix.amount)

			# plastic
			luxshader.addAttribute(luxshader.plastic.kd)
			luxshader.addAttribute(luxshader.plastic.ks)
			luxshader.addAttribute(luxshader.plastic.uroughness)
			luxshader.addAttribute(luxshader.plastic.vroughness)

			# substrate
			luxshader.addAttribute(luxshader.substrate.kd)
			luxshader.addAttribute(luxshader.substrate.ks)
			luxshader.addAttribute(luxshader.substrate.uroughness)
			luxshader.addAttribute(luxshader.substrate.vroughness)

			# arealight
			luxshader.addAttribute(luxshader.arealight.L)

		except:
			OpenMaya.MGlobal.displayError("Failed to add attributes\n")
			raise

		try:
			luxshader.attributeAffects(luxshader.bumpMap,					luxshader.outColor)
			# and these are the attributes that we use in compute
			luxshader.attributeAffects(luxshader.carpaint.kd,				luxshader.outColor)
			luxshader.attributeAffects(luxshader.glass.kt,					luxshader.outColor)
			luxshader.attributeAffects(luxshader.roughglass.kt, 			luxshader.outColor)
			luxshader.attributeAffects(luxshader.matte.kd,					luxshader.outColor)
			luxshader.attributeAffects(luxshader.mattetranslucent.kt,		luxshader.outColor)
			luxshader.attributeAffects(luxshader.metal.n,					luxshader.outColor)
			luxshader.attributeAffects(luxshader.shinymetal.kr, 			luxshader.outColor)
			luxshader.attributeAffects(luxshader.mirror.kr, 				luxshader.outColor)
			luxshader.attributeAffects(luxshader.plastic.kd,				luxshader.outColor)
			luxshader.attributeAffects(luxshader.substrate.kd,				luxshader.outColor)
			# arealight doesn't affect, values are hardcoded

		except:
			OpenMaya.MGlobal.displayError("Failed in setting attributeAffects\n")
			raise
