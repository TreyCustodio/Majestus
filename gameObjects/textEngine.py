import pygame

from . import Drawable,  Animated, Highlight, Map, Number, IconManager

from utils import  vec, RESOLUTION, SpriteManager, SoundManager, INV, INFO, COORD, EQUIPPED

from UI import ACTIONS, EventManager

from pygame.locals import *


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
    
    def getImage(text, color = (255,255,255), box = False, small = False):
        if small:
            return Text.SMALL.render(text, False, color)
        elif box:
            return Text.BOX.render(text, False, color)
        else:
            return Text.FONT.render(text, False, color)

    def __init__(self, position, text, color = (255,255,255), box = False, small = False):
        super().__init__(position, "")
        if small:
            self.image = Text.SMALL.render(text, False, color)
        elif box:
            self.image = Text.BOX.render(text, False, color)
        else:
            self.image = Text.FONT.render(text, False, color)
    

    """
    Static Method drawChar
    Draws a char that appears in textboxes.
    @param char is the char that is drawn
    @param alpha is the alpha value
    @param flag specifies different text styles

    Information for sprite file chars.png:
    row 0 = upper case alphabetical chars, for frames 0-25
    row 1 = lower case alphabetical chars, for frames 0-25
    row 2 = numerical chars, for frames 0-9
    row 3 = special chars, from frames 0-31

    Alphabetical and special chars use ASCII values to print.
    Alphabetical char frame = ascii value - 65
    Special char frame = ascii value - 33
    ! = 33
    @ = 64
    Ex: "A"
    value = 65
    frame = 65-65 = 0
    
    flags:
    0 -> default, 1 -> shake, 2 -> black, 3 -> white
    """
    def drawChar(drawSurface, position = vec(0,0), char: str ="", alpha: int = 255, flag=0):
        ##  Safety Return   ##
        if char == " " or char == "" or len(char) > 1:
            return
        
        ##  Black Text in EB Garamond  ##
        if flag == 2:
            image = Text.getImage(char, (0,0,0))
            drawSurface.blit(image, position)
            return

        ##  Numeric chars   ##
        if char.isnumeric():
            image = SpriteManager.getInstance().getSprite("chars.png", (int(char),3))
        
        ##  Alphabetical chars  ##
        else:
            if char.isupper():
                value = ord(char)
                image = SpriteManager.getInstance().getSprite("chars.png", (value-65,0))

            elif char.islower():
                value = ord(char)
                image = SpriteManager.getInstance().getSprite("chars.png", (value-97,1))
            else:
                ##  Special chars   ##
                value = ord(char)
                
                image = SpriteManager.getInstance().getSprite("chars.png", (value-33,2))

        ##  Adjust surface alpha and display    ##
        image.set_alpha(alpha)
        if flag == 1:
            image = pygame.transform.scale(image, (16,16))
        drawSurface.blit(image, position)

    """
    Draw the cursor at the end of the textBox
    """
    def drawCursor(drawSurface, position = vec(0,0), frame = 0):
        drawSurface.blit(IconManager.getIcon("interact"), position)

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
            self.voiceInt = -1
            self.frameTimer = 0.0
            self.noBox = False
            self.type = 0
            self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (0,1)) #Animated cube at bottom
            self.cubeTick = 0
            #self.a_icon = SpriteManager.getInstance().getSprite()
            self.setImage()


        def setPromptHighlight(self, position):
            self.promptHighlight.position = vec(position[0]+64-6, position[1]+32-6)

        def setImage(self):
            if self.large:
                if self.type == 2:
                    self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))
                    #self.textBox = pygame.transform.scale(SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0)), (248,64))
                elif self.type == 3:
                    self.textBox = SpriteManager.getInstance().getSprite("TextBox3.png", (self.frame,0))
                else:
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
            self.voiceInt = -1

            self.noBox = False
            self.setImage()
            self.type = 2
        

        def playSFX(self, name, checkBusy = False):
            if checkBusy:
                if not pygame.mixer.get_busy():
                    SoundManager.getInstance().playSFX(name)
            else:
                SoundManager.getInstance().playSFX(name)


        def setText(self, text, icon = None, large = False, prompt = False, type = 2):
            
            if prompt:
                self.large = True
                self.prompt = True
                self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))

            elif large:
                self.large = large
                if type == 2:
                    self.type = 2
                    self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))
                elif type == 3:
                    self.type = 3
                    self.textBox = SpriteManager.getInstance().getSprite("TextBox3.png", (self.frame,0))
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
            if self.large:
                self.setAlpha()

            ##Draw the box
            drawSurface.blit(self.textBox, position - Drawable.CAMERA_OFFSET)
            if not self.closing and not self.starting:
                drawSurface.blit(self.cube, position - Drawable.CAMERA_OFFSET)
            
            ##Wait for closing animation
            if self.closing:
                return
            
            ##Do nothing
            elif self.done:
                return
            ##Wait for start animation
            elif self.starting:
                return
            
            ##Draw box one more time after start animation
            elif not self.box_drawn:
                self.box_drawn = True

            
            ##  Text routines
            ##End of dialogue
            if self.end:
                if self.displayIcon != None:
                    self.drawIcon((position[0] + 106, position[1] - 32) - Drawable.CAMERA_OFFSET, drawSurface)
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
                    pass
                return

            ##Continue to next line
            elif self.ready_to_continue:
                if self.displayIcon != None:
                    self.drawIcon((position[0] + 106, position[1] - 32) - Drawable.CAMERA_OFFSET, drawSurface)
                return
            
            ##Buffer
            elif self.displayTimer > 0 and self.displayTimer < 0.1:
                return
                
            else:
                ##Draw text
                if self.displayIcon != None:
                    self.drawIcon((position[0] + 106, position[1] - 32) - Drawable.CAMERA_OFFSET, drawSurface)
                self.displayText(position, drawSurface)

        
        def drawPrompt(self, position, drawSurface):
            drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,5)), position - Drawable.CAMERA_OFFSET)

        def drawIcon(self, position, drawSurface):
            box = SpriteManager.getInstance().getSprite("icon.png", (0,0))
            icon = SpriteManager.getInstance().getSprite("icon.png", self.displayIcon)
            drawSurface.blit(box, position)
            drawSurface.blit(icon, position)

        def drawBox(self, position, drawSurface):
            drawSurface.blit(self.textBox, position)
            self.box_drawn = True

        def drawChars(self):
            ##Sign boxes
            if self.type == 3:
                ##Line 2
                if self.lineNum == 2:
                    Text(((16 + 10) + (8 * self.charIndex), 34), self.line[self.charIndex], color=(0,0,0)).draw(self.textBox, use_camera=False)
                ##Focus line
                elif "&&" in self.line:
                    Text(((16 + 10) + (8 * self.charIndex), 22), self.line[self.charIndex], color=(0,0,0)).draw(self.textBox, use_camera=False)
                ##Line 1
                else:
                    Text(((16 + 10) + (8 * self.charIndex), 7 + 8), self.line[self.charIndex], color=(0,0,0)).draw(self.textBox, use_camera=False)
           
            ##Other boxes
            else:
                if self.lineNum == 2:
                    Text.drawChar(self.textBox, ((12) + (8 * self.charIndex), 34), char= self.line[self.charIndex], flag=2)
                elif "&&" in self.line:
                    Text.drawChar(self.textBox, ((12) + (8 * self.charIndex), 22), char= self.line[self.charIndex], flag=2)
                else:
                    Text.drawChar(self.textBox, ((12) + (8 * self.charIndex), 7), char= self.line[self.charIndex], flag=2)

                ##  Code for original font that includes spacing
                """ if self.lineNum == 2:
                    Text.drawChar(self.textBox, ((0 + 6) + (10 * self.charIndex), 34), char= self.line[self.charIndex])
                elif "&&" in self.line:
                    Text.drawChar(self.textBox, ((0 + 6) + (10 * self.charIndex), 22), char= self.line[self.charIndex])
                else:
                    Text.drawChar(self.textBox, ((0 + 6) + (10 * self.charIndex), 7), char= self.line[self.charIndex]) """

        """
        Main text display method.
        Try if not mixer busy for slower text
        """
        def displayText(self, position, drawSurface, question = False): 
            self.drawChars()
            self.charIndex += 1
            if self.charIndex == len(self.line):
                SoundManager.getInstance().stopSFX("message.wav")
                self.text = self.text[self.charIndex+1:]
                if self.text == "":
                    self.end = True
                    self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (4,1))
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
                        self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (4,1))
                        self.cubeTick = 0
                        self.line = self.text[:self.text.index("\n")]
                        self.playSFX("message-finish.wav")
                        self.charIndex = 0
                        if self.large:
                            self.lineNum = 1
                else:
                    self.ready_to_continue = True
                    self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (4,1))
                    self.cubeTick = 0
                    self.line = self.text
                    self.charIndex = 0
                    self.playSFX("message-finish.wav")
            else:
                self.playSFX("message.wav")
                    
        def handleEvent(self):
            if self.closing or self.starting or self.done:
                return
            ##Prompt selection
            if self.choosing:
                if ACTIONS["right"] and self.highlighted == 0:
                    self.highlighted = 1
                    self.promptHighlight.position = vec(self.promptHighlight.position[0]+88, self.promptHighlight.position[1])
                    self.playSFX("pause_cursor.wav")
                elif ACTIONS["left"] and self.highlighted == 1:
                    self.highlighted = 0
                    self.promptHighlight.position = vec(self.promptHighlight.position[0]-88, self.promptHighlight.position[1])
                    self.playSFX("pause_cursor.wav")

                elif EventManager.getInstance().performAction("interact"):
                    
                    self.setClosing()
                    self.blitBackground()
                    if self.highlighted == 0:
                        self.promptResult = False
                    elif self.highlighted == 1:
                        self.promptResult = True

            elif self.ready_to_continue:       
                ##Progressing text
                Text.drawCursor(self.textBox, (216, 40))
                if EventManager.getInstance().performAction("interact"):
                    if self.end == True:
                        self.setClosing()
                        self.blitBackground()
                    else:
                        self.playSFX("OOT_Dialogue_Next.wav")
                        self.blitBackground()
                        self.box_drawn = False
                        self.ready_to_continue = False
                        self.backgroundBool = True
                    
                    

                elif EventManager.getInstance().performAction("map"):
                    self.setClosing()
                    self.blitBackground()
                    return

        def blitBackground(self): 
            if self.large:
                if self.type == 3:
                    self.textBox.blit(SpriteManager.getInstance().getSprite("TextBox3.png", (0,1)), (0,0))
                else:
                    surf = SpriteManager.getInstance().getSprite("TextBox2.png", (0,6))
                    self.textBox.blit(surf, (0,0))
            else:
                self.textBox.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,5)), (0,0))

            
        def setClosing(self):
            self.playSFX("WW_Textbox_Close.wav")
            self.box_drawn = False
            self.closing = True
            self.frame = 5

        def update(self, seconds):
        
            if self.starting:
                if self.large:
                    if self.frameTimer >= 0.01:
                        self.frameTimer = 0.0
                        self.frame += 1
                        self.frame %= 6
                        self.setImage()
                        if self.frame == 0:
                            self.starting = False
                            self.backgroundBool = True
                    else:
                        self.frameTimer += seconds
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
                    if self.frameTimer >= 0.01:
                        self.frameTimer = 0.0
                        self.frame -= 1
                        if self.frame == 0:
                            self.closing = False
                            self.done = True
                        else:
                            self.setImage()
                    else:
                        self.frameTimer += seconds
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
            else:
                if self.ready_to_continue:
                    pass
                elif self.done:
                    pass
                else:
                    self.frameTimer += seconds
                    if self.frameTimer >= 0.05:
                        self.frameTimer = 0.0
                        self.cubeTick += 1
                        self.cubeTick %= 4
                        self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (self.cubeTick, 1))
