from . import Drawable
from utils import vec
from UI import SpriteManager

class Animated(Drawable):
    def __init__(self, position: tuple = vec(0,0), fileName: str ="", offset: tuple =(0,0), nFrames: int = 1, fps: int = 16):
        super().__init__(position, fileName, offset)
        self.fileName = fileName
        self.nFrames = nFrames
        self.fps = fps
        self.frameCount = 0
        self.row = offset[0]
        self.column = offset[1]
    
    def update(self, seconds):
        super().update(seconds)
        self.frameCount += 1
        if self.frameCount >= self.nFrames:
            self.frameCount = 0
            self.row += 1
            self.row %= self.nFrames
            self.image = SpriteManager.getInstance().getSprite(self.fileName, (self.row, self.column))



        

