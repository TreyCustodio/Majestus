"""
Here's to the NEW and IMPROVED text engine!
May Myer have mercy on my feeble soul!
"""

import pygame

from . import Drawable,  Animated, TextCursor, Highlight, Map, Number, IconManager

from utils import  vec, RESOLUTION, SpriteManager, SoundManager, INV, INFO, COORD, EQUIPPED

from UI import ACTIONS, EventManager

from pygame.locals import *

import numpy as np

import os


def playSfx(effect=""):
    """Here's a useful playSfx() function"""
    SoundManager.getInstance().playSFX(effect)

"""
First, the Text Class.
This class implements functionality for
characters indivudally, giving access to
fonts, colors, and different ways of
drawing each individual character.

Eventually I'd like to add shaking characters,
glowing characters for the intro,
and other effects.

"""

class Char(object):
    """A character class.
    Characters are meant to be displayed on a textbox surface
    """

    def __init__(self, char="", next_char=None):

        #   (1) Parse the char; get any potential color changes and display commands    #
        color, self.displayCommand = self.parse(char, next_char)
        Text.COLOR = color

        #   (2) Get the image from chars.png    #
        self.image = self.getImage(char)


        #   (3) Set the char's position on the textBox  #


        #   (4) Set the visibility value    #
        self.visible = False


        #   (5) Set the text value for debugging    #
        self.text = char

    


    def getImage(self, char, fileName = "chars.png"):
        """Grab the character's image from a specified sprite sheet; chars.png by default"""
        color = Text.COLOR
        if color != "default":
            image = Text.FONT.render(char, False, color)
        else:
            image = Text.FONT.render(char, False, (255, 255, 200))

        return image
    
        #  Numeric chars   #
        if char.isnumeric():
            image = SpriteManager.getInstance().getSprite("chars.png", (int(char),3))
        
        #  Alphabetical chars  #
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

        #  Adjust surface alpha and display    #
        #image.set_alpha(alpha)
        return image

    
    def parse(self, char, next_char):
        """Returns (color, displayCommand)"""

        color = Text.COLOR
        displayCommand = ""

        #   (1) Cutscene Type   #
        if TextEngine.TYPE == 4:

            #  %c -> Color Coating    #
            if char == "%":

                ##  Observe the next char   ##
                if next_char == None or next_char == "\n":
                    pass #Nothing, just display the '%'
                
                ##  '%%' = '%' without any color changing   ##
                elif next_char == '%':
                    ##  Display %
                    displayCommand = "%"
                
                else:
                    displayCommand = "colorSwap"
                    ##   Switch the text color ##
                    if next_char == "~":
                        color = "default"

                    ## Red  ##
                    elif next_char == "r":
                        color = (255,50,50)

                    ## Blue ##
                    elif next_char == "b":
                        color = (50,50,255)
                    
                    ## Green    ##
                    elif next_char == "g":
                        color = (50,255,50)

                    ##  Yellow  ##
                    elif next_char == "y":
                        color = (200, 200, 0)

                    ## White    ##
                    elif next_char == "w":
                        color = (255,255,255)

                    ## Dark Purple  ##
                    elif next_char == "d":
                        color = (200,0,200)

                    ## Pink ##
                    elif next_char == "p":
                        color = (255, 17, 191)

                    ## Fire ##
                    elif next_char == "f":
                        color = (255, 69, 30)

                    ## Ice  ##
                    elif next_char == "i":
                        color = (30, 255, 247)

                    ## Lightning    ##
                    elif next_char == "t":
                        color = (248, 255, 17)

                    
                    ## Return to default    ##
                    else:
                        color = "default"
                
            
            #   $$ -> Clear the textBox #
            elif char == "$":
                if next_char == "$":
                    ##  We're clearing  ##
                    displayCommand = "clear"
            


            #   && -> Wait for input    #
            elif char == "&":
                if next_char == "&":
                    ##  We're waiting for input ##
                    displayCommand = "wait"
            
            
            else:
                pass

        return color, displayCommand
    
    
    def setVisible(self, value=True):
        self.visible = value


    def update(self, seconds):
        return


class Text(object):
    """A static Text Utility class"""

    #   Initialize pygame fonts if not already done #
    if not pygame.font.get_init():
        pygame.font.init()

    #   Metadata about fonts, we'll use ALTTP font for now.
    FONT_FOLDER = "fonts"
    FONT = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 16)
    BOX = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 14)
    SMALL = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 12)
    
    #   The current Cursor object we'll display
    CURSOR = None

    #   The last character's position
    LAST_POS = None

    #   The current color   #
    COLOR = "default"



class TextEngine(object):
    """This class should never be instantiated.
    Not even a singleton class. There's too much data
    that doesn't need to occupy space in memory.
    However, we should keep track of the current dialogue matrix."""
    
    """
    TEXT DISPLAY PROCESS

    (0) TextEngine is initialized with setText(text, icon).

    (1) Build a dialogue matrix,
    consisting of each character object.

    (2) During the draw routine, loop through
    the dialogue matrix and display each character
    that needs to be displayed.
    
    (3) During the handleEvent routine,
    check for inputs.
    
    (4) During the update routine,
    animate characters that need to be animated.

    (5) Once the current text display is done and it is time
    to resume gameplay, reset the engine.
    """

    #   Initialization Data   #
    DIALOGUE = []     # Dialogue Matrix
    TYPE = 0            # Box type
    PROMPT = False      # Is there a Y/N prompt?
    ICON = None         # Icon Image
    BOX = None          # Box Image
    DISPLAY_POS = vec(4, 4) # The text display pos relevant to the box


    #   Character Display   #
    SPACING = 8         # num of pixels to seperate each char image by
    BUFFER = 0.0        # a timer that drives the buffer time between each character that is displayed
    CURRENT_LINE = 0    # the current line to examine for displayChars()
    CURRENT_INDEX = 0   # the current index to examine for displayChars()
    A = 255             # transparency alpha value
    CURSOR = TextCursor() # Text cursor; indicates input

    
    #   States that drive the draw routine  #
    STATES = {"ready_to_continue": False,   # Wait for (interact) to continue text display
              "end": False,                 # At the end of dialogue. Wait for box to close before DONE.
              "closing": False,             # The box is closing / downscaling in most cases
              "done": False,                # We're done. Time to reset and switch states.
              "$$": False,                  # Waiting for input before clearing the box
              }


    def reset():
        """Reset the engine in preparation for the next dialogue routine"""

        #   Reset the States    #
        for k in TextEngine.STATES:
            TextEngine.STATES[k] = False
        
        #   Reset the Dialogue Matrix   #
        TextEngine.DIALOGUE = []

        #   Reset the box Type  #
        TextEngine.TYPE = 0

        #   Reset the prompt boolean    #
        TextEngine.PROMPT = False

        #   Reset the display properties  #
        TextEngine.DISPLAY_POS = vec(4, 4)
        TextEngine.CURRENT_INDEX = 0
        TextEngine.CURRENT_LINE = 0
        TextEngine.BUFFER = 0.0
        TextEngine.SPACING = 8

        #   Reset alpha #
        TextEngine.A = 255

        #   Reset Text's color val  #
        Text.COLOR = "default"

        

    """
    Some auxillary / getter functions
    """

    def finished():
        """Is the current dialogue routine finished? Ready to switch states if so."""
        return TextEngine.STATES["done"]
    
    def closing():
        """Are we closing the box right now?"""
        return TextEngine.STATES["closing"]
    
    def atEnd():
        """Are we at the end of the dialgue?"""
        return TextEngine.STATES["end"]
    
    def waiting():
        """Are we waiting for input before continuing?"""
        return TextEngine.STATES["ready_to_continue"]
    
    def clearing():
        """Has a '$$' triggered a clearing sequence?"""
        return TextEngine.STATES["$$"]
    
    def backgroundBool():
        """Deprecated ???"""
        return False
    
    def setBackgroundBool():
        """Deprecated ???"""
        return
    


    """
    The draw routine.
    (1) Set up the text and Dialogue Matrix at the start.
    (2) Perform draw() continuously.
    """
    def setText(text = "", icon = None, prompt = False, type = 2):
        """
        Prepare the engine for text display.
        (1) Set the box image
        (2) Set the type, prompt boolean, and icon

        Types:
        1 -> Small boxes; 2 -> Default Boxes; 3 -> Signposts; 4 -> Invisible / Journal / Cutscene
        5 -> ???;
        """

        #   (1) Set the box image   #
        ##  Default ##
        if type == 2:
            TextEngine.BOX = SpriteManager.getInstance().getSprite("TextBox2.png", (0,0))
        
        ##  Signpost    ##
        elif type == 3:
            TextEngine.BOX = SpriteManager.getInstance().getSprite("TextBox3.png", (0,0))
        
        ##  Cutscene    ##
        elif type == 4:
            TextEngine.BOX = pygame.surface.Surface(vec(304,208))
        
        ##  Small Box   ##
        elif type == 1:
            TextEngine.BOX = SpriteManager.getInstance().getSprite("TextBox.png", (0,0))
        
        ##  Finish by setting the type variable ##
        TextEngine.TYPE = type


        #   (2) Is there a prompt involved with this dialogue?  #
        TextEngine.PROMPT = prompt
        ##  If so, we need to omit the first 3 chars "Y/N" from the display ##
        if prompt:
            text = text[3:]


        #   (3) Then we set the icon    #
        TextEngine.ICON = icon


        #   (4) And now we can construct the dialogue matrix    #
        TextEngine.buildDialogue(text)


        #   (5) Play the opening sound effect   #
        if TextEngine.TYPE != 4:
            playSfx("text_open1.wav")


        #   (6) Now we can begin the draw routine   #


    def buildDialogue(text=""):
        """
        (1) Construct the dialogue matrix.
        This should only be called ONCE,
        prior to beginning the draw routine.
        """

        charIndex = 0
        line = []

        while True:
            #   Break the loop at the end of the text   #
            if charIndex >= len(text) - 1:
                break
            
            #   Begin by getting the char   #
            char = text[charIndex]

            #   Go to the next line #
            if char == "\n":
                ##  Note that "\n" indicates the end of dialogue too, so you'll always encounter it ##
                
                #   Get the Character Object    #
                ##  Get the next char for parsing   ##
                if charIndex +1 > (len(text) - 1):
                    next_char = None
                else:
                    next_char = text[charIndex+1]

                ##  Create the Char object  ##
                element = Char(char, next_char)
                if element.displayCommand != "":
                    ##  Skip double chars that tell the parser to perform a command ##
                    charIndex += 1

                ##  Append the completed line to DIALOGUE   ##
                line.append(element)
                TextEngine.DIALOGUE.append(line)

                line = []
                charIndex +=1
            
            else:
                #   Get the Character Object    #
                ##  Get the next char for parsing   ##
                if charIndex +1 > (len(text) - 1):
                    next_char = None
                else:
                    next_char = text[charIndex+1]

                ##  Create the Char object  ##
                element = Char(char, next_char)
                if element.displayCommand != "":
                    ##  Skip double chars that tell the parser to perform a command ##
                    charIndex += 1

                line.append(element)

                ##  Increment our index and position    ##
                charIndex += 1

        #   Print the Matrix for debugging  #
        # for line in TextEngine.DIALOGUE:
        #     for c in line:
        #         print(c.text, end=" ")
        #     print()


    def draw(boxPos, screen):
        """
        (1) Blit the box on the screen at the desired position
        (2) Display all necessary dialogue elements,
        loop through
        the dialogue matrix and display each character
        that needs to be displayed.
        """

        #   (Case 0) The engine is finished; we draw nothing
        if TextEngine.finished():
            return
        
        #   Otherwise we always draw the box    #
        screen.blit(TextEngine.BOX, vec(0,0))


        #   (Case 1) We're closing, so we do nothing else
        if TextEngine.closing():
            return
        
        #   (Case 2) We're at the end of the dialogue or awaiting input
        if TextEngine.atEnd() or TextEngine.waiting():
            #   Display the input icon  #
            TextEngine.drawCursor()
            
            #   And there's no more chars to display for now, so we return  #
            return
        
        #   (2) Blit the next char to the box #
        TextEngine.displayChars()

        return
    

    def displayChars():
        #   Wait if buffering   #
        if TextEngine.BUFFER < 0.0:
            return

        #   Draw the next character to display and buffer   #
        ##  Obtain the current char ##
        line = TextEngine.CURRENT_LINE
        index = TextEngine.CURRENT_INDEX
        char = TextEngine.DIALOGUE[line][index]

        ##  To Next Line or Done Entirely ##
        if char.text == "\n":
            TextEngine.CURRENT_LINE += 1
            TextEngine.CURRENT_INDEX = 0

            if TextEngine.CURRENT_LINE >= len(TextEngine.DIALOGUE):
                ##  End of this dialogue box  ##
                TextEngine.STATES["end"] = True
            else:
                TextEngine.DISPLAY_POS[1] += TextEngine.SPACING * 2
                TextEngine.DISPLAY_POS[0] = 4

            return


        ##  Perform the char's displayCommand if needed ##
        command = char.displayCommand
        if command == "": # Just display the char
            TextEngine.display(char.image)
            #   ^^ Eventually this will just be a visibility toggle ^^  #
        
        else:
            ##  Which command is it?    ##
            if command == "clear":
                ##  Reset Display Pos   ##
                TextEngine.DISPLAY_POS = vec(4, 0) # y is 0 because the \n will increment it during parsing
                
                ##  Wait for input  ##
                TextEngine.STATES["ready_to_continue"] = True
                TextEngine.STATES["$$"] = True

                ##  Disable the interact action to force player to lift their finger    ##
                EventManager.getInstance().disableAction("interact")

            elif command == "wait":
                pass
            
            elif command == "buffer":
                TextEngine.BUFFER = -0.4
        

        ##  Decrease the buffer ##
        TextEngine.BUFFER = -0.1
        
        ##  Increase the index  ##
        TextEngine.CURRENT_INDEX += 1




    """
    Helper Funcs for the drawing process
    """
    def display(image):
        """Helper func for the displayChars()"""

        playSfx("text_3.wav")
        TextEngine.DISPLAY_POS[0] += TextEngine.SPACING
        TextEngine.BOX.blit(image, TextEngine.DISPLAY_POS)


    def drawCursor(self, drawSurf):
            """
            Draws the cursor when waiting
            for input from the player.
            Cursor depends on the box type.
            """
            #   (1.) Draw the cursor onto the screen
            ##  Interact Icon stays stationary
            drawSurf.blit(IconManager.getButton("interact"), (0,0))
            
            ##  Arrow moves up and down
            drawSurf.blit(TextEngine.CURSOR.image, (0,0) + TextEngine.CURSOR.y)
    

    """
    Handling Events
    """
    def handleEvent():
        #   (Case x) Waiting for Input  #
        if TextEngine.waiting():

            #   Progress the dialogue   #
            if EventManager.getInstance().performAction("interact"):
                ##  Trigger shutdown sequence if at the end  ##
                if TextEngine.atEnd():
                    pass

                ##  Clear the box if clearing   ##
                elif TextEngine.clearing():
                    playSfx("text_next1.wav")
                    TextEngine.STATES["ready_to_continue"] = False
                    TextEngine.STATES["closing"] = True
                
                ##  Continue the display otherwise  ##
                else:
                    playSfx("text_next1.wav")
                    TextEngine.STATES["ready_to_continue"] = False

        else:
            #   Speed up text display   #
            if EventManager.getInstance().isPressed("interact"):
                TextEngine.BUFFER = 0.0
    


    """
    Updating / Animating
    """
    def updateBuffer(seconds):
        if TextEngine.BUFFER < 0.0:
            TextEngine.BUFFER += seconds
        
    def update(seconds):
        TextEngine.updateBuffer(seconds)

        #   (Case 1) Startup    #



        #   (Case 2) Closing    #
        if TextEngine.closing():
            if TextEngine.TYPE == 4:
                #   Make the box increasingly more transparent  #
                TextEngine.BOX.set_alpha(TextEngine.A)
                TextEngine.A -= 10


                #   Once completely transparent #
                if TextEngine.A <= 0:
                    ##  Reset transparency alpha    ##
                    TextEngine.A = 255

                    ##  Reset clearing state    ##
                    if TextEngine.clearing():
                        TextEngine.STATES["$$"] = False
                        TextEngine.STATES["closing"] = False
                        TextEngine.BOX = pygame.surface.Surface(vec(304,208))
                    
                    ##  Reset closing state ##
                    else:
                        TextEngine.STATES["closing"] = False
                        TextEngine.STATES["done"] = True
        
        
        #   (Case 3) Waiting for input  #
        elif TextEngine.waiting():
            TextEngine.CURSOR.update(seconds)

        return
        #   Animate each of the characters in the dialogue box  #
        for line in TextEngine.DIALOGUE:
            for char in line:
                char.update(seconds)
