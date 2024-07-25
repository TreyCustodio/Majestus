from . import Drawable, Animated, Number
from utils import SpriteManager, SoundManager, vec, INV, RESOLUTION
import pygame


class HealthBar(object):
    """
    Displays the player's health on the HUD
    Make singleton!
    """
    _INSTANCE = None


    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._HB()
        return cls._INSTANCE

    class _HB(object):
        def __init__(self):
            self.position = vec(0,0)
            self.fileName = "bar.png"

            ###Pixel IVs
            self.edge = SpriteManager.getInstance().getSprite(self.fileName, (6,0))
            ##Green pixels
            self.edgeG = SpriteManager.getInstance().getSprite(self.fileName, (7,0))
            self.green = SpriteManager.getInstance().getSprite(self.fileName, (8,0))
            ##Red pixels
            self.edgeR = SpriteManager.getInstance().getSprite(self.fileName, (0,0))
            self.red1 = SpriteManager.getInstance().getSprite(self.fileName, (1,0))
            self.red2 = SpriteManager.getInstance().getSprite(self.fileName, (2,0))
            self.red3 = SpriteManager.getInstance().getSprite(self.fileName, (3,0))
            self.red4 = SpriteManager.getInstance().getSprite(self.fileName, (4,0))
            self.red5 = SpriteManager.getInstance().getSprite(self.fileName, (5,0))
            self.red6 = SpriteManager.getInstance().getSprite(self.fileName, (9,0))
            self.red7 = SpriteManager.getInstance().getSprite(self.fileName, (10,0))
            self.edgeL = SpriteManager.getInstance().getSprite(self.fileName, (11,0))
            self.red8 = SpriteManager.getInstance().getSprite(self.fileName, (12,0))
            self.white = SpriteManager.getInstance().getSprite(self.fileName, (13,0))
            ##lowHp
            self.low1 = SpriteManager.getInstance().getSprite(self.fileName, (14,0))
            self.low2 = SpriteManager.getInstance().getSprite(self.fileName, (15,0))
            self.low3 = SpriteManager.getInstance().getSprite(self.fileName, (16,0))
            self.low4 = SpriteManager.getInstance().getSprite(self.fileName, (17,0))
            self.low5 = SpriteManager.getInstance().getSprite(self.fileName, (18,0))
            #White flashing
            self.low6 = SpriteManager.getInstance().getSprite(self.fileName, (19,0))
            self.low7 = SpriteManager.getInstance().getSprite(self.fileName, (20,0))
            self.low8 = SpriteManager.getInstance().getSprite(self.fileName, (21,0))
            self.low9 = SpriteManager.getInstance().getSprite(self.fileName, (22,0))
            self.low10 = SpriteManager.getInstance().getSprite(self.fileName, (23,0))
            self.whiteL = SpriteManager.getInstance().getSprite(self.fileName, (24,0))

            ###other IVs
            self.drawPos = vec(16,0)
            self.pixelsToDraw = 0
            self.drawn = False
            self.reloading = False
            self.hurtTimer = 0
            self.flashTick = 0#Ticks every 0.2 seconds
            self.drawingHurt = False
            self.damageToDraw = 0
            self.fillerPixels = 0 #Background of red hp bar
            self.subtractingPixels = False
            self.drawingHeal = False
            self.healthPixels = 0
            self.heartFrame = 0
            self.heartFps = 4
            self.heartTimer = 0.0

        
        def getLength(self):
            return 17 + (INV["max_hp"] * 5) + 2

        def getTotalPixels(self):
            return INV["max_hp"] * 5
        
        def getHeartImage(self, player):
            if player.hp == INV["max_hp"]:
                return SpriteManager.getInstance().getSprite("heart.png", (self.heartFrame,1))
            elif player.hp <= INV["max_hp"] // 3:
                return SpriteManager.getInstance().getSprite("heart.png", (self.heartFrame, 0))
            else:
                return SpriteManager.getInstance().getSprite("heart.png", (self.heartFrame, 0))
        
        def blit(self, drawSurface, color):
            drawSurface.blit(color, self.drawPos)
            self.drawPos[0] += 1


        def drawNumber(self, position, number, drawSurface, row = 0):
            if number >= 10:
                currentPos = vec(position[0]-3, position[1])
                number = str(number)
                for char in number:
                    num = Number(currentPos, int(char), row)
                    num.position[0] -= num.getSize()[0] // 2
                    num.draw(drawSurface)
                    currentPos[0] += 6
            else:
                num = Number(position, number, row)
                num.position[0] -= num.getSize()[0] // 2
                num.draw(drawSurface)

        def drawFull(self, drawSurface, player):
            ##Green##
            pixelsToDraw = INV["max_hp"] * 5
            drawSurface.blit(self.edgeG, self.drawPos)
            self.drawPos[0]+= 1
            for i in range(pixelsToDraw):
                drawSurface.blit(self.green, self.drawPos)
                self.drawPos[0] += 1
            drawSurface.blit(self.edgeG, self.drawPos)
            self.drawPos[0] += 1
            drawSurface.blit(self.edge, self.drawPos)
            self.drawPos = vec(16,0)


        ##  For hurt:
        ##  Draws in 2 stages: blinking and subtracting
        def drawRed(self, drawSurface, player, low = False):
            blackPix = (INV["max_hp"] * 5) - (player.hp * 5)
            if self.drawingHeal:
                pixelsToDraw = (player.hp - self.amountToFill // 5) * 5
            else:
                pixelsToDraw = player.hp * 5 #Regular hp, no shading
            if low == True:
                self.blit(drawSurface, self.edgeL)
            else:
                self.blit(drawSurface, self.red6)

            
            if self.drawingHurt:
                #pixelsToDraw - self.damageToDraw//5 - 1
                #Red pixels
                for i in range(pixelsToDraw-(self.damageToDraw//5)-1):
                    if low == True:
                        self.blit(drawSurface, self.low1)
                    else:
                        self.blit(drawSurface, self.red1)
                
                if self.subtractingPixels:
                    ##Subtracting
                    """
                    Each frame, the number of red1 to draw decreases by 1
                    and the number of red5 to draw increases.
                    """
                    for i in range(self.damageToDraw//5 + 1):
                        if low:
                            self.blit(drawSurface, self.low1)
                        else:
                            self.blit(drawSurface, self.red1)

                    for i in range(self.damageToDraw):
                        if low:
                            self.blit(drawSurface, self.low1)
                        else:
                            self.blit(drawSurface, self.red1)
                    
                    for i in range(self.fillerPixels-(self.damageToDraw - 5)):
                        if low:
                            self.blit(drawSurface, self.low5)
                        else:
                            self.blit(drawSurface, self.red5)
                    if low:
                        self.blit(drawSurface, self.edgeL)
                    else:
                        self.blit(drawSurface, self.red6)

                else:
                    ##Blinking
                    #red pixels
                    for i in range(self.damageToDraw//5 + 1):
                        if low:
                            self.blit(drawSurface, self.low1)
                        else:
                            self.blit(drawSurface, self.red1)

                    #White flashing
                    for i in range(self.damageToDraw):
                        if self.flashTick % 2 == 0:
                            if low:
                                self.blit(drawSurface, self.whiteL)
                            else:
                                self.blit(drawSurface, self.white)
                        else:
                            if low:
                                self.blit(drawSurface, self.low1)
                            else:
                                self.blit(drawSurface, self.red1)
                    
                    #Filler
                    for i in range(self.fillerPixels - (self.damageToDraw - 5)):
                        if low:
                            self.blit(drawSurface, self.low5)
                        else:
                            self.blit(drawSurface, self.red5)
                    
                    if low:
                        self.blit(drawSurface, self.edgeL)
                    else:
                        self.blit(drawSurface, self.red6)



            elif self.drawingHeal:
                ##Healing
                for i in range((pixelsToDraw-2) + self.healthPixels):
                    if low:
                        self.blit(drawSurface, self.low1)
                    else:
                        self.blit(drawSurface, self.red1)
                
                ##2 pixels for shading
                if low:
                    self.blit(drawSurface, self.low2)
                    self.blit(drawSurface, self.low3)
                    for i in range(self.fillerPixels):
                        self.blit(drawSurface, self.low5)
                    
                    self.blit(drawSurface, self.edgeL)
                
                else:
                    drawSurface.blit(self.red2, self.drawPos)
                    self.drawPos[0] += 1
                    drawSurface.blit(self.red3, self.drawPos)
                    self.drawPos[0] += 1

                    for i in range(self.fillerPixels):
                        drawSurface.blit(self.red5, self.drawPos)
                        self.drawPos[0] += 1

                    drawSurface.blit(self.red6, self.drawPos)
                    self.drawPos[0] += 1

            else:
                ##Regular draw routine
                #Red pixels
                for i in range(pixelsToDraw-2):
                    if low == True:
                        self.blit(drawSurface,self.low1)
                    else:
                        self.blit(drawSurface, self.red1)
                
                ##2 pixels for shading
                if low == True:
                    self.blit(drawSurface, self.low2)
                    self.blit(drawSurface, self.low3)
                    for i in range(blackPix):
                        self.blit(drawSurface, self.low5)
                    
                    self.blit(drawSurface, self.edgeL)
                else:
                    drawSurface.blit(self.red2, self.drawPos)
                    self.drawPos[0] += 1
                    drawSurface.blit(self.red3, self.drawPos)
                    self.drawPos[0] += 1

                    for i in range(blackPix):
                        drawSurface.blit(self.red5, self.drawPos)
                        self.drawPos[0] += 1

                    drawSurface.blit(self.red6, self.drawPos)
                    self.drawPos[0] += 1

            drawSurface.blit(self.edge, self.drawPos)
            self.drawPos = vec(16,0)

        def drawHeart(self, drawSurface, player):
            drawSurface.blit(self.getHeartImage(player), self.position)
            self.drawNumber(vec(8,0), player.hp, drawSurface)

        def drawFirst(self, drawSurface, player):
            """
            self.pixelsToDraw starts at 0.
            Every frame, in update, self.pixelsToDraw increments.
            Eventually self.pixelsToDraw == (INV["max_hp"] * 5) + 1
            """
            if not pygame.mixer.get_busy():
                SoundManager.getInstance().playSFX("OOT_MagicRefill.wav")
            for i in range(self.pixelsToDraw):
                drawPos = vec(16,0)
                if i >= 0:
                    drawSurface.blit(self.edgeG, drawPos)
                    drawPos[0] += 1
                if i >= 1:
                    for j in range(i):
                        drawSurface.blit(self.green, drawPos)
                        drawPos[0] += 1
                if i >= (INV["max_hp"] * 5) - 1:
                    drawSurface.blit(self.edgeG, drawPos)
                    drawPos[0] += 1
                if i == INV["max_hp"] * 5:
                    drawSurface.blit(self.edge, drawPos)
                    self.drawn = True
                    self.pixelsToDraw = 0
                    player.keyUnlock()
                    SoundManager.getInstance().stopSFX("OOT_MagicRefill.wav")
            

        def drawHurt(self, hp, damage):
            """
            Turn damage * 5 pixels red
            Interrupt healing
            """
            self.subtractingPixels = False
            self.drawingHeal = False
            self.drawingHurt = True
            self.hurtTimer = 0
            self.flashTick = 0
            self.damageToDraw = (damage * 5)
            self.fillerPixels = ((INV["max_hp"] - hp) * 5) - 5


        def drawHeal(self, amountHealed):
            self.amountToFill = amountHealed * 5
            self.fillerPixels = self.amountToFill
            self.drawingHeal = True


        def draw(self, drawSurface, player):
            """
            Green at full, red at low.
            Draw 5 pixels of the healthbar per 1 hp
            """
            ##Full Health
            if player.hp == INV["max_hp"]:
                if not self.drawingHeal:
                    self.drawFull(drawSurface, player)
                else:
                    self.drawRed(drawSurface, player)
            
            elif player.hp == 1 or player.hp <= INV["max_hp"] // 3:
                self.drawRed(drawSurface, player, low = True)
            ##Regular Display
            else:
                self.drawRed(drawSurface, player)
                

        def reload(self):
            self.reloading = True
            self.hurtTimer = 0
            self.drawingHurt = False
            self.drawingHeal = False
            self.subtractingPixels = False
            self.flashTick = 0
            self.damageToDraw = 0
            self.fillerPixels = 0
            self.pixelsToDraw = INV["max_hp"]
            self.drawPos = vec(18+self.pixelsToDraw, 0)


        def update(self, seconds):
            """
            Draws 1 pixel of the healthbar
            each frame on initialization.
            """
            if self.heartTimer > 1/self.heartFps:
                self.heartTimer -= 1/ self.heartFps
                self.heartFrame += 1
                self.heartFrame %= 4
            else:
                self.heartTimer += seconds
            if self.drawingHurt:
                if self.subtractingPixels:
                    self.damageToDraw -= 1
                    if self.damageToDraw == 0:
                        self.pixelsToDraw = 0
                        self.fillerPixels = 0
                        self.subtractingPixels = False
                        self.drawingHurt = False
                else:
                    self.hurtTimer += seconds
                    if self.hurtTimer >= 0.2:
                        self.flashTick += 1
                        #Iframes last 3 flashticks
                        if self.flashTick == 3:
                            self.flashTick = 0
                            self.subtractingPixels = True
                        self.hurtTimer = 0
                
            elif self.drawingHeal:
                self.healthPixels += 1
                self.fillerPixels -= 1
                if self.healthPixels > self.amountToFill:
                    self.drawingHeal = False
            elif self.reloading:
                ##Reload the hp bar after getting an upgrade
                self.pixelsToDraw -= 1
            elif not self.drawn:
                ##Initialization of the healthbar
                self.pixelsToDraw += 1


"""
Represents animated images on the HUD
"""
class HudImage(Animated):
    def __init__(self, position, offset, nFrames=4, fps=2):
        super().__init__(position, fileName="drops.png", offset=(0,0))
        self.row = offset[1]
        self.nFrames = nFrames
        self.framesPerSecond = fps
        self.image = SpriteManager.getInstance().getSprite("drops.png", offset)


"""
Manages images in the hud in a singleton style
"""
class HudImageManager(object):

    MONEY = None
    KEYS = None
    BOMBOS = None
    OBJECTS = []

    def initialize():
        HudImageManager.MONEY = HudImage((0, RESOLUTION[1]-50), offset= (0,1))
        HudImageManager.KEYS = HudImage((0, RESOLUTION[1]-16), offset=(0,3))
        HudImageManager.BOMBOS = HudImage((0, RESOLUTION[1]-34), offset=(0,8))
        
    def addObject(obj):
        HudImageManager.OBJECTS.append(obj)

    def getHealth():
        return HealthBar.getInstance()
     
    def getMoney():
        return HudImageManager.MONEY
    
    def getKeys():
        return HudImageManager.KEYS

    def getBombos():
        return HudImageManager.BOMBOS

    def getObjects():
        return HudImageManager.OBJECTS

    def draw(drawSurface):
        if HudImageManager.OBJECTS:
            for o in HudImageManager.OBJECTS:
                o.draw(drawSurface)

    def update(seconds):
        if HudImageManager.MONEY != None:
            HudImageManager.MONEY.update(seconds)
        if HudImageManager.KEYS != None:
            HudImageManager.KEYS.update(seconds)
        if HudImageManager.BOMBOS != None:
            HudImageManager.BOMBOS.update(seconds)

        if HudImageManager.OBJECTS:
            for o in HudImageManager.OBJECTS:
                o.update(seconds)
