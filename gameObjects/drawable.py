from typing import Any
from utils import SpriteManager, SCALE, RESOLUTION, EQUIPPED, INV, vec, rectAdd, SoundManager
from . import PixelBuilder
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
        
class Text(Drawable):
    """
    Displays text using the font from A Link to the Past
    """
    import os
    if not pygame.font.get_init():
        pygame.font.init()
    FONT_FOLDER = "fonts"
    FONT = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 16)
    BOX = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 14)
    SMALL = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 12)
    
    def __init__(self, position, text, color = (255,255,255), box = False, small = False):
        super().__init__(position, "")
        if small:
            self.image = Text.SMALL.render(text, False, color)
        elif box:
            self.image = Text.BOX.render(text, False, color)
        else:
            self.image = Text.FONT.render(text, False, color)


class AmmoBar(object):
    """
    Displays the currently selected arrow on the HUD
    """
    _INSTANCE = None
    
    @classmethod
    def getInstance(cls):
        if AmmoBar._INSTANCE == None:
            AmmoBar._INSTANCE = cls._AB()
            return AmmoBar._INSTANCE
        else:
            return AmmoBar._INSTANCE
    
    class _AB(Drawable):
        def __init__(self):
            super().__init__(vec(0,15), "ammo.png", (0, EQUIPPED["Arrow"]+1))
            self.damageId = 0
            self.backImage = SpriteManager.getInstance().getSprite("ammo.png", (self.damageId, 0))
            

        def setArrow(self, player):
            if player.arrowCount == 0:
                self.backImage = SpriteManager.getInstance().getSprite("ammo.png", (3, 0))
                self.image = SpriteManager.getInstance().getSprite("ammo.png", (self.damageId, EQUIPPED["Arrow"]+1))
            else:
                self.backImage = SpriteManager.getInstance().getSprite("ammo.png", (self.damageId, 0))
                self.image = SpriteManager.getInstance().getSprite("ammo.png", (self.damageId, EQUIPPED["Arrow"]+1))
            
        def draw(self, drawSurface, player):
            if player.hp == INV["max_hp"]:
                self.damageId = 1

            elif player.hp <= INV["max_hp"]//3 or player.hp == 1:
                self.damageId = 2
            else:
                self.damageId = 0
            
            self.setArrow(player)
            drawSurface.blit(self.backImage, self.position)
            super().draw(drawSurface)

"""
Displays the currently selected element on the HUD
"""
class ElementIcon(object):
    _INSTANCE = None
    
    @classmethod
    def getInstance(cls):
        if ElementIcon._INSTANCE == None:
            ElementIcon._INSTANCE = cls._EI()
            return ElementIcon._INSTANCE
        else:
            return ElementIcon._INSTANCE
    
    class _EI(Drawable):
        def __init__(self):
            super().__init__(vec(15,15), "element.png", (0,0))

        def draw(self, drawSurface):
            equipped = EQUIPPED["C"]
            if equipped != None:
                self.image = SpriteManager.getInstance().getSprite("element.png", (equipped+1, 0))
            super().draw(drawSurface)


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




        

class EnergyBar(Drawable):
    """
    Displays the player's energy meter on the HUD.
    For Gale Slash and Thunder Clap
    """
    def __init__(self):
        super().__init__(vec(0,31), "energy.png", (0,0))
        self.element = 0
        self.flashTimer = 0

    def setElement(self, int=0):
        self.element = int
        self.image = SpriteManager.getInstance().getSprite("energy.png", (self.element,0))

    def draw(self, drawSurface):
        super().draw(drawSurface)


    
    def drawWind(self, timer, drawSurface):
        """
        fill meter as timer increases
        """
        
        #convert timer to an int and shift decimal
        if timer < 2.5:
            convertedTimer = int(timer * 10)
        else:
            convertedTimer = 25

        #print(convertedTimer)
        #28 pixels to fill
        #1 pixel on top and 1 on bottom 
        drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (2, 0)), list(map(int, self.position)))
        
        innerFlash = pygame.Surface((1,1), pygame.SRCALPHA)
        innerFlash.fill(pygame.Color(0,235,0))

        light = pygame.Surface((1,1), pygame.SRCALPHA)
        light.fill(pygame.Color(0,220,0))
        green = pygame.Surface((1,1), pygame.SRCALPHA)
        green.fill(pygame.Color(0,180,0))

        def drawBar(timer, width, drawPos, edge = False):
            if edge:
                for i in range(width):
                    if timer >= 2.5:
                        if timer < 2.7:
                            light.fill(pygame.Color(0,255,0))
                        elif timer >= 2.7 and timer < 2.9:
                            light.fill(pygame.Color(0,220,0))
                        elif timer >= 2.9:
                            light.fill(pygame.Color(0,255,0))
                    drawSurface.blit(light, (drawPos[0]+i, drawPos[1]))
                return
            
            bottomPos = drawPos
            for i in range(1, width):
                if timer >= 2.5:
                    if timer < 2.7:
                        drawSurface.blit(innerFlash, (drawPos[0]+i, drawPos[1]))
                        light.fill(pygame.Color(0,255,0))
                    elif timer >= 2.7 and timer < 2.9:
                        drawSurface.blit(green, (drawPos[0]+i, drawPos[1]))
                        light.fill(pygame.Color(0,220,0))
                    elif timer >= 2.9:
                        drawSurface.blit(innerFlash, (drawPos[0]+i, drawPos[1]))
                        light.fill(pygame.Color(0,255,0))
                    
                    
                else:
                    drawSurface.blit(green, (drawPos[0]+i, drawPos[1]))

            drawSurface.blit(light, bottomPos)
            drawSurface.blit(light, (drawPos[0]+width-1, drawPos[1]))
        
        ##Draw bottom bar of pixels
        if timer > 0:
            drawPos = vec(3,60)
            drawBar(timer, 10, drawPos, edge=True)

            ##Draw the middle part
            if timer >= 0.1:
                drawPos = vec(2, 60-convertedTimer)
                yPos = int(drawPos[1])
                for i in range(60 - yPos):
                    drawPos[1] = yPos + i
                    drawBar(timer,12, drawPos)
   

                ##Draw the top pixel
                if convertedTimer >= 25:
                    drawPos = vec(2,34)
                    drawBar(timer,12, drawPos)
            
            

                    drawPos = vec(3,33)
                    drawBar(timer, 10, drawPos, edge= True)


        """ elif timer > 0:
            print("B")
            sprite = pygame.Surface((10,1), pygame.SRCALPHA)
            sprite.fill(pygame.Color(0,255,0))
            drawPos = vec(3,60-convertedTimer)
            drawSurface.blit(sprite, drawPos) """

            
     
        """ if timer >= 2.5:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (2, 5)), list(map(int, self.position)))
        elif timer >= 1.5:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (2, 3)), list(map(int, self.position)))
        elif timer >= 0.5:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (2, 2)), list(map(int, self.position)))
        else: """
        

    def drawThunder(self, timer, drawSurface):
        if timer == 0:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (1, 5)), list(map(int, self.position)))
        else:
            drawSurface.blit(SpriteManager.getInstance().getSprite("energy.png", (1, int(timer))), list(map(int, self.position)))
            