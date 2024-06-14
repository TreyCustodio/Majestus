from FSMs import ScreenManagerFSM
from gameObjects import PauseEngine, TextEngine, HudImageManager
from rooms import *

from utils import SoundManager
from . import TextEntry, EventMenu

from utils import vec, RESOLUTION

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
                            self.game.getDrunk()
                        
                        elif self.pauseEngine.promptFlag == "joint":
                            INV["joint"] -= 1
                            self.game.getHigh()
                        
                        elif self.pauseEngine.promptFlag == "speed":
                            INV["speed"] -= 1
                            self.game.zoom()

                        elif self.pauseEngine.promptFlag == "syringe":
                            self.game.useSyringe()
                        
                        elif self.pauseEngine.promptFlag == "quit":
                            SoundManager.getInstance().fadeoutBGM()
                            self.returningToMain = True
                            self.fade.setRow(1)             
                            
                    

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
            self.textEngine.draw(self.pauseEngine.boxPos, drawSurf)

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
                    self.textEngine.setText(self.game.text, self.game.icon, self.game.largeText)



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
        
        if (not (self.fading or self.fadingIn)) and self.game and self.game.fading:
            self.fading = True

        if self.fading or self.returningToMain:
            self.fade.draw(drawSurf)
            return
        
        elif self.fadingIn:
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
            self.fade.setRow(1)


        elif choice == 1:
            SoundManager.getInstance().fadeoutBGM()
            #SoundManager.getInstance().playSFX("WW_PressStart.wav")
            self.continuingGame = True
            self.fade.setRow(1)
            
        elif choice == 2:
            return pygame.quit()
        
    def moveMenuCursor(self):
        if self.state == "mainMenu":
            self.mainMenu.moveCursor()

    def handleEvent(self, event):
        ##Quick quit for debugging##
        """ if event.type == pygame.KEYDOWN and event.key == K_DELETE:
            return pygame.quit() """
            
        if self.state == "game":
            ##  Pause the game if the window is moved   ##
            if not self.game.pause_lock:
                if event.type == pygame.WINDOWMOVED:
                    if self.game.player:
                        self.game.player.stop()
                    self.state.pause()
                    return

                ##  Handle events once the healthbar is initialized   ##
                if self.game.getHealthbarInitialized():
                    if self.controller == "Controller (Xbox One For Windows)":
                        if event.type == JOYBUTTONDOWN and event.button == 7:
                            self.pause()
                        
                        elif event.type == JOYBUTTONDOWN and event.button == 6:
                            self.openMap()
                            
                        else:
                            self.game.handleEvent_C(event)

                    else:
                        if not self.game.fading:
                            if event.type == KEYDOWN and event.key == K_RETURN:
                                self.pause()
                                return
                            
                            
                            elif event.type == KEYDOWN and event.key == K_LSHIFT:
                                if INV["map0"]:
                                    self.openMap()
                                return
                            
                        self.game.handleEvent(event)



        elif self.state == "paused":
            if self.returningToMain:
                return
            if self.controller == "Controller (Xbox One For Windows)":
                if event.type == JOYBUTTONDOWN and (event.button == 7):
                    self.pauseEngine.paused = False
                    SoundManager.getInstance().playSFX("OOT_PauseMenu_Close.wav")
                    self.pauseEngine.mapOpen = False
                    self.state.pause()

                else:
                    self.pauseEngine.handleEvent_C(event)
                    
            
            else:
                if event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                    pygame.display.toggle_fullscreen()
                elif event.type == KEYDOWN and (event.key == K_RETURN or event.key == K_LSHIFT):
                    self.pauseEngine.paused = False
                    self.pauseEngine.closing = True
                    SoundManager.getInstance().playSFX("OOT_PauseMenu_Close.wav")
                    self.pauseEngine.mapOpen = False

                else:
                    self.pauseEngine.handleEvent(event)
                    if self.pauseEngine.text != "":
                        self.state.speakP()
                        if "Y/N" in self.pauseEngine.text:
                            self.textEngine.setText(self.pauseEngine.text, prompt = True)
                        else:
                            self.textEngine.setText(self.pauseEngine.text)
                
        elif self.state == "mainMenu":
            if self.mainMenu.readyToDisplay:
                if not self.fadingIn and not self.continuingGame and not self.startingGame:
                    if self.controller == "Controller (Xbox One For Windows)":
                        self.mainMenu.handleEvent_C(event)
                        if event.type == JOYBUTTONDOWN and (event.button == 0):
                            choice = self.mainMenu.getChoice()
                            self.handleChoice(choice)
                    else:
                        self.mainMenu.handleEvent(event)
                        if event.type == pygame.KEYDOWN and event.key == K_z:
                            choice = self.mainMenu.getChoice()
                            self.handleChoice(choice)
                        elif event.type == pygame.KEYDOWN and event.key == K_ESCAPE:
                            pygame.display.toggle_fullscreen()
                    
            


        elif self.state == "textBox":
            if self.controller == "Controller (Xbox One For Windows)":
                if self.textEngine.ready_to_continue and event.type == JOYBUTTONDOWN and event.button == 2:
                    if self.pauseEngine.paused:
                        self.pauseEngine.textBox = False
                        self.pauseEngine.text = ""
                        self.state.speakP()

                    elif self.inIntro:
                        ##Skip the intro
                        self.intro.textBox = False
                        self.intro.text = ""
                        self.intro.icon = None
                        self.intro.fading = True
                        self.state.speakI()
                        self.intro.fading = True
                        self.intro.textInt = 11
                        
                        
                    else:
                        self.game.textBox = False
                        self.game.text = ""
                        self.game.icon = None
                        self.state.speak()
                    self.textEngine.reset()
                    return
                    ##Close the textBox

            else:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    if self.pauseEngine.paused:
                        self.pauseEngine.textBox = False
                        self.pauseEngine.text = ""
                        self.state.speakP()
                    elif self.inIntro:
                        ##Skip the intro
                        self.intro.textBox = False
                        self.intro.text = ""
                        self.intro.icon = None
                        self.intro.fading = True
                        self.state.speakI()
                        self.intro.fading = True
                        self.intro.textInt = 11
                        
                        
                    else:
                        self.game.textBox = False
                        self.game.text = ""
                        self.game.icon = None
                        self.state.speak()
                    self.textEngine.reset()
                    return
                    ##Close the textBox

            if self.controller == "Controller (Xbox One For Windows)":
                self.textEngine.handleEvent_C(event)
            else:
                self.textEngine.handleEvent(event)

            

        elif self.state == "intro":
            if self.controller == "Controller (Xbox One For Windows)":
                if event.type == JOYBUTTONDOWN and event.button == 7:
                    self.intro.fading = True
                    self.intro.textInt = 11
            else:
                if event.type == KEYDOWN and event.key == K_SPACE:
                    self.intro.fading = True
                    self.intro.textInt = 11

    #Only runs if in game
    def handleCollision(self):
        if self.state == "game":
            self.game.handleCollision()
    
    #Update all states
    def update(self, seconds): 
        if self.state == "game":
            if self.returningToMain:
                self.fade.update(seconds)
                if self.fade.frame == 8:
                    self.state.toMain()
                    self.fadingIn = True
                return
            
            if self.fadingIn:
                self.game.updatingPlayer = False
                self.game.update(seconds)
            else:
                if not self.game.updatingPlayer:
                    self.game.updatingPlayer = True
                self.game.update(seconds)
            if self.game.dead:
                self.returningToMain = True
            
            ##Room transition
            elif self.game.readyToTransition:
                #print("transition")
                pos = self.game.tra_pos
                player = self.game.player
                newGame = self.game.tra_room.getInstance()
                keepBGM = self.game.tra_keepBGM
                self.game.reset()
                self.game = newGame
                self.game.initializeRoom(player, pos, keepBGM)
                self.fade.frame = 9
                self.fading = False
                self.fadingIn = True

        elif self.state == "textBox":
            #self.updateLight(seconds)
            self.textEngine.update(seconds)

        elif self.state == "paused":
            self.pauseEngine.update(seconds)
            if self.game.getHealthBarDrawing():
                self.game.updateHealthBar(seconds)
            
            if self.returningToMain:
                self.fade.update(seconds)
                if self.fade.frame == 8:
                    self.state.toMain()
                    self.fadingIn = True

        elif self.state == "mainMenu":
            self.mainMenu.update(seconds)
            

            ##New Game
            if self.startingGame:
                if self.fade.frame == 8:
                    if not pygame.mixer.get_busy():
                        self.intro = Intro_Cut.getInstance()
                        self.inIntro = True
                        self.state.toIntro()
                        self.fadingIn = True
                        """ if FLAGS[51]:
                            self.game = Grand_Chapel.getInstance()
                            self.game.initializeRoom()
                            self.state.startGame()

                        elif FLAGS[50]:
                            self.game = Entrance.getInstance()
                            self.game.initializeRoom()
                            self.state.startGame()
                            
                        else: """
                        
                else:
                    self.fade.update(seconds)
            
            ##Continue
            elif self.continuingGame:
                if self.fade.frame == 8:
                    if not pygame.mixer.get_busy():
                        self.game = Alpha_Flapper.getInstance()
                        self.game.lockHealth()
                        self.game.initializeRoom()
                        self.state.startGame()
                        self.fadingIn = True
                        return
                        if FLAGS[52]:
                            self.game = Flame_4.getInstance()
                            self.game.lockHealth()
                            self.game.initializeRoom()
                            self.state.startGame()
                            self.fadingIn = True
                        elif FLAGS[51]:
                            self.game = Grand_Chapel.getInstance()
                            self.game.lockHealth()
                            self.game.initializeRoom()
                            self.state.startGame()
                            self.fadingIn = True
                        elif FLAGS[110]:
                            self.game = Alpha_Flapper.getInstance()
                            self.game.lockHealth()
                            self.game.initializeRoom()
                            self.state.startGame()
                            self.fadingIn = True
                        elif FLAGS[50]:
                            self.game = Entrance.getInstance()
                            self.game.lockHealth()
                            self.game.initializeRoom()
                            self.state.startGame()
                            self.fadingIn = True
                        else:
                            self.intro = Intro_Cut.getInstance()
                            self.inIntro = True
                            self.state.toIntro()
                            self.fadingIn = True
                        
                else:
                    self.fade.update(seconds)

        elif self.state == "intro":
            #self.updateLight(seconds)
            """ if self.intro.frameTimer >= 0.8:
                self.intro.frame += 1
                self.intro.frame %= 9
                self.intro.light.image = SpriteManager.getInstance().getSprite("light.png", (self.intro.frame, 0))
            else:
                self.intro.frameTimer += seconds """

            self.intro.update(seconds)
            if self.intro.introDone:
                self.fadingIn = True
                ##Transition to Entrance##
                self.inIntro = False
                self.intro.reset()
                self.game = Entrance.getInstance()
                self.game.initializeRoom()
                self.state.toGame()

        if self.fading:
            self.fade.update(seconds)
            if self.fade.frame == 8:
                self.game.finishFade()
                self.fading = False

        elif self.fadingIn:
            self.fade.updateIn(seconds)
            if self.fade.frame == 0:
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