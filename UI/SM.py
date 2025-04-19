import gc
from gameObjects import PauseEngine, TextEngine, HudImageManager
from UI import ACTIONS, EventManager
from rooms import *

from utils import SoundManager
from . import TextEntry, EventMenu

from utils import vec, RESOLUTION

from utils.load import LOAD

from pygame import Surface
from pygame.locals import *

import os

"""
Original ScreenManager written by Dr. Liz Matthews.
Modified by Trey Custodio 1/23/2025
"""
class ScreenManager(object):
    def __init__(self):

        #   Start the music on opening the game
        self.playTheme()

        #   Initialize the Hud Manager
        HudImageManager.initialize()

        #   Controller data
        self.controller = "key"
        self.controllerSet = False
        self.inIntro = False

        #   Engines
        self.game = None
        self.pauseEngine = PauseEngine() # This will be rewrittem
        self.state = "mainMenu"

        #   States
        self.startingGame = False
        self.continuingGame = False
        self.returningToMain = False

        #  Fade control
        self.fade = Fade.getInstance()
        self.white = WhiteOut()
        self.fade.setRow(1)
        self.fade.setFrame(8)
        self.fading = False
        self.fadingIn = False
        self.wipe = Wipe() # only 1 instantiated
        
        #   Screen Geometry
        # midpoint = RESOLUTION // 2 - size

        #   Title Screen
        self.titleTimer = 0.0
        self.mainMenu = EventMenu("title_screen.png", fontName="zelda")

        self.mainMenu.addOption("start", "New Game",
                                RESOLUTION // 2 + vec(0,5),
                                center="both")
        
        self.mainMenu.addOption("continue", "Continue",
                                RESOLUTION // 2 + vec(0,50),
                                center="both")
        
        self.mainMenu.addOption("quit", "Quit",
                                RESOLUTION // 2 + vec(0,90),
                                center="both")
        

    """
    (1.) Auxillary ---------------------------------
    """                    
    def playTheme(self):
        """
        Play the title theme.
        """
        SoundManager.getInstance().playBGM("Fontaines.mp3")

    
    def setController(self, text):
        """
        Set the controller
        """
        self.controller = text


    def fadeOn(self, speed: int = 1):
        """
        Fade screen to black.
        Param: speed = the number you increase
        the black alpha value by each frame.
        """
        self.wipe.increase(speed)
    
    
    def fadeOff(self, speed: int = 1):
        """
        Fade the screen in from black.
        Param: speed = the number you decrease
        the black alpha value by each frame
        """
        self.wipe.decrease(speed)
    
    
    def drawWipe(self, drawSurf):
        """
        Draw the screen wipe (black image).
        """
        self.wipe.draw(drawSurf)
    
    
    def setWipe(self, image: Surface):
        """
        Change the wipe's image.
        """
        pass


    """
    (2.) Drawing -----------------------------------
    """ 
    