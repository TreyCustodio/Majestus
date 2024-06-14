from . import NonPlayer
from utils import vec, SpriteManager, SoundManager
import pygame

"""
The default type of switch.
Once pressed, it stays pressed.
"""
class Switch(NonPlayer):
    def __init__(self, position = vec(0,0), pressed = False):
        super().__init__(position, "Objects.png")
        self.pressed = pressed
        self.set_sprite()
    
    def getCollisionRect(self):
        newRect = pygame.Rect(0,0,12,12)
        newRect.left = int(self.position[0]+2)
        newRect.top = int(self.position[1]+2)
        return newRect
    
    def set_sprite(self):
        """
        Subclasses will have to override this method for their sprites
        """
        if self.pressed:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (3,0))
        else:
            self.image = SpriteManager.getInstance().getSprite(self.imageName, (2,0))

    def press(self):
        if not self.pressed:
            SoundManager.getInstance().playSFX("LTTP_Switch.wav")
            self.pressed = True
            self.set_sprite()
    
    def reset(self):
        self.pressed = False
        self.set_sprite()