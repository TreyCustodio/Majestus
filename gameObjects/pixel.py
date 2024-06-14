import pygame

class Pixel(object):
    """
    pygame Surface objects to be appended to the
    PixelBuilder's list.
    drawPos -> position to draw
    width, height color -> self-explanatory
    """
    def __init__(self, drawPos, width, height, color = (255,255,255)):
        self.data = pygame.Surface((width, height), pygame.SRCALPHA)
        self.data.fill(color)
        self.drawPos = drawPos

    def setColor(self, color = (0,0,0)):
        self.data.fill(color)

    def getPixel(self):
        return self.data
    
    def getDrawPos(self):
        return self.drawPos


class PixelBuilder(object):
    """
    A class to help with predictive aiding
    for health bars. Draws pixels from a list.
    """
    def __init__(self):
        #self.pixels = []
        self.changeColors = False
        self.colorTimer = 0.0
    
    def addPixel(self, lyst, drawPos, width, height, color = (255,255,255)):
        pixel = Pixel(drawPos, width, height, color)
        lyst.append(pixel)
        #self.changeColors = True

    def setColor(self, color = (0,0,0)):
        for p in self.pixels:
            p.setColor(color)

    def draw(self, drawSurface):
        for i in range(len(self.pixels)):
            pixel = self.pixels.pop(0)
            drawSurface.blit(pixel.getPixel(), pixel.getDrawPos())

    def update(self, seconds):
        self.colorTimer += seconds
        if self.changeColors:
            if self.colorTimer >= 0.2:
                self.setColor()
                self.colorTiemr = 0.0
                self.changeColors = False