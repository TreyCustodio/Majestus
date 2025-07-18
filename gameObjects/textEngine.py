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


def playSfx(effect="", low = False):
    """Here's a useful playSfx() function"""
    if low:
        SoundManager.getInstance().playLowSFX(effect, 0.02)
    
    else:   
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
    """
    This class represents characters to be appended
    to the dialogue matrix.
    Chars contain values that specify how to
    display them. Certain Chars call upon special effetcs,
    which are handled in parse().
    """

    def __init__(self, char="", next_char=None):

        #   (1) Parse the char; get any potential color changes and display commands    #
        color, self.displayCommand, sound = self.parse(char, next_char)
        self.color = color # Keep track of the color for the index display
        self.sound = sound # Keep track of the sound


        #   (2) Get the image from chars.png    #
        self.image = self.getImage(char)


        #   (3) Set the visibility value    #
        self.visible = False


        #   (4) Set the text value for debugging    #
        self.text = char


        #   (5) Set the spacing value   #
        #   ASSUMING OPEN-SANS  #
        #   Letters taking up more space    #
        if char == 'm' or char == "W" or char == "M":
            self.spacing = 4
        
        elif char == 'w':
            self.spacing = 3

        elif char == "D" or char == "U"or char == "N":
            self.spacing = 1
        

        #   Letters taking up less space    #
        elif char == "i" or char == "I" or char == "l" or char == "'" or char in "()":
            self.spacing = -4
        
        elif char == "t" or char == "f" or char == "J" or char == "j":
            self.spacing = -3
        
        elif char == "r" or char == "1":
            self.spacing = -2
        
        elif char == "c" or char == "y" or char == "s":
            self.spacing = -1


        #   Default to 0
        else:
            self.spacing = 0


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
        sound = Text.SOUND
        speaker = Text.SPEAKER

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

                    elif next_char == "0":
                        color = (0,0,0)
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
                
            
            #   $ -> For Portraying Emotional Sounds and Clearing #
            elif char == "$":
                ##  $$ -> Clear the box  ##
                if next_char == "$":
                    displayCommand = "clear"
                
                ##  $s -> Sad sound ##
                elif next_char == 's':
                    sound = speaker + "sad1.wav"
                    displayCommand = "sound"

                ##  $s -> Sad sound ##
                elif next_char == 'a':
                    sound = speaker + "angry1.wav"
                    displayCommand = "sound"

                ##  $_ -> No sound  ##
                elif next_char == '_':
                    sound = ""
                    displayCommand = "sound"

                ##  $~ -> End sound section ##
                elif next_char == '~':
                    sound = speaker +"2.wav"
                    displayCommand = "sound"
            


            #   & -> For different input commands   #
            elif char == "&":
                ##   && -> Wait for input    ##
                if next_char == "&":
                    displayCommand = "wait"
                

            #   , -> For controlling the display buffer  #
            elif char == ",":

                ##  ,, -> buffer -= 0.2 ##
                if next_char == ",":
                    displayCommand = "buff_short"
                
                ##  ,. -> buffer -= 0.8 ##
                elif next_char == ".":
                    displayCommand = "buff_long"
                
                ##  ,* -> ignore the buffer; instantly display text ##
                elif next_char == "*":
                    displayCommand = "instant"
                
                ##  ,~ -> reset the buffer effects  ##
                elif next_char == "~":
                    displayCommand = "buff_reset"
                
                ##  Any other char following ',' tells the engine to display the ','    ##
                else:
                    pass

            else:
                pass
        
        #   Set the values for Text!
        Text.COLOR = color
        Text.SOUND = sound

        #   Set values for text based on displayCommand
        
        return color, displayCommand, sound
    
    
    def setVisible(self, value=True):
        self.visible = value


    def update(self, seconds):
        return


class Text(object):
    """
    A static Text Utility class.
    The class variables in this class are used
    to display special effects when displaying dialogue.
    Char.parse() will change this class's variables.
    """

    #   Initialize pygame fonts if not already done #
    if not pygame.font.get_init():
        pygame.font.init()


    #   Metadata about fonts, we'll use ALTTP font for now.
    FONT_FOLDER = "fonts"
    FONT = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "ReturnofGanon.ttf"), 16)
    
    FONT = pygame.font.Font(os.path.join(FONT_FOLDER,
                                    "OpenSans-Regular.ttf"), 12)
    
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


    #   The current sound   #
    SOUND = "text_2.wav"


    #   The current speaker #
    SPEAKER = "text_"


    #   Display the chars instantly?    #
    INSTANT = False


class TextEngine(object):
    """
    ------------------- PURPOSE ----------------------------

    This class is never instantiated, but it is
    called upon and referenced when text needs to be displayed.
    
    
    -------------- TEXT DISPLAY PROCESS --------------------

    (0) TextEngine is initialized with setText(text, icon).

    (1) Build the dialogue matrix,
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

    
    -------------- MEMORY CONCERNS -------------------------
    I believe this structure is fine, but it should be
    noted that every single CLASS VARIABLE will persist
    in memory as long as the program is running.

    I am thinking about switching to a singleton framework,
    where the reset function will free up memory for every single
    CLASS VARIABLE (which would be converted into instance variables for the singleton),
    by setting them all = None, allowing the GC to collect it.

    However, the only variable that contains large data is
    the DIALOGUE. Reinstantiating variables like STATES, TICKERS, BUFFERS, etc.
    just seems overtly redundant. Therefore, I believe keeping this class a static class
    is fine under the condition that DIALOUGE is set to [] in the reset() function.

    TLDR: I'm considering making this a singleton, but it's
    fine as is as long as I set DIALOGUE = [] in reset().
    """

    #   Initialization Data   #
    DIALOGUE = []     # Dialogue Matrix
    TYPE = 0            # Box type
    PROMPT = False      # Is there a Y/N prompt?
    ICON = None         # Icon Image
    BOX = None          # Box Image
    DISPLAY_POS = vec(4, 4) # The text display pos relevant to the box


    #   Character Display   #
    SPACING = 8        # num of pixels to seperate each char image by
    BUFFER = -0.2       # timer that drives the buffer time between each character that is displayed
    CURRENT_LINE = 0    # the current line to examine for displayChars()
    CURRENT_INDEX = 0   # the current index to examine for displayChars()
    A = 255             # transparency alpha value
    CURSOR = None       # Text cursor; indicates input
    INDEX_IMAGE = None  # Index Image; moves as each character is displayed
    INPUT_TICK = 0
    SOUND_TICK = 0


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
        TextEngine.BUFFER = -0.2
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
            TextEngine.BOX = pygame.surface.Surface(vec(304,208), pygame.SRCALPHA)
            TextEngine.BOX.fill((0,0,0,0))

            # black_surf = pygame.surface.Surface((vec(196, 128)), pygame.SRCALPHA)
            # black_surf.fill((0,0,0,200))
            # TextEngine.BOX.blit(black_surf, vec(64,32))
        
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
        TextEngine.CURSOR = TextCursor()
        TextEngine.INDEX_IMAGE = pygame.transform.scale(SpriteManager.getInstance().getSprite("white_px.png"), (6,20))

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
            if charIndex >= len(text) :
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
            TextEngine.drawCursor(screen)
            
            #   And there's no more chars to display for now, so we return  #
            return
        
        #   (2) Blit the next char to the box #
        TextEngine.displayChars()
        TextEngine.drawIndex(screen)

        return
    

    def displayRoutine(silent=False):
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
                playSfx("text_done1.wav")
                TextEngine.STATES["end"] = True
                TextEngine.STATES["ready_to_continue"] = True

                ##  Disable the interact action to force player to lift their finger    ##
                EventManager.getInstance().disableAction("interact")

            else:
                TextEngine.DISPLAY_POS[1] += TextEngine.SPACING * 2
                TextEngine.DISPLAY_POS[0] = 4

            return


        ##  Perform the char's displayCommand if needed ##
        command = char.displayCommand
        if command == "": # Just display the char
            TextEngine.display(char.image, char.sound, silent, char.spacing)
            #   ^^ Eventually this will just be a visibility toggle ^^  #
        
        else:
            ##  Which command is it?    ##
            if command == "clear":                
                ##  Wait for input; then clear the box  ##
                TextEngine.STATES["ready_to_continue"] = True
                TextEngine.STATES["$$"] = True

                ##  Disable the interact action to force player to lift their finger    ##
                EventManager.getInstance().disableAction("interact")

            elif command == "wait":
                ##  Wait for input  ##
                TextEngine.STATES["ready_to_continue"] = True

                ##  Disable the interact action to force player to lift their finger    ##
                EventManager.getInstance().disableAction("interact")
                
            elif command == "buff_short":
                TextEngine.BUFFER = -0.4
            
            elif command == "buff_long":
                TextEngine.BUFFER = -0.8

            elif command == "instant":
                Text.INSTANT = True
            
            elif command == "buff_reset":
                Text.INSTANT = False
                TextEngine.BUFFER = -1.2
        

        ##  Decrease the buffer ##
        TextEngine.BUFFER = -0.1
        
        ##  Increase the index  ##
        TextEngine.CURRENT_INDEX += 1



    def displayChars():
        #   Instantly display chars
        if Text.INSTANT:
            while Text.INSTANT:
                TextEngine.displayRoutine(silent=True)
            return

        #   Wait if buffering   #
        elif TextEngine.BUFFER < 0.0:
            return
        
        #   Perform the usuual routine  #
        TextEngine.displayRoutine()



    """
    Helper Funcs for the drawing process
    """
    def getCurrentChar():
        line = TextEngine.CURRENT_LINE
        index = TextEngine.CURRENT_INDEX
        char = TextEngine.DIALOGUE[line][index]

        return char
    
    def display(image, sound="text_2.wav", silent=False, spacing=0):
        """Helper func for the displayChars()"""
        if not silent and sound != "":
            if EventManager.getInstance().isPressed("interact"):
                if TextEngine.SOUND_TICK == 1 or TextEngine.SOUND_TICK == 4 or TextEngine.SOUND_TICK == 7:
                    playSfx(sound)
            else:
                playSfx(sound)

        TextEngine.DISPLAY_POS[0] += TextEngine.SPACING
        TextEngine.BOX.blit(image, TextEngine.DISPLAY_POS)
        TextEngine.DISPLAY_POS[0] += spacing


    def drawIndex(drawSurf):
            #   (1.) Get the color value from dialogue arr
            try:
                char = TextEngine.getCurrentChar()
            except:
                return
            
            color = char.color
            
            index = TextEngine.INDEX_IMAGE

            #   (2.) Set the color of the index image
            if color == "default":
                index.fill((255,255,200))

            else:
                index.fill(color)


            #   (3.) Display the index image; flashing when buffering
            if TextEngine.TYPE == 4:
                # if TextEngine.BUFFER < 0.0:
                #     ##  Draw
                #     if TextEngine.INPUT_TICK < 17:
                #         drawSurf.blit(index, TextEngine.DISPLAY_POS + vec(TextEngine.SPACING, 0))

                # else:
                drawSurf.blit(index, TextEngine.DISPLAY_POS + vec(TextEngine.SPACING, 0))

    def drawCursor(drawSurf):
            """
            Draws the cursor when waiting
            for input from the player.
            Cursor depends on the box type.
            """
            #   (1.) Draw the cursor onto the screen
            ##  Interact Icon stays stationary
            drawSurf.blit(IconManager.getButton("interact"), TextEngine.DISPLAY_POS + vec(TextEngine.SPACING, 14 - 2))
            
            ##  Arrow moves up and down
            drawSurf.blit(TextEngine.CURSOR.image, TextEngine.DISPLAY_POS + vec(TextEngine.SPACING, TextEngine.CURSOR.y - 2))
    

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
                    ### Reset the Display Pos   ###
                    TextEngine.DISPLAY_POS = vec(4, -4) # y is 0 because the \n will increment it during parsing
                    
                    ### Play the continue sfx   ###
                    playSfx("text_close1.wav")

                    ### Reset relevant states   ###
                    TextEngine.STATES["ready_to_continue"] = False
                    TextEngine.STATES["closing"] = True

                ##  Clear the box if clearing   ##
                elif TextEngine.clearing():
                    ### Reset the Display Pos   ###
                    TextEngine.DISPLAY_POS = vec(4, -4) # y is 0 because the \n will increment it during parsing
                    
                    ### Play the continue sfx   ###
                    playSfx("text_next1.wav")

                    ### Reset relevant states   ###
                    TextEngine.STATES["ready_to_continue"] = False
                    TextEngine.STATES["closing"] = True
                
                ##  Continue the display otherwise  ##
                else:
                    playSfx("text_next1.wav")
                    TextEngine.STATES["ready_to_continue"] = False

                    ##  Wait a little bit before displaying again   ##
                    TextEngine.BUFFER = -0.4

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
                    elif TextEngine.atEnd():
                        TextEngine.STATES["closing"] = False
                        TextEngine.STATES["done"] = True
        
        
        #   (Case 3) Waiting for input  #
        elif TextEngine.waiting():
            TextEngine.CURSOR.update(seconds)
            

        #   (Case x) Other Animations   #
        else:
            TextEngine.INPUT_TICK += 1
            TextEngine.INPUT_TICK %= 20
            if EventManager.getInstance().isPressed("interact"):
                TextEngine.SOUND_TICK += 1
                TextEngine.SOUND_TICK %= 10
            else:
                TextEngine.SOUND_TICK = 0

            pass

        return
        #   Animate each of the characters in the dialogue box  #
        for line in TextEngine.DIALOGUE:
            for char in line:
                char.update(seconds)
