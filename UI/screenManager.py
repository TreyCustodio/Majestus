from FSMs import ScreenManagerFSM
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


class ScreenManager(object):
      
    def __init__(self):
        self.playTheme()
        HudImageManager.initialize()
        self.controller = "key"
        self.controllerSet = False
        self.inIntro = False
        self.game = None # Add your game engine here!
        self.mobsterEngine = MobsterEngine()
        self.pauseEngine = PauseEngine()
        self.textEngine = TextEngine.getInstance()
        self.state = ScreenManagerFSM(self)
        self.pausedText = TextEntry(vec(0,0),"Paused")
        self.transparency = False #Boolean that activates the transparent surface

        ##  Main Menu transitioning states
        self.startingGame = False
        self.continuingGame = False
        self.returningToMain = False

        ##  Fade control
        self.fade = Fade.getInstance()
        self.white = WhiteOut()
        self.fade.setRow(1)
        self.fade.setFrame(8)
        self.fading = False
        self.fadingIn = False
        
        size = self.pausedText.getSize()
        midpoint = RESOLUTION // 2 - size
        self.pausedText.position = vec(*midpoint)

        self.displayTitle = False
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
        

                                    
    def playTheme(self):
        SoundManager.getInstance().playBGM("Fontaines.mp3")

    def setController(self, text):
        self.controller = text

    """
    Draw routine for textboxes.
    drawSurf -> specific surface for textboxes passed in by main.py
    """
    def drawText(self, drawSurf):
        if self.inIntro:
            #image = Drawable(self.boxPos, "TextBox2.png", (0,7))
            #image.draw(drawSurf)
            #self.intro.background.draw(drawSurf)

            if self.intro.textInt == 3:
                self.intro.light.draw(drawSurf)
                self.intro.dark.draw(drawSurf)

        ##TextEngine finished
        if self.textEngine.done:
            ##Paused
            if self.pauseEngine.paused:
                ##Evaluating prompts
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
                            SoundManager.getInstance().fadeoutBGM()
                            self.returningToMain = True
                            self.fading = True
                            self.fade.setRow(1)             
                            
                    
                ##Reset pause engine text states
                self.pauseEngine.textBox = False
                self.pauseEngine.text = ""
                self.state.speakP()
            ##Intro
            elif self.inIntro:
                self.intro.textBox = False
                self.intro.text = ""
                self.intro.icon = None
                if self.intro.textInt == 11:
                    self.intro.fading = True
                
                self.state.speakI()
            ##Game, evaluate prompt
            else:
                if "Y/N" in self.game.text:
                    self.game.promptResult = self.textEngine.promptResult
                self.game.textBox = False
                self.game.text = ""
                self.game.icon = None
                self.state.speak()
            #Reset
            self.textEngine.reset()
            return

        ##Paused
        if self.pauseEngine.paused:
            if self.textEngine.closing:
                self.drawGame(drawSurf)
                self.drawPause(drawSurf)
            elif self.textEngine.backgroundBool:
                self.drawGame(drawSurf)
                self.drawPause(drawSurf)
                self.textEngine.setBackgroundBool()
            self.textEngine.draw(self.pauseEngine.boxPos + Drawable.CAMERA_OFFSET, drawSurf)

        ##Intro
        elif self.inIntro:
            if self.textEngine.closing:
                self.intro.draw(drawSurf)
            elif self.textEngine.backgroundBool:
                self.drawGame(drawSurf)
                self.textEngine.setBackgroundBool()
            self.textEngine.draw(self.intro.boxPos, drawSurf)

        ##Draw the game ONCE after the textbox finishes the upscale
        ##Game
        else:
            if self.textEngine.closing:
                self.drawGame(drawSurf)
            elif self.textEngine.backgroundBool:
                self.drawGame(drawSurf, True)
                self.textEngine.setBackgroundBool()
            self.drawGame(drawSurf)
            self.textEngine.draw(self.game.boxPos, drawSurf)

    def drawGame(self, drawSurf, drawBox = False):
        if self.inIntro:
            if drawBox:
                self.intro.drawText(drawSurf)
            else:
                self.intro.draw(drawSurf)
        else:
            if drawBox:
                if self.textEngine.large:
                    self.game.drawText(drawSurf)
                else:
                    self.game.draw(drawSurf)
            else:
                self.game.draw(drawSurf)
    
    def drawPause(self, drawSurf):
        self.pauseEngine.draw(drawSurf)

    def drawTitle(self, drawSurf):
        if self.mainMenu.initialized:
            self.mainMenu.draw(drawSurf)
            if self.fadingIn:
                self.fade.draw(drawSurf)
        else:
            self.fade.draw(drawSurf)
            self.mainMenu.drawText(drawSurf)
            

        if self.startingGame or self.continuingGame or self.returningToMain:
            self.fade.draw(drawSurf)
            return
        
    #Displaying Text
    def draw(self, drawSurf):
        """
        Drawing the game based on the state
        """
        if self.state == "game":
            
            self.game.draw(drawSurf)
            if self.game.textBox:
                self.state.speak()
                if "Y/N" in self.game.text:
                    self.textEngine.setText(self.game.text, self.game.icon, prompt = True)
                else:
                    self.textEngine.setText(self.game.text, self.game.icon, self.game.largeText, type = self.game.boxType)

            if self.game.whiting:
                self.white.draw(drawSurf)
            if self.game.area_fading:
                self.game.drawArea(drawSurf)


        elif self.state == "paused":
            if self.pauseEngine.closed:
                self.pauseEngine.resetMenu()
                self.state.pause()
                return
            self.game.draw(drawSurf)
            

            if self.pauseEngine.text != "":
                self.state.speakP()
                #self.textEngine = TextEngine.getInstance()
                if "Y/N" in self.pauseEngine.text:
                    self.textEngine.setText(self.pauseEngine.text, prompt = True)
                    
                else:
                    self.textEngine.setText(self.pauseEngine.text)
            self.pauseEngine.draw(drawSurf)

        elif self.state == "intro":
            if not self.intro.playingBgm:
                self.intro.playBgm()
            self.intro.draw(drawSurf)
            if self.intro.textBox:
                self.state.speakI()
                self.textEngine.setText(self.intro.text, self.intro.icon, self.intro.largeText)

        elif self.state == "mobster":
            self.mobsterEngine.draw(drawSurf)

        if self.fading or self.returningToMain:
            self.fade.draw(drawSurf)
            return
        
    
    """
    Handling Events
    """
    def pause(self):
        self.game.player.stop()
        SoundManager.getInstance().playSFX("OOT_PauseMenu_Open.wav")
        Map.getInstance().updateHighlight()
        self.state.pause()
    
    def openMap(self):
        self.game.player.stop()
        SoundManager.getInstance().playSFX("OOT_PauseMenu_Open.wav")
        Map.getInstance().updateHighlight()
        self.state.pause()
        self.pauseEngine.mapOpen = True

    def handleChoice(self, choice):
        self.fade.setFrame(0)
        if choice == 0:
            SoundManager.getInstance().fadeoutBGM()
            #SoundManager.getInstance().playSFX("WW_PressStart.wav")
            self.startingGame = True
            self.fading =  True
            self.fade.setRow(1)


        elif choice == 1:
            SoundManager.getInstance().fadeoutBGM()
            #SoundManager.getInstance().playSFX("WW_PressStart.wav")
            self.continuingGame = True
            self.fading =  True
            self.fade.setRow(1)
            
        elif choice == 2:
            return pygame.quit()
        
    

    def handleEvent(self):
        ##Quick quit for debugging##
        """ if event.type == pygame.KEYDOWN and event.key == K_DELETE:
            return pygame.quit() """
            
        if self.state == "game":
            ##  Pause the game if the window is moved   ##
            if not self.game.pause_lock:
                ##  Handle events once the healthbar is initialized   ##
                if self.game.getHealthbarInitialized():
                    if not self.game.fading:
                        if EventManager.getInstance().performAction("pause"):
                            self.pause()
                            return

                    self.game.handleEvent()



        elif self.state == "paused":
            if self.returningToMain:
                return
            if EventManager.getInstance().performAction("map"):
                pygame.display.toggle_fullscreen()

            elif not self.pauseEngine.closing and EventManager.getInstance().performAction("pause"):
                self.pauseEngine.paused = False
                self.pauseEngine.closing = True
                SoundManager.getInstance().playSFX("OOT_PauseMenu_Close.wav")
                self.pauseEngine.mapOpen = False

            else:
                self.pauseEngine.handleEvent()
                if self.pauseEngine.text != "":
                    self.state.speakP()
                    if "Y/N" in self.pauseEngine.text:
                        self.textEngine.setText(self.pauseEngine.text, prompt = True)
                    else:
                        self.textEngine.setText(self.pauseEngine.text)
                
                
        elif self.state == "mainMenu":
            if self.mainMenu.readyToDisplay:
                if not self.fadingIn and not self.continuingGame and not self.startingGame:
                    self.mainMenu.handleEvent()
                    if EventManager.getInstance().performAction("interact"):
                        choice = self.mainMenu.getChoice()
                        self.handleChoice(choice)

        elif self.state == "textBox":
            self.textEngine.handleEvent()

            

        elif self.state == "intro":
            if EventManager.getInstance().performAction("map"):
                self.intro.fading = True
                self.intro.textInt = 11

        elif self.state == "mobster":
            self.mobsterEngine.handleEvent()

    #Only runs if in game
    def handleCollision(self):
        if self.state == "game":
            self.game.handleCollision()
    
    #Update all states
    def update(self, seconds): 
        if self.state == "game":
            
            if self.returningToMain:
                if self.fade.frame == 8:
                    self.state.toMain()
                    self.fadingIn = True
                else:
                    self.fade.update(seconds)
                return
            
            if self.game.dead:
                self.fading = True
                self.returningToMain = True
                self.fade.setRow(1)
                return
            
            if self.fadingIn:
                self.game.updatingPlayer = False
            else:
                if not self.game.updatingPlayer:
                    self.game.updatingPlayer = True
                self.game.update(seconds)

            

            if not self.fading and self.game.fading:
                self.fading = True
            ##Room transition
            if self.game.readyToTransition:
                ##Runs twice
                pos = self.game.tra_pos
                player = self.game.player
                newGame = self.game.tra_room.getInstance()
                keepBGM = self.game.tra_keepBGM
                if not self.game.transporting_area:
                    self.game.reset()
                    gc.collect()
                    self.game = newGame
                    self.game.initializeRoom(player, pos, keepBGM)
                    self.fadingIn = True
                    self.fade.frame = 9
                else:
                    self.game.reset()
                    gc.collect()
                    self.game = newGame
                    self.game.initializeArea(player, pos, keepBGM)

                
            elif self.game.whiting:
                if self.white.alpha == 255:
                    if self.game.transporting_area:
                        self.game.readyToTransition = True
                    elif self.game.areaIntro.fading_out:
                        self.white.alpha = 0
                        self.white.setAlpha()
                        self.game.whiting = False
                else:
                    self.white.update(seconds)
            
            if self.game.startingMobster:
                self.game.reset()
                self.state = "mobster"
                self.mobsterEngine.initialize()

        elif self.state == "textBox":
            #self.updateLight(seconds)
            self.textEngine.update(seconds)
            self.game.update(seconds, updateEnemies=False)

        elif self.state == "paused":
            self.pauseEngine.update(seconds)
            if self.game.getHealthBarDrawing():
                self.game.updateHealthBar(seconds)
            
            if self.returningToMain:
                if self.fade.frame == 8:
                    self.state.toMain()
                    self.fadingIn = True

        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
            

            ##New Game
            if self.startingGame:
                if self.fade.frame == 8:
                    if not pygame.mixer.get_busy():
                        self.game = Tutorial_1.getInstance()
                        self.game.lockHealth()
                        self.state.startGame()
                        self.fadingIn = True
            
                    
            ##Continue
            elif self.continuingGame:
                if self.fade.frame == 8:
                    if not pygame.mixer.get_busy():
                        self.game = LOAD["room"].getInstance()
                        self.game.lockHealth()
                        if LOAD["area"]:
                            self.game.initializeArea(pos=LOAD["position"])
                        else:
                            self.game.initializeRoom(pos=(LOAD["position"]))
                        self.state.startGame()
                        self.fadingIn = True
                        return
                        
        elif self.state == "intro":

            if self.textEngine.voiceInt == -1:
                self.textEngine.voiceInt = 0

            self.intro.update(seconds)
            if self.intro.introDone:
                self.fading = True
                self.fadingIn = True
                ##Transition to Entrance##
                self.inIntro = False
                self.intro.reset()
                self.game = Entrance.getInstance()
                self.game.initializeRoom()
                self.state.toGame()

        elif self.state == "mobster":
            self.mobsterEngine.update(seconds)

        if self.fading:
            if self.fadingIn:
                self.fade.updateIn(seconds)
                if self.fade.frame == 0:
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
                            self.game.deathReset()
                            self.pauseEngine.resetMenu()
                            self.playTheme()
                            self.fade.setRow()
                            self.returningToMain = False 
            else:
                self.fade.update(seconds)
                if self.game and self.game.transporting and self.fade.frame == 8:
                    self.game.finishFade()
    
        self.updateLight(seconds)

    def updateLight(self, seconds):
        if self.inIntro:
            if self.intro.textInt == 3:
                if self.intro.frameTimer >= 0.1:
                    self.intro.frameTimer = 0.0
                    self.intro.frame += 1
                    self.intro.frame %= 9
                    self.intro.darkFrame += 1
                    self.intro.darkFrame %=9
                    self.intro.dark.image = SpriteManager.getInstance().getSprite("light.png", (self.intro.darkFrame, 0))
                    self.intro.light.image = SpriteManager.getInstance().getSprite("light.png", (self.intro.frame, 0))
                else:
                    self.intro.frameTimer += seconds