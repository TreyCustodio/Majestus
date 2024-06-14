import pygame

from . import Drawable,  Animated, Text, Highlight, Map, Number

from utils import  vec, RESOLUTION, SpriteManager, SoundManager, INV, INFO, COORD, EQUIPPED

from pygame.locals import *

class TextEngine(object):
    
    _INSTANCE = None
    
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._TE()
      
        return cls._INSTANCE

    @classmethod
    def tearDown(cls):
        if cls._INSTANCE != None:
            cls._INSTANCE = None
        return None

    class _TE(object):
        def __init__(self):
            self.backgroundBool = False
            self.blackBool = False
            self.black = SpriteManager.getInstance().getSprite("TextBox2.png", (0,6))
            self.text = ""
            self.line = ""
            self.starting = True
            self.displayIcon = None

            self.large = False #Boolean determining if you display the large textbox or not

            self.charIndex = 0
            self.box_drawn = False
            self.ready_to_display = True
            self.ready_to_continue = False
            self.end = False
            self.closing = False
            self.done = False
            self.frame = 1
            self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (0,0))
            
            self.displayTimer = 0.0

            self.lineNum = 1 #The line the text display is currently on

            self.promptHighlight = Highlight((16*6 - 8, 16*5 + 10), flag = 2)
            self.prompt = False
            self.highlightTimer = 0
            self.highlighted = 0 #0 -> No, #1 -> Yes
            self.choosing = False#The state of choosing yes or no
            self.promptResult = False

        def setPromptHighlight(self, position):
            self.promptHighlight.position = vec(position[0]+64-6, position[1]+32-6)

        def setImage(self):
            if self.large:
                self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))
            else:
                self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (self.frame,0))
        
        """

        """
        def setBackgroundBool(self):
            self.backgroundBool = not self.backgroundBool

        def reset(self):
            self.text = ""
            self.line = ""
            self.displayIcon = None
            self.starting = True

            self.frame = 1
            self.large = False #Boolean determining if you display the large textbox or not

            self.charIndex = 0
            self.box_drawn = False
            self.ready_to_display = True
            self.ready_to_continue = False
            self.end = False
            self.closing = False
            self.done = False
            self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (0,0))
            
            
            self.displayTimer = 0.0

            self.lineNum = 1 #The line the text display is currently on

            self.promptHighlight = Highlight((16*6 - 8, 16*5 + 10), flag = 2)
            self.prompt = False
            self.highlightTimer = 0
            self.highlighted = 0 #0 -> No, #1 -> Yes
            self.choosing = False#The state of choosing yes or no
        

        def playSFX(self, name, checkBusy = False):
            if checkBusy:
                if not pygame.mixer.get_busy():
                    SoundManager.getInstance().playSFX(name)
            else:
                SoundManager.getInstance().playSFX(name)


        def setText(self, text, icon = None, large = False, prompt = False):
            
            
            if prompt:
                self.large = True
                self.prompt = True
                self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (0,0))

            elif large:
                self.large = large
                self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (0,0))

            if icon != None and self.displayIcon == None:
                self.displayIcon = icon

            if self.prompt:
                self.text = text[3:]
            else:
                self.text = text

            if len(self.text) <= 8:
                #self.playSFX("TextBox_Short.wav")
                pass
            else:
                self.playSFX("TextBox_Open.wav")
            
            if "\n" in self.text:
                self.line = self.text[self.charIndex:self.text.index("\n")]
            else:
                #1 line
                self.line = self.text
        
        def setAlpha(self):
            self.textBox.set_alpha(220)

        def draw(self, position, drawSurface):
            ##unused
            if self.blackBool:
                if self.large:
                    drawSurface.blit(self.black, position)
                self.blackBool = False

            self.setAlpha()
            #Still drawing previous frame
            if self.starting:
                drawSurface.blit(self.textBox, position)
                return
            elif self.closing:
                drawSurface.blit(self.textBox, position)
                return
            elif self.done:
                return
            
            if self.end:
                if self.prompt:
                    self.choosing = True
                    if self.promptHighlight.initialized:
                        self.drawPrompt(position, drawSurface)
                        if self.prompt:
                            self.promptHighlight.draw(drawSurface)
                    else:
                        self.setPromptHighlight(position)
                        self.promptHighlight.setInitialized()

                else:
                    self.drawEnd(position, drawSurface)

            elif not self.box_drawn:
                self.drawBox(position, drawSurface)
                if self.displayIcon != None:
                    self.drawIcon((position[0] + 106, position[1] - 32), drawSurface)
                self.displayText(position, drawSurface)
        
            elif self.ready_to_continue:
                self.drawContinue(position, drawSurface)

            elif self.displayTimer > 0 and self.displayTimer < 0.1:
                self.drawYellow1(position, drawSurface)
                
            else:
                self.drawYellow2(position, drawSurface)
               
        
        
        def drawPrompt(self, position, drawSurface):
            drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,5)), position)


        def drawIcon(self, position, drawSurface):
            box = SpriteManager.getInstance().getSprite("icon.png", (0,0))
            icon = SpriteManager.getInstance().getSprite("icon.png", self.displayIcon)
            drawSurface.blit(box, position)
            drawSurface.blit(icon, position)

        def drawBox(self, position, drawSurface):
            drawSurface.blit(self.textBox, position)
            self.box_drawn = True

        def drawContinue(self, position, drawSurface):
            if self.large:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,1)), position)
            else:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,1)), position)

        def drawYellow1(self, position, drawSurface):
            if self.large:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,3)), position)
            else:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,3)), position)
            self.displayText(position, drawSurface)
        
        def drawYellow2(self, position, drawSurface):
            if self.large:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,4)), position)
            else:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,4)), position)
            self.displayText(position, drawSurface)

        def drawEnd(self, position, drawSurface):
            if self.large:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,2)), position)
            else:
                drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,2)), position)

        
        """
        Main text display method.
        Try if not mixer busy for slower text
        """
        def displayText(self, position, drawSurface, question = False): 
                
            if self.lineNum == 2:
                Text(((position[0] + 10) + (8 * self.charIndex), position[1]+34), self.line[self.charIndex]).draw(drawSurface)
            elif "&&" in self.line:
                Text(((position[0] + 10) + (8 * self.charIndex), position[1]+22), self.line[self.charIndex]).draw(drawSurface)
            else:
                Text(((position[0] + 10) + (8 * self.charIndex), position[1]+7), self.line[self.charIndex]).draw(drawSurface)
            
            self.charIndex += 1
            if self.charIndex == len(self.line):
                SoundManager.getInstance().stopSFX("message.wav")
                self.text = self.text[self.charIndex+1:]

                if self.text == "":
                    self.end = True
                    self.ready_to_continue = True
                    self.playSFX("OOT_Dialogue_Done.wav")
                    self.charIndex = 0

                elif "\n" in self.text:
                    if self.large and self.lineNum == 1 and (not "&&" in self.line):
                        self.line = self.text[:self.text.index("\n")]
                        self.charIndex = 0
                        self.lineNum = 2
                    else:
                        self.ready_to_continue = True
                        self.line = self.text[:self.text.index("\n")]
                        self.playSFX("message-finish.wav")
                        self.charIndex = 0
                        if self.large:
                            self.lineNum = 1
                else:
                    self.ready_to_continue = True
                    self.line = self.text
                    self.charIndex = 0
                    self.playSFX("message-finish.wav")
            else:
                self.playSFX("message.wav")
                    
                
                
                

        def handleEvent(self, event):
            ##Prompt selection
            if self.choosing:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT and self.highlighted == 0:
                    self.highlighted = 1
                    self.promptHighlight.position = vec(self.promptHighlight.position[0]+88, self.promptHighlight.position[1])
                    self.playSFX("pause_cursor.wav")
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT and self.highlighted == 1:
                    self.highlighted = 0
                    self.promptHighlight.position = vec(self.promptHighlight.position[0]-88, self.promptHighlight.position[1])
                    self.playSFX("pause_cursor.wav")

                elif (event.type == pygame.KEYDOWN and event.key == pygame.K_z):
                    self.playSFX("WW_Textbox_Close.wav")
                    self.setClosing()
                    if self.highlighted == 0:
                        self.promptResult = False
                    elif self.highlighted == 1:
                        self.promptResult = True
                    
            ##Progressing text
            elif (event.type == pygame.KEYDOWN and event.key == pygame.K_z) and self.ready_to_continue:
                if self.end == True:
                    self.playSFX("WW_Textbox_Close.wav")
                    self.setClosing()
                else:
                    self.playSFX("OOT_Dialogue_Next.wav")
                    self.box_drawn = False
                    self.ready_to_continue = False
                    self.backgroundBool = True
                    #self.blackBool = True
                    


        def handleEvent_C(self, event):
            if self.choosing:
                if event.type == JOYAXISMOTION:
                    if event.value >= 0.8 and self.highlighted == 0:
                        self.highlighted = 1
                        self.promptHighlight.position = vec(self.promptHighlight.position[0]+88, self.promptHighlight.position[1])
                        self.playSFX("pause_cursor.wav")
                    elif event.value <= -0.8 and self.highlighted == 1:
                        self.highlighted = 0
                        self.promptHighlight.position = vec(self.promptHighlight.position[0]-88, self.promptHighlight.position[1])
                        self.playSFX("pause_cursor.wav")
                elif event.type == JOYBUTTONDOWN and event.button == 0:
                    self.playSFX("WW_Textbox_Close.wav")
                    self.setClosing()
                    if self.highlighted == 0:
                        self.promptResult = False
                    elif self.highlighted == 1:
                        self.promptResult = True

            ##Progress text
            elif (event.type == pygame.JOYBUTTONDOWN and event.button == 0) and self.ready_to_continue:
                if self.end == True:
                    self.playSFX("WW_Textbox_Close.wav")
                    self.setClosing()
                else:
                    self.playSFX("OOT_Dialogue_Next.wav")
                    self.box_drawn = False
                    self.ready_to_continue = False

        def setClosing(self):
            self.closing = True
            self.frame = 5

        def update(self, seconds):
            if self.starting:
                if self.large:
                    self.frame += 1
                    self.frame %= 6
                    self.setImage()
                    if self.frame == 0:
                        self.starting = False
                        self.setBackgroundBool()
                    return
                else:
                    self.frame += 1
                    self.frame %= 5
                    self.setImage()
                    if self.frame == 0:
                        self.starting = False
                        self.setBackgroundBool()
                    return
            
            elif self.closing:
                if self.large:
                    self.frame -= 1
                    if self.frame == 0:
                        self.closing = False
                        self.done = True
                    else:
                        self.setImage()
                    return
                else:
                    self.frame -= 1
                    if self.frame == 0:
                        self.closing = False
                        self.done = True
                    else:
                        self.setImage()
                    return
            if self.prompt:
                self.promptHighlight.update(seconds)
            """ self.displayTimer += seconds
            self.highlightTimer += seconds

            if self.displayTimer >= 0.2:
                self.ready_to_display = True
                self.displayTimer = 0
            
            if self.highlightTimer >= .5:
                self.highlightTimer = 0 """



            

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
        self.highlight = Highlight(COORD[3][6])
        self.highlightQuit = Highlight(COORD[3][8], flag = 1)
        self.highlighted = vec(0,2)
        self.promptResult = False
        self.promptFlag = ""

    def resetMenu(self):
        self.menu.position = vec(0,100)
        self.inPosition = False
        self.closing = False
        self.closed = False
        self.paused = False

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

    def drawEquipped(self, drawSurf):
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
        image1 = SpriteManager.getInstance().getSprite("item.png", (0, 2))
        image2 = SpriteManager.getInstance().getSprite("item.png", (1, 2))
        image3 = SpriteManager.getInstance().getSprite("item.png", (2, 2))
        image4 = SpriteManager.getInstance().getSprite("item.png", (3, 2))
        drawSurf.blit(image1, (16*12 + 6, 16*10))
        drawSurf.blit(image2, (16*13 + 6, 16*10))
        drawSurf.blit(image3, (16*14 + 6, 16*10))
        drawSurf.blit(image4, (16*15 + 6, 16*10))
        Text((16*12 + 12, 16*11), str(INV["flameShard"])).draw(drawSurf)
        Text((16*13 + 12, 16*11), str(INV["frostShard"])).draw(drawSurf)
        Text((16*14 + 12, 16*11), str(INV["boltShard"])).draw(drawSurf)
        Text((16*15 + 12, 16*11), str(INV["galeShard"])).draw(drawSurf)
    
    def drawMap(self, drawSurf):

        Map.getInstance().draw(drawSurf)

    def draw(self, drawSurf):
        if not self.paused:
            self.paused = True

        if self.mapOpen:
            self.drawMap(drawSurf)
            return
        
        self.menu.draw(drawSurf)
        if not self.inPosition or self.closing or self.closed:
            return
        
        self.drawEquipped(drawSurf)

        self.drawShards(drawSurf)
        if INV["plant"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (0,0))
            drawSurf.blit(image, (COORD[3][4]))
            Number(COORD[3][4], INV["plant"], row = 4).draw(drawSurf)
        
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
            Number(COORD[4][7], INV["potion"], row = 4).draw(drawSurf)
        
        if INV["smoothie"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (9,0))
            drawSurf.blit(image, (COORD[5][7]))
            Number(COORD[5][7], INV["smoothie"], row = 4).draw(drawSurf)

        if INV["beer"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (6,0))
            drawSurf.blit(image, (COORD[6][7]))
            #Text((16*4+12, 16*7+4), str(INV["beer"]), small = True).draw(drawSurf)
            Number(COORD[6][7], INV["beer"], row = 4).draw(drawSurf)
        
        if INV["joint"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (7,0))
            drawSurf.blit(image, (COORD[7][7]))
            #Text((16*4+12, 16*7+4), str(INV["beer"]), small = True).draw(drawSurf)
            Number(COORD[7][7], INV["joint"], row = 4).draw(drawSurf)
        
        if INV["speed"] >= 1:
            image = SpriteManager.getInstance().getSprite("item.png", (8,0))
            drawSurf.blit(image, (COORD[8][7]))
            #Text((16*4+12, 16*7+4), str(INV["beer"]), small = True).draw(drawSurf)
            Number(COORD[8][7], INV["speed"], row = 4).draw(drawSurf)

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
            self.highlightQuit.draw(drawSurf)
        else:
            self.highlight.draw(drawSurf)


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

    def showInfo(self):
        if self.highlighted[1] == 4:
            self.promptFlag = "quit"
            self.text = "Y/NReturn to title screen?"

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

    def handleEvent_C(self, event):
        if self.closing or not self.inPosition:
            return
        
        if self.mapOpen and INV["map"+str(Map.getInstance().mapNum)]:
            if event.type == JOYBUTTONDOWN:
                if event.button == 2:
                    #close map
                    self.mapOpen = False
            
            if event.type == JOYAXISMOTION and self.trackAnalog:
                if event.axis == 1 and event.value < -0.8:
                    if Map.getInstance().selectedPos[1] < 146.0:
                        Map.getInstance().selectedPos[1] += 10
                        Map.getInstance().updateSelected()

                elif event.axis == 1 and event.value > 0.8:
                    #print(Map.getInstance().selectedPos[1])
                    Map.getInstance().selectedPos[1] -= 10
                    Map.getInstance().updateSelected()

                elif event.axis == 0 and event.value < 0.8:
                    #print(Map.getInstance().selectedPos[0])
                    Map.getInstance().selectedPos[0] -= 10
                    Map.getInstance().updateSelected()
                elif event.axis == 0 and event.value > 0.8:
                    #print(Map.getInstance().selectedPos[0])
                    Map.getInstance().selectedPos[0] += 10
                    Map.getInstance().updateSelected()
            return
        
        if event.type == JOYBUTTONDOWN:
            if event.button == 0:
                self.showInfo()
            elif event.button == 3:
                self.equipElement()


        if event.type == JOYAXISMOTION and self.trackAnalog:
            if event.axis == 1 and event.value < -0.8:
                #print("A")
                if self.highlighted[1] != 0:
                    SoundManager.getInstance().playSFX("pause_cursor.wav")
                    self.highlighted[1] -= 1
                    self.highlight.position[1] -= 16
                self.trackAnalog = False
                    

            elif event.axis == 1 and event.value > 0.8:
                #print("A")
                if self.highlighted[1] != 4:
                    SoundManager.getInstance().playSFX("pause_cursor.wav")
                    self.highlighted[1] += 1
                    self.highlight.position[1] += 16
                self.trackAnalog = False
            
            ##Move right
            elif event.axis == 0 and event.value > 0.8:
                #print("A")
                if self.highlighted[0] != 7 and self.highlighted[1] != 4:
                    SoundManager.getInstance().playSFX("pause_cursor.wav")
                    self.highlighted[0] += 1
                    self.highlight.position[0] += 16
                self.trackAnalog = False

            elif event.axis == 0 and event.value < -0.8:
                #print("A")
                if self.highlighted[0] != 0 and self.highlighted[1] != 4:
                    SoundManager.getInstance().playSFX("pause_cursor.wav")
                    self.highlighted[0] -= 1
                    self.highlight.position[0] -= 16
                self.trackAnalog = False
                    
            

    def handleEvent(self, event):
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
        if self.closing or not self.inPosition:
            return
        if self.mapOpen and INV["map"+str(Map.getInstance().mapNum)]:
            if event.type == KEYDOWN:
                if event.key == K_x:
                    #close map
                    self.mapOpen = False
                elif event.key == K_DOWN:
                    if Map.getInstance().selectedPos[1] < 146.0:
                        Map.getInstance().selectedPos[1] += 10
                        Map.getInstance().updateSelected()
                elif event.key == K_UP:
                    #print(Map.getInstance().selectedPos[1])
                    Map.getInstance().selectedPos[1] -= 10
                    Map.getInstance().updateSelected()
                elif event.key == K_LEFT:
                    #print(Map.getInstance().selectedPos[0])
                    Map.getInstance().selectedPos[0] -= 10
                    Map.getInstance().updateSelected()
                elif event.key == K_RIGHT:
                    #print(Map.getInstance().selectedPos[0])
                    Map.getInstance().selectedPos[0] += 10
                    Map.getInstance().updateSelected()
            
            return
        
        if event.type == KEYDOWN and event.key == K_c:
            self.equipElement()

        elif event.type == KEYDOWN and event.key == K_z:
            ##Selecting an item and pulling up textbox
            ##Will have to switch the order of conditionals. Check position first so that the program
            ##Doesn't check every inventory slot
            self.showInfo()
        
        elif event.type == KEYDOWN and event.key == K_x:
            self.equipArrow()
        
            """
            Highlight positions
            Top left (plant) = (16*3, 16*4)
            highlighted = integer value corresponding to inv item
            highlight.position = actual value to draw at (mult. of 16)
            """
        elif event.type == KEYDOWN and event.key == K_UP:
            if self.highlighted[1] == 0:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[1] = 4
                self.highlight.position[1] = 128

            else:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[1] -= 1
                self.highlight.position[1] -= 16

        elif event.type == KEYDOWN and event.key == K_DOWN:
            #print(self.highlight.position[1])
            if self.highlighted[1] == 4:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[1] = 0
                self.highlight.position[1] = 16*4
            else:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[1] += 1
                self.highlight.position[1] += 16

        elif event.type == KEYDOWN and event.key == K_RIGHT:
            if self.highlighted[0] == 7:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[0] = 0
                self.highlight.position[0] = 16*3

            elif self.highlighted[1] != 4:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[0] += 1
                self.highlight.position[0] += 16

        elif event.type == KEYDOWN and event.key == K_LEFT:
            #print(self.highlight.position[0])
            if self.highlighted[0] == 0:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[0] = 7
                self.highlight.position[0] = 160

            elif self.highlighted[1] != 4:
                SoundManager.getInstance().playSFX("pause_cursor.wav")
                self.highlighted[0] -= 1
                self.highlight.position[0] -= 16

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
        
        if self.mapOpen:
            Map.getInstance().update(seconds)
        

        self.timer += seconds
        if self.timer >= .5:
            self.timer = 0
        
        if not self.trackAnalog:
            self.joyTimer += seconds
            if self.joyTimer >= 0.2:
                self.joyTimer = 0.0
                self.trackAnalog = True
        
        self.highlight.update(seconds)
        self.highlightQuit.update(seconds)