from . import Drawable, Animated, Number, IconManager
from utils import SpriteManager, SoundManager, vec, INV, RESOLUTION, EQUIPPED, INV, ACTIVE_SHORTCUT, SHORTCUTS
import pygame

class HudButtons(object):
    """
    Controls button images on the HUD.
    Draws the correct button based on the controller.
    """

    def draw(drawSurface):
        ##  Shoot, Element, Dodge
        drawSurface.blit(IconManager.getButton("shoot"), vec(0, 24))
        drawSurface.blit(IconManager.getButton("element"), vec(19, 24))
        drawSurface.blit(IconManager.getButton("interact"), vec(19*2, 24))

        ##  Shortcuts
        pos = AmmoBar.getInstance().getShortcutPos()
        drawSurface.blit(IconManager.getButton("shortcut_left"), (pos[0] - 21, pos[1] + 17))
        drawSurface.blit(IconManager.getButton("shortcut_right"), (pos[0] + 33, pos[1] + 17))
        drawSurface.blit(IconManager.getButton("shortcut_trigger"), (pos[0] + 6, pos[1] + 24))

class AmmoBar(object):
    """
    Displays the currently selected arrow on the HUD
    Naming conventions are off in this class. Try to keep to to camelCaseJavaStyle or c_case_style
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
            self.shortCutBackground = SpriteManager.getInstance().getSprite("shortcut.png", (0,0))
            self.shortCutLeft  = SpriteManager.getInstance().getSprite("shortcut.png", (1,0))
            self.shortCutRight = SpriteManager.getInstance().getSprite("shortcut.png", (1,0))

            self.shortCutImage = None
            self.shortcutPos = vec(272,0)
            self.big_box = vec(0,0)
            self.shortcutImages = {
                0:None,
                1:None,
                2:None,
                3:None,
                4:None,
                5:None,
            }
            self.ammoImages = {
                0:False,
                1:False,
                2:False,
                3:False,
                4:False,
                5:False,
            }

        def getShortcut_image(self, index: int = 0):
            if self.shortcutImages[index]:
                return pygame.transform.scale(self.shortcutImages[index], (16,16))
        
        def setShortcutImage(self, item, index: int = 0):
            """
            Params:
            item -> ("action", attack_integer)
            """
            image = None
            ammo = False

            ##  Display Main shortcut
            if item[0] == "shoot":
                if item[1] == 0:
                    image = SpriteManager.getInstance().getSprite("ammo.png", (0,1))
                elif item[1] == 1:
                    image = SpriteManager.getInstance().getSprite("ammo.png", (0,2))
                    ammo = True

            elif item[0] == "element":
                id = item[1]
                if id == 0:
                    image = SpriteManager.getInstance().getSprite("element.png",(1,0))
                elif id == 1:
                    image = SpriteManager.getInstance().getSprite("element.png",(2,0))
                elif id == 2:
                    image = SpriteManager.getInstance().getSprite("element.png",(3,0))
                elif id == 3:
                    image = SpriteManager.getInstance().getSprite("element.png",(4,0))
                elif id == 4:
                    pass
                elif id == 5:
                    pass
                elif id == 6:
                    pass
                elif id == 7:
                    pass

            elif item[0] == "item":
                id = item[1]
                if id == 0:
                    image = SpriteManager.getInstance().getSprite("item.png",(3,0))
                elif id == 1:
                    image = SpriteManager.getInstance().getSprite("item.png",(2,0))
                    ammo = True
                elif id == 2:
                    ammo = True
                    image = SpriteManager.getInstance().getSprite("item.png",(9,0))
                elif id == 3:
                    ammo = True
                    image = SpriteManager.getInstance().getSprite("item.png",(6,0))
                elif id == 4:
                    ammo = True
                    image = SpriteManager.getInstance().getSprite("item.png",(7,0))
                elif id == 5:
                    ammo = True
                    image = SpriteManager.getInstance().getSprite("item.png",(8,0))
                elif id == 6:
                    pass
                elif id == 7:
                    pass
            
            if image:
                pass
            self.shortcutImages[index] = image
            self.ammoImages[index] = ammo


        def drawNumber(self, position, number, drawSurface, row = 0):
            position += Drawable.CAMERA_OFFSET
            if number >= 10:
                currentPos = vec(position[0]-3, position[1])
                number = str(number)
                for char in number:
                    num = Number(currentPos, int(char), row)
                    num.position[0] -= num.getSize()[0] // 2
                    
                    num.draw(drawSurface)
                    currentPos[0] += 6
            else:
                ##Items
                num = Number(position, number, row)
                num.image = pygame.transform.scale(num.image, (32,32))
                num.position[0] -= num.getSize()[0] // 2 + 6
                num.position[1] -= 12
                num.draw(drawSurface)


        def setArrow(self, player):
            if not player.arrowReady:
                self.backImage = SpriteManager.getInstance().getSprite("ammo.png", (3, 0))
                self.image = SpriteManager.getInstance().getSprite("ammo.png", (self.damageId, EQUIPPED["Arrow"]+1))
            else:
                self.backImage = SpriteManager.getInstance().getSprite("ammo.png", (self.damageId, 0))
                self.image = SpriteManager.getInstance().getSprite("ammo.png", (self.damageId, EQUIPPED["Arrow"]+1))
        
        def getShortcutPos(self):
            return self.big_box
        
        def draw(self, drawSurface, player):
            if player.hp <= INV["max_hp"]//3 or player.hp == 1:
                self.damageId = 2
            elif player.hp == INV["max_hp"]:
                self.damageId = 1
            else:
                self.damageId = 0
            
            self.setArrow(player)
            drawSurface.blit(self.backImage, self.position)
            drawSurface.blit(self.image, self.position)
            

            ##  Shortcuts
            self.big_box = (self.shortcutPos[0] - 32, self.shortcutPos[1])
            drawSurface.blit(self.shortCutBackground, self.big_box)
            drawSurface.blit(self.shortCutLeft, (self.big_box[0]-19, self.big_box[1]+8))
            drawSurface.blit(self.shortCutRight, (self.big_box[0]+35, self.big_box[1]+8))
            
            ##  Calculate index of active shortcut and left/right shortcuts
            active = ACTIVE_SHORTCUT[0]
            active_left = active - 1
            if active_left < 0:
                active_left = 5
            active_right = active + 1
            if active_right > 5:
                active_right = 0
            
            ##  Left and Right Shortcuts
            if self.shortcutImages[active_left]:
                drawSurface.blit(self.shortcutImages[active_left], (self.big_box[0] - 19, self.big_box[1] + 8))
            if self.shortcutImages[active_right]:
                drawSurface.blit(self.shortcutImages[active_right], (self.big_box[0] + 35, self.big_box[1] + 8))

            ##  Main Shortcut Image
            if self.shortcutImages[ACTIVE_SHORTCUT[0]]:
                drawSurface.blit(pygame.transform.scale(self.shortcutImages[ACTIVE_SHORTCUT[0]], (32,32)), (self.big_box))
                if self.ammoImages[ACTIVE_SHORTCUT[0]]:
                    if SHORTCUTS[ACTIVE_SHORTCUT[0]][0] == "item":
                        pos = (self.big_box[0] + 30, self.big_box[1] + 16)
                        id = SHORTCUTS[ACTIVE_SHORTCUT[0]][1]
                        if id == 1:
                            self.drawNumber(pos, INV["potion"], drawSurface)
                        elif id == 2:
                            self.drawNumber(pos, INV["smoothie"], drawSurface)
                        elif id == 3:
                            self.drawNumber(pos, INV["beer"], drawSurface)
                        elif id == 4:
                            self.drawNumber(pos, INV["joint"], drawSurface)
                        elif id == 5:
                            self.drawNumber(pos, INV["speed"], drawSurface)

                    else:
                        pos = (self.big_box[0] + 16, self.big_box[1] + 12)
                        self.drawNumber(pos, INV["bombo"], drawSurface)

        def update(self, seconds):
            if self.shortcutImages[ACTIVE_SHORTCUT[0]]:
                pass
                #self.shortcutImages[ACTIVE_SHORTCUT[0]].set_alpha(50)
                    
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
            drawSurface.blit(self.image, (self.position[0] + 4, self.position[1]))

            dodge = EQUIPPED["Dodge"]
            if dodge != None:
                image = SpriteManager.getInstance().getSprite("element.png", (dodge+1, 0))
                drawSurface.blit(image, (self.position[0] + 4 + 19, self.position[1]))


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
        return
        drawSurface.blit(self.image, self.position)


    
    def drawWind(self, timer, drawSurface):
        """
        fill meter as timer increases
        """
        
        #convert timer to an int and shift decimal
        if timer < 2.5:
            convertedTimer = int(timer * 10)
        else:
            convertedTimer = 25

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
            position += Drawable.CAMERA_OFFSET
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
                        #self.damageToDraw = 0
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

    def draw(self, drawSurface, drawHitbox=False, use_camera=True):
        drawSurface.blit(self.image, self.position)

"""
Manages images in the hud in a singleton style
"""
class HudImageManager(object):

    MONEY = None
    KEYS = None
    BOMBOS = None
    OBJECTS = []
    dropTimer = 0.0
    abovePlayer = vec(0,0)
    vibrationTick = 0

    def initialize():
        HudImageManager.MONEY = HudImage((0, RESOLUTION[1]-50), offset= (0,1))
        HudImageManager.KEYS = HudImage((0, RESOLUTION[1]-16), offset=(0,3))
        HudImageManager.BOMBOS = HudImage((0, RESOLUTION[1]-34), offset=(0,8))
        
    def addObject(obj):
        HudImageManager.OBJECTS = []
        HudImageManager.dropTimer = 0.0
        HudImageManager.vibrationTick = 0
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
                drawSurface.blit(o, (HudImageManager.abovePlayer[0], HudImageManager.abovePlayer[1] + HudImageManager.vibrationTick))

    def update(seconds, player):
        if HudImageManager.MONEY != None:
            HudImageManager.MONEY.update(seconds)
        if HudImageManager.KEYS != None:
            HudImageManager.KEYS.update(seconds)
        if HudImageManager.BOMBOS != None:
            HudImageManager.BOMBOS.update(seconds)

        if HudImageManager.OBJECTS:
            HudImageManager.dropTimer += seconds
            if HudImageManager.dropTimer >= 0.5:
                HudImageManager.dropTimer = 0.0
                HudImageManager.OBJECTS = []
                HudImageManager.vibrationTick = 0
            

        HudImageManager.abovePlayer = vec(player.position[0] + 1, player.position[1] - 16) - Drawable.CAMERA_OFFSET


class Wipe(object):
    def __init__(self) -> None:
        self.image = pygame.transform.scale(SpriteManager.getInstance().getSprite("fade.png"), (304, 208))
        self.alpha = 0
        self.image.set_alpha(0)
        self.circle = SpriteManager.getInstance().getSprite("black.png", (0,1))
        self.increasing = False
        self.decreasing = False
        self.alpha_delta = 1
        
        ##Values for Animations##
        self.nFrames = 9
        self.framesPerSecond = 20
        self.frameTimer = 0.0
        self.animate = True
        self.frame = 0
        self.row = 0
        self.animate = True
        self.mode = "fade"
    
    def draw(self, drawSurface):
        drawSurface.blit(self.image, vec(0,0))
        if self.mode == "circle":
            drawSurface.blit(self.circle, vec(0,0))

    def setColor(self, color: tuple):
        self.image.fill(color)
        
    def setMode(self, name: str = "fade"):
        self.mode = name

    def setAlpha(self, value: int):
        if value <= 255 and value >= 0:
            self.alpha = value
            self.image.set_alpha(value)

    def increase(self, speed: int = 1):
        self.alpha_delta = speed
        self.setAlpha(0)
        self.increasing = True
        self.circle.set_alpha(255)
        if self.mode == "circle":
            self.animate = True
            self.reverse = False
    
    def decrease(self, speed: int = 1):
        self.alpha_delta = speed
        self.setAlpha(255)
        self.decreasing = True
        if self.mode == "circle":
            self.animate = True
            self.reverse = True

    def updateFade(self):
        if self.increasing:
            self.alpha += self.alpha_delta
            if self.alpha > 255:
                self.alpha = 255
                self.increasing = False
                self.image.set_alpha(self.alpha)
            else:
                self.image.set_alpha(self.alpha)
        
        elif self.decreasing:
            self.alpha -= self.alpha_delta
            if self.alpha < 0:
                self.alpha = 0
                self.decreasing = False
                self.image.set_alpha(self.alpha)
            else:
                self.image.set_alpha(self.alpha)

    def updateCircle(self, seconds):
        if self.animate:
            self.frameTimer += seconds
            if self.frameTimer > 1 / self.framesPerSecond:
                
                if self.reverse:
                    self.frame -= 1
                    if self.frame == -1:
                        self.animate = False
                        self.circle.set_alpha(0)
                        return
                    self.frameTimer -= 1/self.framesPerSecond
                    self.circle = SpriteManager.getInstance().getSprite("black.png",
                                                        (self.frame, 1))

                else:
                    self.frame += 1
                    if self.frame == 9:
                        self.animate = False
                        return
                    self.frameTimer -= 1/self.framesPerSecond
                    self.circle = SpriteManager.getInstance().getSprite("black.png",
                                                        (self.frame, 1))

    def update(self, seconds):
        if self.mode == "fade":
            self.updateFade()
        
        elif self.mode == "circle":
            self.updateFade()
            self.updateCircle(seconds)

        elif self.mode == "triangle":
            pass