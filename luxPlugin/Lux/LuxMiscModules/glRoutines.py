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
# miscellaneous routines: OpenGL module
# 
# Taken mostly from the locator examples at http://www.robthebloke.org/mayaapi.html
#
# ------------------------------------------------------------------------------

from maya import OpenMayaRender
import math

class glRoutines:
    """
    OpenGL helper routines for drawing the custom locators
    """
    
    def DrawCircleXY(self, r, divs):
        self.glFT.glBegin( OpenMayaRender.MGL_LINE_LOOP )
        for i in range(0, divs):
            angle = i*360/divs * math.pi/180
            ca = math.cos(angle)
            sa = math.sin(angle)
            self.glFT.glVertex3f(ca*r, sa*r, 0.0)
        self.glFT.glEnd()
        
    def DrawCircleXZ(self, r, divs):
        self.glFT.glBegin( OpenMayaRender.MGL_LINE_LOOP )
        for i in range(0, divs):
            angle = i*360/divs * math.pi/180
            ca = math.cos(angle)
            sa = math.sin(angle)
            self.glFT.glVertex3f(ca*r, 0.0, sa*r)
        self.glFT.glEnd()
        
    def DrawCircleYZ(self, r, divs):
        self.glFT.glBegin( OpenMayaRender.MGL_LINE_LOOP )
        for i in range(0, divs):
            angle = i*360/divs * math.pi/180
            ca = math.cos(angle)
            sa = math.sin(angle)
            self.glFT.glVertex3f(0, ca*r, sa*r)
        self.glFT.glEnd()
    
    def DrawSphere(self, r):
        self.DrawCircleXY(r, 30)
        self.DrawCircleXZ(r, 30)
        self.DrawCircleYZ(r, 30)
    
    def DrawFilledQuadXY(self, w, h):
        self.glFT.glBegin( OpenMayaRender.MGL_QUADS )
        self.glFT.glVertex3f( -0.5*w, -0.5*h, 0 )
        self.glFT.glVertex3f(  0.5*w, -0.5*h, 0 )
        self.glFT.glVertex3f(  0.5*w,  0.5*h, 0 )
        self.glFT.glVertex3f( -0.5*w,  0.5*h, 0 )
        self.glFT.glEnd();

    def DrawFilledQuadXZ(self, w, h):
        self.glFT.glBegin( OpenMayaRender.MGL_QUADS )
        self.glFT.glVertex3f( -0.5*w, 0, -0.5*h )
        self.glFT.glVertex3f(  0.5*w, 0, -0.5*h )
        self.glFT.glVertex3f(  0.5*w, 0,  0.5*h )
        self.glFT.glVertex3f( -0.5*w, 0,  0.5*h )
        self.glFT.glEnd();
 
    def DrawFilledQuadYZ(self, w, h):
        self.glFT.glBegin( OpenMayaRender.MGL_QUADS )
        self.glFT.glVertex3f( 0, -0.5*w, -0.5*h )
        self.glFT.glVertex3f( 0,  0.5*w, -0.5*h )
        self.glFT.glVertex3f( 0,  0.5*w,  0.5*h )
        self.glFT.glVertex3f( 0, -0.5*w,  0.5*h )
        self.glFT.glEnd();

    def DrawFilledCube(self, w, h, d):
        self.glFT.glPushMatrix()
        self.glFT.glTranslatef(0,0,d/2)
        self.DrawFilledQuadXY(w,h)
        self.glFT.glPopMatrix()
        self.glFT.glPushMatrix()
        self.glFT.glTranslatef(0,0,-d/2)
        self.DrawFilledQuadXY(w,h)
        self.glFT.glPopMatrix()
    
        self.glFT.glPushMatrix()
        self.glFT.glTranslatef(0,h/2,0)
        self.DrawFilledQuadXZ(w,d)
        self.glFT.glPopMatrix()
        self.glFT.glPushMatrix()
        self.glFT.glTranslatef(0,-h/2,0)
        self.DrawFilledQuadXZ(w,d)
        self.glFT.glPopMatrix()
    
        self.glFT.glPushMatrix()
        self.glFT.glTranslatef(w/2,0,0)
        self.DrawFilledQuadYZ(h,d)
        self.glFT.glPopMatrix()
        self.glFT.glPushMatrix()
        self.glFT.glTranslatef(-w/2,0,0)
        self.DrawFilledQuadYZ(h,d)
        self.glFT.glPopMatrix()