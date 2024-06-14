from . import Drawable, Animated

class Boulder(Drawable):
    def __init__(self, position):
        super().__init__(position, fileName="boulder.png", offset=(0,0))
        self.render = True
        
    def handleCollision(self, projectile, engine):
        if projectile.id == "bombo":
            engine.disappear(self)
    
    def vanish(self):
        return
    def setRender(self):
        return
class ForceField(Animated):
    """
    Should be converted into an enemy type
    or simply add a damaging effect.
    """
    def __init__(self, position, color = 0, render=True):
        super().__init__(position, "barrier.png", (0, color))
        self.top = False
        self.belowDrops = False
        self.nFrames = 4
        self.framesPerSecond = 8
        self.dead = False
        self.row = color
        self.frame += color
        self.render = render
        self.rendering = False
        self.fading = False
        if render:
            self.alpha = 255
        else:
            self.alpha = 0
        self.set_alpha()

    def handleCollision(self, projectile, engine):
        return
    
    def set_alpha(self):
        self.image.set_alpha(self.alpha)

    def vanish(self):
        self.render = False
        self.fading = True
    
    def setRender(self):
        self.render = True
        self.rendering = True

    def draw(self, drawSurface):
        super().draw(drawSurface)
    
    def update(self, seconds, position = None):
        if self.render:
            if self.rendering:
                self.alpha += 25
                if self.alpha >= 255:
                    self.alpha = 255
                    self.rendering = False
        
            super().update(seconds)
            self.set_alpha()
        else:
            if self.fading:
                self.alpha -= 25
                if self.alpha <= 0:
                    self.alpha = 0
                    self.rendering = False
                    self.fading = False
                super().update(seconds)
                self.set_alpha()