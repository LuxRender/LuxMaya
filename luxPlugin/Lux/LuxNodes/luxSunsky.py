# ------------------------------------------------------------------------------
# Lux sunsky for Maya
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
# luxSunsky: a locator (light) node for lux's sunsky system
#
# ------------------------------------------------------------------------------

from maya import OpenMaya
from maya import OpenMayaMPx
from maya import OpenMayaRender
from maya import OpenMayaUI

from Lux.LuxMiscModules.glRoutines import glRoutines

from LuxNode import LuxNode

class luxSunsky(OpenMayaMPx.MPxLocatorNode, glRoutines, LuxNode):
	"""
	Sunsky direction locator node for Maya
	"""
	
	# This is the size of the locator on the grid
	displayRadius = 5
	
	@staticmethod
	def nodeName():
		return "luxSunsky"

	@staticmethod
	def nodeId():
		return OpenMaya.MTypeId(0x6C757806) # 'lux' 06

	@staticmethod
	def nodeCreator():
		return OpenMayaMPx.asMPxPtr( luxSunsky() )

	@staticmethod
	def nodeClassify():
		return "light"

	def __init__(self):
		OpenMayaMPx.MPxLocatorNode.__init__(self)
		
		# init attr objects here
		
		nsamples              = OpenMaya.MObject()
		gain                  = OpenMaya.MObject()
		turbidity             = OpenMaya.MObject()
		relsize               = OpenMaya.MObject()
		
		latitude              = OpenMaya.MObject()
		longitude             = OpenMaya.MObject()
		
		timezone              = OpenMaya.MObject()
		localhour             = OpenMaya.MObject()
		localminute           = OpenMaya.MObject()
		usehourvalue          = OpenMaya.MObject()
		localhourvalue        = OpenMaya.MObject()
		
		day                   = OpenMaya.MObject()
		month                 = OpenMaya.MObject()
		year                  = OpenMaya.MObject()
		usedayvalue           = OpenMaya.MObject()
		dayvalue              = OpenMaya.MObject()
		
#		effectivelocalhour    = OpenMaya.MObject()
#		effectivelocalminute  = OpenMaya.MObject()
#		effectiveday          = OpenMaya.MObject()
#		effectivemonth        = OpenMaya.MObject()
#		
#		elevation             = OpenMaya.MObject()
#		azimuth               = OpenMaya.MObject()

		glRenderer = OpenMayaRender.MHardwareRenderer.theRenderer()
		self.glFT = glRenderer.glFunctionTable()
		

	@staticmethod
	def nodeInitializer():
		enumAttr	= OpenMaya.MFnEnumAttribute()
		nAttr = OpenMaya.MFnNumericAttribute()
		
		try:
			
			luxSunsky.nsamples = luxSunsky.makeInteger( 'nsamples', 'ns', default = 1 )
			luxSunsky.gain = luxSunsky.makeFloat( 'gain', 'ga', default = 1.0 )
			luxSunsky.turbidity = luxSunsky.makeFloat( 'turbidity', 'tb', default = 2.0 )
			luxSunsky.relsize = luxSunsky.makeFloat( 'relsize', 'rs', default = 1.0 )
			
			luxSunsky.latitude = luxSunsky.makeFloat( 'latitude', 'lat', default = 51.55, input = True )
			luxSunsky.longitude = luxSunsky.makeFloat( 'longitude', 'lon', default = -0.12, input = True )
			
			luxSunsky.timezone = enumAttr.create("timeZone", "tz", 15)
			tzListStr = "-12.00:-11.00:-10.00 US/Hawaii:-9.30:-9.00 CAN/Yukon:-8.30:-8.00 US/Pacific:-7.00 US/Mountain:-6.00 US/Central:-5.00 US/Eastern:-4.00 Caracas:-3.30:-3.00 Rio:-2.0:-1.00:GMT London:+1.00 Paris:+2.00 Cairo:+3.00 Jeddah:+3.30 Tehran:+4.00 Dubai:+4.30 Kabul:+5.00 Karachi:+5.30 Delhi:+6.00 Dhaka:+6.30 Rangoon:+7.00 Bangkok:+8.00 Hong Kong:+9.00 Tokyo:+9.30 Adelaide:+10.00 Sydney:+10.30:+11.00 Noumea:+11.30:+12.00 Wellington:+13.00"
			tzList = tzListStr.split(':')
			i=0
			for tz in tzList:
				enumAttr.addField( tz, i)
				i+=1
			luxSunsky.makeInput( enumAttr )
			
			luxSunsky.localhour = luxSunsky.makeInteger( 'localHour', 'lh', default = 14, input = True )
			luxSunsky.localminute = luxSunsky.makeInteger( 'localMinute', 'lm', default = 0, input = True )
			luxSunsky.usehourvalue = luxSunsky.makeBoolean( 'useHourValue', 'uhv', input = True )
			luxSunsky.localhourvalue = luxSunsky.makeFloat( 'localHourValue', 'lhv', default = 14.0, input = True )
			
			luxSunsky.day = luxSunsky.makeInteger( 'day', 'd', default = 25, input = True )
			
			luxSunsky.month = enumAttr.create("month", "mo", 4)
			mListStr = "Jan:Feb:Mar:Apr:May:Jun:Jul:Aug:Sep:Oct:Nov:Dec"
			mList = mListStr.split(':')
			i=0
			for month in mList:
				enumAttr.addField( month, i )
				i+=1
			luxSunsky.makeInput( enumAttr )
			
			luxSunsky.year = luxSunsky.makeInteger( 'year', 'y', default = 2008, input = True )
			luxSunsky.usedayvalue = luxSunsky.makeBoolean( 'useDayValue', 'udv', input = True )
			luxSunsky.dayvalue = luxSunsky.makeFloat( 'dayValue', 'dv', default = 144.0, input = True )
			
#			luxSunsky.effectivelocalhour = luxSunsky.makeInteger( 'effectiveLocalHour', 'elh', input = True )
#			luxSunsky.effectivelocalminute = luxSunsky.makeInteger( 'effectiveLocalMinute', 'elm', input = True )
#			luxSunsky.effectiveday = luxSunsky.makeInteger( 'effectiveDay', 'ed', input = True )
#			
#			luxSunsky.effectivemonth = enumAttr.create("effectiveMonth", "emo", 4)
#			i=0
#			for month in mList:
#				enumAttr.addField( month, i )
#				i+=1
#			luxSunsky.makeInput( enumAttr )
#			
#			luxSunsky.elevation = luxSunsky.makeFloat( 'elevation', 'e', input = True )
#			luxSunsky.azimuth = luxSunsky.makeFloat( 'azimuth', 'a', input = True)
			
		except:
			OpenMaya.MGlobal.displayError("Failed to create attributes\n")
			raise
		
		try:
			pass
			# base attributes
			luxSunsky.addAttribute(luxSunsky.nsamples)
			luxSunsky.addAttribute(luxSunsky.gain)
			luxSunsky.addAttribute(luxSunsky.turbidity)
			luxSunsky.addAttribute(luxSunsky.relsize)
			
			luxSunsky.addAttribute(luxSunsky.latitude)
			luxSunsky.addAttribute(luxSunsky.longitude)
			luxSunsky.addAttribute(luxSunsky.timezone)
			luxSunsky.addAttribute(luxSunsky.localhour)
			luxSunsky.addAttribute(luxSunsky.localminute)
			luxSunsky.addAttribute(luxSunsky.usehourvalue)
			luxSunsky.addAttribute(luxSunsky.localhourvalue)
			luxSunsky.addAttribute(luxSunsky.day)
			luxSunsky.addAttribute(luxSunsky.month)
			luxSunsky.addAttribute(luxSunsky.year)
			luxSunsky.addAttribute(luxSunsky.usedayvalue)
			luxSunsky.addAttribute(luxSunsky.dayvalue)
#			luxSunsky.addAttribute(luxSunsky.effectivelocalhour)
#			luxSunsky.addAttribute(luxSunsky.effectivelocalminute)
#			luxSunsky.addAttribute(luxSunsky.effectiveday)
#			luxSunsky.addAttribute(luxSunsky.effectivemonth)
#			luxSunsky.addAttribute(luxSunsky.elevation)
#			luxSunsky.addAttribute(luxSunsky.azimuth)
			
		except:
			OpenMaya.MGlobal.displayError("Failed to add attributes\n")
			raise
		
		return OpenMaya.MStatus.kSuccess
	
	def postConstructor(self):
		self._setMPSafe(True)
		
		
	@staticmethod
	def sunskyCallback( msg, plug, otherPlug, srcNode ):
		OpenMaya.MGlobal.displayInfo('Got sunsky callback')
#		from Lux.LuxMiscModules.geoSunData import updateSunNode
#		usn = updateSunNode()
#		args = OpenMaya.MArgList()
#		args.addArg( OpenMaya.MFnDependencyNode( srcNode ).name() )
#		usn.doIt(args)
	
	@staticmethod	
	def isBounded():
		return True
	
	def boundingBox(self):
		bbox = OpenMaya.MBoundingBox()
		bbox.expand( OpenMaya.MPoint( -self.displayRadius, -self.displayRadius, -self.displayRadius ) )
		bbox.expand( OpenMaya.MPoint(  self.displayRadius,  self.displayRadius,  self.displayRadius ) )
		return bbox
	
	
	def draw(self, view, DGpath, style, status):
		
		try:
			col = self.colorRGB( status )
			
			if status == OpenMayaUI.M3dView.kLead:
				self.glFT.glColor4f( 0, 1, 0, 0.3 )
			else:
				self.glFT.glColor4f( col.r, col.g, col.b, 0.3 )
			
			# You want the sun on a stick!!
			self.glFT.glBlendFunc(OpenMayaRender.MGL_SRC_ALPHA,OpenMayaRender.MGL_ONE_MINUS_SRC_ALPHA)
			self.glFT.glEnable(OpenMayaRender.MGL_BLEND)
			self.DrawSphere( self.displayRadius )
			self.glFT.glPushMatrix();
			self.glFT.glTranslatef(0,0,2.0*self.displayRadius);
			self.DrawSphere( self.displayRadius/10.0 )
			self.glFT.glPopMatrix();
			self.glFT.glBegin( OpenMayaRender.MGL_LINES )
			self.glFT.glVertex3f( 0.0,  0.0, 0.0 )
			self.glFT.glVertex3f( 0.0,  0.0, 2.0*self.displayRadius)
			self.glFT.glEnd()
			self.glFT.glDisable(OpenMayaRender.MGL_BLEND)
			
		except:
			OpenMaya.MGlobal.displayError("Failed to draw luxSunsky\n")
			raise