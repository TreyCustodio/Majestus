import pygame

from . import Drawable,  Animated, TextCursor, Highlight, Map, Number, IconManager

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
    
    cursor = None
    last_pos = None

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
    

    
    def drawChar(drawSurface, position = vec(0,0), char: str ="", alpha: int = 255, color = "default", flag=0):
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

        Alphabetical and special chars use ASCII values to display.
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
        
        Text.last_pos = position
        ##  Black Text in EB Garamond  ##
        if flag == 2:
            image = Text.getImage(char, (0,0,0))
            drawSurface.blit(image, position)
            return
        
        ##  Off-white Text in EB Garamond   ##
        elif flag == 3:
            if color != "default":
                image = Text.getImage(char, color)
            else:
                image = Text.getImage(char, (255, 255, 200))
            
            #   Major change here; return the image instead of blitting
            #drawSurface.blit(image, position)
            return (image, char, color)

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
        
        #   Making a huge change here.
        #   Just return the image and the position
        drawSurface.blit(image, position)


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
        """
        Handles displaying dialogue.

        A scalable, robust engine that allows you 
        to display text in a variety of ways
        and easily implement new ways.
        (1.) TextEngine instantiated by the ScreenManager

        (2.) ScreenManager checks if the RoomEngine needs a textbox.

        (3.) ScreenManager draws game then check's
             TextEngine's state (let TextEngine handle state checking)

        (4.) TextEngine draws the textbox onto the drawSurface

        (5.) TextEngine resets its state

        Goals for new engine implementation:------------------------

        (1.) Doesn't need to be a singleton.
        Only 1 instance of the class is ever in memory.

        (2.) Use less instance variables or at least organize them.

        (3.) Overall make the code more readable

        (4.) Easily allow for unique text box displays

        (5.) Make parsing much less complicated
        """

        def __init__(self):
            self.backgroundBool = False
            self.blackBool = False
            self.black = SpriteManager.getInstance().getSprite("TextBox2.png", (0,6))
            self.text = ""
            self.line = ""
            self.starting = True
            self.displayIcon = None

            #   Colors
            self.color = "default"

            #   Textbox States
            self.input_tick = 0
            self.box_drawn = False
            self.ready_to_display = True
            self.ready_to_continue = False
            self.end = False
            self.closing = False
            self.done = False
            self.motionTick = 0

            #   Textbox Images
            self.frame = 1
            self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (0,0))
            self.displayTimer = 0.0
            self.cursor = TextCursor()
            self.displayLine = 0
            self.index_image = pygame.transform.scale(SpriteManager.getInstance().getSprite("white_px.png"), (6,20))

            #   Parsing
            self.lineNum = 1 #The line the text display is currently on
            self.charIndex = 0

            self.promptHighlight = Highlight((16*6 - 8, 16*5 + 10), flag = 2)
            self.prompt = False
            self.highlightTimer = 0
            self.highlighted = 0 #0 -> No, #1 -> Yes
            self.choosing = False#The state of choosing yes or no
            self.promptResult = False
            self.voiceInt = -1
            self.frameTimer = 0.0
            self.noBox = False
            

            self.clearing = False

            #   Buffers
            self.buffTimer = 0.0
            self.buffering = False
            self.buffTime = 0.2

            self.type = 0
            self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (0,1)) #Animated cube at bottom
            self.cubeTick = 0
            self.alpha = 255
            self.setImage()

            #   Character array
            self.dialogue = [[]]

        """
        (1.) Auxillary Methods-------------------------------------------------------
        """

        def setPromptHighlight(self, position):
            self.promptHighlight.position = vec(position[0]+64-6, position[1]+32-6)

        def setImage(self):
                #   Small
                if self.type == 1:
                    self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (self.frame,0))
                    
                #   Regular
                elif self.type == 2:
                    self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))
                    #self.textBox = pygame.transform.scale(SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0)), (248,64))
                
                #   Sign
                elif self.type == 3:
                    self.textBox = SpriteManager.getInstance().getSprite("TextBox3.png", (self.frame,0))
                
                #   Invisible / Intro
                elif self.type == 4:
                    pass
                
                else:
                    self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))
        

        def setBackgroundBool(self):
            self.backgroundBool = not self.backgroundBool

        def reset(self):
            self.text = ""
            self.line = ""
            self.displayIcon = None
            self.starting = True
            self.buffering = False
            self.buffTimer = 0.0
            self.frame = 1
            self.alpha = 255

            self.charIndex = 0
            self.box_drawn = False
            self.ready_to_display = True
            self.ready_to_continue = False
            self.end = False
            self.closing = False
            self.done = False
            self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (0,0))
            self.textSpace = 0

            self.displayTimer = 0.0

            self.lineNum = 1 #The line the text display is currently on

            self.promptHighlight = Highlight((16*6 - 8, 16*5 + 10), flag = 2)
            self.prompt = False
            self.highlightTimer = 0
            self.highlighted = 0 #0 -> No, #1 -> Yes
            self.choosing = False#The state of choosing yes or no
            self.voiceInt = -1

            self.noBox = False
            self.clearing = False
            self.setImage()
            self.type = 2

            self.dialogue = [[]]
            self.color = "default"
        

        def playSFX(self, name, checkBusy = False):
            if checkBusy:
                if not pygame.mixer.get_busy():
                    SoundManager.getInstance().playSFX(name)
            else:
                SoundManager.getInstance().playSFX(name)


        def setText(self, text, icon = None, prompt = False, type = 2):
            """
            Create the textBox surface.

            Expects:
            1. text to display, 
            2. an icon if there is one, 
            3. if it is a prompt, 
            4. the type of box
            """
            #   (1.) Get the box ---------------------

            ##  (i.) Prompt
            if prompt:
                self.prompt = True
                self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))

            ##  (ii.) Common Box
            elif type == 2:
                self.type = 2
                self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))
            
            ##  (iii.) Sign Post
            elif type == 3:
                self.type = 3
                self.textBox = SpriteManager.getInstance().getSprite("TextBox3.png", (self.frame,0))
            
            ##  (iv.) Invisible
            elif type == 4:
                self.type = 4
                self.textBox = pygame.surface.Surface(vec(304,208))
            
            ##  (v.) Small Box
            elif type == 1:
                self.type = 1
                self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (self.frame,0))


            #   (2.) Add an Icon --------------------------
            if icon != None and self.displayIcon == None:
                self.displayIcon = icon
            

            #   (3.) Parse the text ----------------------
            if self.prompt:
                ##  Exclude "Y/N" from text prompt display
                self.text = text[3:]
            else:
                self.text = text

            self.buildDialogue()

            #   (4.) Play the opening sfx -------------------
            if len(self.text) <= 8:
                pass
            else:
                if self.type != 4:
                    self.playSFX("TextBox_Open.wav")

        
        def setAlpha(self):
            """
            Make the textbox slightly
            transparent.
            """
            self.textBox.set_alpha(220)



        """
        (2.) Drawing Methods-------------------------------------------------------
        """
            
        def draw(self, position, drawSurface):
            """
            Draw the textbox.
            """

            #   (1.) Set the transparency
            if self.type != 4:
                self.setAlpha()
            

            #   (2.) Blit the box to the surface
            if self.type == 4:

                ##  Invisible: Blit in the top right
                drawSurface.blit(self.textBox, vec(0,0) - Drawable.CAMERA_OFFSET)
                if not self.ready_to_continue:
                    pass

            else:
                ##  Others: Blit at the desired position
                drawSurface.blit(self.textBox, position - Drawable.CAMERA_OFFSET)
                if not self.closing and not self.starting:
                    drawSurface.blit(self.cube, position - Drawable.CAMERA_OFFSET)
                
            
            #   (3.) Draw onto the surface according to the state
            if self.closing:

                ##  Invisible text
                if self.type == 4:
                    drawSurface.blit(self.textBox, vec(0,0) - Drawable.CAMERA_OFFSET)
                    return
                
                else:
                    return
                
            elif self.done:
                return
            
            elif self.starting:
                return
            
            elif not self.box_drawn:
                self.box_drawn = True
            

            #   (4.) Draw the end of the dialogue
            if self.end:

                ##  Draw the cursor for box 4
                if self.type == 4:
                    self.drawCursor(drawSurface)
                
                ##  Draw the Icon
                if self.displayIcon != None:
                    self.drawIcon((position[0] + 106, position[1] - 32) - Drawable.CAMERA_OFFSET, drawSurface)
                
                ##  Draw the Prompt
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


            #   (5.) Draw the waiting for input display
            elif self.ready_to_continue:

                ##  Draw the cursor for box 4; Waiting for input but not finished.
                if self.type == 4:
                    self.drawCursor(drawSurface)
                
                ##  Draw the Icon
                if self.displayIcon != None:
                    self.drawIcon((position[0] + 106, position[1] - 32) - Drawable.CAMERA_OFFSET, drawSurface)
                
                return
            

            #   (6.) Wait to display Text
            elif self.displayTimer > 0 and self.displayTimer < 0.1:
                return
            

            #   (7.) Display the text and Icon
            else:

                ##  Draw the Text
                self.displayText(self.textBox, drawSurface)
                if not self.ready_to_continue:
                    self.drawInput(drawSurface)

                ##  Draw the Icon
                if self.displayIcon != None:
                    self.drawIcon((position[0] + 106, position[1] - 32) - Drawable.CAMERA_OFFSET, drawSurface)
        
        
        def drawPrompt(self, position, drawSurface):
            drawSurface.blit(SpriteManager.getInstance().getSprite("TextBox2.png", (0,5)), position - Drawable.CAMERA_OFFSET)

        def drawCursor(self, drawSurf):
            """
            Draws the cursor when waiting
            for input from the player.
            Cursor depends on the box type.
            """
            #   (1.) Draw the cursor onto the screen
            ##  Interact Icon stays stationary
            drawSurf.blit(IconManager.getButton("interact"), (10 + (8 * self.charIndex) , 20 * (self.displayLine + 1) + 14))
            
            ##  Arrow moves up and down
            drawSurf.blit(self.cursor.image, (10 + (8 * self.charIndex) , 19 * (self.displayLine + 1) + self.cursor.y))


        def drawInput(self, drawSurf):
            #   (1.) Get the color value from dialogue arr
            # print(self.dialogue[self.lineNum-1][self.charIndex])
            # print("Index: " + str(self.charIndex))
            # print("Line: " + str(self.lineNum))
            # print()

            char = self.dialogue[self.lineNum-1][self.charIndex]
            if len(char) > 2:
                color = char[2]
            else:
                color = "default"
            

            #   (2.) Set the color of the index image
            if color == "default":
                self.index_image.fill((255,255,200))

            else:
                self.index_image.fill(color)


            #   (3.) Display the index image; flashing when buffering
            if self.buffering and self.buffTimer < 0.0:
                ##  Draw
                if self.input_tick < 10:
                    drawSurf.blit(self.index_image, (10 + (8 * self.charIndex) , 20 * (self.displayLine + 1)))

            else:
                drawSurf.blit(self.index_image, (10 + (8 * self.charIndex) , 20 * (self.displayLine + 1)))
            

        def drawIcon(self, position, drawSurface):
            box = SpriteManager.getInstance().getSprite("icon.png", (0,0))
            icon = SpriteManager.getInstance().getSprite("icon.png", self.displayIcon)
            drawSurface.blit(box, position)
            drawSurface.blit(icon, position)


        def parseChar(self, char = "", drawSurface = None):
            """
            Produce certain effects depending
            on the dialogue type and the char.
            drawSurface -> textBox
            """
            #   (1.) Sign boxes
            if self.type == 3:

                ##  Line 2
                if self.lineNum == 2:
                    Text(((16 + 10) + (8 * self.charIndex), 34), self.line[self.charIndex], color=(0,0,0)).draw(self.textBox, use_camera=False)
                
                ##  Focus line
                elif "&&" in self.line:
                    Text(((16 + 10) + (8 * self.charIndex), 22), self.line[self.charIndex], color=(0,0,0)).draw(self.textBox, use_camera=False)
                
                ##  Line 1
                else:
                    Text(((16 + 10) + (8 * self.charIndex), 7 + 8), self.line[self.charIndex], color=(0,0,0)).draw(self.textBox, use_camera=False)
            
            
            #   (2.) Invisible
            elif self.type == 4:
                
                #  (i). Color Coating
                if char == "%":
                    #   (a.) Observe the next char
                    next_char = self.text[self.charIndex + 1]

                    #   (b.) '%%' = '%' without any color changing
                    if next_char == '%':
                        ##  Display %
                        return
                    
                    #   (c.) Switch the text color
                    elif next_char == "~":
                        self.color = "default"

                    ## Red
                    elif next_char == "r":
                        self.color = (255,50,50)

                    ## Blue
                    elif next_char == "b":
                        self.color = (50,50,255)
                    
                    ## Green
                    elif next_char == "g":
                        self.color = (50,255,50)

                    ## White
                    elif next_char == "w":
                        self.color = (255,255,255)

                    ## Dark Purple
                    elif next_char == "d":
                        self.color = (200,0,200)

                    ## Pink
                    elif next_char == "p":
                        self.color = (255, 17, 191)

                    ## Fire
                    elif next_char == "f":
                        self.color = (255, 69, 30)

                    ## Ice
                    elif next_char == "i":
                        self.color = (30, 255, 247)

                    ## Lightning
                    elif next_char == "t":
                        self.color = (248, 255, 17)

                    ## Return to default
                    else:
                        self.color = "default"
                    
                    ##  Go to the next regular char, skipping '%c'
                    self.charIndex += 1
                    return
                
                #   (ii.) Clearing the text
                elif char == "$":
                    next_char = self.text[self.charIndex + 1]
                    if next_char == "$":
                        ##  We're clearing
                        self.dialogue[self.lineNum - 1].append(("clear", "$"))
                        self.charIndex += 1
                        return
                
                #   (iii.) Waiting for input
                elif char == "&":
                    pass

                #   (iv.) Regular draw routine / other effects
                else:
                    pass

                #   (v.) Append the image and position to the dialogue array
                self.dialogue[self.lineNum - 1].append(Text.drawChar(drawSurface, char= char, color=self.color, flag=3))

            #   (3.) Other Boxes
            else:
                if self.lineNum == 2:
                    Text.drawChar(self.textBox, ((12) + (8 * self.charIndex), 34), char= self.line[self.charIndex], flag=2)
                elif "&&" in self.line:
                    Text.drawChar(self.textBox, ((12) + (8 * self.charIndex), 22), char= self.line[self.charIndex], flag=2)
                else:
                    Text.drawChar(self.textBox, ((12) + (8 * self.charIndex), 7), char= self.line[self.charIndex], flag=2)


        def buildDialogue(self):
            """
            Build an array containing
            the surfaces and positions
            of each character's image.
            """

            while True:
                char = self.text[self.charIndex]
                #   (1.) Go to next line
                if char == '\n':
                    self.lineNum += 1
                    self.dialogue.append([])
                    self.charIndex += 1
                    continue
                
                #   (2.) Get the image and position of the char
                self.parseChar(char, self.textBox)
                self.charIndex += 1

                if self.charIndex >= len(self.text) - 1:
                    break
                
            self.charIndex = 0
            self.lineNum = 1

        
        def displayText(self, drawSurface, mainSurface): 
            """
            Driver code for text display.

            Expects:
            drawSurface -> the textbox
            """
            #   (1.) Wait if buffering
            if self.buffering or self.clearing:
                return
            

            #   (2.) Start the Buffer for certain boxes
            elif self.type == 4:
                self.buffering = True


            #   (3.) Draw the character, increment the index
                    
            #   (i.) Get the char and position
            char = self.dialogue[self.lineNum-1][self.charIndex][0]
            pos = vec(10 + (8 * self.charIndex) , 20 * (self.displayLine + 1))
            
            #   (ii.) Display the char
            if char == "clear":
                ##   Clear, wait for input
                self.clearing = True
                self.ready_to_continue = True
                EventManager.getInstance().disableAction("interact")
                self.lineNum += 1
                return

            else:
                ##  Buffer for commas
                if self.dialogue[self.lineNum-1][self.charIndex][1] == ",":
                    self.buffTimer -= 0.6

                ##  Play sfx and display
                self.playSFX("text_2.wav")
                drawSurface.blit(char, pos)
            
            
            #   (iii.) Increment the charIndex
            self.charIndex += 1
            

            #   (4.) Check if we are at the end of the line
            if self.charIndex >= len(self.dialogue[self.lineNum - 1]):

                #  (i.) Increment the line number
                self.lineNum += 1
                self.displayLine += 1

                #   (ii.) Check if there are no more lines
                if self.lineNum > len(self.dialogue):
                    ##  Reset the indices, wait for input, end dialogue
                    Text.last_pos = pos
                    self.end = True
                    self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (4,1))
                    self.ready_to_continue = True
                    EventManager.getInstance().disableAction("interact")
                    self.playSFX("OOT_Dialogue_Done.wav")
                    self.lineNum -= 1
                    self.displayLine -= 1

                #   (iii.) Reset the charIndex, ready to display next line
                else:
                    self.charIndex = 0


        """
        (3.) Handling Events and Updating ---------------------------------------------
        """

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
                ##  Progressing text
                if EventManager.getInstance().performAction("interact"):
                    if self.end == True:
                        self.setClosing()
                        self.blitBackground()

                    else:
                        self.playSFX("OOT_Dialogue_Next.wav")
                        self.box_drawn = False
                        self.ready_to_continue = False
                        self.backgroundBool = True
                        if self.type == 4:
                            if self.clearing:
                                self.charIndex = 0
                                self.displayLine = 0
                                self.closing = True
                            return
                        self.blitBackground()
                    
                elif EventManager.getInstance().performAction("map"):
                    self.setClosing()
                    self.blitBackground()
                    return
            else:
                #   Speed up text
                if EventManager.getInstance().isPressed("interact"):
                    self.buffTimer = self.buffTime
        
        def blitBackground(self):
            """
            Blit the background of the textBox.
            Cleans text off the screen.
            """

            #   (1.) Small box
            if self.type == 1:
                self.textBox.blit(SpriteManager.getInstance().getSprite("TextBox.png", (0,5)), (0,0))

            #   (2.) Sign Post                
            if self.type == 3:
                self.textBox.blit(SpriteManager.getInstance().getSprite("TextBox3.png", (0,1)), (0,0))
            
            #   (3.) Invisible
            elif self.type == 4:
                return
            
            #   (4.) Common Box
            else:
                surf = SpriteManager.getInstance().getSprite("TextBox2.png", (0,6))
                self.textBox.blit(surf, (0,0))                

            
        def setClosing(self):
            self.playSFX("WW_Textbox_Close.wav")
            self.box_drawn = False
            self.closing = True
            self.frame = 5

            if self.type == 4:
                self.charIndex = 0
                self.displayLine = 0

        def update(self, seconds):
            
            #   (1.) Update Cursor
            


            #   (2.) Update Buffer
            if self.buffering:
                self.buffTimer += (seconds*2)
                if self.type == 4:
                    if self.buffTimer >= self.buffTime:
                        self.buffering = False
                        self.buffTimer = 0.0


            #   (3.) Startup Animation
            if self.starting:

                #   (i.) Skip Animation for type 4
                if self.type == 4:
                    self.starting = False
                    return
                
                #   (ii.) Small Box Animation
                elif self.type == 1:
                    self.frame += 1
                    self.frame %= 5
                    self.setImage()
                    if self.frame == 0:
                        self.starting = False
                        self.setBackgroundBool()
                    return
                
                #   (iii.) Other box animation
                else:
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
                    
            
            #   (4.) Closing Animation
            elif self.closing:
                #   (i.) Small Box Animation
                if self.type == 1:
                    self.frame -= 1
                    if self.frame == 0:
                        self.closing = False
                        self.done = True
                    else:
                        self.setImage()
                    return
                
                #   (ii.) Other Box Animation
                else:
                    ##  Track the frameTimer
                    if self.frameTimer >= 0.01:
                        self.frameTimer = 0.0

                        ###  Invisible: Decrease Alpha
                        if self.type == 4:
                            self.textBox.set_alpha(self.alpha)
                            self.alpha -= 20
                            if self.alpha <= 0:
                                self.alpha = 255
                                if self.clearing:
                                    self.clearing = False
                                    self.buffering = True
                                    self.closing = False
                                    self.textBox = pygame.surface.Surface(vec(304,208))
                                else:
                                    self.closing = False
                                    self.done = True
                                    self.buffering = True
                            
                        ###  Other Types: Decrease Frame  
                        else:
                            self.frame -= 1
                            if self.frame == 0:
                                self.closing = False
                                self.done = True
                            else:
                                self.setImage()

                    ##  Increment the frame timer
                    else:
                        self.frameTimer += seconds
                    
                    

                    return
                                    
          
            #   (5.) Update Prompt Elements
            if self.prompt:
                self.promptHighlight.update(seconds)
            

            #   (6.) Waiting for Input Animation
            elif self.ready_to_continue:
                self.cursor.update(seconds)


            #   (7.) End of dialogue; not waiting for input
            elif self.done:
                pass
            

            #   (8.) Update Text Animation
            else:
                self.input_tick += 1
                if self.input_tick >= 20:
                    self.input_tick = 0

                self.frameTimer += seconds
                if self.frameTimer >= 0.05:
                    self.frameTimer = 0.0
                    self.cubeTick += 1
                    self.cubeTick %= 4
                    self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (self.cubeTick, 1))

