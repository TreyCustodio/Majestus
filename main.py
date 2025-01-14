import pygame
from UI import ScreenManager, Xbox, EventManager
from utils import RESOLUTION, UPSCALED
from random import randint

import time

"""
Majestus v0.2
Author - Trey Custodio 12/26/2024

This file drives the code for the game,
handles debugging, and sets up all
of the game's objects.
Time module is used for runtime analysis.
"""

def main():
    """
    Driver Function.
    The While loop runs until the game closes.
    """

    #   Initialize Pygame
    pygame.init()
    pygame.font.init()
    pygame.joystick.init()

    #   Initialize the Screen
    flags = pygame.SCALED #| pygame.NOFRAME | pygame.FULLSCREEN
    screen = pygame.display.set_mode(list(map(int, UPSCALED)), flags=flags)
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))
    transparentSurface = drawSurface.subsurface(drawSurface.get_rect())
    textSurface = drawSurface.subsurface(drawSurface.get_rect())
    
    pygame.mouse.set_visible(False)

    #   Window Icon and Message
    rand = randint(0,5)
    if rand == 1:
        pygame.display.set_caption("Majestus: I'll learn pixel art one day...")
    elif rand == 2:
        pygame.display.set_caption("Majestus: More than a Link to the Past clone!")
    elif rand == 3:
        pygame.display.set_caption("Majestus: I'll give you one try to guess what my favorite video game franchise is.")
    elif rand == 4:
        pygame.display.set_caption("Majestus: Super Metroid clone when?")
    elif rand == 5:
        pygame.display.set_caption("Majestus: RIP Big L")
    else:
        pygame.display.set_caption("Majestus: I got the caption idea from Minecraft!")

    iconSurf = pygame.Surface((32,32))
    
    image = pygame.image.load("displayIcon.png").convert()
    iconSurf.blit(image, (0,0))
    pygame.display.set_icon(iconSurf)
    
    #   Main Engines
    gameEngine = ScreenManager()
    eventManager = EventManager.getInstance()
    
    #   Runtime / FPS Analysis
    start_time = time.time()
    frame_count = 0

    """
    Run Loop
    """
    RUNNING = True
    while RUNNING:
        
        #   (1.) Draw
        pygame.transform.scale(drawSurface,
                               list(map(int, UPSCALED)),
                               screen)
        
        
        gameClock = pygame.time.Clock()
        
        
        if gameEngine.state == "textBox":
            
            pygame.transform.scale(textSurface,
                               list(map(int, UPSCALED)),
                               screen)
            pygame.display.flip()
            gameEngine.drawText(textSurface)
            gameEngine.drawWipe(textSurface)

        elif gameEngine.state == "mainMenu":
            pygame.transform.scale(transparentSurface,
                               list(map(int, UPSCALED)),
                               screen)
            pygame.display.flip()
            gameEngine.drawTitle(transparentSurface)
            gameEngine.drawWipe(drawSurface)
            
        else:
            pygame.display.flip()
            gameEngine.draw(drawSurface)
            gameEngine.drawWipe(drawSurface)
        

        #   (2.) Handle events
        eventManager.handleEvents(gameEngine)

        #   (3.) Update
        if gameEngine.state == "mainMenu" or eventManager.readyToUpdate():
            gameClock.tick(60)
            seconds = gameClock.get_time() / 1000
            eventManager.updateBuffer(seconds)   
            gameEngine.update(seconds)
        
            #   (i)  Calculate FPS each second
            #   Should be as close to 60 as possible per the tick(60)
            """ frame_count += 1
            if time.time() - start_time > 1:
                fps = frame_count / (time.time() - start_time)
                print(f"FPS: {fps:.2f}")
                frame_count = 0
                start_time = time.time() """

        


    #   quit if not running
    pygame.quit()


if __name__ == '__main__':
    main()