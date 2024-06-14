from . import Block, Animated
from utils import vec, SoundManager, SpriteManager
import pygame

"""
This file contains unique types of blocks.
All of them inherit from the Block class
"""
class LockBlock(Block):
    """
    Requires a key to unlock -> handled in engine
    """
    def __init__(self, position=vec(0,0)):
        super().__init__(position, (4,4))

class BreakableBlock(Block):
    """
    A block that can be broken by the player
    """
    def __init__(self, position=vec(0,0)):
        super().__init__(position, (4,1))
        self.broken = False
    
    def brake(self):
        self.broken = True

class PushableBlock(Animated):
    """
    A block that can be pushed by the player
    """
    def __init__(self, position=vec(0,0)):
        super().__init__(position, "blockP.png", (0,0))

        self.nFrames = 5
        self.vel = vec(0,0)
        self.originalPos = position
        self.pushing = False

        self.resetting = False
        self.resetTimer = 0

    def handleCollision(self, other):
        pass
    
    def reset(self):
        self.resetting = True
        SoundManager.getInstance().stopSFX("LA_Rock_Push.wav")
        if not pygame.mixer.get_busy():
            SoundManager.getInstance().playSFX("LA_Dungeon_Signal.wav")
        #self.position = self.originalPos


    def push(self):
        self.pushing = True
        if not pygame.mixer.get_busy():
            SoundManager.getInstance().playSFX("LA_Rock_Push.wav", -1)
    

        
    def update(self, seconds, player = None, direction = 0):
        # (0 down), (2 up)
        # (1 right), (3 left)
        if self.resetting:
            super().update(seconds)
            self.resetTimer += seconds
            if self.resetTimer >= 0.2:
                self.resetTimer = 0
                self.position = self.originalPos
                self.resetting = False
                self.image = SpriteManager.getInstance().getSprite("blockP.png",(0,0))
        else:

            if self.pushing:
                player.pushing = True
                if direction == 0:
                    self.vel = vec(0, player.getSpeed()/3)
                elif direction == 2:
                    self.vel = vec(0, -player.getSpeed()/3)
                elif direction == 1:
                    self.vel = vec(player.getSpeed()/3, 0)
                else:
                    self.vel = vec(-player.getSpeed()/3, 0)

                
                self.position += self.vel * (seconds)
                self.pushing = False
                self.vel = (0,0)
                
            elif player.pushing == True:
                SoundManager.getInstance().stopSFX("LA_Rock_Push.wav")
                player.pushing = False
                
