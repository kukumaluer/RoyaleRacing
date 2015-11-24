# Roaming-car was modified to remove collision part.

import direct.directbase.DirectStart
from panda3d.core import Filename,AmbientLight,DirectionalLight
from panda3d.core import PandaNode,NodePath,Camera,TextNode
from panda3d.core import Vec3,Vec4,BitMask32
from direct.gui.OnscreenText import OnscreenText
from direct.actor.Actor import Actor
from direct.showbase.DirectObject import DirectObject
from direct.interval.IntervalGlobal import *  # Needed to use Intervals
import random, sys, os, math
from panda3d.core import LVector3
from panda3d.core import *


# Function to put instructions on the screen.
def addInstructions(pos, msg):
    return OnscreenText(text=msg, style=1, fg=(1,1,1,1),
                        pos=(-1.3, pos), align=TextNode.ALeft, scale = .05)

# Function to put title on the screen.
def addTitle(text):
    return OnscreenText(text=text, style=1, fg=(1,1,1,1),
                        pos=(1.3,-0.95), align=TextNode.ARight, scale = .07)



def ModelSet(name):

    return NodePath(name)

class World(DirectObject):

    def __init__(self):
        
        self.setupLights()

        self.keyMap = {"left":0, "right":0, "forward":0, "cam-left":0, "cam-right":0}
        base.win.setClearColor(Vec4(0,0,0,1))

       


        self.env = loader.loadModel("models/env")
        self.env.reparentTo(render)
        self.env.setPos(0,0,-1)
        self.env.setScale(200,200,200)
        self.environ_tex = loader.loadTexture("models/env_sky.jpg")
        self.env.setTexture(self.environ_tex, 1)
        self.period_cloud = self.env.hprInterval(400, (360, 0, 0))
        self.period_cloud.loop()
        


 

        self.ground = loader.loadModel("models/Ground2")      
        self.ground.reparentTo(render)
        self.ground.setPos(0,0,0)
        self.ground.setScale(0.5,0.5,0)
        self.ground_tex = loader.loadTexture("models/ground.tif")
        self.ground.setTexture(self.ground_tex, 1)

        
        # Create the main character, car

        self.car = Actor("models/batcar")
        self.car.reparentTo(render)
        self.car.setScale(.6)
        self.car.setPos(-11,-5,0.17)



        


        # self.track = loader.loadModel("models/track(nowalls)")      
        # self.track.reparentTo(render)
        # self.track.setPos(0,0,0)
        # self.track.setScale(0.6,0.6,1)
        # self.track_tex = loader.loadTexture("models/road2.jpg")
        # self.track.setTexture(self.track_tex,1)

        # self.wall = loader.loadModel("models/trackwalls2wall")      
        # self.wall.reparentTo(render)
        # self.wall.setPos(0,0,0)
        # self.wall.setScale(0.6,0.6,1)
        # self.wall_tex = loader.loadTexture("models/ads2.jpg")
        # self.wall.setTexture(self.wall_tex,1)

        # self.hills = loader.loadModel("models/land")      
        # self.hills.reparentTo(render)
        # self.hills.setPos(0,0,0)
        # self.hills.setScale(0.6,0.6,1)
        # self.hill_tex = loader.loadTexture("models/mt.jpg")
        # self.hill_tex.setWrapU(Texture.WM_mirror)
        # self.hill_tex.setWrapV(Texture.WM_mirror)
        # self.hills.setTexture(self.hill_tex,1)

       
        
       

        # Create a floater object.  We use the "floater" as a temporary
        # variable in a variety of calculations.
        
        self.floater = NodePath(PandaNode("floater"))
        self.floater.reparentTo(render)

        # Accept the control keys for movement and rotation

    

        self.accept("escape", sys.exit)
        self.accept("arrow_left", self.setKey, ["left",1])
        self.accept("arrow_right", self.setKey, ["right",1])
        self.accept("arrow_up", self.setKey, ["forward",1])
        self.accept("a", self.setKey, ["cam-left",1])
        self.accept("s", self.setKey, ["cam-right",1])
        self.accept("arrow_left-up", self.setKey, ["left",0])
        self.accept("arrow_right-up", self.setKey, ["right",0])
        self.accept("arrow_up-up", self.setKey, ["forward",0])
        self.accept("a-up", self.setKey, ["cam-left",0])
        self.accept("s-up", self.setKey, ["cam-right",0])
        self.accept('x', self.toggleTerrain)
        self.accept('c', self.toggleTrack1)
        self.accept('v', self.toggleTrack2)
        self.accept('r', self.reset1)
        self.accept('n', self.reset2)

        taskMgr.add(self.move,"moveTask")

        # Game state variables
        self.isMoving = False

        # Set up the camera
        
        base.disableMouse()
        base.camera.setPos(self.car.getX(),self.car.getY()+10,2)


    def setupLights(self):    

        # Create some lighting
        ambientLight = AmbientLight("ambientLight")
        ambientLight.setColor(Vec4(.3, .3, .3, 1))
        directionalLight1 = DirectionalLight("directionalLight")
        directionalLight1.setDirection(Vec3(5, 5, -5))
        directionalLight1.setColor(Vec4(1, 1, 1, 1))
        directionalLight1.setSpecularColor(Vec4(1, 1, 1, 1))
        directionalLight2 = DirectionalLight("directionalLight")
        directionalLight2.setDirection(Vec3(5, -5, -5))
        directionalLight2.setColor(Vec4(1, 1, 1, 1))
        directionalLight2.setSpecularColor(Vec4(1, 1, 1, 1))
        directionalLight3 = DirectionalLight("directionalLight")
        directionalLight3.setDirection(Vec3(-5, -5, -5))
        directionalLight3.setColor(Vec4(1, 1, 1, 1))
        directionalLight3.setSpecularColor(Vec4(1, 1, 1, 1))
        directionalLight4 = DirectionalLight("directionalLight")
        directionalLight4.setDirection(Vec3(-5, 5, -5))
        directionalLight4.setColor(Vec4(1, 1, 1, 1))
        directionalLight4.setSpecularColor(Vec4(1, 1, 1, 1))
        render.setLight(render.attachNewNode(ambientLight))
        render.setLight(render.attachNewNode(directionalLight1))
        render.setLight(render.attachNewNode(directionalLight2))
        render.setLight(render.attachNewNode(directionalLight3))
        render.setLight(render.attachNewNode(directionalLight4))


      

    
    #Records the state of the arrow keys
    def setKey(self, key, value):
        self.keyMap[key] = value

    def reset1(self):
        self.set1.removeNode()
        

    def reset2(self):
        self.set2.removeNode()



    def toggleTerrain(self):

        self.hills = loader.loadModel("models/land")      
        self.hills.reparentTo(render)
        self.hills.setPos(0,0,0)
        self.hills.setScale(0.6,0.6,1)
        self.hill_tex = loader.loadTexture("models/mt.jpg")
        self.hill_tex.setWrapU(Texture.WM_mirror)
        self.hill_tex.setWrapV(Texture.WM_mirror)
        self.hills.setTexture(self.hill_tex,1)

    def toggleTrack1(self):

        self.set1 = ModelSet("set1")
        self.set1.reparentTo(render)

        self.track = loader.loadModel("models/track(nowalls)")      
        self.track.reparentTo(self.set1)
        self.track.setPos(0,0,0)
        self.track.setScale(0.6,0.6,1)
        self.track_tex = loader.loadTexture("models/road2.jpg")
        self.track.setTexture(self.track_tex,1)

        self.wall = loader.loadModel("models/trackwalls2wall")      
        self.wall.reparentTo(self.set1)
        self.wall.setPos(0,0,0)
        self.wall.setScale(0.6,0.6,1)
        self.wall_tex = loader.loadTexture("models/ads2.jpg")
        self.wall.setTexture(self.wall_tex,1)

        self.line = loader.loadModel("models/startline")      
        self.line.reparentTo(self.set1)
        self.line.setPos(-11,-5,0.175)
        self.line.setScale(1.8,1.8,0)
        self.line_tex = loader.loadTexture("models/startline.jpg")
        self.line.setTexture(self.line_tex, 1)
       

    def toggleTrack2(self):

        self.set2 = ModelSet("set2")
        self.set2.reparentTo(render)

        self.track = loader.loadModel("models/track(nowalls)")      
        self.track.reparentTo(self.set2)
        self.track.setPos(0,0,0)
        self.track.setScale(0.6,0.6,1)
        self.track_tex = loader.loadTexture("models/road2.jpg")
        self.track.setTexture(self.track_tex,1)

        self.wall = loader.loadModel("models/trackwallsmt")      
        self.wall.reparentTo(self.set2)
        self.wall.setPos(0,0,0)
        self.wall.setScale(0.6,0.6,1)
        self.wall_tex = loader.loadTexture("models/mt2.jpg")
        self.wall.setTexture(self.wall_tex,1)

        self.line = loader.loadModel("models/startline")      
        self.line.reparentTo(self.set2)
        self.line.setPos(-11,-5,0.175)
        self.line.setScale(1.8,1.8,0)
        self.line_tex = loader.loadTexture("models/startline.jpg")
        self.line.setTexture(self.line_tex, 1)

        

    # Accepts arrow keys to move either the player or the menu cursor,
    # Also deals with grid checking and collision detection
    def move(self, task):

        # If the camera-left key is pressed, move camera left.
        # If the camera-right key is pressed, move camera right.

        base.camera.lookAt(self.car)
        if (self.keyMap["cam-left"]!=0):
            base.camera.setX(base.camera, -20 * globalClock.getDt())
        if (self.keyMap["cam-right"]!=0):
            base.camera.setX(base.camera, +20 * globalClock.getDt())

        # save car's initial position so that we can restore it,
        # in case he falls off the map or runs into something.

        startpos = self.car.getPos()

        # If a move-key is pressed, move car in the specified direction.

        if (self.keyMap["left"]!=0):
            self.car.setH(self.car.getH() + 300 * globalClock.getDt())
        if (self.keyMap["right"]!=0):
            self.car.setH(self.car.getH() - 300 * globalClock.getDt())
        if (self.keyMap["forward"]!=0):
            self.car.setY(self.car, -25 * globalClock.getDt())

        # If car is moving, loop the run animation.
        # If he is standing still, stop the animation.

        if (self.keyMap["forward"]!=0) or (self.keyMap["left"]!=0) or (self.keyMap["right"]!=0):
            if self.isMoving is False:
                self.car.loop("run")
                self.isMoving = True
        else:
            if self.isMoving:
                self.car.stop()
                self.car.pose("walk",5)
                self.isMoving = False

        # If the camera is too far from car, move it closer.
        # If the camera is too close to car, move it farther.

        camvec = self.car.getPos() - base.camera.getPos()
        camvec.setZ(0)
        camdist = camvec.length()
        camvec.normalize()
        if (camdist > 10.0):
            base.camera.setPos(base.camera.getPos() + camvec*(camdist-10))
            camdist = 10.0
        if (camdist < 5.0):
            base.camera.setPos(base.camera.getPos() - camvec*(5-camdist))
            camdist = 5.0

         
        # The camera should look in car's direction,
        # but it should also try to stay horizontal, so look at
        # a floater which hovers above car's head.
        
        self.floater.setPos(self.car.getPos())
        self.floater.setZ(self.car.getZ() + 2.0)
        base.camera.lookAt(self.floater)

        return task.cont


w = World()
run()

