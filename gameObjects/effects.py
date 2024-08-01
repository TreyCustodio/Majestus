
from . import Drawable
import pygame
from utils import SpriteManager, vec

"""
This file contains several objects that add special effects
to room images. Additionally, I've decided to include
all the building blocks that compose a room's layers, such as
tiles, walls, etc. for more precice effects, as well as
the Camera.
"""

class Camera(object):
    def __init__(self, position = vec(0,0)):
        self.position = position
    
    def getSize(self):
        return vec(304,208)
        
class Floor(Drawable):
    """
    The bottom layer of a room that may be animated
    """
    def __init__(self, room_dir, prefix = "tiles", animate = False, nFrames = 6, fps = 8, tick = 3):
        self.position = vec(0,0)
        self.prefix = prefix
        
        self.animate = animate
        if animate:
            self.roomDir = room_dir
            self.frame = 0
            self.nFrames = nFrames
            self.fps = fps
            self.frameTimer = 0.0
            self.image = SpriteManager.getInstance().getFx(self.roomDir, self.prefix  + "_" + str(self.frame+1)+".png")
        else:
            self.image = SpriteManager.getInstance().getFx(room_dir, prefix + ".png")
        
    def update(self, seconds):
        if self.animate:
            ##Update frame
            if self.frameTimer > 1 / self.fps:
                self.frameTimer -= 1 / self.fps
                self.frame += 1
                self.frame %= self.nFrames
                self.image = SpriteManager.getInstance().getFx(self.roomDir, self.prefix  + "_" + str(self.frame+1)+".png")
            else:
                self.frameTimer += seconds
   

class Walls(Drawable):
    """
    The walls are most commonly placed on the layer
    directly above tiles
    """
    def __init__(self, room_dir, animate = False):
        self.position = vec(0,0)
        self.image = SpriteManager.getInstance().getFx(room_dir, "walls.png")

class Shadow(Drawable):
    
    """
    A transparent shadow/light object
    @param color -> rgb color value
    @param alpha -> alpha value
    """
    def __init__(self, room_dir, fileName = "", alpha=48, minAlpha=100, animate = False, nFrames = 6, fps = 8, tick = 3):
        
        if animate:
            if fileName == "":
                self.image = SpriteManager.getInstance().getFx(room_dir, "shadow_1.png")
            else:
                self.image = SpriteManager.getInstance().getFx(room_dir, fileName)
            self.animate = nFrames > 1
            self.frameTimer = 0.0
            self.fps = fps
            self.frame = 0
            self.fading_in = True
            self.nFrames = nFrames
            
        else:
            if fileName == "":
                self.image = SpriteManager.getInstance().getFx(room_dir, "shadow.png")
            else:
                self.image = SpriteManager.getInstance().getFx(room_dir, fileName)
            self.animate = False

        self.roomDir = room_dir
        self.image.set_alpha(alpha)
        self.position = vec(0,0)
        self.alpha = alpha
        self.maxAlpha = alpha
        self.minAlpha = minAlpha
        self.tick = tick

    def setAlpha(self):
        self.image.set_alpha(self.alpha)

    
    def update(self, seconds):
        if self.animate:
            
            ##Update frame
            if self.frameTimer > 1 / self.fps:
                self.frameTimer -= 1 / self.fps
                self.frame += 1
                self.frame %= self.nFrames
                self.image = SpriteManager.getInstance().getFx(self.roomDir, "shadow_"+str(self.frame+1)+".png")
            else:
                self.frameTimer += seconds
            
            ##Glow effect
            if self.fading_in:
                self.alpha += self.tick
                if self.alpha >= self.maxAlpha:
                    self.alpha = self.maxAlpha
                    self.fading_in = False
            else:
                self.alpha -= self.tick 
                if self.alpha <= self.minAlpha:
                    self.alpha = self.minAlpha
                    self.fading_in = True
            self.setAlpha()
            
class WhiteOut(Drawable):
    def __init__(self, position = vec(0,0)):
        self.position = position
        self.image = SpriteManager.getInstance().getSprite("white.png")
        self.image.set_alpha(0)
        self.alpha = 0
    
    def reset(self):
        self.image.set_alpha(0)
        self.alpha = 0

    def setAlpha(self):
        self.image.set_alpha(self.alpha)

    def update(self, seconds):
        if self.alpha <= 255:
            self.alpha += 5
            self.image.set_alpha(self.alpha)
        else:
            self.image.set_alpha(self.alpha)

class AreaIntro(Drawable):
    def __init__(self, room_dir, fileName = "area_intro.png", position = vec(0,0)):
        self.position = position
        self.image = SpriteManager.getInstance().getFx(room_dir, fileName)
        self.image.set_alpha(0)
        self.fading = False
        self.fading_in = False
        self.fading_out = False
        self.alpha = 0
        self.timer = 0.0
        
    def fadeIn(self):
        self.fading = True
        self.fading_in = True

    def update(self, seconds):
        if self.fading:
            if self.fading_in:
                if self.alpha <= 255:
                    self.alpha += 5
                    self.image.set_alpha(self.alpha)
                else:
                    self.fading_in = False
            elif self.fading_out:
                if self.alpha >= 0:
                    self.alpha -= 5
                    self.image.set_alpha(self.alpha)
                else:
                    self.fading_out = False
                    self.fading = False
            else:
                if self.timer >= 2.0:
                    self.timer = 0.0
                    self.fading_out = True
                else:
                    self.timer += seconds
            
      