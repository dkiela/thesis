#!/usr/bin/env python

import sys
import time
import random
import math
import getopt

YSCALE=1.0   #   was YSCALE=50.0
#YSHIFT=-200.0
XZSCALE=10.0
YSHIFT=0.0


"""
NOTE:  pyramids have tips up.  Apical dendrite goes mostly upward toward L1.
       major axon output is from bottom, flat side of pyramid.

Quick GL refresher:

glMatrixMode applies subsequent matrix operations to the modelview
matrix stack.  But if you don't do any matrix operations, then nothing
in the world will be affected (just be sure to set mode back before e.g.
gluLookAt()!  The model and then projection matrices are just part of
drawing pipeline.  However, when you call any drawing functions, like
CallList, things are transformed according to the model view.

Then afterward things are transformed according to 

example usage for new style cell and synapse data:
./netplot.py -d areabrain

FIXME:  why don't CallLists (ISLIST and ESLIST) work on laptop?
    Calling drawsyns seach time does work.  Does appear to be a problem
    with laptop driver or PyOpenGL version . . . 

+y is definitely up on screen
+z is ?
+x is ?

model and projection matrices
order of application?
what is display pipeline?
glutLookAt operates on what?

"""

try:
    from OpenGL.GL import *
    from OpenGL.GLE import *
    from OpenGL.GLU import *
    from OpenGL.GLUT import *
except:
    print "Problem importing opengl libraries.  Did you install them?"


# confirm depth z buffer is active

# scp cortex.cs.unr.edu:/home/drewes/*server/ncs5k/brainmap .

# GL coords:
# x and y are as cartesian, -z goes into distance
# x cross y is z (curl fingers from x to y, thumb is toward you which is +z)
# backface culling doesn't take place unless you request it, so order of points
# in polys or tris doesn't matter

# would it be better to store each terminating synapse with the cell
# that it terminates on?
class NetPlot:
    superpretty=False       # True is slow and big and no text, for LJ cover hopefully!
    vp=3
    DLIST=1
    ESLIST=2            # excitatory synapses
    ISLIST=3            # inhibitory synapses
    PSLIST=4
    CELLHEIGHT=20.0
    CELLWIDTH=10.0
    idxstart={}
    startx=None; startz=None        # for differential motion drag
    showlabels=False
    cells={}
    esyns=[]
    isyns=[]
    syns=[]
    maxcell=-1
    fi=[]
    lasty=0.0
    lastrad=700.0            # radius of eye point
    lasttheta=0.6       # theta of last eye point, radians
    lastx=None      # now compute from lastrad and lasttheta before display
    lastz=None
    showesyn=False
    showisyn=False
    playspikes=-1
    playspikestarttime=-1
    playspikestarttick=0
    playspikestartidx=0
    playspikeendidx=-1
    # only show this fraction of synapses
    # set to None will show all
    SHOWSYNAPSEFRACTION=None
    light1Position = (100.0, 100, 0.0, 0.0)
    vp=0      # current viewport.  numbered going across in cols for row 0, then next row
    nvpx=3    # number of viewports in each dimension
    nvpy=4

    def __init__(self, cells, idxstart, maxcell, esyns, isyns, syns, names, w=800, h=600, superpretty=False, maxsyndist=None, nvpx=3, nvpy=4):
        self.superpretty=superpretty
        self.syns=syns
        self.esyns=esyns
        self.isyns=isyns
        self.cells=cells
        self.idxstart=idxstart
        self.maxcell=maxcell
        self.names=names
        self.dends={}
        self.axons={}
        self.w=w
        self.h=h
        self.maxsyndist=maxsyndist
        self.nvpx=nvpx
        self.nvpy=nvpy
        self.near=100.0
        self.far=4000.0

        wid=w; hei=h

        args=glutInit(sys.argv)
        # "always enable depth buffer when using lighting"
        glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
        #glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB )
        glutInitWindowSize(int(wid), int(hei))
        glutCreateWindow('Brainlab netplot:  3D neural network plotter')

        #glClearColor(0.0, 0.0, 0.0, 0.0)
        #glClearColor(1.0, 1.0, 1.0, 0.0)    # white
        self.bgbrightness=0.8
        glClearColor(self.bgbrightness, self.bgbrightness, self.bgbrightness, 0.0)
        #glClearColor(0.0, 0.0, 1.0, 0.0)    # blue background
        #glClearDepth(1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        #glShadeModel(GL_SMOOTH)        # SMOOTH is default

        self.linesmooth=True

        glEnable(GL_DEPTH_TEST)

        ltp=-10.0; rtp=10.0; botp=-10.0; topp=10.0; nearp=10.0; farp=300.0
        # Applies subsequent matrix operations to the projection matrix stack
        glMatrixMode(GL_PROJECTION)     # FIXME:  what is this?
        if superpretty:
            # so we can do screen cap 4xwindow res
            x,y=glGetIntegerv(GL_MAX_VIEWPORT_DIMS)
            print "max viewport dims", x,y
            #glViewport(0, 0, w*self.nvpx, h*self.nvpy)
            if 1:
                # start view in middleish area
                #sx=((self.w * self.nvpx) / 2) - (self.w/2)
                #sy=((self.h * self.nvpy) / 2) - (self.h/2)
                sx,sy=self.ScreenCenter()
                glViewport(sx, sy, w*self.nvpx, h*self.nvpy)
            else:
                glViewport(0, 0, w*self.nvpx, h*self.nvpy)
                # for some reason, viewport is negative in extent
        #glFrustum (ltp, rtp, botp, topp, nearp, farp)
        #glFrustum (-9.0, 9.0, -9.0, 9.0, 50.0, 1000.0)
        #glFrustum (-2000.0, 2000.0, -2000.0, 2000.0, 20.0, 2000.0)
        # FIXME gluPerspective takes care of keeping view same if window resized (confirm)
        # which glFrustum do not
        gluPerspective(120.0, float(wid)/float(hei), self.near, self.far)

        glMatrixMode(GL_MODELVIEW)
        # we leave it here for the rest of the run

        glFrontFace(GL_CCW)          # this makes backs of neurons disappear.  what we want.
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)

        if False:
            light1Color = (0.99, 0.99, 0.99, 1.0)
            #light2Position = (-4000.0, 4000, 1000.0, 0.0)
            #light2Color = (0.99, 0.99, 0.99, 1.0)
            glLightfv(GL_LIGHT1, GL_POSITION, self.light1Position)
            glLightfv(GL_LIGHT1, GL_DIFFUSE, light1Color)
            #glLightfv(GL_LIGHT2, GL_POSITION, light2Position)
            #glLightfv(GL_LIGHT2, GL_DIFFUSE, light2Color)
            glEnable(GL_LIGHT1)
            #glEnable(GL_LIGHT2)
            glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
            glEnable(GL_COLOR_MATERIAL)
            glEnable(GL_LIGHTING)

        # for certain light locations, this looks good
        self.light1Position=(-781, -550, 789, 0.0)
        self.diffuse=.7
        self.shininess=20.0
        self.ambient=.2
        self.specular=.75

        if True:
            # based on recs from http://www.sjbaker.org/steve/omniv/opengl_lighting.html
            #glLightfv(GL_LIGHT0, GL_POSITION, (1000, 1000, 0))
            #glLightfv(GL_LIGHT0, GL_POSITION, (1000, 0, 0))
            #glLightfv(GL_LIGHT0, GL_POSITION, (100, 100, 0))
            glLightfv(GL_LIGHT0, GL_POSITION, self.light1Position)
            glLightfv(GL_LIGHT0, GL_AMBIENT, (self.ambient, self.ambient, self.ambient, 1))
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (self.diffuse, self.diffuse, self.diffuse, 1))
            glLightfv(GL_LIGHT0, GL_SPECULAR, (self.specular, self.specular, self.specular, 1))
            glEnable(GL_LIGHT0)

            # global ambient:  (this is default, actually)
            glLightModel(GL_LIGHT_MODEL_AMBIENT, (0.4,0.4,0.4,1))
            glEnable(GL_LIGHTING)

            # difference btwn glColorMaterial and glMaterial

            #glColorMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE)
            """ Docs:
            glColorMaterial specifies which material parameters track
            the current color. When GL_COLOR_MATERIAL is enabled, the
            material parameter or parameters specified by mode, of the
            material or materials specified by face, track the current
            color at all times.

            glColorMaterial makes it possible to change a subset of
            material parameters for each vertex using only the glColor
            command, without calling glMaterial. If only such a subset
            of parameters is to be specified for each vertex, calling
            glColorMaterial is preferable to calling glMaterial.

            Call glColorMaterial before enabling GL_COLOR_MATERIAL
            """
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
            #glColorMaterial(GL_FRONT_AND_BACK, GL_SPECULAR)     # is this desired?
            # do multiple calls override previous settings or add to them?

            # should be default:
            # setting EMISSION up seems to disable other light effects.  hmm.
            # emission defaults to 0:
            #glMaterial(GL_FRONT_AND_BACK, GL_EMISSION, (0, 0, 0, 1));
            # 0 0 0 1 is default specular:
            #glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (.1, .1, .1, 1));
            # specular defaults to 0:
            glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (.5, .5, .5, 1));
            #glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (1.0, 1.0, 1.0, 1));
            #glMaterial(GL_FRONT_AND_BACK, GL_SPECULAR, (0.0, 0.0, 0.0, 1));
            # man page says do this after glColorMaterial
            # ambient defaults to .2:
            #glMaterial(GL_FRONT_AND_BACK, GL_AMBIENT, (.5, .5, .5, 1));
            # diffuse defaults to .8:
            #glMaterial(GL_FRONT_AND_BACK, GL_DIFFUSE, (.5, .5, .5, 1));
            #glMaterial(GL_FRONT, GL_SHININESS, 100.0);
            # shininess defaults to 0
            glMaterial(GL_FRONT, GL_SHININESS, self.shininess);      # max 128
            # do multiple calls override previous settings or add to them?  assume add

            glEnable(GL_COLOR_MATERIAL)

        if True:
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);
            glEnable(GL_BLEND);

        glNewList(self.DLIST, GL_COMPILE)
        self.drawcells()
        glEndList()

        self.RemakeSynLists()

        #glutSpecialFunc(self.on_special)
        glutKeyboardFunc(self.on_key)
        glutIdleFunc(self.idle)
        glutDisplayFunc(self.on_display)
        glutMotionFunc(self.on_motion)
        glutReshapeFunc(self.on_reshape)
        glutMouseFunc(self.on_mouse)
        #glutButtonBoxFunc(self.on_button)
        glutMainLoop()

    def RemakeSynLists(self):
        glNewList(self.ESLIST, GL_COMPILE)
        glColor3f(1.0, 0.0, 0.0)
        self.drawsyn(self.esyns)
        glEndList()

        glNewList(self.ISLIST, GL_COMPILE)
        glColor3f(0.0, 1.0, 0.0)
        self.drawsyn(self.isyns)
        glEndList()

    def drawcell(self, cellnum):
        # when we draw the cell, axons and dends, we draw with cell located origin of 0,0,0 
        # we push matrices to translate and rotate cell 
        # the points that we store in axon and dendrite lists should be in world coords though!
        CELLHEIGHT=self.CELLHEIGHT
        CELLWIDTH=self.CELLWIDTH
        # portrait:
        (nx, ny, nz) = self.cells[cellnum] 
        # landscape:  (?test)
        #(y, x, z) = self.cells[cellnum] 
        glPushMatrix()
        rr=random.randint(0, 359)
        #glIdentity()            # back to world space origin
        glTranslatef(nx, ny, nz)

        # we don't draw axons and dendrites unless superpretty is on
        # also if superpretty is off, cell is just a tetrahedron

        # axon
        if self.superpretty and True:
            axon=[]
            #axon.append((x, y, z))
            gleSetJoinStyle(TUBE_JN_ANGLE | TUBE_CONTOUR_CLOSED | TUBE_NORM_PATH_EDGE)
            cx=0; cz=0
            for al in range(-1, 20):        # first and last segments aren't drawn
                xp=random.randint(0, 4) -2
                zp=random.randint(0, 4) -2
                #axon.append((xp, -10*al, zp))
                axon.append((cx, -10*al, cz))
                cx+=xp; cz+=zp
            glePolyCylinder(axon, None, 2)  # draw relative to cell at 0,0,0
            # we don't store the last point in the polycylinder list into the axon list
            # because the last segment isn't drawn
            self.axons[cellnum]=[(ax+nx, ay+ny, az+nz) for (ax, ay, az) in axon[:-1]]   # but shift connection points to world space

        # dendrites
        # do this before scale!
        if self.superpretty and True:
            cd=[]
            self.dends[cellnum]=cd
            ndend=random.randint(2,6)
            gleSetJoinStyle (TUBE_NORM_EDGE | TUBE_JN_ANGLE | TUBE_JN_CAP)
            #gleSetJoinStyle(TUBE_JN_ANGLE | TUBE_CONTOUR_CLOSED | TUBE_NORM_PATH_EDGE)
            twopi=2.0*math.pi
            deg=random.random()*twopi
            # side dendrites, come out from sides and trends outward and a bit upwardish
            sl=10.0
            if 1:
                for i in range(ndend):
                    cx=0; cz=0; cy=0
                    dend=[]
                    y=0; x=0; z=0
                    xi=math.sin(deg)
                    zi=math.cos(deg)
                    dend.append((x, y, z))      # first segment won't be plotted, so repeat it
                    for al in range(0, 25):        # first and last segments aren't drawn
                        dend.append((x, y, z))
                        yp=random.randint(0, 9) -3      # trend upward
                        y+=yp
                        x+=xi*sl
                        z+=zi*sl
                    dend.append((x, y, z))      # last one isn't drawn
                    glePolyCylinder(dend, None, 1)  # draw relative to cell at 0,0,0
                    dend=[(dx+nx, dy+ny, dz+nz) for (dx, dy, dz) in dend[:-1]]   # but shift connection points to world space
                    cd.append(dend)
                    deg+=twopi/float(ndend)     # ndend+1?
            # basal dendrite, comes out from top and trends upwardish
            y=0; x=0; z=0
            dend=[]
            dend.append((x, y, z))
            #while y < self.TOPY:       # keep going to top of L1?
            for al in range(0, 30):        # first and last segments aren't drawn
                dend.append((x, y, z))
                xp=random.randint(0, 8) -4
                zp=random.randint(0, 8) -4
                y+=sl; x+=xp; z+=zp
            glePolyCylinder(dend, None, 2)  # draw relative to cell at 0,0,0
            dend=[(dx+nx, dy+ny, dz+nz) for (dx, dy, dz) in dend[:-1]]   # but shift connection points to world space
            cd.append(dend)

        # we did axon and dendrites first because we don't want them rotate
        # (that would make it harder to know the world-space coords for making
        # connections later).  we do want to rotate the cell though so that shading
        # effects vary per cell 
        glRotatef(rr, 0.0, 1.0, 0.0)

        # tetrahedral cell
        if False:
            glBegin(GL_TRIANGLE_FAN)
            # connects first vertex to each other
            glVertex3f(0,           CELLHEIGHT, 0)
            glVertex3f(CELLWIDTH,   0,          CELLWIDTH)
            glVertex3f(0,           0,         -CELLWIDTH)
            glVertex3f(-CELLWIDTH,  0,          CELLWIDTH)
            glVertex3f(CELLWIDTH,   0,          CELLWIDTH)
            glEnd()    
            # now fill in base
            glBegin(GL_TRIANGLES)
            glVertex3f(-CELLWIDTH,  0,          CELLWIDTH)
            glVertex3f(0,           0,         -CELLWIDTH)
            glVertex3f(CELLWIDTH,   0,          CELLWIDTH)
            glEnd()    

        if True:
            s1=random.randint(5,15)
            s2=random.randint(4,10)
            s3=random.randint(5,15)
            #s1=10.0; s2=10.0; s3=10.0
            glScale(s1, s2, s3)
            glutSolidIcosahedron()  # radius 1
            #glutSolidDodecahedron()  # radius 1
            #glScale(20.0, 20.0, 20.0)

        if False:
            glutSolidSphere(10.0, 40, 40) 

        glPopMatrix()

    def drawcell2(self, cellnum):
        CELLHEIGHT=self.CELLHEIGHT
        CELLWIDTH=self.CELLWIDTH
        (x, y, z) = self.cells[cellnum] 
        glPushMatrix()
        rr=random.randint(0, 359)
        glTranslatef(x, y, z)
        glRotatef(rr, 0.0, 1.0, 0.0)
        glutSolidSphere(10.0, 40, 40) 

        # axon
        axon=[]
        #axon.append((x, y, z))
        #gleSetJoinStyle(TUBE_JN_ANGLE | TUBE_CONTOUR_CLOSED | TUBE_NORM_PATH_EDGE)
        gleSetJoinStyle (TUBE_NORM_EDGE | TUBE_JN_ANGLE | TUBE_JN_CAP)

        cx=0; cz=0
        for al in range(-1, 20):
            xp=random.randint(0, 4) -2
            zp=random.randint(0, 4) -2
            #axon.append((xp, -10*al, zp))
            axon.append((cx, -10*al, cz))
            cx+=xp; cz+=zp
        glePolyCylinder(axon, None, 2)

        glPopMatrix()

    def drawcells(self):
        """ create a list of cells to plot, for speed
            note that the fat part of the pyramid is the output, where the axon comes out!
        """
        cells=self.cells
        CELLHEIGHT=self.CELLHEIGHT

        #glBegin(GL_POINTS)
        #for i in range(0, 1000):
        #    x=(random.random()*50.0)-25.0
        #    y=(random.random()*50.0)-25.0
        #    z=(random.random()*50.0)-25.0
        #    glVertex3f(x, y, z)
        #glEnd()

        #glColor3f(0.8, 0.8, 0.0)      # yellow
        glColor3f(0.9, 0.9, 0.9)      # whitish
        glLineWidth(1.0)
        #for k in [1]:
        for k in cells.keys():
            #(x, y, z) = cells[k] 
            #x=0; y=0; z=0
            if 0:
                glBegin(GL_POINTS)
                glVertex3f(x, y, z)
                glEnd()
            if 1:
                if random.random() < .15:
                    glColor3f(0.9, 0.0, 0.0)      # red
                    self.drawcell(k)
                    glColor3f(0.9, 0.9, 0.9)      # whitish
                else:
                    self.drawcell(k)
                #self.drawcell2(k)
            if 0:
                glBegin(GL_TRIANGLES)
                # make z more negative to shift down
                # make y more positive to put further away
                #glVertex3f(0, 150, -100)
                #glVertex3f(50, 150, -300)
                #glVertex3f(-50, 150, -300)
                glVertex3f(0, self.lasty, -100)
                glVertex3f(50, self.lasty, -300)
                glVertex3f(-50, self.lasty, -300)
                glEnd()    
            if 0:
                print "wirecube"
                glutWireCube(30.0)
            #print x, y, z

    def FindClosestAxonDendrite(self, c1, c2):
        #print "FindClosest", c1, c2
        ax=self.axons[c1]
        delist=self.dends[c2]
        #print "axon:", ax 
        #print "dend:", de 
        nax=len(ax)
        # for now, pick a random point in the second half or 2/3 of the axon:
        axpt=random.randint(nax/3, nax-3)
        (axx, axy, axz)=ax[axpt]
        # pick a dendrite to connect to
        mindi=5000000000
        cde=0       # current dendrite number
        for de in delist:
            nde=len(de)
            for pt in range(nde/3, nde):
                (dex, dey, dez)=de[pt]      # only look at points 1/3 away from cell, to reduce crowding
                dx=dex-axx; dy=dey-axy; dz=dez-axz
                di=dx*dx+dy*dy+dz*dz
                if di < mindi:
                    mindi=di
                    deidx=cde
                    dept=pt
                pt+=1
            cde+=1
        #print "closest point is on dendrite", deidx, "of", len(delist), "dendrite, with dist", mindi, "pt num", dept
        (dex, dey, dez)=(delist[deidx])[dept]
        return ((axx, axy, axz), (dex, dey, dez), mindi)

    def drawsyn(self, syns):
        """
            Now may only show a fraction of all synapses (showing all may make screen too cluttered)
            If SHOWSYNFRACTION is changed, have to re-draw display list by calling this routine.
        """
        CELLHEIGHT=self.CELLHEIGHT
        cells=self.cells
        if self.superpretty:        # FIXME clean this up . . . 
            gleSetJoinStyle (TUBE_NORM_EDGE | TUBE_JN_ANGLE | TUBE_JN_CAP)
            #glColor3f(0.0, 0.0, 0.9)        # blue
            glColor3f(0.9, 0.9, 0.9)        # white
        else:
            glEnable(GL_MAP1_VERTEX_3)
        for (c1, c2) in syns:
            if self.superpretty:
                if self.SHOWSYNAPSEFRACTION==None:
                    showthis=True
                elif random.random() < self.SHOWSYNAPSEFRACTION:
                    showthis=True
                else:
                    showthis=False
                if showthis:
                    ((x1, y1, z1), (x2, y2, z2), di)=self.FindClosestAxonDendrite(c1, c2)
                    if self.maxsyndist is not None:
                        if di > self.maxsyndist: continue
                    #print x1, y1, z1, x2, y2, z2
                    con=[]
                    x,y,z=x1,y1,z1
                    nseg=int(di/1000.0)
                    if nseg > 50: nseg=50
                    if nseg < 4: nseg=4
                    #print nseg
                    #nseg=20
                    dx=(float(x2)-float(x1))/float(nseg)
                    dy=(float(y2)-float(y1))/float(nseg)
                    dz=(float(z2)-float(z1))/float(nseg)
                    con.append((x-dx, y-dy, z-dz))
                    # these squiggles don't look too good if there isn't a dominant direction in y
                    # make a parabola?  bezier curve?
                    for s in range(nseg+1):     # make number of segs proportional to distance?
                        rx=random.randint(0, 4)-2
                        rz=random.randint(0, 4)-2
                        #rx=0; rz=0
                        con.append((x+rx, y, z+rz))  # repeat first point since first segment isn't drawn
                        x+=dx; y+=dy; z+=dz 
                    con.append((x, y, z))  # go one more point since last segment isn't drawn
                    #print "con", con
                    glePolyCylinder(con, None, .5)
                    continue
            (x1, y1, z1)=cells[c1]      # output comes from flat bottom of pyramid, at y
            #y1=y1+CELLHEIGHT
            (x2, y2, z2)=cells[c2]
            y2=y2+CELLHEIGHT    # connect *to* top of cell, thin part, input
            if self.SHOWSYNAPSEFRACTION==None:
                showthis=True
            elif random.random() < self.SHOWSYNAPSEFRACTION:
                showthis=True
            else:
                showthis=False
            if showthis:
                # points in our cell list have xz as a layer, flat, and y stacked up and down (cortical depth)
                # we want bezier curve to drop down a little for close connections (in a column)
                # and a lot for distant connections (area to area)
                # this captures that:
                # FIXME:  make bezier control points drop more dramatically near source and dest.
                # one drop in middle is too far.
                bezscale=math.sqrt((x1-x2)*(x1-x2) + (z1-z2)*(z1-z2))/2.0
                if ((x1-x2) < .5) and ((z1-z2)) < .5:   # if a cell connects to itself . . .
                    ctrlpoints=[[x1, y1, z1], [x1-20.0, y1+bezscale, z1-20.0], [x2-20.0, y2-bezscale, z2-20.0], [x2, y2, z2]]
                else:
                    ctrlpoints=[[x1, y1, z1], [x1, y1+bezscale, z1], [x2, y2-bezscale, z2], [x2, y2, z2]]
                glMap1f(GL_MAP1_VERTEX_3, 0.0, 1.0, ctrlpoints)    # no stride or order in pygl
                glBegin(GL_LINE_STRIP)
                SEGS=15
                for p in range(0, SEGS+1):      # curve will have 10 segments
                    glEvalCoord1f(float(p)/float(SEGS))      # uses the enabled glMap
                glEnd()

    def on_mouse(self, but, state, x, y):
        #print but, state, x, y 
        if but==3:
            self.lasty=self.lasty+10
            glutPostRedisplay()
        if but==4:
            self.lasty=self.lasty-10
            glutPostRedisplay()
        if but==0:
            if state==1:        # released, apparently
                #print "reset drag"
                self.startx=None    # reset drag start
                self.startz=None    # reset drag start

    def idle(self):
        if self.playspikes >= 0:
            nowt=time.time() 
            # we'll play back at 1/10 realtime, and there are 10000 ticks per second in
            # NCS.  this means we will play 1000 ticks per second
            #TIMESCALE=1000.0   # 1/10th realtime playback
            #TIMESCALE=500.0     # 1/20th realtime playback
            TIMESCALE=100.0     # 1/100th realtime playback
            eltime=nowt-self.playspikestarttime
            #print eltime
            stick=self.playspikestarttick  # not really tick, really time
            etick=eltime*TIMESCALE
            #print "displaying from ticks", stick, "to <", etick
            self.playspikestarttick=etick
            fi=self.fi
            # find the indices in the fi array that are in the desired range
            ps=0
            dcl=[]      # cells to draw/hilite this time
            psi=self.playspikestartidx
            pse=self.playspikeendidx
            while psi < pse:
                (spktype, timestep, cellnum) = fi[psi]
                if(timestep < etick):
                    psi=psi+1
                    ps=ps+1
                    dcl.append(cellnum)
                else:       # got all spikes up to current (scaled) time 
                    #print "breaking because ts >= etick", timestep, etick
                    break

            # FIXME:  this will result in irregular display times for cells
            # each cell should really appear for some fixed period after
            # it spikes
            if dcl: # there are cells to draw, replace spikeplay list
                dc=self.drawcell
                #glDeleteLists(self.PSLIST, 1)
                glNewList(self.PSLIST, GL_COMPILE)
                glColor3f(1.0, 0.0, 0.0)      # red
                #glColor3f(0.0, 0.0, 0.0)
                glLineWidth(4.0)
                for cn in dcl:
                    dc(cn) 
                glEndList()
                glutPostRedisplay()
                #print "drew", len(dcl), "cells"

            if psi >= pse:
                self.playspikes = -1    # done playing sequence after this one
                print "play spikes complete"
            # FIXME:  what about spikes in last group?  will they be shown?
            else:
                self.playspikestartidx=psi
            #print "found",ps,"spikes"
            
    def on_special(self, key, x, y):
        if key==GLUT_KEY_LEFT:
            #self.lastx-=10
            #glutPostRedisplay()
            print "left"
        elif key==GLUT_KEY_RIGHT:
            #self.lastx+=10
            #glutPostRedisplay()
            print "right"

    def ScreenCenter(self):
        if self.nvpx%2==1: sx=-self.w * (self.nvpx/2)
        else: sx=-self.w * ((self.nvpx+1)/2)
        if self.nvpy%2==1: sy=-self.h * (self.nvpy/2)
        else: sy=-self.h * ((self.nvpy+1)/2)
        print "starting x,y of viewport:", sx, sy
        return (sx, sy)

    def on_key(self, k, j, l):
        #print k, j, l
        if k=="z":
            self.lastz=self.lastz+10
            glutPostRedisplay()
        elif k=='V':
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            vw=self.w*self.nvpx; vh=self.h*self.nvpy
            if self.vp==(self.nvpx*self.nvpy - 1):
                print "back to normal"
                glViewport(0, 0, vw, vh)
                self.vp=0
            else:
                print "this is broken because vpx and vpy may be different now"
                vp=self.vp 
                xx=-self.w*(2-(vp%3))
                yy=-self.h*(2-(vp/3))
                print vp, xx, yy
                glViewport(xx, yy, vw, vh)
                self.vp+=1
            print self.w, self.h
            gluPerspective(120.0, float(self.w)/float(self.h), 10, 3000.0)
            glMatrixMode(GL_MODELVIEW)
            glutPostRedisplay()
        elif k=='v':
            import Image
            # full viewport size is vw x vh
            vw=self.w*self.nvpx; vh=self.h*self.nvpy
            # cycle through each viewport and take a snapshot
            #nvp=self.nvpx*self.nvpy
            bigimage=Image.new('RGB', (vw, vh))
            #sx=self.w/2; sy=self.h/2
            #cx=-((self.nvpx)/2)*self.w
            #if self.nvpx%2==0: cx+=sx
            #cx=-(self.nvpx-1)*self.w
            px=0
            #cx=-self.w
            cx=0
            # I don't understand why the viewport coordinates are specified all negative of 0, per example
            # at http://astronomy.swin.edu.au/~pbourke/opengl/windowdump/
            for vpx in range(0, self.nvpx):
                #cy=-((self.nvpy)/2)*self.h
                #if self.nvpy%2==0: cy+=sy
                #cy=-(self.nvpy-1)*self.h
                #cy=0
                cy=-(self.nvpy-1)*self.h
                py=0
                for vpy in range(0, self.nvpy):
                    #for vp in range(nvp):
                    #cx=sx+((vpx-1)-(self.nvpx+1)/2) * self.w
                    #cy=sy+((vpy-1)-(self.nvpy+1)/2) * self.h
                    print "vpx, vpy", vpx, vpy, "cx, cy", cx, cy
                    glMatrixMode(GL_PROJECTION)
                    glLoadIdentity()
                    glViewport(cx, cy, vw, vh)
                    gluPerspective(120.0, float(self.w)/float(self.h), self.near, self.far)
                    glMatrixMode(GL_MODELVIEW)
                    # we actually have to force a redraw *now* so we can't just post a redisplay
                    #glutPostRedisplay()
                    self.on_display() 
                    # now save this viewport
                    #ox, oy, width, height = glGetIntegerv(GL_VIEWPORT)
                    #print "viewport get shows w,h, x, y", width, height, ox, oy
                    #glPixelStorei(GL_PACK_ALIGNMENT, 1)
                    # we don't get the whole viewport, which is bigger than the screen
                    # we can only get our part
                    data = glReadPixels(0, 0, self.w, self.h, GL_RGB, GL_UNSIGNED_BYTE)
                    image = Image.fromstring("RGB", (self.w, self.h), data)
                    image = image.transpose(Image.FLIP_TOP_BOTTOM)
                    #oo=(self.w*(2-(vp%3)), self.h*((vp/3)))
                    oo=(px, py)
                    print "pasting viewport section to", oo
                    bigimage.paste(image, oo)
                    py+=self.h 
                    #cy-=self.h
                    cy+=self.h
                cx-=self.w
                px+=self.w
            # restore default viewport
            glMatrixMode(GL_PROJECTION)
            glLoadIdentity()
            sx,sy=self.ScreenCenter()
            glViewport(sx, sy, w*self.nvpx, h*self.nvpy)
            gluPerspective(120.0, float(self.w)/float(self.h), self.near, self.far)
            glMatrixMode(GL_MODELVIEW)
            glutPostRedisplay()
            bigimage.save('snap.png', 'PNG')
        elif k=="S":
            # use this one in non-superpretty mode
            import Image
            #width, height = self.getViewPort()
            ox, oy, width, height = glGetIntegerv(GL_VIEWPORT)
            print width, height, ox, oy
            glPixelStorei(GL_PACK_ALIGNMENT, 1)
            data = glReadPixels(0, 0, width, height, GL_RGB, GL_UNSIGNED_BYTE)
            image = Image.fromstring("RGB", (width, height), data)
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
            image.save("snap.png", "PNG")
        elif k=='L':
            r=2000; r2=1000
            self.light1Position=(random.randint(0,r)-r2, random.randint(0,r)-r2, random.randint(0,r)-r2, 0.0)
            print "light now at ", self.light1Position
            glLightfv(GL_LIGHT0, GL_POSITION, self.light1Position)
            glutPostRedisplay()
        elif k=='1':
            self.ambient+=.05
            if self.ambient> 1.0:
                self.ambient=0.0
            glLightfv(GL_LIGHT0, GL_AMBIENT, (self.ambient, self.ambient, self.ambient, 1))
            glutPostRedisplay()
            print "ambient now", self.ambient
        elif k=='2':
            self.diffuse+=.05
            if self.diffuse> 1.0:
                self.diffuse=0.0
            glLightfv(GL_LIGHT0, GL_DIFFUSE, (self.diffuse, self.diffuse, self.diffuse, 1))
            glutPostRedisplay()
            print "diffuse now", self.diffuse
        elif k=='3':
            # changing specular light strength doesn't seem to alter display.  why?
            # actually it does, but effect is very subtle.  look at red neurons.
            self.specular+=.05
            if self.specular> 1.0:
                self.specular=0.0
            glLightfv(GL_LIGHT0, GL_SPECULAR, (self.specular, self.specular, self.specular, 1))
            glutPostRedisplay()
            print "specular now", self.specular
        elif k=='4':
            # setting to 0.0 causes big change, but other than that not much difference
            self.shininess+=16.0
            if self.shininess>128.0:
                self.shininess=0.0
            glMaterial(GL_FRONT, GL_SHININESS, self.shininess);      # max 128
            glutPostRedisplay()
            print "shininess now", self.shininess
        elif k=='5':
            # can't tell any difference on poly tubes
            self.linesmooth=not self.linesmooth
            if self.linesmooth:
                print "line smooth on"
                glEnable(GL_LINE_SMOOTH)
            else:
                print "line smooth off"
                glDisable(GL_LINE_SMOOTH)
            glutPostRedisplay()
        elif k=='6':
            self.bgbrightness=self.bgbrightness+.05
            if self.bgbrightness > 1.0:
                self.bgbrightness=0.0
            glClearColor(self.bgbrightness, self.bgbrightness, self.bgbrightness, 0.0)
            print "background brightness ", self.bgbrightness
            glutPostRedisplay()
        elif k=="Z":
            self.lastz=self.lastz-10
            glutPostRedisplay()
        elif k=="y":
            self.lasty=self.lasty+5
            print "xyz", self.lastx, self.lasty, self.lastz
            glutPostRedisplay()
        elif k=="Y":
            self.lasty=self.lasty-5
            print "xyz", self.lastx, self.lasty, self.lastz
            glutPostRedisplay()
        elif k=="r":
            self.lastrad+=10
            print "view radius", self.lastrad
            glutPostRedisplay()
        elif k=="R":
            self.lastrad-=10
            print "view radius", self.lastrad
            glutPostRedisplay()
        elif k=="x":
            self.lastx=self.lastx+5
            print "xyz", self.lastx, self.lasty, self.lastz
            glutPostRedisplay()
        elif k=="X":
            self.lastx=self.lastx-5
            print "xyz", self.lastx, self.lasty, self.lastz
            glutPostRedisplay()
        elif k=="s":
            self.showesyn=not self.showesyn
            self.showisyn=self.showesyn
            glutPostRedisplay()
        elif k=="i":
            self.showisyn=not self.showisyn
            glutPostRedisplay()
        elif k=="e":
            self.showesyn=not self.showesyn
            glutPostRedisplay()
        elif k=="q" or ord(k)==27:
            #glutLeaveGameMode()
            sys.exit(0)
        elif k=="l":
            self.showlabels=not self.showlabels
            glutPostRedisplay()
        elif k=="c":      # turn on backface culling.  make this default at some point
            print "backface culling on"
            #glFrontFace(GL_CW)          # this makes fronts disappear
            glFrontFace(GL_CCW)          # this makes backs of neurons disappear.  what we want.
            glEnable(GL_CULL_FACE)
            glCullFace(GL_BACK)
            glutPostRedisplay()
        elif k=='f':
            self.showesyn=True
            self.showisyn=True
            if self.SHOWSYNAPSEFRACTION==None:
                self.SHOWSYNAPSEFRACTION=.1
            elif self.SHOWSYNAPSEFRACTION<.81:
                self.SHOWSYNAPSEFRACTION+=.1
            else: self.SHOWSYNAPSEFRACTION=None
            #print "show synapse fraction:", self.SHOWSYNAPSEFRACTION
            # regenerate synapse display list:
            self.RemakeSynLists()
            glutPostRedisplay()
        elif k=="p":
            self.playspikes=0
            self.playspikestarttime=time.time()
            self.playspikestartidx=0
            self.playspikeendidx=len(self.fi)
            #print "end index:", self.playspikeendidx
            # clear the play spike display list
            glNewList(self.PSLIST, GL_COMPILE)
            glEndList()
        else:
            print "got", ord(k)

    def on_motion(self, x, y):
        #print "motion", x, y
        #global lastx, lasty
        if False:
            self.lastx=x
            self.lasty=y
            glutPostRedisplay()
        #self.lastx=1000.0*math.sin(3.14159*(float(x)/800.0))
        #self.lastz=1000.0*math.cos(3.14159*(float(x)/800.0))
        if False:
            # screen y position defines distance from origin, x position defines
            # angular position on that radius; always look toward origin (via glutLookAt later)
            # this has good, intuitive motion control but unfortunately releasing and
            # reclicking causes jump to new point
            self.lastx=y*4.0*math.sin(3.14159*(float(x)/800.0))
            self.lastz=y*4.0*math.cos(3.14159*(float(x)/800.0))
            #print self.lastx, self.lastz
        if True:
            # alternate display method that modifies the current position rather than jumping
            # to new point
            if self.startx==None:
                self.startx=x
                self.startz=y
                dx=0
                dy=0
            else:
                dx=x-self.startx
                dy=y-self.startz 
                self.startx=x
                self.startz=y
            #print dy
            dy=dy*2.0   # bump up sensitivity
            self.lastrad=self.lastrad+dy
            self.lasttheta=self.lasttheta+(dx/100.0)
            self.lasttheta=self.lasttheta%(2*3.14159)
            #print dx, dy

        glutPostRedisplay()
        #print "xyz obs.", self.lastx, self.lasty, self.lastz

    def on_display(self):
        #print "on display"
        #glPushMatrix()
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #glTranslatef(self.lastx, self.lasty, -300.0)

        #glutEnterGameMode()
        if True:
            # new differential display approach
            self.lastx=self.lastrad*math.sin(self.lasttheta)
            self.lastz=self.lastrad*math.cos(self.lasttheta)
            #print self.lastx, self.lastz, self.lasty
            
        #print "on display", self.lastx, self.lasty, self.lastrad, self.lasttheta

        # if we don't clear before we draw, we just draw over previous stuff:
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glEnable(GL_LIGHTING)

        #glLoadIdentity()
        #glPushMatrix()      # keep an identity around
        # draw cells in world space, before we xform to view coords with LookAt:
        #glCallList(self.DLIST)      # cells

        # now transform all cells into view coords: 
        if 0:
            # with identity matrix we are looking into screen, down -z into distance
            glLoadIdentity()
            #glTranslatef(0.0, 0.0, -50.0)
            #glRotatef(self.lastx, 0.0, 1.0, 0.0)
            #glRotatef(self.lasty, 1.0, 0.0, 0.0)
        # leave everything at origin and just look from a different position toward origin
        else:
            #"The matrix generated by gluLookAt postmultiplies the current matrix."
            #"Viewing transformations must precede modeling transformations in OpenGL code."
            #glMatrixMode(GL_MODELVIEW)     # not needed if we never change Mode elsewhere
            glLoadIdentity()
            #print "lookfrom pos xyz", self.lastx, self.lasty, self.lastz
            # hmm, logically up look vec should be 0,1,0 (head up along y) but z seems to work right 
            # now, we always look FROM y=0 but at y=self.lasty.  then we can shift network up or down, essentially
            #gluLookAt(self.lastx, self.lasty, self.lastz, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
            #gluLookAt(self.lastx, 0, self.lastz, 0.0, self.lasty, 0.0, 0.0, 1.0, 0.0);
            # to keep horizontal view, look both from and at lasty
            gluLookAt(self.lastx, self.lasty, self.lastz, 0.0, self.lasty, 0.0, 0.0, 1.0, 0.0);
            #gluLookAt(200.0, 0.0, 200.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
            #gluLookAt(0.0, 0.0, 200.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0);
            #gluLookAt(0.0, 0.0, 0.0, 0.0, 0.0, -200.0, 0.0, 1.0, 0.0);

        #glColor3f(1.0, 0.0, 0.0)      # red
        #glutSolidCube(32.0)

        # going in to list, we have camera xform on top of stack
        # list will push it, use it for each draw, then pop back
        #glPushMatrix()
        glCallList(self.DLIST)      # cells
        #glPopMatrix()

        # show axes:
        if False:
            glColor3f(1.0, 0.0, 1.0)
            #glRasterPos2i(100,-240);
            #ax=[(0, 0, 0), (500, 0, 0), (0, 500, 0), (0, 0, 500), (-200, 0, 0), (200, 0, 0), (-500, 0, 0)]
            #ax=[(0, 0, 0), (500, 0, 0), (-200, 0, 0), (200, 0, 0), (-500, 0, 0)]
            ax=[(0, 0, 0), (0, 0, -500), (0, 0, -200), (0, 0, 200), (0, 0, 400)]
            for x, y, z in ax: 
                l="X %d, %d, %d" %(x, y, z)
                glRasterPos3i(x,y,z)
                for c in l:
                    glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

        # want text to be unlit 
        # want synapses to be unlit
        if self.showisyn or self.superpretty:
            glCallList(self.ISLIST)
        if self.showesyn or self.superpretty:
            glCallList(self.ESLIST)
        if self.playspikes >= 0:
            glCallList(self.PSLIST)

        glDisable(GL_LIGHTING)

        if 0:
            glColor3f(1.0, 0.0, 0.0)      # red
            # super simple sanity test;
            # we start by looking into screen, down z axis
            # -z is into screen
            glBegin(GL_TRIANGLES)
            # make z more negative to shift away into distance
            # make y more positive to put higher up 
            glVertex3f(0, 200, -400)
            glVertex3f(50, -50, -400)
            glVertex3f(-50, -50, -400)
            glEnd()    

        # show col/layer/cellgroup name identifiers on screen:
        # here we are using the first cell address.  might be
        # better to have precomputed the average
        # this comes after LookAt matrix is set up in Model view, so it will be transformed
        # it would be nice to have the text shown on top regardless of depth.
        if self.showlabels:
            #glColor3f(1.0, 0.0, 1.0)       # kind of magentaish
            #glColor3f(1.0, 1.0, 1.0)       # white
            glColor3f(0.0, 0.0, 0.0)        # black
            for k in self.names.keys():
                # kind of special purpose hack.  if we have a set of columns beginning
                # with name thal, data, or key, only display first label
                # remove this after Linux Journal article work :)
                if k[:4]=='thal':
                    if k[0:5]!='thal0':
                        continue
                if k[:4]=='data':
                    if k[0:7]!='datain0':
                        continue
                if k[:3]=='key':
                    if k[0:6]!='keyin0':
                        continue
                #for (x, y, z) in self.names[k]:        # label al in each cell group
                for (x, y, z) in self.names[k][:1]:     # label only first in each cell group
                    glRasterPos3i(int(x),int(y),int(z))
                    for c in k: glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(c))

            # we want these to be absolutely positioned on the screen.
            bigfont=GLUT_BITMAP_TIMES_ROMAN_24
            yspc=30
            glLoadIdentity()
            glColor3f(1.0, 1.0, 1.0)
            if self.showesyn or self.showisyn:
                s=self.SHOWSYNAPSEFRACTION
                if s==None: s=1.0
            else:
                s=0.0
            y=300
            k="%d%% of synapses shown" %(round(s*100.0))
            glRasterPos3i(-400,y,-200)
            for c in k: glutBitmapCharacter(bigfont, ord(c))

            y-=yspc
            glColor3f(1.0, 0.0, 0.0)
            k="Excitatory synapses in red"
            glColor3f(1.0, 0.0, 0.0)
            glRasterPos3i(-400,y,-200)
            glColor3f(1.0, 0.0, 0.0)
            for c in k: glutBitmapCharacter(bigfont, ord(c))

            y-=yspc
            glColor3f(0.0, 1.0, 0.0)
            k="Inhibitory synapses in green"
            glRasterPos3i(-400,y,-200)
            for c in k: glutBitmapCharacter(bigfont, ord(c))

        # current status:  putting bezier curves in CallList doesn't work, but
        glutSwapBuffers()

    def on_reshape(self, w, h):
        # untested.  make sure it uses same code as initial setup.  I don't think it does now.
        print "on reshape"
        return
        glViewport (0, 0, w, h)
        glMatrixMode (GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(40.0, w/h, 1.0, 20.0)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

def ReadBrainmap(fn, YSCALE, XZSCALE):
    """ my original file format """
    f=open(fn, "r") 
    l=f.readline()
    ncells=int(l.split()[0])
    print ncells,"cells to read"
    for l in range(0, ncells):
        l=f.readline()
        # for cell output from NCS, z is up and down (depth in cortex), for us y is up.  we convert here:
        (idx, x, z, y)=l.split()
        idx=int(idx)
        x=float(x)*XZSCALE
        y=float(y)*YSCALE      # to exaggerate height
        z=float(z)*XZSCALE
        #print idx, x, y, z 
        x=x*.5      # temp hack
        z=z*.5
        cells[idx]=(x, y, z)
    print "read all cells"
    l=f.readline()
    nsyns=int(l.split()[0])
    print nsyns,"syns to read"
    for l in range(0, nsyns):
        l=f.readline()
        (frm, sto, t)=l.split()
        frm=int(frm)
        sto=int(sto)
        syns.append((frm, sto, t, "unknown"))
        if(t=="e"):
            esyns.append((frm, sto))
        else:
            isyns.append((frm, sto))
    print "read all syns"
    return (cells, esyns, isyns, syns)

def ReadBrainmap2(fn, YSCALE, XZSCALE):
    """
        Read cell data from new file format
    """
    cells={}
    idxstart={}
    f=open(fn, "r") 
    names={}
    done=False
    idx=0
    while not done:
        try:
            l=f.readline()
            try:
                (colname, layname, clusname)=l.split()
            except:
                break
            #name=f.readline().split()
            ncells=int(f.readline())
            #print ncells,"to read for", colname, layname, clusname
            k=colname+"-"+layname+"-"+clusname
            idxstart[k]=idx
            print k
            for c in range(0, ncells):
                # z in input file is height, but it is our y
                (x, z, y)=f.readline().split()
                (x, y, z)=(XZSCALE*float(x), YSCALE*float(y)-YSHIFT, XZSCALE*float(z))
                cells[idx]=(x, y, z)
                names.setdefault(k, []).append((x, y, z))
                idx=idx+1
            f.readline()        # blank line at end
        except EOFError:
            done=True
    #print "max cell index",idx
    # FIXME self.maxcell=idx
    f.close()
    maxcell=idx
    return (cells, idxstart, maxcell, names)

def ReadSynmap2(fn, idxstart, maxcell):
    """
       Read synapses info from new file format.
    """
    esyns=[]
    isyns=[]
    syns=[]
    f=open(fn, "r")
    done=False
    while not done:
        try:
            (fcolname, flayname, fclusname, fcompname)=f.readline().split()
            (tcolname, tlayname, tclusname, tcompname)=f.readline().split()
            synname=f.readline().rstrip()
            if synname[0:3]=="Exc" or synname[0:3]=="exc" or synname[0]=="E" or synname[0]=="e":
                t="e"
            elif synname[0:3]=="Inh" or synname[0:3]=="inh" or synname[0]=="I" or synname[0]=="i":
                t="i"
            else:
                print "WARNING:  not sure if synname", synname, "is excitatory or inhibitory; assuming exc"
                t="e"
            (c, l)=f.readline().split()
            #print fcolname, flayname, fclusname, fcompname
            #print tcolname, tlayname, tclusname, fcompname
            #print c, l
            # what follows in input file is a bitmap of connections
            # dimensions of bitmap are dimensions of cellgroup (aka cluster)
            c=int(c); l=int(l)              # c is cols in each line, l is num lines
            fidx=idxstart[fcolname+"-"+flayname+"-"+fclusname]
            tidx=idxstart[tcolname+"-"+tlayname+"-"+tclusname]
            #print "from idx", fidx, "to idx", tidx, "cols ", c, "lines", l
            #print "max cell num ref will be", fidx+c, tidx+l
            tc=0
            for ln in range(0, l):
                li=f.readline()
                #print len(li),
                #print
                for fc in range(0, c):
                    #print li[fc],
                    if li[fc]=="1":
                        frm=fc+fidx; sto=tc+tidx;
                        #print frm, sto
                        if frm > maxcell:
                            print "cell ref err", frm, maxcell
                            sys.exit(0)
                        if sto > maxcell:
                            print "cell ref err", sto, maxcell
                            sys.exit(0)
                        syns.append((frm, sto, t, synname))
                        if(t=="e"):
                            esyns.append((frm, sto))
                        else:
                            isyns.append((frm, sto))
                tc=tc+1
            # note, no blank line after each set here, unlike cell file
        except:
            done=True
    f.close()
    return (syns, esyns, isyns)

def ReadFirefile(fn):
    """
      Read data from my original file format.
    """
    f=open(fn, "r")
    ln=0
    for l in f.xreadlines():
        (spktype, timestep, cellnum) = l.split()
        fi.append((spktype, float(timestep), int(cellnum)))
        ln=ln+1
    print "read", ln, "spikes from firefile"
    return fi

def ReadFirefile2(fn):
    """ Not implemented yet, wait for my hooks to be ported to latest NCS.
    """
    fi=[]
    return fi

def FreqPlotSyns(syns, maxcell):
    # cell conns gives all the synapses organized by each cell
    # key:  cell name, value:  hash of synvals
    #   key of that:  synapse name, value:  number of synapses of they type originating at that cell
    cellconns={}
    # reorganize syns by source cell:
    for (frm, sto, t, synname) in syns:
        if frm not in cellconns:
            cellconns[frm]={}
        h=cellconns[frm]
        if synname in h: h[synname]=h[synname]+1
        else: h[synname]=1
    #print cellconns
    # cellconns sums the above to give a network wide summary of how many synapses there are of each type
    # key:  synapse name, value:  number of synapses of that type in the entire network
    allconns={}
    for c in cellconns.keys():
        h=cellconns[c]     # h is one cell
        for s in h.keys():      # s is a synapse type
            if s in allconns:
                allconns[s]=allconns[s]+h[s]
            else:
                allconns[s]=h[s]
    #print allconns

    cellexcUSE={}
    # make frequency plot of cells having average excitatory x
    for (frm, sto, t, synname) in syns:
        # only doing this for exc synapses
        if synname[0]=="E":     # e.g. E__10 or E__5
            sv=int(synname[3:])
            if frm not in cellexcUSE:
                cellexcUSE[frm]=(sv, 1)
            else:
                (svt, n)=cellexcUSE[frm]
                svt=svt+sv
                n=n+1
                cellexcUSE[frm]=(svt, n)
    # now compute averages from total and n
    cellexcavg={}
    cellUSEbins={}
    for c in cellexcUSE:
        (svt, n)=cellexcUSE[c] 
        c=`c`
        # generalplot wants strings as x vals
        sv=float(svt)/float(n)
        cellexcavg[c]=sv
        sv=int(math.floor(sv))
        sv="%02d" % sv
        if sv in cellUSEbins:
            cellUSEbins[sv]=cellUSEbins[sv]+1
        else:
            cellUSEbins[sv]=1

    #print cellexcavg
    #print cellUSEbins
    #sys.exit(0)
    return (cellconns, allconns, cellexcavg, cellUSEbins)

if __name__ == '__main__':
    """
        for NCS SVN version use something like:
            ./netplot.py -b job13.cells.dat -s job13.synapse.dat
    """
    justfreq=False

    # default:  load c2.cells.dat and c2.synapse.dat in new format
    names={}
    oldformat=False
    brainmap="c2.cells.dat"
    synfile="c2.synapse.dat"
    firefile=None

    superpretty=False
    maxsyndist=None
    w=800; h=600
    nvpx=3; nvpy=4
    o, a = getopt.getopt(sys.argv[1:], "ob:f:s:d:FRp")
    for k,v in o:
        if k=="-o":
            print "using old style config files"
            oldformat=True
            brainmap="brainmap"
            synfile="None"
            firefile="firefile"
        elif k=="-p":
            superpretty=True
            w=1024; h=1024
            maxsyndist=30000.0
            print "superpretty! screen res", w, h, "screen cap res", w*nvpx, h*nvpy
            print "won't show synapses longer than", maxsyndist, "to reduce clutter of off-column connects"
            #w=3200; h=2400
        elif k=="-f":
            # my old style firefile
            firefile=v
        elif k=="-b":
            brainmap=v
        elif k=="-s":
            synfile=v
        elif k=="-d":
            brainmap=v+".cells.dat"
            synfile=v+".synapse.dat"
        elif k=="-F":
            # just print connection frequency map, don't do graphics
            justfreq=True
        elif k=="-R":
            import generalplot2

            v="exp8-t1/Gen0/job1"
            brainmap=v+".cells.dat"
            synfile=v+".synapse.dat"
            (cells0, idxstart0, maxcell0, names)=ReadBrainmap2(brainmap, YSCALE, XZSCALE)
            (syns0, esyns0, isyns0)=ReadSynmap2(synfile, idxstart0, maxcell0)
            print len(cells0), "cells"
            print len(syns0), "syns"
            (ch0, ah0, cea0, cub0)=FreqPlotSyns(syns0, maxcell0)

            v="exp8-t1/Gen300/job1"
            brainmap=v+".cells.dat"
            synfile=v+".synapse.dat"
            (cells1, idxstart1, maxcell1, names)=ReadBrainmap2(brainmap, YSCALE, XZSCALE)
            (syns1, esyns1, isyns1)=ReadSynmap2(synfile, idxstart1, maxcell1)
            (ch1, ah1, cea1, cub1)=FreqPlotSyns(syns1, maxcell1)
            
            if True:
                generalplot2.HistogramHash2("network USE", {"Gen0": ah0, "Gen300": ah1})

            #print "cea0:", cea0
            #print "cea1:", cea1
            if True:
                generalplot2.HistogramHash2("cell USE profile", {"Gen0": cub0, "Gen300": cub1})
            sys.exit(0)
    
    if oldformat:
        # FIXME:  not tested since loader functions pulled out of class
        # old file format
        (cells, esyns, isyns, syns)=ReadBrainmap(brainmap, YSCALE, XZSCALE)
        fi=ReadFirefile(firefile)
        #self.lastrad=2000.0
    else:
        # new file format
        (cells, idxstart, maxcell, names)=ReadBrainmap2(brainmap, YSCALE, XZSCALE)
        (syns, esyns, isyns)=ReadSynmap2(synfile, idxstart, maxcell)

    if justfreq:
        print len(cells), "cells"
        print len(syns), "synapses"
        FreqPlotSyns(syns, maxcell)
    else:
        print "superpretty is", superpretty
        NetPlot(cells, idxstart, maxcell, esyns, isyns, syns, names, w=w, h=h, superpretty=superpretty, maxsyndist=maxsyndist, nvpx=nvpx, nvpy=nvpy)

#gluLookAt(212, 60, 194,  186, 55, 171,  0, 1, 0);
# position, where you want to look, up vector
