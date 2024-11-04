from typing import Any
from utils import SCALE, RESOLUTION, vec, rectAdd
from UI import SpriteManager
import pygame

"""
This file contains Drawable Objects, including HUD-related objects
and text-related objects.
"""

        
class Drawable(object):
    """
    Drawable object class written by Professor Matthews
    """
    
    CAMERA_OFFSET = vec(0,0)
    
    @classmethod
    def updateOffset(cls, trackingObject, worldSize):
        
        objSize = trackingObject.getSize()
        objPos = trackingObject.position
        
        offset = objPos + (objSize // 2) - (RESOLUTION // 2)
        
        for i in range(2):
            offset[i] = int(max(0,
                                min(offset[i],
                                    worldSize[i] - RESOLUTION[i])))
        
        cls.CAMERA_OFFSET = offset

    @classmethod
    def resetOffset(cls):
        cls.CAMERA_OFFSET = vec(0,0)

    @classmethod    
    def translateMousePosition(cls, mousePos):
        newPos = vec(*mousePos)
        newPos /= SCALE
        newPos += cls.CAMERA_OFFSET
        
        return newPos
    
    def __init__(self, position=vec(0,0), fileName="", offset=None):
        
        if fileName != "":
            self.image = SpriteManager.getInstance().getSprite(fileName, offset)
        
        self.position  = vec(*position)
        self.imageName = fileName
        self.block = False

    def draw(self, drawSurface, drawHitbox = False, use_camera = True):
        if use_camera:
            drawSurface.blit(self.image, list(map(int, self.position - Drawable.CAMERA_OFFSET)))
        else:
            drawSurface.blit(self.image, list(map(int, self.position)))
            
        if drawHitbox:
            collision = rectAdd(-Drawable.CAMERA_OFFSET, self.getCollisionRect())
            pygame.draw.rect(drawSurface, (255,255,255), collision, 1)

    def getSize(self):
        return vec(*self.image.get_size())
    
    """
    Returns the x coordinate on the screen
    representing the center point
    """
    def getCenterX(self):
        size = self.getSize()
        x = size[0] // 2
        return self.position[0] + x
    
    def handleEvent(self, event):
        pass
    
    def update(self, seconds):
        pass
    
    
    def getCollisionRect(self):
        newRect = self.image.get_rect()
        newRect.left = int(self.position[0])
        newRect.top = int(self.position[1])
        return newRect
    
    def doesCollide(self, other):
        return self.getCollisionRect().colliderect(other.getCollisionRect())   
    
    def doesCollideList(self, others):
        rects = [r.getCollisionRect() for r in others]
        return self.getCollisionRect().collidelist(rects)


class Level(Drawable):
    """
    Gets the image for the level using the SpriteManager
    """
    def __init__(self, fileName):
        super().__init__((0,0), "")
        self.image = SpriteManager.getInstance().getLevel(fileName)


class Number(Drawable):
    """
    If number >= 10
    """
    def __init__(self, position = vec(0,0), number = 0, row = 0):
        super().__init__(position, "numbers.png", (number,row))
    
    def getImage(number = 0, row = 0):
        return SpriteManager.getInstance().getSprite("numbers.png",(number,row))
    

class DamageIndicator(Drawable):
    """
    Displays the health, name, and image
    of the currently targeted (last hit) enemy
    """
    def __init__(self):
        super().__init__(vec(RESOLUTION[0] - 58, 0), "indicator.png", (0,0) )
        self.invisible = True
        self.row = 0
        self.indicatorTimer = 0
        self.currentHp_before = 0
        self.currentHp = 0
        self.currentMaxHp = 0
        self.currentDrawPos = 0#X position of current draw position
        self.pixelBuilder = PixelBuilder()
        self.currentPixels = []
        self.pixelsToDraw = 0

        
    
    
    def draw(self, drawSurface):
        if not self.invisible:
            super().draw(drawSurface)
            if self.row > 0:
                index = 0
                for p in self.currentPixels:
                    index += 1
                    drawSurface.blit(p.getPixel(), p.getDrawPos())


    def setPixelsToDraw(self, value):
        self.pixelsToDraw = value

    def setImage(self, value, hp_before=0, hp_after=0, maxHp = 0, damage = 0):
        """
        Called every time an enemy is struck.
        Start from far right
        Calculate # of pixels to turn white based on damage and max hp
        Subtract drawPos[0] and increase the width of the pixels
        to draw by the same amount
        Turn that # of pixels white
        Wait a bit
        Gradually turn the white pixels black
        But just fill in the pixels with black according to
        hp_before

        Expects the following parameters:
        value -> int value of enemy's indicator image row
        hp_before -> enemy's hp before taking damage
        hp_after -> enemy's hp after taking damage
        maxHp -> enemy's max hp
        damage -> the damage dealt to the enemy

        MaxHp - previous hp, draw those pixels
        then draw current pixels
        """
        ##Turn invisible and return if setImage(0) called
        if value == 0:
            #self.pixelsToDraw = 0
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (0, value))
            self.invisible = True
            return
        
        self.invisible = False
        ##Reset the indicator timer
        self.indicatorTimer = 0
        ##Set the row value if not already set to that row
        if value != self.row:
            self.row = value
        
        ##Defining temporary variables
        self.currentHp_before = hp_before
        self.currentHp = hp_after
        self.currentMaxHp = maxHp
        #Temporary list object used to draw the pixels
        currentPixels = []

        
        cumulativeDamage = self.currentMaxHp - self.currentHp 
        result = self.currentMaxHp // 28
        if result == 0:
            #Figure out how to draw x pixels for every 1 pt of damage
            result = 1
        else:
            #draw 1 pixel for every result points of damage
            self.setPixelsToDraw(cumulativeDamage // result)
        

        #pixelsToDraw = int(pixelsPerHit * damage)
        #prevPixels = int(pixelsPerHit * (self.currentMaxHp - self.currentHp))
        

        ##Adjust drawPos to account for previously dealt damage
        self.currentDrawPos = (self.position[0]+53)


        ##Set the indicator imagess
        if self.currentHp <= 0:
            #Enemy dead, make the indicator invisible
            self.row = 0
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (0, 0))
            self.indicatorTimer = 0
        else:
            self.image = SpriteManager.getInstance().getSprite("indicator.png", (0, value))

        for i in range(self.pixelsToDraw):
            self.pixelBuilder.addPixel(currentPixels, vec(self.currentDrawPos - i, self.position[1]+8), 1, 8, color = (0,0,0))
        
        self.currentPixels = currentPixels


        """         if black > 0:
            #print("B")
            ##Add black pixels
            for i in range(black):
                self.pixelBuilder.addPixel(self.currentPixels, vec(self.currentDrawPos - i, self.position[1]+8), 1, 8, color = (0,0,0))
            
            ##Add white pixels
            for i in range(black, (pixelsToDraw - black)):
                self.pixelBuilder.addPixel(self.currentPixels, vec(self.currentDrawPos - i, self.position[1]+8), 1, 8)

        else:
            #print("C")
            ##First hit
            ##Add the necessary pixels to the pixelBuilder
            ##pixelsToDraw needs to be an int for looping
            for i in range(pixelsToDraw):
                self.pixelBuilder.addPixel(self.currentPixels, vec(self.currentDrawPos - i, self.position[1]+8), 1, 8) """
        
        
    
    def update(self, seconds):
        """
        Update the pixelBuilder and indicatorTimer.
        Set the indicator to invisible after 3 seconds
        of no action.
        """
        if self.row > 0:
            #If currently targeting an enemy
            #self.pixelBuilder.update(seconds)
            self.indicatorTimer += seconds
            if self.indicatorTimer >= 3:
                #Set invisible
                self.setImage(0)




        


            