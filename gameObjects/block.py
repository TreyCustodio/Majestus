from . import Drawable, Animated, FireIcon
from utils import vec, RESOLUTION, COORD, rectAdd, SpriteManager
import pygame

"""
Blocks are static, 16x16, cube-shaped objects
that impede the player's movement.
"""
class Block(Drawable):
    def __init__(self, position=vec(0,0), offset = (5,0), vanish = False):
        super().__init__(position, "Objects.png", offset)
        self.width = 16
        self.height = 16
        self.popProjectiles = True
        self.vanish = vanish
    
    def draw(self, drawSurface, drawBox = False):
        super().draw(drawSurface, drawBox)
        
    def update(self, player):
        if player.pushing == True:
            player.pushing = False

class IBlock(Block):
    """
    Invisible blocks
    """
    def __init__(self, position = vec(0,0), width = 16, height = 16, popProjectiles = True, vanish = False):
        super().__init__(position, (0,0), vanish)
        self.popProjectiles = popProjectiles
        self.width = width
        self.height = height

    def getCollisionRect(self):
        return pygame.Rect(self.position, (self.width, self.height))
    
    def draw(self, drawSurface, drawBox = False):
        super().draw(drawSurface, False)

class Terrain(IBlock):
    def __init__(self, position=vec(0, 0), width=16, height=16, popProjectiles=True, vanish=False, id = ""):
        super().__init__(position, width, height, popProjectiles, vanish)
        self.id = id

class Lava(Terrain):
    def __init__(self, position=vec(0, 0), width=16, height=16, popProjectiles=True, vanish=False):
        super().__init__(position, width, height, popProjectiles, vanish, "lava")

    def draw(self, drawSurface, drawBox = False):
        super().draw(drawSurface, False)
        self.speedFactor = 1.5 #value to decrease speed by
        if drawBox:
            collision = rectAdd(-Drawable.CAMERA_OFFSET, self.getCollisionRect())
            pygame.draw.rect(drawSurface, (255,100,0), collision, 1)


class HBlock(Block):
    """
    Half a block (8 x 16 pixels) of collision.
    The block will be placed within a 16 x 16 space.
    If right, the collision will appear on the right.
    If left, the collision will appear on the left."""
    def __init__(self, position = vec(0,0), right = False):
        super().__init__(position, (0,0))
        self.width = 8
        self.right = right
        
    def getCollisionRect(self):
        newRect = pygame.Rect((0,0),(8,16))
        if self.right:
            newRect.left = int(self.position[0]+8)
        else:
            newRect.left = int(self.position[0])
        newRect.top = int(self.position[1])
        return newRect
    
class Trigger(IBlock):
    """
    Triggers activate when the player collides with them
    """
    def __init__(self, position = vec(0,0), text="", door = -1, width = 16, height = 16):
        if door == 0:
            super().__init__((16*9, (16*12 + 8)))
        elif door == 3:
            super().__init__((0, 6*16))
        elif door == 2:
            super().__init__((16*9, (-6)))
        elif door == 1:
            super().__init__((RESOLUTION[0]-16, 6*16))
        
        #Specific pos
        elif door == 5:
            super().__init__(position, (1,0))

        ##Quadrant 2
        elif door == 10:
            super().__init__((16*9 +304, (16*12 + 8)))

        elif door == 13:
            super().__init__((0 +304, 6*16))
            
        elif door == 12:
            super().__init__((16*9 +304, (-6)))

        elif door == 11:
            super().__init__((RESOLUTION[0]-16 +304, 6*16))
        
        ##Quadrant 3
        elif door == 20:
            super().__init__((16*9 + 608, (16*12 + 8)))
        elif door == 23:
            super().__init__((0 + 608, 6*16))
            
        elif door == 22:
            super().__init__((16*9 + 608, (-6)))

        elif door == 21:
            super().__init__((RESOLUTION[0]-16 + 608, 6*16))

        else:
            super().__init__(position)
            self.width = width
            self.height = height
        
        self.door = door
        self.text = text
    
    def draw(self, drawSurface):
        super().draw(drawSurface)

    def getCollisionRect(self):
        if self.door == 0 or self.door == 2 or self.door == 10 or self.door == 12 or self.door == 20 or self.door == 22:
            return pygame.Rect((self.position[0]-8, self.position[1]), (32, 16))
        elif self.door == 1 or self.door == 3:
            return pygame.Rect((self.position[0],self.position[1]-8), (16,32))
        else:
            return pygame.Rect(self.position, (self.width, self.height))
    def interact(self, player, engine):
        engine.displayText(self.text)
        player.vel = vec(0,0)

class Torch(Animated):
    def __init__(self, position = vec(0,0), color = 0, lit = True):
        if lit:
            super().__init__(position, "torch.png", (0,color))
        else:
            super().__init__(position, "torch.png", (0,4))
            color = 4
        self.lit = lit
        self.nFrames = 4
        self.framesPerSecond = 8

        self.row = color
        if color == 1 or color == 3:
            self.frame = 2
        
        self.interactable = False
        self.interactIcon = FireIcon((self.position[0],self.position[1]-16))
    
    def getInteractionRect(self):
        return pygame.Rect((self.position[0]-8, self.position[1]-8), (32,32))
    
    def setInteractable(self):
        self.interactable = True
    
    def light(self):
        if not self.lit:
            self.row = 0
            self.lit = True
    
    def draw(self, drawSurface):
        super().draw(drawSurface)
        if self.interactable:
            self.interactIcon.draw(drawSurface)
    
    def update(self, seconds):
        
        super().update(seconds)
        
        if self.interactable:
            self.interactIcon.update(seconds)