from . import Drawable
import pygame
from utils import SpriteManager, vec

"""
This file contains several objects that add special effects
to room images.
"""

class Shadow(Drawable):
    """
    A transparent shadow that covers everything below the HUD
    @param color -> rgb color value
    @param alpha -> alpha value
    """
    def __init__(self, fileName = "shadow.png", alpha=48):
        self.image = SpriteManager.getInstance().getLevel(fileName)
        self.image.set_alpha(alpha)
        self.position = vec(0,0)
        self.alpha = alpha
        self.fading_in = True
    
    def update(self, seconds):
        if self.fading_in:
            self.alpha += 1
            if self.alpha >= 51:
                self.fading_in = False
        else:
            self.alpha -= 1
            if self.alpha <= 0:
                self.fading_in = True

        self.image.set_alpha(self.alpha)
