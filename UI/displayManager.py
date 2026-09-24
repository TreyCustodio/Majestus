import gc
from gameObjects import PauseEngine, TextEngine
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
Modified DisplayManager class written by Trey Custodio 1/23/2025
"""
class DisplayManager(object):
    """Manage the display of the game"""
    def __init__(self):

        #   Start the music
        self.playTheme()

        #   Initialize the Hud Manager

        #   Controller data
        self.controller = "key"
        self.controllerSet = False
        self.inIntro = False

        #   Engines
        self.game = None
        #self.mobsterEngine = MobsterEngine()
        self.pauseEngine = PauseEngine()
        #self.textEngine = TextEngine.getInstance()
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
        self.mainMenu = EventMenu("title_screen_m.png", fontName="zelda")

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
        SoundManager.getInstance().play_ost("01", has_intro=False)

    
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
    
    
    def draw_wipe(self, drawSurf):
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
    def drawText(self, drawSurf):
        #   (Case 1) The Current Dialogue is Over. Return to the previous state. #
        if TextEngine.finished():

            #   Return to being Paused  #
            if self.pauseEngine.paused:

                ##   Evaluate Prompts like using items in the menu   ##
                if "Y/N" in self.pauseEngine.text:
                    self.pauseEngine.promptResult = self.textEngine.promptResult
                    if self.pauseEngine.promptResult:
                        if self.pauseEngine.promptFlag == "potion":
                            INV["potion"] -= 1
                            self.game.healPlayer(3)
                        
                        elif self.pauseEngine.promptFlag == "smoothie":
                            INV["smoothie"] -= 1
                            self.game.healPlayer(6)
                        
                        elif self.pauseEngine.promptFlag == "beer":
                            INV["beer"] -= 1
                            self.game.drink()
                        
                        elif self.pauseEngine.promptFlag == "joint":
                            INV["joint"] -= 1
                            self.game.see()
                        
                        elif self.pauseEngine.promptFlag == "speed":
                            INV["speed"] -= 1
                            self.game.zoom()

                        elif self.pauseEngine.promptFlag == "syringe":
                            self.game.useSyringe()
                        
                        elif self.pauseEngine.promptFlag == "quit":
                            SoundManager.getInstance().fadeout_bgm()
                            self.returningToMain = True
                            self.fadeOn(5)
                            #self.fading = True
                            #self.fade.setRow(1)             
                            
                    
                ##  Reset pause engine text states; Go back to being paused  ##
                self.pauseEngine.textBox = False
                self.pauseEngine.text = ""
                self.state = "paused"


            #   Return to Intro   #
            elif self.inIntro:
                self.game.speaking = False
                self.game.text = ""
                self.game.icon = None
                if self.game.textInt == 6:
                    self.game.fading = True
                self.state = "game"


            #   Return to Game  #
            else:
                ##  Evaluate Prompts    ##
                if "Y/N" in self.game.text:
                    self.game.promptResult = self.textEngine.promptResult
                
                ##  Reset gameEngine's text states  ##
                self.game.stop_dialogue()
                self.state = "game"


            #   Finally, Reset the textEngine
            TextEngine.reset()
            return



        #   (Case 2) Display Text on the pause menu #
        if self.pauseEngine.paused:
            if self.textEngine.closing:
                self.drawGame(drawSurf)
                self.drawPause(drawSurf)

            elif self.textEngine.backgroundBool:
                self.drawGame(drawSurf)
                self.drawPause(drawSurf)
                self.textEngine.setBackgroundBool()
            self.textEngine.draw(self.pauseEngine.boxPos + Drawable.CAMERA_OFFSET, drawSurf)



        #   (Case 3) Display Text during the Intro cutscene #
        # elif self.inIntro:
        #     #   Draw the intro background while the text display is closing #
        #     # if self.textEngine.closing:
        #     #     self.intro.draw(drawSurf)

        #     #   Draw the intro background when prompted to do so    #
        #     # elif self.textEngine.backgroundBool:
        #     #     self.drawGame(drawSurf)
        #     #     self.textEngine.setBackgroundBool()

        #     #   Perform the TextEngine's draw routine   #
        #     TextEngine.draw(self.intro.boxPos, drawSurf)



        #   (Case 4) Display Text during gameplay   #
        else:
            #   Draw the game ONCE after the textbox finishes upscaling #
            if TextEngine.closing():
                self.drawGame(drawSurf)

            #   Draw the game if prompted to do so  #
            elif TextEngine.backgroundBool():
                self.drawGame(drawSurf, True)
                TextEngine.setBackgroundBool()

            #   Draw the game once more #
            self.drawGame(drawSurf)

            #   Perform the TextEngine's draw routine   #
            TextEngine.draw(self.game.box_pos, drawSurf)

    
    def drawGame(self, drawSurf, drawBox = False):
        if drawBox:
            if self.textEngine.type == 1:
                self.game.draw(drawSurf)
            else:
                self.game.drawText(drawSurf)
        else:
            self.game.draw(drawSurf)
    
    def drawPause(self, drawSurf):
        self.pauseEngine.draw(drawSurf)

    def draw_title(self, drawSurf):
        if self.mainMenu.initialized:
            self.mainMenu.draw(drawSurf)
            
        else:
            self.mainMenu.drawText(drawSurf)
            

        if self.startingGame or self.continuingGame or self.returningToMain:
            return
    

    def draw_fps(self, drawSurf, fps):
        """Draw the current FPS"""
        text = Text(vec(*(RESOLUTION - 16)), str(fps))
        text.draw(drawSurf)


    def draw(self, drawSurf):
        """
        Drawing the game based on the state
        """
        #   (1) Main Menu   #
        if self.state == "mainMenu":
            self.draw_title(drawSurf)

        #   (2) Playing the game  #
        elif self.state == "game":
            #   Perform the gameEngine's draw routine   #
            self.game.draw(drawSurf)

            #   Initiate the TextEngine when prompted   #
            if self.game.speaking:
                self.state = "textBox"
                if "Y/N" in self.game.text:
                    TextEngine.set_text(self.game.text, self.game.icon, prompt = True)
                else:
                    TextEngine.set_text(self.game.text, self.game.icon, type = self.game.boxType, cube_state=self.game.cube_state)

            #   Draw transition effects (fade outs, white outs, etc.)   #
            if self.game.whiting:
                self.white.draw(drawSurf)


        #   (3) Paused  #
        elif self.state == "paused":

            #   Resume Gameplay #
            if self.pauseEngine.closed:
                self.pauseEngine.resetMenu()
                self.state = "game"
                return
            
            #   Transition to settings menu #
            if self.pauseEngine.toSettings:
                if self.wipe.alpha >= 255:
                    self.pauseEngine.fadeIn()
                    self.fadeOff(20)
                    self.pauseEngine.inSettings = True
                    self.pauseEngine.toSettings = False
                else:
                    self.fadeOff(10)

            #   Transition to inventory #
            elif self.pauseEngine.inSettings and self.pauseEngine.toInventory:
                self.fadeOff(10)

            #   Draw the game behind the menu   #
            self.game.draw(drawSurf)
            

            #   Initiate the TextEngine #
            if self.pauseEngine.text != "":
                self.state = "textBox"

                ##  Handle Prompts  ##
                if "Y/N" in self.pauseEngine.text:
                    self.textEngine.set_text(self.pauseEngine.text, prompt = True, type = 1)
                    
                else:
                    self.textEngine.set_text(self.pauseEngine.text, type = 3)
            
            #   Draw the menu overtop everything    #
            self.pauseEngine.draw(drawSurf)


        elif self.state == "textBox":
            self.drawText(drawSurf)

        #   (4) In a special cutscene    #
        elif self.state == "cutscene":
            #   Start the music if not already playing  #
            if not self.intro.playingBgm:
                self.intro.playBgm()

            #   Perform the intro's draw routine    #
            self.intro.draw(drawSurf)

            #   Transition to dialogue state; Initiate the TextEngine   #
            if self.intro.textBox:
                self.state = "textBox"
                TextEngine.set_text(self.intro.text, icon = None, prompt = False, type = 4)

        #   (5) Playing Monster Mobster  #
        elif self.state == "mobster":
            self.mobsterEngine.draw(drawSurf)

        #    Draw the Wipe   #
        self.draw_wipe(drawSurf)
        
    """
    (3.) Handling Events ------------------------------
    """
    def pause(self):
        """
        Pause the game.
        Open the pause screen.
        """
        self.game.player.stop()
        SoundManager.getInstance().playSFX("OOT_PauseMenu_Open.wav")
        self.state = "paused"
        #self.state.pause()
    
    def openMap(self):
        """
        Open the map.
        """
        self.game.player.stop()
        SoundManager.getInstance().playSFX("OOT_PauseMenu_Open.wav")
        Map.getInstance().updateHighlight()
        #self.state.pause()
        self.state = "paused"
        self.pauseEngine.mapOpen = True

    def handleChoice(self, choice):
        """
        Handle choice of title screen
        selection.
        """
        self.fade.setFrame(0)
        if choice == 0:
            # SoundManager.getInstance().fadeout_bgm()
            SoundManager.getInstance().playSFX("WW_PressStart.wav")
            self.startingGame = True
            self.fadeOn(4)


        elif choice == 1:
            SoundManager.getInstance().fadeout_bgm()
            self.continuingGame = True
            self.fadeOn(4)
            
        elif choice == 2:
            return pygame.quit()
        
    
    def handle_events(self):
        """
        Decide whether to have the
        other engines handle events or not.
        """
        if self.state == "game":
            if EventManager.getInstance().performAction("pause"):
                self.state = "paused"
                self.paused_events()
                return
            
            self.game.handle_events()

        elif self.state == "paused":
            if self.returningToMain:
                return
            self.paused_events()
                
        elif self.state == "mainMenu":
            if self.mainMenu.readyToDisplay:
                if not self.fadingIn and not self.continuingGame and not self.startingGame:
                    self.mainMenu.handleEvent()
                    if EventManager.getInstance().performAction("interact"):
                        choice = self.mainMenu.getChoice()
                        self.handleChoice(choice)

        elif self.state == "textBox":
            TextEngine.handleEvent()

        elif self.state == "mobster":
            self.mobsterEngine.handleEvent()


    def paused_events(self):
        if EventManager.getInstance().performAction("map"):
            pygame.display.toggle_fullscreen()

        elif not self.pauseEngine.closing and EventManager.getInstance().performAction("pause"):
            self.pauseEngine.paused = False
            self.pauseEngine.closing = True
            SoundManager.getInstance().playSFX("OOT_PauseMenu_Close.wav")
            self.pauseEngine.mapOpen = False

        else:
            self.pauseEngine.handleEvent()
            ##  Paused -> TextBox
            if self.pauseEngine.text != "":
                self.state = "textBox"
                #self.state.speakP()
                if "Y/N" in self.pauseEngine.text:
                    self.textEngine.set_text(self.pauseEngine.text, prompt = True)
                else:
                    self.textEngine.set_text(self.pauseEngine.text)

    def handle_collision(self):
        """
        Decide whether to have the
        game engine handle collision or not.
        """
        return
        if self.state == "game":
            self.game.handleCollision()
    
    
    """
    (4.) Updating --------------------------------
    """
    def transition(self):
        """
        Transition to another room.
        Move from one game engine to another.

        Runs Twice -> but why?
        """
        self.fading = True
        self.fadeOff(15)
        pos = self.game.tra_pos
        player = self.game.player
        keepBGM = self.game.tra_keepBGM
        room = self.game.tra_room

        #   Reset the previous room #
        self.game.reset()
        gc.collect()
        self.fadingIn = True
        self.fade.frame = 9

        #   Finish the transition and load the next room    #
        if issubclass(room, MajestusEngine):
            self.game = room()
            self.game.initialize_room(player, pos, keepBGM)
        else:
            self.game = room.getInstance()
            self.game.initializeRoom(player, pos, keepBGM)


        # if not self.game.transporting_area:
        #     self.game.reset()
        #     gc.collect()
        #     self.game = newGame
        #     self.game.initializeRoom(player, pos, keepBGM)
        #     self.fadingIn = True
        #     self.fade.frame = 9
        # else:
        #     self.game.reset()
        #     gc.collect()
        #     self.game = newGame
        #     self.game.initializeArea(player, pos, keepBGM)

    
    def update(self, seconds):
        """
        Update all states.
        """
        #   (1.) Update the screen wipe
        self.wipe.update(seconds)


        #   (2.) Update the room
        if self.state == "game":
            #   Quit to Title   #
            if self.returningToMain:
                if self.wipe.increasing == False:
                    self.fadeOff(20)
                    self.state = "mainMenu"
                    #self.state.toMain()
                    self.fadingIn = True
                return
            
            #   Death   #
            elif self.game.dead:
                self.wipe.setColor((255,0,0))
                self.fadeOn(5)
                self.fading = True
                self.returningToMain = True
                return

            #   Transition  #
            if self.game.readyToTransition:
                self.transition()

            #   Fading Out  #
            elif self.game.fading:
                if not self.fading:
                    self.fadeOn(15)
                    self.fading = True

            else:
                self.game.update(seconds)

        #   (3.) Update the textbox
        elif self.state == "textBox":
            TextEngine.update(seconds)
            if self.game.cutscene:
                self.game.update(seconds)
            else:
                self.game.update(seconds, update_enemies=False, update_weapons = False)


        #   (4.) Update the pause screen
        elif self.state == "paused":
            self.pauseEngine.update(seconds)
            # if self.game.getHealthBarDrawing():
                # self.game.updateHealthBar(seconds)
            
            if self.returningToMain:
                if self.wipe.increasing == False:
                    self.fadeOff(20)
                    self.state = "mainMenu"
                    #self.state.toMain()
                    self.fading = True
                    self.fadingIn = True
        

        #   (5.) Update the title screen
        elif self.state == "mainMenu":
            #   (i.) Update / Animate
            self.mainMenu.update(seconds)
            
            #   (ii.) Starting a new game
            if self.startingGame:
                if self.wipe.increasing == False:
                    self.fadeOff(5)
                    self.game = Intro_Cut.getInstance()
                    self.game.lockHealth()
                    self.state = "game"
                    self.startingGame = False
                    self.inIntro = True
                    # self.state.startGame()

            
                    
            #   (iii.) Continuing a game
            elif self.continuingGame:
                if self.wipe.increasing == False:
                    #   Continue the game after the sound effects are done  #
                    self.fadeOff(5)
                    room = LOAD["room"]
                    if issubclass(room, MajestusEngine):
                        self.game = room()
                        self.game.initialize_room(position=(LOAD["position"]))
                    else:
                        self.game = room.getInstance()
                        self.game.initializeRoom(pos=(LOAD["position"]))
                    
                    # self.game = LOAD["room"]()
                    # if LOAD["area"]:
                    #     self.game.initialize_area(position=LOAD["position"])
                    # else:
                    #     if issubclass(self.game, MajestusEngine):
                    #         self.game.initialize_room(position=(LOAD["position"]))
                    #     else:
                    #         self.game.initializeRoom(position=(LOAD["position"]))

                    self.state = "game"
                    #self.state.startGame()
                    self.continuingGame = False
                    # self.game.stopFadeIn()
                    return

        #   (6.) Update monster mobster
        elif self.state == "mobster":
            self.mobsterEngine.update(seconds)
        
        #   (7.) Update the wipe
        if self.fading:
            if self.fadingIn:
                if self.wipe.decreasing == False:
                    self.fading = False
                    self.fadingIn = False
                    if self.state == "game":
                        if self.continuingGame:
                            self.fade.setRow()
                            self.continuingGame = False
                            self.game.unlockHealth()
                        self.game.stopFadeIn()
                    elif self.state == "intro":
                        self.fade.setRow()
                        self.startingGame = False
                    elif self.state == "mainMenu":
                        if self.returningToMain:
                            self.wipe.setColor((0,0,0))
                            self.game.deathReset()
                            self.pauseEngine.resetMenu()
                            self.playTheme()
                            self.fade.setRow()
                            self.returningToMain = False 
            else:
                if self.game and self.game.transporting and self.wipe.increasing == False:
                    self.game.finish_fade()