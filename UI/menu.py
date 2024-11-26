from gameObjects import Drawable, Text, Pointer
from utils import SoundManager, vec, magnitude
from UI import ACTIONS
from . import TextEntry

import pygame
"""
Author - Doctor Liz Matthews
Modified by Trey Custodio
"""
class AbstractMenu(Drawable):
    def __init__(self, background, fontName="default",
                 color=(255,255,255)):
        super().__init__((0,0), background)
        
        self.options = {}
        
        self.color = color      
        self.font = fontName
     
    def addOption(self, key, text, position, center=None):
        self.options[key] = TextEntry(position, text, self.font,
                                  self.color)
        optionSize = self.options[key].getSize()
        
        if center != None:
            if center == "both":
                offset = optionSize // 2
            elif center == "horizontal":
                offset = vec(optionSize[0] // 2, 0)
            elif center == "vertical":
                offset = vec(0, optionSize[1] // 2)
            else:
                offset = vec(0,0)
            
            self.options[key].position -= offset
 
    def draw(self, surface):
        super().draw(surface)
        
        for item in self.options.values():
           item.draw(surface)


class EventMenu(AbstractMenu):
    """
    This Class represents the Title Screen.
    Describes Title Screen Buttons and Animations
    """
    def __init__(self, background, fontName="default",
                color=(255,255,255)):
        super().__init__(background, fontName, color)

        ##Display Control for debugging
        displayBool = False
        self.readyToDisplay = displayBool
        self.initialized = displayBool

        self.pointer = Pointer(vec(16*6-8, 98), displayFlag=1)
        self.pointer2 = Pointer(vec(16*12+2, 98), displayFlag=2)
        self.titleTimer = 0.0
        self.eventMap = {}
        self.pointerTick = 0
        self.eventBufferTimer = 0.0
        self.eventHandle = True
        self.movingDown = False
        self.movingUp = False
        self.colorVal = 0
        self.greenVal = 0
        self.colorId = 0 #0-> orange, 1 -> blue, 2 -> yellow, 3 -> wind
        self.increasing = True
        self.frameCounter = 50
     
    def addOption(self, key, text, position, eventLambda=None,
                                              center=None):
        super().addOption(key, text, position, center)      
        if eventLambda:
            self.eventMap[key] = eventLambda
    
    def adjustColor(self):
        self.frameCounter += 1
        ##Getting brighter
        if self.increasing:
            if self.frameCounter >= 10:
                if self.frameCounter % 2 == 0:
                    self.colorVal += 2
                    self.greenVal += 1
                    if self.greenVal == 40:
                        self.increasing = False
        ##Dimming out
        else:
            if self.frameCounter % 2 == 0:
                self.colorVal -= 2
                self.greenVal -= 1
                if self.greenVal == 0:
                    self.colorId += 1
                    self.colorId %= 4
                    self.increasing = True
                    self.frameCounter = 0
                    
    def setReady(self):
        self.readyToDisplay = True
    
    def drawText(self, drawSurf):
        if self.titleTimer >= 9:
                return
        elif self.titleTimer >= 6.5:
            Text((16*6,16*4+8), "Designed with PyGame", color = (220,190,0)).draw(drawSurf)
        elif self.titleTimer >= 4:
            drawSurf.fill((0,0,0))
            return
        elif self.titleTimer >= 1.0:
            Text((16*5,16*4+8), "YungTrey Games Presents...", color = (220,0,0)).draw(drawSurf)
        
    def draw(self, drawSurf):
        if self.colorId == 0:
            drawSurf.fill(pygame.Color(self.colorVal+8, self.greenVal, 0))
        elif self.colorId == 1:
            drawSurf.fill(pygame.Color(0, self.colorVal, self.colorVal+4))
        elif self.colorId == 2:
            drawSurf.fill(pygame.Color(self.colorVal+4, self.colorVal, 0))
        elif self.colorId == 3:
            drawSurf.fill(pygame.Color(self.greenVal, self.colorVal, 0))

        self.adjustColor()

        if self.readyToDisplay:
            super().draw(drawSurf)
            self.pointer.draw(drawSurf)
            self.pointer2.draw(drawSurf)

    def addEvent(self, key, eventLambda):
        """
        Adjust the options for starting the game
        if you're using a controller
        """
        self.eventMap[key] = eventLambda
        

    def editText(self, key, text):
        position = vec(self.options[key].position[0] + 18, self.options[key].position[1])
        self.options[key] = Text(position, text)


    def getChoice(self):
        return self.pointer.getChoice()
    
    def newGame_down(self):
        self.eventHandle = False
        self.pointer.increaseChoice()
        self.pointer.position[1] = self.options["continue"].position[1]
        self.pointer2.position[1] = self.options["continue"].position[1]
        SoundManager.getInstance().playSFX("FF_cursor.wav")
        self.eventHandle = False
        
    def newGame_up(self):
        self.eventHandle = False
        self.pointer.setChoice(2)
        self.pointer.position[0] += 16
        self.pointer2.position[0] -= 16
        self.pointer.position[1] = self.options["quit"].position[1]
        self.pointer2.position[1] = self.options["quit"].position[1]
        SoundManager.getInstance().playSFX("FF_cursor.wav")
        self.eventHandle = False

    def continueGame_down(self):
        self.eventHandle = False
        self.pointer.position[0] += 16
        self.pointer2.position[0] -= 16
        self.pointer.increaseChoice()
        self.pointer.position[1] = self.options["quit"].position[1]
        self.pointer2.position[1] = self.options["quit"].position[1]
        SoundManager.getInstance().playSFX("FF_cursor.wav")
        self.eventHandle = False

    def continueGame_up(self):
        self.eventHandle = False
        self.pointer.decreaseChoice()
        self.pointer.position[1] = self.options["start"].position[1]
        self.pointer2.position[1] = self.options["start"].position[1]
        SoundManager.getInstance().playSFX("FF_cursor.wav")
        self.eventHandle = False

    def quitGame_down(self):
        self.eventHandle = False
        self.pointer.setChoice(0)
        self.pointer.position[0] -= 16
        self.pointer2.position[0] += 16
        self.pointer.position[1] = self.options["start"].position[1]
        self.pointer2.position[1] = self.options["start"].position[1]
        SoundManager.getInstance().playSFX("FF_cursor.wav")
        self.eventHandle = False

    def quitGame_up(self):
        self.eventHandle = False
        self.pointer.decreaseChoice()
        self.pointer.position[0] -= 16
        self.pointer2.position[0] += 16
        self.pointer.position[1] = self.options["continue"].position[1]
        self.pointer2.position[1] = self.options["continue"].position[1]
        SoundManager.getInstance().playSFX("FF_cursor.wav")
        self.eventHandle = False

    def handleEvent(self):
        if self.eventHandle:
            ##On new Game
            if self.pointer.choice == 0:
                if ACTIONS["down"]:
                    self.newGame_down()
                
                elif ACTIONS["up"]:
                    self.newGame_up()

            ##On continue
            elif self.pointer.choice == 1:
                if ACTIONS["up"]:
                    self.continueGame_up()

                elif ACTIONS["down"]:
                    self.continueGame_down()

            ##On quit
            elif self.pointer.choice == 2:
                if ACTIONS["up"]:
                    self.quitGame_up()

                elif ACTIONS["down"]:
                    self.quitGame_down()
    
    """
    Returns:
    True if the joystick is moved down
    """
    def movedDown(self, event):
        if event.value < 0.8:
            self.movingDown = False
        else:
            self.movingDown = True
    
    """
    Returns:
    True if the joystick is moved up
    """
    def movedUp(self, event):
        if event.value > -0.8:
            self.movingUp = False
        else:
            self.movingUp = True
    
    

    def update(self, seconds):
        if not self.initialized:
            self.titleTimer += seconds
            if self.titleTimer >= 10:
                self.initialized = True
                self.titleTimer = 0.0
            return
            
        elif not self.readyToDisplay:
            self.titleTimer += seconds
            if self.titleTimer >= 7.2:
                self.setReady()
                self.titleTimer = 0.0
            
        super().update(seconds)
        self.pointer.update(seconds)
        self.pointer2.update(seconds)
        if not self.eventHandle:
            self.eventBufferTimer += seconds
            if self.eventBufferTimer >= 0.2:
                self.eventHandle = True
                self.eventBufferTimer = 0.0

        if self.pointerTick < 10:
            self.pointer.position[0] += 1
            self.pointer2.position[0] -= 1
            self.pointerTick += 1
        else:
            self.pointer.position[0] -= 1
            self.pointer2.position[0] += 1
            self.pointerTick += 1
            if self.pointerTick >= 20:
                self.pointerTick = 0

    
    
        
    
    
        
        

