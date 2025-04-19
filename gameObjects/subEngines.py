import pygame

from . import Drawable,  Animated, Text, Highlight, Map, Number, AmmoBar

from utils import vec, RESOLUTION, SpriteManager, SoundManager, INV, INFO, COORD, EQUIPPED, SHORTCUTS, ACTIVE_SHORTCUT

from UI import ACTIONS, EventManager

from pygame.locals import *

class PauseEngine(object):


    def __init__(self):
        """
        Initialize item icons.
        Screen is 304 x 200

        [               ]  
        

        
        [               ]

        128 x 96 space
        16 x 16 squares
        beggining at (3,1)

        if self.link.hasItem:
        items.append(item)
        for i in items:
            i.draw
        
        """
        self.inPosition = False
        self.closed = False
        self.closing = False
        self.mapOpen = False
        self.paused = False
        self.textBox = False
        self.text = ""
        self.icon = None
        self.boxPos = vec(30,64)
        self.joyTimer = 0.0
        self.trackAnalog = True

        self.menu = Drawable(vec(0,100), "Pause.png")
        self.timer = 0
        self.highlight = Highlight(COORD[3][4])
        self.highlightQuit = Highlight(COORD[3][8], flag = 1)
        self.highlighted = vec(0,0)
        self.promptResult = False
        self.promptFlag = ""

        
        ##  Button Icons
        self.scaled = False
        self.interactIcon = SpriteManager.getInstance().getSprite("keys.png", (2,0))
        self.elementIcon = SpriteManager.getInstance().getSprite("keys.png",(3,0))
        self.shootIcon = SpriteManager.getInstance().getSprite("keys.png",(5,0))
        self.triggerIcon = SpriteManager.getInstance().getSprite("keys.png", (1,0))

        ##  Transition states
        self.toShortcuts = False
        self.toInventory = False
        self.inShortcuts = False
        self.placing = False
        self.toSettings = False
        self.inSettings = False

        ##  Fading
        self.alpha = 255
        self.fading_in = False
        self.fading_out = False
        self.item = None

    def resetMenu(self):
        self.menu.position = vec(0,100)
        self.item = None
        self.placing = False
        self.inPosition = False
        self.closing = False
        self.closed = False
        self.paused = False
        self.menu.position[0] = 0
        self.inShortcuts = False
        self.toShortcuts = False
        self.toInventory = False
        self.highlighted = vec(0,0)
        self.highlight.position = vec(16*3, 16*4)
        self.fading_in = False
        self.fading_out = False

    def drawNumber(self, position, number, drawSurface, row = 0):
        if number >= 10:
            currentPos = vec(position[0]-3, position[1])
            number = str(number)
            for char in number:
                num = Number(currentPos, int(char), row)
                num.position[0] -= num.getSize()[0] // 2
                num.draw(drawSurface, use_camera=False)
                currentPos[0] += 6
        else:
            num = Number(position, number, row)
            num.position[0] -= num.getSize()[0] // 2
            num.draw(drawSurface, use_camera=False)

    def drawEquipped(self, drawSurf):
        if self.inShortcuts:
            image = AmmoBar.getInstance().getShortcut_image(0)
            if image != None:
                drawSurf.blit(image, COORD[13][5])
            
            image = AmmoBar.getInstance().getShortcut_image(1)
            if image != None:
                drawSurf.blit(image, COORD[16][5])
            
            image = AmmoBar.getInstance().getShortcut_image(2)
            if image != None:
                drawSurf.blit(image, COORD[13][7])
            
            image = AmmoBar.getInstance().getShortcut_image(3)
            if image != None:
                drawSurf.blit(image, COORD[16][7])
            
            image = AmmoBar.getInstance().getShortcut_image(4)
            if image != None:
                drawSurf.blit(image, COORD[13][9])
            
            image = AmmoBar.getInstance().getShortcut_image(5)
            if image != None:
                drawSurf.blit(image, COORD[16][9])

        else:
            #Arrow
            arrow = EQUIPPED["Arrow"]
            imageA = SpriteManager.getInstance().getSprite("item.png", (arrow, 3))
            drawSurf.blit(imageA, (COORD[14][4]))
            if arrow == 1:
                self.drawNumber((16*15 + 2, 16*4 -2), INV["bombo"], drawSurf, row = 4)
            #Element
            element = EQUIPPED["C"]
            if element != None:
                imageE = SpriteManager.getInstance().getSprite("item.png", (element, 2))
                drawSurf.blit(imageE, (COORD[14][7]))
    

    def drawShards(self, drawSurf):
        return
        image1 = SpriteManager.getInstance().getSprite("item.png", (0, 2))
        image2 = SpriteManager.getInstance().getSprite("item.png", (1, 2))
        image3 = SpriteManager.getInstance().getSprite("item.png", (2, 2))
        image4 = SpriteManager.getInstance().getSprite("item.png", (3, 2))
        drawSurf.blit(image1, (16*12 + 6, 16*10))
        drawSurf.blit(image2, (16*13 + 6, 16*10))
        drawSurf.blit(image3, (16*14 + 6, 16*10))
        drawSurf.blit(image4, (16*15 + 6, 16*10))
        drawSurf.blit(Text.getImage(text=str(INV["flameShard"])), (16*12 + 12, 16*11))
        drawSurf.blit(Text.getImage(text=str(INV["frostShard"])), (16*13 + 12, 16*11))
        drawSurf.blit(Text.getImage(text=str(INV["boltShard"])), (16*14 + 12, 16*11))
        drawSurf.blit(Text.getImage(text=str(INV["galeShard"])), (16*15 + 12, 16*11))

    
    def drawMap(self, drawSurf):

        Map.getInstance().draw(drawSurf)

    def draw(self, drawSurf):
        AmmoBar.getInstance().shortCutBackground.set_alpha(255)
        if not self.paused:
            self.paused = True

        if self.inSettings:
            drawSurf.blit(self.menu.image, (self.menu.position[0], self.menu.position[1] - 208))
            return
        
        if self.mapOpen:
            self.drawMap(drawSurf)
            return
        
        drawSurf.blit(self.menu.image, self.menu.position)
        #self.menu.draw(drawSurf)
        if not self.inPosition or self.closing or self.closed or self.toInventory or self.toShortcuts:
            return
        
        self.drawEquipped(drawSurf)

        if not self.inShortcuts:
            self.drawShards(drawSurf)
            ##Key Items
            if INV["plant"] >= 1:
                image = SpriteManager.getInstance().getSprite("item.png", (0,0))
                drawSurf.blit(image, (COORD[3][4]))
                drawSurf.blit(Number.getImage(INV["plant"], 4), COORD[3][4])
                #Number(COORD[3][4], INV["plant"], row = 4).draw(drawSurf)
            
            if INV["chanceEmblem"]:
                image = SpriteManager.getInstance().getSprite("item.png", (4,0))
                drawSurf.blit(image, (COORD[4][4]))

            if INV["map0"]:
                image = SpriteManager.getInstance().getSprite("item.png", (5,0))
                drawSurf.blit(image, (COORD[5][4]))

        if INV["syringe"]:
            image = SpriteManager.getInstance().getSprite("item.png", (3,0))
            drawSurf.blit(image, (COORD[3][7]))

        if INV["potion"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (2,0))
            drawSurf.blit(image, (COORD[4][7]))
            drawSurf.blit(Number.getImage(INV["potion"], 4), COORD[4][7])
        
        if INV["smoothie"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (9,0))
            drawSurf.blit(image, (COORD[5][7]))
            drawSurf.blit(Number.getImage(INV["smoothie"], 4), COORD[5][7])

        if INV["beer"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (6,0))
            drawSurf.blit(image, (COORD[6][7]))
            drawSurf.blit(Number.getImage(INV["beer"], 4), COORD[6][7])
        
        if INV["joint"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (7,0))
            drawSurf.blit(image, (COORD[7][7]))
            #Text((16*4+12, 16*7+4), str(INV["beer"]), small = True).draw(drawSurf)
            drawSurf.blit(Number.getImage(INV["joint"], 4), COORD[7][7])
        
        if INV["speed"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (8,0))
            drawSurf.blit(image, (COORD[8][7]))
            #Text((16*4+12, 16*7+4), str(INV["beer"]), small = True).draw(drawSurf)
            drawSurf.blit(Number.getImage(INV["speed"], 4), COORD[8][7])

        if INV["shoot"]:
            image = SpriteManager.getInstance().getSprite("item.png", (0,3))
            drawSurf.blit(image, (COORD[3][5]))
        
        if INV["hasBombo"]:
            image = SpriteManager.getInstance().getSprite("item.png", (1,3))
            drawSurf.blit(image, (COORD[4][5]))

        if INV["fire"]:
            image = SpriteManager.getInstance().getSprite("item.png", (0,2))
            drawSurf.blit(image, (COORD[3][6]))
        
        if INV["cleats"]:
            image = SpriteManager.getInstance().getSprite("item.png", (1,2))
            drawSurf.blit(image, (COORD[5][6]))
        
        if INV["clap"]:
            image = SpriteManager.getInstance().getSprite("item.png", (2,2))
            drawSurf.blit(image, (COORD[7][6]))
        
        if INV["slash"]:
            image = SpriteManager.getInstance().getSprite("item.png", (3,2))
            drawSurf.blit(image, (COORD[9][6]))
        
        if self.highlighted[1] == 4:
            drawSurf.blit(self.highlightQuit.image, (self.highlightQuit.position))
        else:
            drawSurf.blit(self.highlight.image, (self.highlight.position))
            self.drawButton(drawSurf)
    
    def drawButton(self, drawSurf):
        if self.scaled:
            if self.placing:
                drawSurf.blit(self.interactIcon, (self.highlight.position - 24))
            elif self.inShortcuts:
                drawSurf.blit(self.triggerIcon, (self.highlight.position - 24))
            else:
                if self.highlighted[1] == 3 or self.highlighted[1] == 0:
                    drawSurf.blit(self.interactIcon, (self.highlight.position - 24))
                elif self.highlighted[1] == 1:
                    drawSurf.blit(self.shootIcon, (self.highlight.position - 24))
                if self.highlighted[1] == 2:
                    drawSurf.blit(self.elementIcon, (self.highlight.position - 24))

        else:
            if self.placing:
                drawSurf.blit(self.interactIcon, (self.highlight.position - 12))
            elif self.inShortcuts:
                drawSurf.blit(self.triggerIcon, (self.highlight.position - 12))
            else:
                if self.highlighted[1] == 3 or self.highlighted[1] == 0:
                    drawSurf.blit(self.interactIcon, (self.highlight.position - 12))
                elif self.highlighted[1] == 1:
                    drawSurf.blit(self.shootIcon, (self.highlight.position - 12))
                if self.highlighted[1] == 2:
                    drawSurf.blit(self.elementIcon, (self.highlight.position - 12))
            

    def equipElement(self):
        if self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16*6:
            SoundManager.getInstance().playSFX("TextBox_Open.wav")
            EQUIPPED["C"] = 0
        elif self.highlight.position[0] == 16*5 and self.highlight.position[1] == 16*6:
            SoundManager.getInstance().playSFX("TextBox_Open.wav")
            EQUIPPED["C"] = 1
        elif self.highlight.position[0] == 16*7 and self.highlight.position[1] == 16*6:
            SoundManager.getInstance().playSFX("TextBox_Open.wav")
            EQUIPPED["C"] = 2
        elif self.highlight.position[0] == 16*9 and self.highlight.position[1] == 16*6:
            SoundManager.getInstance().playSFX("TextBox_Open.wav")
            EQUIPPED["C"] = 3
        else:
            SoundManager.getInstance().playSFX("bump.mp3")


    def equipArrow(self):
        if self.highlight.position[1] == 16*5:
            if self.highlight.position[0] == 16*3:
                SoundManager.getInstance().playSFX("TextBox_Open.wav")
                EQUIPPED["Arrow"] = 0
            elif self.highlight.position[0] == 16*4:
                if INV["hasBombo"]:
                    SoundManager.getInstance().playSFX("TextBox_Open.wav")
                    EQUIPPED["Arrow"] = 1
                else:
                    SoundManager.getInstance().playSFX("bump.mp3")
            else:
                SoundManager.getInstance().playSFX("bump.mp3")
        else:
            SoundManager.getInstance().playSFX("bump.mp3")

    def equipSpecial(self):
        return
        ACTIONS["trigger_r"] == False
        ##Arrow Row
        if self.highlight.position[1] == 16*5:
            ##Ol' Reliable
            if self.highlight.position[0] == 16*3:
                SoundManager.getInstance().playSFX("TextBox_Open.wav")
                AmmoBar.getInstance().setShortcutImage("ammo.png",(0,1))
                EventManager.getInstance().setSpecial("shoot")
                SHORTCUTS[ACTIVE_SHORTCUT[0]][0] = "shoot"
                SHORTCUTS[ACTIVE_SHORTCUT[0]][1] = 0

            ##Bombofaun
            if self.highlight.position[0] == 16*4:
                SoundManager.getInstance().playSFX("TextBox_Open.wav")
                AmmoBar.getInstance().setShortcutImage("ammo.png",(0,2), True)
                EventManager.getInstance().setSpecial("shoot")
                SHORTCUTS[ACTIVE_SHORTCUT[0]][0] = "shoot"
                SHORTCUTS[ACTIVE_SHORTCUT[0]][1] = 1

        ##Element Row
        elif self.highlight.position[1] == 16*6:
            if self.highlight.position[0] == 16*3:
                SoundManager.getInstance().playSFX("TextBox_Open.wav")
                AmmoBar.getInstance().setShortcutImage("element.png",(1,0))
                EventManager.getInstance().setSpecial("element")
                SHORTCUTS[ACTIVE_SHORTCUT[0]][0] = "element"
                SHORTCUTS[ACTIVE_SHORTCUT[0]][1] = 0

    def showInfo(self):
        if self.highlighted[1] == 4:
            if self.inShortcuts:
                self.text = "You can select up to 6\nattacks for your shortcuts.\nPress [Right Trigger] to\nselect an attack, and place\nit on the grid to the right.\nBack in the game, you can\npress the [bumpers] to cycle\nthrough your shortcuts.\nPress [Right Trigger] to use\nyour selected attack."
            else:
                self.toSettings = True
                ##self.promptFlag = "quit"
                ##self.text = "Y/NReturn to title screen?"

        ##  Key items   ##
        elif self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16*4:
            if INV["plant"] >= 1:
                self.text = INFO["plant"]
                return
            
        elif self.highlight.position[0] == 16*4 and self.highlight.position[1] == 16*4:
            if INV["chanceEmblem"]:
                self.text = INFO["chance"]
                return
        
        elif self.highlight.position[0] == 16*5 and self.highlight.position[1] == 16*4:
            if INV["map0"]:
                self.mapOpen = True
                #Map.getInstance().updateHighlight()
                return
        
        ##  Arrows  ##
        elif self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16*5:
            if INV["shoot"]:
                self.text = INFO["shoot"]
                return
        
        elif self.highlight.position[0] == 16*4 and self.highlight.position[1] == 16*5:
            if INV["hasBombo"]:
                self.text = INFO["bombo"]
                return
            else:
                SoundManager.getInstance().playSFX("bump.mp3")
            
        
        ##  Elements    ##
        elif self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16*6:
            if INV["fire"]:
                self.text = INFO["fire"]
                return
        
        elif self.highlight.position[0] == 16*5 and self.highlight.position[1] == 16*6:
            if INV["cleats"]:
                self.text = INFO["cleats"]
                return
            
        
        elif self.highlight.position[0] == 16*7 and self.highlight.position[1] == 16*6:
            if INV["clap"]:
                self.text = INFO["clap"]
                return
        
        elif self.highlight.position[0] == 16*9 and self.highlight.position[1] == 16*6:
            if INV["slash"]:  
                self.text = INFO["slash"]
                return
        
        ##  Consumables   ##
        elif self.highlight.position[0] == 16*3 and self.highlight.position[1] == 16*7:
            if INV["syringe"]:
                self.promptFlag = "syringe"
                self.text = "Y/NUse the syringe?"
        
        elif self.highlight.position[0] == 16*4 and self.highlight.position[1] == 16*7:
            if INV["potion"] >= 1:
                self.promptFlag = "potion"
                self.text = "Y/NA cherry-flavored potion\nthat restores 3 health.\nDrink the potion?\n"

        elif self.highlight.position[0] == 16*5 and self.highlight.position[1] == 16*7:
            if INV["smoothie"] >= 1:
                self.promptFlag = "smoothie"
                self.text = "Y/NThe best smoothie in town!\nSoothes your woes 5 fold!\nDrink delectable smoothie?\n"
        
        elif self.highlight.position[0] == 16*6 and self.highlight.position[1] == 16*7:
            if INV["beer"] >= 1:
                self.promptFlag = "beer"
                self.text = "Y/NDrink a beer?"
        
        elif self.highlight.position[0] == 16*7 and self.highlight.position[1] == 16*7:
            if INV["joint"] >= 1:
                self.promptFlag = "joint"
                self.text = "Y/NSmoke a blunt?"
        
        elif self.highlight.position[0] == 16*8 and self.highlight.position[1] == 16*7:
            if INV["speed"] >= 1:
                self.promptFlag = "speed"
                self.text = "Y/NDrink a can of speed?"

        else:
            SoundManager.getInstance().playSFX("bump.mp3")
                
    def startPlacing(self):
        SoundManager.getInstance().playSFX("TextBox_Open.wav")
        self.placing = True
        self.highlight.position = vec(16*13, 16*5)
        self.highlighted = vec(0,0)
    
    def stopPlacing(self):
        SoundManager.getInstance().playSFX("TextBox_Open.wav")
        self.placing = False
        self.highlight.position = vec(16*3, 16*5)
        self.highlighted = vec(0,1)
        self.item = None

    def placeItem(self):
        if self.highlighted[0] == 0:
            if self.highlighted[1] == 0:
                SHORTCUTS[0] = self.item
                AmmoBar.getInstance().setShortcutImage(self.item, 0)

            elif self.highlighted[1] == 1:
                SHORTCUTS[2] = self.item
                AmmoBar.getInstance().setShortcutImage(self.item, 2)

            elif self.highlighted[1] == 2:
                SHORTCUTS[4] = self.item
                AmmoBar.getInstance().setShortcutImage(self.item, 4)
            
        elif self.highlighted[0] == 1:
            if self.highlighted[1] == 0:
                SHORTCUTS[1] = self.item
                AmmoBar.getInstance().setShortcutImage(self.item, 1)

            elif self.highlighted[1] == 1:
                SHORTCUTS[3] = self.item
                AmmoBar.getInstance().setShortcutImage(self.item, 3)

            elif self.highlighted[1] == 2:
                SHORTCUTS[5] = self.item
                AmmoBar.getInstance().setShortcutImage(self.item, 5)

    def handleEvent(self):
        """
           0    1    2   3   4   5   6   7
        0
        1
        2
        3
        4
        5

        min offset[0] = 0
        max offset[0] = 7
        min offset[1] = 0
        max offset[1] = 5
        """
        if self.closing or not self.inPosition or self.toSettings or self.toShortcuts or self.toInventory:
            return
        
        if self.placing:
            if EventManager.getInstance().performAction("element"):
                self.stopPlacing()

            elif EventManager.getInstance().performAction("interact"):
                self.placeItem()
                self.stopPlacing()
                return
            
            else:
                ##  Cursor Movement
                if EventManager.getInstance().getCursorReady():
                    if  ACTIONS["up"]:
                        EventManager.getInstance().buffCursor()
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        if self.highlighted[1] == 0:
                            self.highlighted[1] = 2
                            self.highlight.position[1] = 16*5 + 64
                        else:
                            self.highlighted[1] -= 1
                            self.highlight.position[1] -= 32

                    elif ACTIONS["down"]:
                        EventManager.getInstance().buffCursor()
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        if self.highlighted[1] == 2:
                            self.highlighted[1] = 0
                            self.highlight.position[1] = 16*5
                        else:
                            self.highlighted[1] += 1
                            self.highlight.position[1] += 32


                    elif ACTIONS["right"]:
                        EventManager.getInstance().buffCursor()
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        if self.highlighted[0] == 1:
                            self.highlighted[0] = 0
                            self.highlight.position[0] = 16*13
                        else:
                            self.highlighted[0] += 1
                            self.highlight.position[0] += 48

                    elif ACTIONS["left"]:
                        EventManager.getInstance().buffCursor()
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        if self.highlighted[0] == 0:
                            self.highlighted[0] = 1
                            self.highlight.position[0] = 16*16
                        else:
                            self.highlighted[0] -= 1
                            self.highlight.position[0] -= 48
            return
        
        ##  Map Controls
        if self.mapOpen and INV["map"+str(Map.getInstance().mapNum)]:
            if ACTIONS["shoot"]:
                #close map
                self.mapOpen = False
            elif ACTIONS["down"]:
                if Map.getInstance().selectedPos[1] < 146.0:
                    Map.getInstance().selectedPos[1] += 10
                    Map.getInstance().updateSelected()

            elif ACTIONS["up"]:
                Map.getInstance().selectedPos[1] -= 10
                Map.getInstance().updateSelected()

            elif ACTIONS["left"]:
                Map.getInstance().selectedPos[0] -= 10
                Map.getInstance().updateSelected()
                
            elif ACTIONS["right"]:
                Map.getInstance().selectedPos[0] += 10
                Map.getInstance().updateSelected()
        
            return
        
        ##  Menu Controls
        ##  Shortcuts
        if self.inShortcuts:
            ##  Pickup Item for shortcut placement
            if EventManager.getInstance().getCursorReady() and ACTIONS["trigger_r"]:
                EventManager.getInstance().buffCursor()

                ##Arrows
                if self.highlight.position[1] == 16*5:
                    #Ol' reliable
                    if self.highlight.position[0] == 16*3:
                        if INV["shoot"]:
                            self.item = ("shoot", 0)
                            self.startPlacing()
                    #Bombofaun
                    elif self.highlight.position[0] == 16*4:
                        if INV["hasBombo"]:
                            self.item = ("shoot", 1)
                            self.startPlacing()

                ##Elements
                elif self.highlight.position[1] == 16*6:
                    #Fire Sword
                    if self.highlight.position[0] == 16*3:
                        if INV["fire"]:
                            self.item = ("element", 0)
                            self.startPlacing()
                    #Blizzard
                    elif self.highlight.position[0] == 16*5:
                        if INV["cleats"]:
                            self.item = ("element", 1)
                            self.startPlacing()
                    #Clap
                    elif self.highlight.position[0] == 16*7:
                        if INV["clap"]:
                            self.item = ("element", 2)
                            self.startPlacing()
                    #Slash
                    elif self.highlight.position[0] == 16*9:
                        if INV["slash"]:
                            self.item = ("element", 3)
                            self.startPlacing()

                ##Items
                elif self.highlight.position[1] == 16*7:
                    #Syringe
                    if self.highlight.position[0] == 16*3:
                        if INV["syringe"]:
                            self.item = ("item", 0)
                            self.startPlacing()
                    #Potion
                    elif self.highlight.position[0] == 16*4:
                        if INV["potion"] >= 1:
                            self.item = ("item", 1)
                            self.startPlacing()
                    #Smoothie
                    elif self.highlight.position[0] == 16*5:
                        if INV["smoothie"] >= 1:
                            self.item = ("item", 2)
                            self.startPlacing()
                    #Beer
                    elif self.highlight.position[0] == 16*6:
                        if INV["beer"] >= 1:
                            self.item = ("item", 3)
                            self.startPlacing()
                    
                    #Joint
                    elif self.highlight.position[0] == 16*7:
                        if INV["joint"] >= 1:
                            self.item = ("item", 4)
                            self.startPlacing()

                    #Speed
                    elif self.highlight.position[0] == 16*8:
                        if INV["speed"] >= 1:
                            self.item = ("item", 5)
                            self.startPlacing()
                return
            
            elif EventManager.getInstance().performAction("interact"):
                self.showInfo()
                return
            
            elif self.inShortcuts and EventManager.getInstance().getCursorReady() and ACTIONS["target"]:
                self.toInventory = True
                ACTIONS["target"] = False
                self.highlighted = vec(0,0)
                self.highlight.position = vec(16*3, 16*4)
                EventManager.getInstance().buffCursor()
                SoundManager.getInstance().playSFX("menu_shift_1.wav")
                return
            
        ##  Settings
        elif self.inSettings:
            pygame.quit()
            return

        ##  Inventory
        else:
            if EventManager.getInstance().performAction("element"):
                self.equipElement()
                return

            elif EventManager.getInstance().performAction("interact"):
                self.showInfo()
                return
            
            elif EventManager.getInstance().performAction("shoot"):
                self.equipArrow()
                return
            
            ##  Shift Menus
            elif EventManager.getInstance().getCursorReady() and ACTIONS["trigger_r"]:
                self.toShortcuts = True
                ACTIONS["trigger_r"] = False
                self.highlighted = vec(0,1)
                self.highlight.position = vec(16*3, 16*5)
                EventManager.getInstance().buffCursor()
                SoundManager.getInstance().playSFX("menu_shift.wav")
                return
            
            



        
            """
            Highlight positions
            Top left (plant) = (16*3, 16*4)
            highlighted = integer value corresponding to inv item
            highlight.position = actual value to draw at (mult. of 16)
            """
        ##Move cursor
        if EventManager.getInstance().getCursorReady():
            if  ACTIONS["up"]:
                EventManager.getInstance().buffCursor()
                if self.inShortcuts:
                    if self.highlighted[1] == 1:
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        self.highlighted[1] = 4
                        self.highlight.position[1] = 128

                    else:
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        self.highlighted[1] -= 1
                        self.highlight.position[1] -= 16
                else:
                    if self.highlighted[1] == 0:
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        self.highlighted[1] = 4
                        self.highlight.position[1] = 128

                    else:
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        self.highlighted[1] -= 1
                        self.highlight.position[1] -= 16

            elif ACTIONS["down"]:
                EventManager.getInstance().buffCursor()
                if self.inShortcuts:
                    if self.highlighted[1] == 4:
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        self.highlighted[1] = 1
                        self.highlight.position[1] = 16*5
                    else:
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        self.highlighted[1] += 1
                        self.highlight.position[1] += 16
                else:
                    if self.highlighted[1] == 4:
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        self.highlighted[1] = 0
                        self.highlight.position[1] = 16*4
                    else:
                        SoundManager.getInstance().playSFX("pause_cursor.wav")
                        self.highlighted[1] += 1
                        self.highlight.position[1] += 16

            elif ACTIONS["right"]:
                EventManager.getInstance().buffCursor()
                if self.highlighted[0] == 7:
                    SoundManager.getInstance().playSFX("pause_cursor.wav")
                    self.highlighted[0] = 0
                    self.highlight.position[0] = 16*3

                elif self.highlighted[1] != 4:
                    SoundManager.getInstance().playSFX("pause_cursor.wav")
                    self.highlighted[0] += 1
                    self.highlight.position[0] += 16

            elif ACTIONS["left"]:
                EventManager.getInstance().buffCursor()
                #print(self.highlight.position[0])
                if self.highlighted[0] == 0:
                    SoundManager.getInstance().playSFX("pause_cursor.wav")
                    self.highlighted[0] = 7
                    self.highlight.position[0] = 160

                elif self.highlighted[1] != 4:
                    SoundManager.getInstance().playSFX("pause_cursor.wav")
                    self.highlighted[0] -= 1
                    self.highlight.position[0] -= 16



    def toggleScale(self):
        if not self.scaled:
            self.interactIcon = pygame.transform.scale(self.interactIcon, (40,32))
            self.shootIcon = pygame.transform.scale(self.shootIcon, (40,32))
            self.elementIcon = pygame.transform.scale(self.elementIcon, (40,32))
            self.triggerIcon = pygame.transform.scale(self.triggerIcon, (40,32))
            self.scaled = True
        else:
            self.interactIcon = pygame.transform.scale(self.interactIcon, (20,16))
            self.shootIcon = pygame.transform.scale(self.shootIcon, (20,16))
            self.elementIcon = pygame.transform.scale(self.elementIcon, (20,16))
            self.triggerIcon = pygame.transform.scale(self.triggerIcon, (20,16))
            self.scaled = False

    def updateButtons(self):
        controller = EventManager.getInstance().getController()
        if controller == "key":
            self.interactIcon = SpriteManager.getInstance().getSprite("keys.png", (2,4))
            self.elementIcon = SpriteManager.getInstance().getSprite("keys.png",(3,0))
            self.shootIcon = SpriteManager.getInstance().getSprite("keys.png",(5,0))
            self.triggerIcon = SpriteManager.getInstance().getSprite("keys.png", (1,0))
        elif controller == "Switch":
            self.interactIcon = SpriteManager.getInstance().getSprite("keys.png", (2,0))
            self.elementIcon = SpriteManager.getInstance().getSprite("keys.png",(3,0))
            self.shootIcon = SpriteManager.getInstance().getSprite("keys.png",(5,0))
            self.triggerIcon = SpriteManager.getInstance().getSprite("keys.png", (1,0))

    def fadeOut(self):
        """
        Begins fade out process.
        Surface Alpha value will decrement by 20
        """
        self.alpha = 255
        self.fading_out = True

    def fadeIn(self):
        """
        Begins fade in process.
        Surface Alpha value will increment by 20
        """
        self.alpha = 0
        self.fading_in = True

    def update(self, seconds):
        if self.closing:
            self.menu.position[1] += 1000 * seconds
            if self.menu.position[1] >= RESOLUTION[1]:
                self.menu.position[1] = 0
                self.closed = True
            return
        
        if not self.inPosition:
            self.menu.position[1] -= 1000 * seconds
            if self.menu.position[1] <= 0:
                self.menu.position[1] = 0
                self.inPosition = True
            return
        
        if self.toShortcuts:
            self.menu.position[0] -= 8
            if self.menu.position[0] <= -304:
                self.menu.position[0] = -304
                self.toShortcuts = False
                self.inShortcuts = True
                return
        elif self.toInventory:
            if self.inSettings:
                return
            else:
                self.menu.position[0] += 8
                if self.menu.position[0] >= 0:
                    self.menu.position[0] = 0
                    self.toInventory = False
                    self.inShortcuts = False
                    return
        
        elif self.inSettings:
            if self.fading_in:
                self.alpha += 20
                self.alpha %= 255
                if self.alpha == 0: 
                    self.alpha = 255
                    self.fading_in = False
                self.menu.image.set_alpha(self.alpha)
            else:
                self.alpha -= 20
                if self.alpha <= 0:
                    self.alpha = 0
                    self.fading_out = False
                self.menu.image.set_alpha(self.alpha)
        

            
        if self.mapOpen:
            Map.getInstance().update(seconds)
        

        if self.placing:
            pass

        self.timer += seconds
        if self.scaled:
            if self.timer >= .2:
                self.toggleScale()
                self.timer = 0
        else:
            if self.timer >= .8:
                self.toggleScale()
                self.timer = 0
        
        if not self.trackAnalog:
            self.joyTimer += seconds
            if self.joyTimer >= 0.2:
                self.joyTimer = 0.0
                self.trackAnalog = True
        
        self.highlight.update(seconds)
        self.highlightQuit.update(seconds)
