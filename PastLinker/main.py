import pygame
from utils import vec
from objects import Engine
from UI import EventManager
from utils import RESOLUTION, UPSCALED




def main():
    #   Initialize modules
    pygame.init()
    pygame.font.init()

    #   Set the screen up
    flags = pygame.SCALED #| pygame.NOFRAME | pygame.FULLSCREEN
    screen = pygame.display.set_mode(list(map(int, UPSCALED)), flags=flags)
    drawSurface = pygame.Surface(list(map(int, RESOLUTION)))

    #   Set mouse visible
    pygame.mouse.set_visible(True)

    #   Set application icon
    iconSurf = pygame.Surface((32,32))
    image = pygame.image.load("displayIcon.png").convert()
    iconSurf.blit(image, (0,0))
    pygame.display.set_icon(iconSurf)
    
    #   Initialize the engine and eventManager
    gameEngine = Engine()
    #eventManager = EventManager()

    RUNNING = True
    while RUNNING:
        
        #   Draw
        pygame.transform.scale(drawSurface,
                            list(map(int, UPSCALED)),
                            screen)
        pygame.display.flip()
        gameEngine.draw(drawSurface)
        gameEngine.drawWipe(drawSurface)
        

        #   Handle events
        EventManager.handleEvents(gameEngine)

        #   Update
        gameClock = pygame.time.Clock()
        if EventManager.readyToUpdate():
            gameClock.tick(60)
            seconds = gameClock.get_time() / 1000
            EventManager.updateBuffer(seconds)   
            gameEngine.update(seconds)
    
    #   Quit if not running
    pygame.quit()

if __name__ == '__main__':
    main()