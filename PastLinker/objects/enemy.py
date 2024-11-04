import pygame
from abc import abstractmethod
from typing import Any, override
from . import Animated
from utils import RESOLUTION, FLOOR, vec
from UI import SoundManager

class Enemy(Animated):
    """
    An Abstract Enemy Class.
    Specifies an enemy's states,
    how to draw them, and how to update them.
    """
    def __init__(self, position, fileName="", offset = (0,0), velocity = vec(-50,0), nFrames = 1, fps = 16, color = (255,255,255)):
        """
        Initialize all of the enemy's variables.
        """
        super().__init__(position, fileName, offset, nFrames, fps)
        
        #   Attributes
        self.vel    = velocity
        self.type = None
        self.color = color

        #   States
        self.attacking = False   # Attacking the player
        self.dead   = False # Ready to disappear
        self.dying  = False # Death animation

    def stop(self):
        """
        Stop moving and attack.
        """
        self.vel = vec(0,0)
        self.attacking = True

    def draw(self, drawSurface, drawHitbox=False, use_camera=True):
        """
        Blit the enemy onto
        the drawSurface.
        """
        if self.dead or self.dying:
            return
        else:
            super().draw(drawSurface, drawHitbox, use_camera)
            text = pygame.font.SysFont("Garamond", 24).render(self.string, False, self.color)
            drawSurface.blit(text, (self.position[0] + 8, self.position[1] - 24))

    @abstractmethod
    def kill(self):
        """
        Defines the enemy's
        death routine.
        """
        return
    
    @abstractmethod
    def getDamage(self):
        """
        Return the enemy's damage.
        """
        return
    
    def handleKey(self, key):
        #   Typing damage
        if key == self.string[0]:
            self.string.pop(0)
            if len(self.string) == 0:
                self.dead = True
                SoundManager.getInstance().playSFX("death.wav")
                
    def update(self, seconds, key = None):
        #   Death States
        if self.dead:
            return
        
        elif self.dying:
            return
        
        #   Typing Damage
        if key != None:
            self.handleKey(key)

        #   Update Position
        self.position += self.vel * seconds

        #   Animate
        super().update(seconds)

        #   Out of bounds safety
        if self.position[0] <= 0:
            self.dead = True

class Walker(Enemy):
    def __init__(self, string = "a", color = (255,255,255)):
        super().__init__(vec(RESOLUTION[0], RESOLUTION[1] - FLOOR - 16), "walker.png", (0,0), velocity=vec(-50,0), color=color)
        self.string = string

    @override
    def kill(self):
        """
        Begin death animation.
        """
        self.dead = True
    
    @override
    def getDamage(self):
        return 5


class Flyer(Enemy):
    def __init__(self, string = "a", color=(255, 255, 255)):
        super().__init__(vec(RESOLUTION[0], 20), "flyer.png", (0,0), velocity=(vec(-100, 0)), color=color)

    @override
    def kill(self):
        """
        Begin death animation.
        """
        self.dead = True
    
    @override
    def getDamage(self):
        return 8
    
    
class Sniper(Walker):
    """
    Type this word to receive an upgrade
    that shortens every enemy's word to 1 char
    for 10 seconds.
    """
    def __init__(self, string="Snipealicious"):
        super().__init__(string, color=(255,255,70))
        self.type = "snipe"


class Builder():
    def __call__(self, *args: Any, **kwds: Any) -> Any:
        pass