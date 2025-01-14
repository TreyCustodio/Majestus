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
    def drawChar(drawSurface, position = vec(0,0), char: str ="", alpha: int = 255, color = "default", flag=0):
        ##  Safety Return   ##
        if char == " " or char == "" or char == "&" or len(char) > 1:
            return
        
        Text.last_pos = position
        ##  Black Text in EB Garamond  ##
        if flag == 2:
            image = Text.getImage(char, (0,0,0))
            drawSurface.blit(image, position)
            return
        
        ##  Off-white Text in EB Garamond   ##
        elif flag == 3:
            SoundManager.getInstance().playSFX("text_2.wav")
            if color != "default":
                image = Text.getImage(char, color)
            else:
                image = Text.getImage(char, (255,255, 200))
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
    def drawCursor(drawSurface, mainSurface):
        if Text.cursor == None:
            Text.cursor = TextCursor()

        ##  Set position for moving cursor
        motionTick = Text.cursor.motionTick
        if motionTick == 0:
            y = 0
        elif motionTick == 1:
            y = -2
        elif motionTick == 2:
            y = 0
        elif motionTick == 3:
            y = 2
        cursorSurf = pygame.surface.Surface(vec(16,22))
        cursorSurf.blit(Text.cursor.image, (0,0))
        mainSurface.blit(cursorSurf, (Text.last_pos[0] + 16, (Text.last_pos[1] - 14) + y))
        mainSurface.blit(IconManager.getButton("interact"), (Text.last_pos[0] + 16, Text.last_pos[1]))


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

            self.charIndex = 0
            self.textSpace = 0
            self.color_index_start = -1
            self.color_index_end = -1
            self.color_char = ""
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
            self.buffering = False
            self.clearing = False
            self.buffTimer = 0.0
            self.type = 0
            self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (0,1)) #Animated cube at bottom
            self.cubeTick = 0
            self.alpha = 255
            self.setImage()


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
            self.color_index_end = -1
            self.color_index_start = -1
            self.color_char = ""
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
        

        """
        (1.) Auxillary Methods-------------------------------------------------------
        """

        def playSFX(self, name, checkBusy = False):
            if checkBusy:
                if not pygame.mixer.get_busy():
                    SoundManager.getInstance().playSFX(name)
            else:
                SoundManager.getInstance().playSFX(name)


        def setText(self, text, icon = None, prompt = False, type = 2):
            """
            Prepare to display the text
            and the textBox.

            Expects:
            1. text to display, 
            2. an icon if there is one, 
            3. if it is a prompt, 
            4. the type of box
            """
            #   (1.) Prompt Display
            if prompt:
                self.prompt = True
                self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))

            #   (2.) Common Box
            elif type == 2:
                self.type = 2
                self.textBox = SpriteManager.getInstance().getSprite("TextBox2.png", (self.frame,0))
            
            #   (3.) Sign Post
            elif type == 3:
                self.type = 3
                self.textBox = SpriteManager.getInstance().getSprite("TextBox3.png", (self.frame,0))
            
            #   (4.) Invisible
            elif type == 4:
                self.type = 4
                self.textBox = pygame.surface.Surface(vec(304,208))
            
            #   (5.) Small Box
            elif type == 1:
                self.type = 1
                self.textBox = SpriteManager.getInstance().getSprite("TextBox.png", (self.frame,0))

            #   (6.) Add an Icon
            if icon != None and self.displayIcon == None:
                self.displayIcon = icon
            
            #   (7.) Exclude "Y/N" from text prompt display
            if self.prompt:
                self.text = text[3:]
            else:
                self.text = text

            #   (8.) Play sound effects
            if len(self.text) <= 8:
                pass
            else:
                if self.type != 4:
                    self.playSFX("TextBox_Open.wav")
            
            #   (9.) Set the text to display
            if "\n" in self.text:
                ##  Multiple lines
                self.line = self.text[self.charIndex:self.text.index("\n")]
            
            else:
                ##  1 line
                self.line = self.text
        
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
                    Text.drawCursor(self.textBox, drawSurface)
                
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
                    Text.drawCursor(self.textBox, drawSurface)
                
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
                self.displayText(position, self.textBox)

                ##  Draw the Icon
                if self.displayIcon != None:
                    self.drawIcon((position[0] + 106, position[1] - 32) - Drawable.CAMERA_OFFSET, drawSurface)
        
        
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

        def drawChars(self, drawSurface = None):
            """
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

                ##  Get the character at the current index
                char = self.line[self.charIndex]

                ##  Set a buffer for commas
                if char == ",":
                    if self.charIndex < len(self.line) - 3:
                        self.buffTimer = -0.5

                ##  Begin / End Color Coating
                elif char == "%":

                    ###  End of colored phrase; reset elements
                    if self.color_index_end != -1 and self.charIndex >= self.color_index_end:
                        self.color_index_end = -1
                        self.color_index_start = -1
                        self.color_char = ""
                        return
                    
                    ###  Start of colored phrase; set the indices
                    else:
                        self.color_index_start = self.charIndex
                        self.color_index_end = self.line.index(char, self.charIndex+1)# Find next index of '%'
                        self.color_char = self.line[self.charIndex+1]#  Find the color char
                        self.charIndex += 2
                        self.textSpace += 1
                
                ##  Draw the char according to the color char
                if self.color_index_end != -1 and self.charIndex >= self.color_index_start:
                    ### Red
                    if self.color_char == "r":
                        color = (255,50,50)

                    ### Blue
                    elif self.color_char == "b":
                        color = (50,50,255)
                    
                    ### Green
                    elif self.color_char == "g":
                        color = (50,255,50)

                    ### White
                    elif self.color_char == "w":
                        color = (255,255,255)

                    ### Dark Purple
                    elif self.color_char == "d":
                        color = (200,0,200)

                    ### Pink
                    elif self.color_char == "p":
                        color = (255, 17, 191)

                    ### Fire
                    elif self.color_char == "f":
                        color = (255, 69, 30)

                    ### Ice
                    elif self.color_char == "i":
                        color = (30, 255, 247)

                    ### Lightning
                    elif self.color_char == "t":
                        color = (248, 255, 17)

                    ### Wind is green
                    

                    ### Draw the char after setting the color
                    Text.drawChar(drawSurface, ((10) + (8 * (self.charIndex - (2 * self.textSpace) - (self.textSpace - 1))), (8 + (self.lineNum * 28)) ), char= self.line[self.charIndex], color=color, flag=3)
                
                ##  Draw a normal char
                else:
                    Text.drawChar(drawSurface, ((10) + (8 * (self.charIndex - (3 * self.textSpace))), (8 + (self.lineNum * 28)) ), char= self.line[self.charIndex], flag=3)
            

            #   (3.) Other Boxes
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
                    Text.drawChar(self.textBox, ((0 + 6) + (10 * self.charIndex), 7), char= self.line[self.charIndex])
                """


        """
        Main text display method.
        Try if not mixer busy for slower text.

        drawSurface -> textbox
        """
        def displayText(self, position, drawSurface, question = False): 
            
            #   (1.) Wait if buffering
            if self.buffering:
                return
            

            #   (2.) Start the Buffer for certain boxes
            elif self.type == 4:
                self.buffering = True


            #   (3.) Draw the character, increment the index
            self.drawChars(drawSurface)
            self.charIndex += 1

            #   (4.) Update the engine at the end of the line
            if self.charIndex >= len(self.line):

                ##  (i.) Play a sound effect, Update self.text
                SoundManager.getInstance().stopSFX("message.wav")
                self.text = self.text[self.charIndex+1:]

                ##  (ii.) Finish the text display once self.text is empty
                if self.text == "":
                    self.end = True
                    self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (4,1))
                    self.ready_to_continue = True
                    if self.type == 4:
                        return
                        self.playSFX("text_2.wav")
                    else:
                        self.playSFX("OOT_Dialogue_Done.wav")
                    self.charIndex = 0


                ##  (iii.) Get ready to display additional lines
                elif "\n" in self.text:

                    ###  Invisible Text
                    if self.type == 4:
                        ####    Wait for input and continue
                        if "&&" in self.line:
                            self.ready_to_continue = True
                            self.charIndex = 0
                            self.textSpace = 0
                            self.lineNum += 1
                            self.line = self.text[:self.text.index("\n")]
                        
                        ####    Wait for input, clear text, and continue
                        elif "$$" in self.line:
                            self.clearing = True
                            self.ready_to_continue = True
                            self.charIndex = 0
                            self.textSpace = 0
                            self.lineNum = 1
                            self.line = self.text[:self.text.index("\n")]
                        
                        ####    Draw to the next line
                        else:
                            self.line = self.text[:self.text.index("\n")]
                            self.charIndex = 0
                            self.textSpace = 0
                            self.lineNum += 1

                    ###  Other Boxes
                    else:
                        if self.lineNum == 1 and (not "&&" in self.line):
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
                            if self.type != 1:
                                self.lineNum = 1


                ##  (iv.) Wait for input
                else:
                    self.ready_to_continue = True
                    self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (4,1))
                    self.cubeTick = 0
                    self.line = self.text
                    self.charIndex = 0
                    self.playSFX("message-finish.wav")
            

            #   (5.) Play a sound effect for each character
            """ else:
                if self.type == 4:
                    return
                    self.playSFX("text_2.wav")
                else:
                    self.playSFX("message.wav") """
                    
        
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
                #Text.drawCursor(self.textBox, (216, 40))
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
                                self.closing = True
                            return
                        self.blitBackground()
                    
                    

                elif EventManager.getInstance().performAction("map"):
                    self.setClosing()
                    self.blitBackground()
                    return

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

        def update(self, seconds):
            
            #   (1.) Update Cursor
            if Text.cursor != None:
                Text.cursor.update(seconds)


            #   (2.) Update Buffer
            if self.buffering:
                self.buffTimer += (seconds * 2)
                if self.type == 4:
                    if self.buffTimer >= 0.1:
                        self.buffering = False
                        self.buffTimer = 0.0


            #   (3.) Startup Animation
            if self.starting:

                ##  Skip Animation for type 4
                if self.type == 4:
                    self.starting = False
                    return
                
                ##  Small Boxes
                elif self.type == 1:
                    self.frame += 1
                    self.frame %= 5
                    self.setImage()
                    if self.frame == 0:
                        self.starting = False
                        self.setBackgroundBool()
                    return
                
                ##  Other Boxes
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
                ##  Small Boxes
                if self.type == 1:
                    self.frame -= 1
                    if self.frame == 0:
                        self.closing = False
                        self.done = True
                    else:
                        self.setImage()
                    return
                
                ##  Other Boxes
                else:
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
                    else:
                        self.frameTimer += seconds
                    
                    return
                                    
          
            ##  Update Prompt Elements
            if self.prompt:
                self.promptHighlight.update(seconds)
            
            else:
                ##  Update for ready to continue
                if self.ready_to_continue:
                    pass
                ##  No Update Once Done
                elif self.done:
                    pass
                else:
                    ##  Update Cube Animation
                    self.frameTimer += seconds
                    if self.frameTimer >= 0.05:
                        self.frameTimer = 0.0
                        self.cubeTick += 1
                        self.cubeTick %= 4
                        self.cube = SpriteManager.getInstance().getSprite("TextBox2.png", (self.cubeTick, 1))

