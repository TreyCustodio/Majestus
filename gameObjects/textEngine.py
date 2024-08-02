import pygame

from . import Drawable,  Animated, Text, Highlight, Map, Number

from utils import  vec, RESOLUTION, SpriteManager, SoundManager, INV, INFO, COORD, EQUIPPED

from UI import ACTIONS, EventManager

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
            self.voiceInt = -1
            self.frameTimer = 0.0
            self.noBox = False
            self.setImage()


        def setPromptHighlight(self, position):
            self.promptHighlight.position = vec(position[0]+64-6, position[1]+32-6)

        def setImage(self):
            if self.large:
                if self.type == 2:
                    self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))
                elif self.type == 3:
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
            ##Draw the box
            if not self.box_drawn:
                #print(self.frame)
                pass
                drawSurface.blit(self.textBox, position - Drawable.CAMERA_OFFSET)

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
                    #self.drawEnd(position, drawSurface)

            ##Continue to next line
            elif self.ready_to_continue:
                return
                #self.drawContinue(position, drawSurface)
            
            ##Buffer
            elif self.displayTimer > 0 and self.displayTimer < 0.1:
                return
                #self.drawYellow1(position, drawSurface)
                
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
                        if self.voiceInt == 0:
                            SoundManager.getInstance().stopAllSFX()
                            SoundManager.getInstance().playVoice("Before.wav")
                            self.voiceInt += 1
                        elif self.voiceInt == 1:
                            SoundManager.getInstance().stopAllSFX()
                            SoundManager.getInstance().playVoice("Abyss.wav")
                            self.voiceInt += 1
                        elif self.voiceInt == 2:
                            SoundManager.getInstance().stopAllSFX()
                            SoundManager.getInstance().playVoice("Transformed.wav")
                            self.voiceInt += 1
                        elif self.voiceInt == 3:
                            SoundManager.getInstance().stopAllSFX()
                            SoundManager.getInstance().playVoice("Factions.wav")
                            self.voiceInt += 1
                        elif self.voiceInt == 4:
                            SoundManager.getInstance().stopAllSFX()
                            SoundManager.getInstance().playVoice("Foundation.wav")
                            self.voiceInt += 1
                        elif self.voiceInt == 5:
                            SoundManager.getInstance().stopAllSFX()
                            SoundManager.getInstance().playVoice("Infant.wav")
                            self.voiceInt += 1

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
                    if self.highlighted == 0:
                        self.promptResult = False
                    elif self.highlighted == 1:
                        self.promptResult = True

            elif self.ready_to_continue:       
                ##Progressing text
                if EventManager.getInstance().performAction("interact"):
                    if self.end == True:
                        self.setClosing()
                    else:
                        self.playSFX("OOT_Dialogue_Next.wav")
                        self.box_drawn = False
                        self.ready_to_continue = False
                        self.backgroundBool = True
                elif EventManager.getInstance().performAction("map"):
                    self.setClosing()
                    return
                    

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