import pygame
from UI import ScreenManager, Xbox, EventManager
from utils import RESOLUTION, UPSCALED
from random import randint

def main():
    ##Initialize the module
    pygame.init()
    pygame.font.init()

    ##Set the screen up
    flags = pygame.SCALED | pygame.NOFRAME | pygame.FULLSCREEN
    screen = pygame.display.set_mode(list(map(int, UPSCALED)), flags=flags)
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))
    transparentSurface = drawSurface.subsurface(drawSurface.get_rect())
    textSurface = drawSurface.subsurface(drawSurface.get_rect())
    
    pygame.mouse.set_visible(False)
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
    
    gameEngine = ScreenManager()
    eventManager = EventManager.getInstance()

    controller = Xbox()
    def setJoystick():
        ##Set up joystick
        joysticks = pygame.joystick.get_count()
        if joysticks == 0:
            gameEngine.setController("key")
            gameEngine.controllerSet = False

        elif not gameEngine.controllerSet:
            for i in range(pygame.joystick.get_count()):
                controller.setValue(pygame.joystick.Joystick(i))
                gameEngine.setController(controller.name)
                gameEngine.controllerSet = True
            

    RUNNING = True
    while RUNNING:
        
        pygame.transform.scale(drawSurface,
                               list(map(int, UPSCALED)),
                               screen)
        
        
        gameClock = pygame.time.Clock()
        setJoystick()
        
        if gameEngine.state == "textBox":
            
            pygame.transform.scale(textSurface,
                               list(map(int, UPSCALED)),
                               screen)
            pygame.display.flip()
            gameEngine.drawText(textSurface)

        elif gameEngine.state == "mainMenu":
            pygame.transform.scale(transparentSurface,
                               list(map(int, UPSCALED)),
                               screen)
            pygame.display.flip()
            gameEngine.drawTitle(transparentSurface)
            
        else:
            pygame.display.flip()
            gameEngine.draw(drawSurface)

        eventManager.handleEvents(gameEngine)
        gameEngine.moveMenuCursor()
        gameEngine.handleCollision()
        gameClock.tick(60)
        seconds = gameClock.get_time() / 1000     
        gameEngine.update(seconds)
        #gameEngine.updateLight(seconds)
     
    pygame.quit()


if __name__ == '__main__':
    main()