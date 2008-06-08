#/* GeoSun 1.0 for Maya 8.5
#    Adapted for MtI by Doug Hammond.
#    Translated into python for Lux renderer by Doug Hammond 
#Adds geographical location, time and date features to the physical sun in MtI and calculates daylight angle.
#Based on SunLight v1.0 by Miguel Kabantsov (miguelkab@gmail.com)
#Replaces the faulty sun position calculation algorythm with a precise calculation (Source for algorythm: http://de.wikipedia.org/wiki/Sonnenstand),
#( support for z-Up systems is now fully automatic - DH )
#Co-Ordinates: http://www.bcca.org/misc/qiblih/latlong.html
#Author: Nils-Peter Fischer (Nils-Peter.Fischer@web.de)
#Date of creation:    07-05-07
#Last change:        07-05-07
#MtI implementation: 09-04-08
#
#Usage comments:
#- All coordinates in decimal degrees, North/East positive, South/West values negative.
#- Use "useHourValue" to animate daydime (decimal hours instead of hours:mins)
#- Use "useDayValue" to animate the date (float value for julian day instead of day/month)
#
#(- effective daytime and date actually used for calculation are displayed in the attribute window.)
# -- DH not any more    
#*/

import math

from maya import cmds
from maya import OpenMaya
from maya import OpenMayaMPx

class updateSunNode(OpenMayaMPx.MPxCommand):
    """
    Command to calculate the SunSky rotations from the geographic
    location/time input, via azimuth/elevation values.
    """
    
    @staticmethod
    def commandName():
        return "updateSunNode"
    
    @staticmethod
    def commandCreator():
        return OpenMayaMPx.asMPxPtr( updateSunNode() )

    def __init__(self):
        OpenMayaMPx.MPxCommand.__init__(self)
    #end def __init__
    
    def doIt(self, args):
        """
        Command entry point. Start the calculation on the given node.
        """
        
        if (args.length() < 1):
            OpenMaya.MGlobal.displayError("You need to specify the node to update")
            return
        
        nodeName = args.asString(0)
        
        # TODO validate that we're reading data from the correct type of node (ie, luxSunsky)
        
        Latitude  = cmds.getAttr (nodeName+".latitude")
        Longitude = cmds.getAttr (nodeName+".longitude")
        tz = 0
        
        ssTZ = cmds.getAttr(nodeName+".timeZone")
        
        if (ssTZ==0):    tz = -12
        elif (ssTZ==1):  tz = -11
        elif (ssTZ==2):  tz = -10
        elif (ssTZ==4):  tz = -9.5
        elif (ssTZ==5):  tz = -9
        elif (ssTZ==6):  tz = -8.5
        elif (ssTZ==7):  tz = -8
        elif (ssTZ==8):  tz = -7
        elif (ssTZ==9):  tz = -6
        elif (ssTZ==10): tz = -5
        elif (ssTZ==11): tz = -4
        elif (ssTZ==12): tz = -3.5
        elif (ssTZ==13): tz = -3
        elif (ssTZ==14): tz = -2
        elif (ssTZ==15): tz = -1
        elif (ssTZ==16): tz = 0
        elif (ssTZ==17): tz = 1
        elif (ssTZ==18): tz = 2
        elif (ssTZ==19): tz = 3
        elif (ssTZ==20): tz = 3.5
        elif (ssTZ==21): tz = 4
        elif (ssTZ==22): tz = 4.5
        elif (ssTZ==23): tz = 5
        elif (ssTZ==24): tz = 5.5
        elif (ssTZ==25): tz = 6
        elif (ssTZ==26): tz = 6.5
        elif (ssTZ==27): tz = 7
        elif (ssTZ==28): tz = 8
        elif (ssTZ==29): tz = 9
        elif (ssTZ==30): tz = 9.5
        elif (ssTZ==31): tz = 10
        elif (ssTZ==32): tz = 10.5
        elif (ssTZ==33): tz = 11
        elif (ssTZ==34): tz = 11.5
        elif (ssTZ==35): tz = 12
        else:            tz = 13
        
        fLocalTime = 0
    
        if cmds.getAttr (nodeName+".useHourValue") == 1:
            fLocalTime = cmds.getAttr(nodeName+".localHourValue")    
        else:
            fLocalTime = ( cmds.getAttr(nodeName+".localHour") + (cmds.getAttr(nodeName+".localMinute")/60)  )
        
        self.effectiveLocalHour = math.floor(fLocalTime)
        self.effectiveLocalMinute = (fLocalTime - math.floor(fLocalTime)) * 60
        
        # cmds.setAttr (nodeName+".effectiveLocalHour", math.floor(fLocalTime) )
        # cmds.setAttr (nodeName+".effectiveLocalMinute", (fLocalTime - math.floor(fLocalTime)) * 60 )
    
        if cmds.getAttr(nodeName+".useDayValue") == 1:
            mon = 0
            effFullMonthDays = 0
            ssDV = cmds.getAttr(nodeName+".dayValue")
         
            if (ssDV<=31):
                mon = 0
            elif (ssDV<=59):
                mon = 1
                effFullMonthDays = 31
            elif (ssDV<=90):
                mon = 2
                effFullMonthDays = 59
            elif (ssDV<=120):
                mon = 3
                effFullMonthDays = 90
            elif (ssDV<=151):
                mon = 4
                effFullMonthDays = 120
            elif (ssDV<=181):
                mon = 5
                effFullMonthDays = 151
            elif (ssDV<=212):
                mon = 6
                effFullMonthDays = 181
            elif (ssDV<=243):
                mon = 7
                effFullMonthDays = 212
            elif (ssDV<=273):
                mon = 8
                effFullMonthDays = 243
            elif (ssDV<=304):
                mon = 9
                effFullMonthDays = 273
            elif (ssDV<=334):
                mon = 10
                effFullMonthDays = 304
            else:
                mon = 11
                effFullMonthDays = 334

            self.effectiveMonth = mon
            self.effectiveDay = ssDV - effFullMonthDays
            
            #cmds.setAttr (nodeName+".effectiveMonth", mon )
            #cmds.setAttr (nodeName+".effectiveDay",   ssDV - effFullMonthDays)
        else:
            self.effectiveMonth = cmds.getAttr (nodeName+".month")
            self.effectiveDay   = cmds.getAttr (nodeName+".day")
            #cmds.setAttr (nodeName+".effectiveMonth", cmds.getAttr (nodeName+".month") )
            #cmds.setAttr (nodeName+".effectiveDay",   cmds.getAttr (nodeName+".day")   )
            
        
        Day   = self.effectiveDay #cmds.getAttr (nodeName+".effectiveDay")
        Month = self.effectiveMonth + 1 # cmds.getAttr (nodeName+".effectiveMonth") + 1
        Year  = cmds.getAttr (nodeName+".year")
        
    
        sun = self.geoSunData(Latitude, Longitude, Year, Month, Day, fLocalTime, tz)
        az = sun[0]
        el = sun[1]
        
        self.azimuth = az
        self.elevation = el
        
        #cmds.setAttr (nodeName+".azimuth",   az)
        #cmds.setAttr (nodeName+".elevation", el)
    
        ssXFm = self.listTransforms(nodeName)
        
        oldX = cmds.getAttr( ssXFm[0] + '.rotateX' )
        oldY = cmds.getAttr( ssXFm[0] + '.rotateY' )
        oldZ = cmds.getAttr( ssXFm[0] + '.rotateZ' )
        
        if OpenMaya.MGlobal.isZAxisUp():
            newX = 90 - el
            newY = 0
            newZ = -az
        else:
            newX = 180 + el
            newY = 180 - az
            newZ = 0
            
        if newX != oldX:
            cmds.setAttr (ssXFm[0]+".rotateX", newX )
        if newY != oldY:
            cmds.setAttr (ssXFm[0]+".rotateY", newY )
        if newZ != oldZ:
            cmds.setAttr (ssXFm[0]+".rotateZ", newZ )
        
    
    
    def listTransforms(self, nodeName):
        """
        Find the luxSunsky node's transform parent
        """
        
        return cmds.listRelatives( nodeName, p = True, path = True )
    
    # mathematical helpers
    def sind(self, deg):
        return math.sin(math.radians(deg))
    
    def cosd(self, deg):
        return math.cos(math.radians(deg))
    
    def tand(self, deg):
        return math.tan(math.radians(deg))
    
    def asind(self, deg):
        return math.degrees(math.asin(deg))
    
    def atand(self, deg):
        return math.degrees(math.atan(deg))
    
    
    def geo_sun_astronomicJulianDate(self, Year, Month, Day, LocalTime, Timezone):
        """
        See quoted source in file header for explanation
        """
        
        if Month > 2.0:
            Y = Year
            M = Month
        else:
            Y = Year - 1.0
            M = Month + 12.0
            
        UT = LocalTime - Timezone
        hour = UT / 24.0
        A = int(Y/100.0)
        B = 2.0 - A+int(A/4.0)
        
        JD = math.floor(365.25*(Y+4716.0)) + math.floor(30.6001*(M+1.0)) + Day + hour + B - 1524.4
        
        return JD
    
    def geoSunData(self, Latitude, Longitude, Year, Month, Day, LocalTime, Timezone):
        """
        See quoted source in file header for explanation
        """
        
        JD = self.geo_sun_astronomicJulianDate(Year, Month, Day, LocalTime, Timezone)
        
        phi = Latitude
        llambda = Longitude
                
        n = JD - 2451545.0
        LDeg = (280.460 + 0.9856474*n) - (math.floor((280.460 + 0.9856474*n)/360.0) * 360.0)
        gDeg = (357.528 + 0.9856003*n) - (math.floor((357.528 + 0.9856003*n)/360.0) * 360.0)
        LambdaDeg = LDeg + 1.915 * self.sind(gDeg) + 0.02 * self.sind(2.0*gDeg)
        
        epsilonDeg = 23.439 - 0.0000004*n
        
        alphaDeg = self.atand( (self.cosd(epsilonDeg) * self.sind(LambdaDeg)) / self.cosd(LambdaDeg) )
        if self.cosd(LambdaDeg) < 0.0:
            alphaDeg += 180.0
            
        deltaDeg = self.asind( self.sind(epsilonDeg) * self.sind(LambdaDeg) )
        
        JDNull = self.geo_sun_astronomicJulianDate(Year, Month, Day, 0.0, 0.0)
        
        TNull = (JDNull - 2451545.0) / 36525.0
        T = LocalTime - Timezone
        
        thetaGh = 6.697376 + 2400.05134*TNull + 1.002738*T
        thetaGh -= math.floor(thetaGh/24.0) * 24.0
        
        thetaG = thetaGh * 15.0
        theta = thetaG + llambda
        
        tau = theta - alphaDeg
        
        a = self.atand( self.sind(tau) / ( self.cosd(tau)*self.sind(phi) - self.tand(deltaDeg)*self.cosd(phi)) )
        if self.cosd(tau)*self.sind(phi) - self.tand(deltaDeg)*self.cosd(phi) < 0.0:
            a += 180.0
        
        h = self.asind( self.cosd(deltaDeg)*self.cosd(tau)*self.cosd(phi) + self.sind(deltaDeg)*self.sind(phi) )
        
        R = 1.02 / (self.tand (h+(10.3/(h+5.11))))
        hR = h + R/60.0
        
        azimuth = a
        elevation = hR
        
        result = OpenMaya.MFloatArray()
        result.append(azimuth)
        result.append(elevation)
        
        return result