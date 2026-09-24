from . import Drawable, Animated, QuestIcon, IconManager, InteractIcon, HudManager
from utils import SpriteManager, SCALE, RESOLUTION, vec, rectAdd, SoundManager, SPEECH, ICON, INV, FLAGS
import pygame

class Drop(Animated):
    """
    Parent class for item pickups
    """
    def __init__(self, position=vec(0,0),
                 row=0, nFrames = 4, life_time=5,
                 fps = 8, ignore_collision = False):
        super().__init__(position, "drops.png", (0,row), nFrames, fps)
        
        # self.position[0] -= self.get_width() // 2

        self.id = ""
        self.ignore_collision = ignore_collision
        self.timer = 0.0
        self.row = row
        self.nFrames = nFrames
        self.animate = True
        self.fps = fps
        self.disappear = False
        self.life_time = life_time
        self.interacted = False
    
    def get_width(self):
        """Return the width of the drop's image"""
        return self.image.get_width()
    
    def draw(self, drawSurf, drawIcon = False):
        """Draw the drop's image"""
        if self.disappear:
            return
        
        if self.timer >= self.life_time-2:
            temp = self.life_time-2
            if (self.timer >= temp and self.timer <= temp+0.2) or (self.timer >= temp+0.4 and self.timer <= temp+0.6) or (self.timer >= temp+0.8 and self.timer <= temp+1.0) or (self.timer >= temp+1.2 and self.timer <= temp+1.4) or (self.timer >= temp+1.6 and self.timer <= temp+1.8):
                pass
            else:
                super().draw(drawSurf)
        else:
            super().draw(drawSurf)

    def collect(self, player):
        """Collect the drop"""
        self.collected = True
    
    def update(self, seconds):
        """Update the drop"""
        if self.disappear:
            return
        
        super().update(seconds)
        if self.life_time > 0:
            self.timer += seconds
            if self.timer >= self.life_time:
                self.disappear = True
        
class Frost(Drop):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, (0))

class Bombodrop(Drop):
    def __init__(self, position=vec(0,0)):
        super().__init__(position, 8)
        self.id = "bombo"
    
    def getCollisionRect(self):
        return pygame.Rect(self.position[0]+1, self.position[1]+1, 14,15)
    
    def interact(self, player):
        if INV["hasBombo"]:
            if not self.interacted:
                SoundManager.getInstance().playLowSFX("solve.wav", volume = 0.3)
                self.interacted = True
                if INV["bombo"] < INV["maxBombo"]:
                    INV["bombo"] += 2
                    if INV["bombo"] > INV["maxBombo"]:
                        INV["bombo"] = INV["maxBombo"]

class LargeBombo(Drop):
    def __init__(self, position=vec(0,0)):
        super().__init__(position, 9)
        self.id = "bombo"
    
    def getCollisionRect(self):
        return pygame.Rect(self.position[0]+1, self.position[1]+1, 14,15)
    
    def interact(self, player):
        if INV["hasBombo"]:
            if not self.interacted:
                SoundManager.getInstance().playLowSFX("solve.wav", volume = 0.3)
                self.interacted = True
                if INV["bombo"] < INV["maxBombo"]:
                    INV["bombo"] += 5
                    if INV["bombo"] > INV["maxBombo"]:
                        INV["bombo"] = INV["maxBombo"]

class GiantBombo(Drop):
    def __init__(self, position=vec(0,0)):
        super().__init__(position, 10)
        self.id = "bombo"
    
    def getCollisionRect(self):
        return pygame.Rect(self.position[0]+1, self.position[1]+1, 14,15)
    
    def interact(self, player):
        if INV["hasBombo"]:
            if not self.interacted:
                SoundManager.getInstance().playLowSFX("solve.wav", volume = 0.3)
                self.interacted = True
                if INV["bombo"] < INV["maxBombo"]:
                    INV["bombo"] += 20
                    if INV["bombo"] > INV["maxBombo"]:
                        INV["bombo"] = INV["maxBombo"]

class Heart(Drop):
    def __init__(self, position=vec(0,0)):
        super().__init__(position, 0)
        self.id = "heart"
        self.disappear = False
        
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+3,self.position[1]+5), (10,8))
    
    
    def interact(self, player):
        if not self.interacted:
            SoundManager.getInstance().playLowSFX("solve.wav", volume = 0.3)
            self.interacted = True
            if player.hp < INV["max_hp"]:
                player.hp += 1


    def update(self, seconds):
        super().update(seconds)

class BigHeart(Drop):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, 4, lifeTime=8)
        self.id = "bigHeart"
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+1), (16,14))
    
    def interact(self, player):
        if not self.interacted:
            SoundManager.getInstance().playSFX("solve.wav")
            self.interacted = True
            if player.hp < INV["max_hp"]:
                player.hp += 5
                if player.hp > INV["max_hp"]: 
                    player.hp = INV["max_hp"]
    

class Buck(Drop):
    """The agreed upon currency used inside Majestus"""
    def __init__(self, position = vec(0,0)):
        super().__init__(position, 1)
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+3), (16,10))
    
    def interact(self, player):
        if not self.interacted:
            SoundManager.getInstance().playLowSFX("buck.wav")
            self.interacted = True
            if INV["money"] < INV["wallet"]:
                INV["money"] += 1
                if INV["money"] > INV["wallet"]:
                    INV["money"] = INV["wallet"]

class Buck_R(Drop):
    """Worth 10 Bucks"""
    def __init__(self, position = vec(0,0)):
        super().__init__(position, 7)
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+3), (16,10))
    
    def interact(self, player):
        if not self.interacted:
            SoundManager.getInstance().playSFX("buck.wav")
            self.interacted = True
            if INV["money"] < INV["wallet"]:
                INV["money"] += 10
                if INV["money"] > INV["wallet"]:
                    INV["money"] = INV["wallet"]

class Buck_B(Drop):
    """Worth 5 Bucks"""
    def __init__(self, position = vec(0,0)):
        super().__init__(position, 6)
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+3), (16,10))
    
    def interact(self, player):
        if not self.interacted:
            SoundManager.getInstance().playSFX("buck.wav")
            self.interacted = True
            if INV["money"] < INV["wallet"]:
                INV["money"] += 5
                if INV["money"] > INV["wallet"]:
                    INV["money"] = INV["wallet"]
            
class FireShard(Drop):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, 2, lifeTime=20)

    def interact(self, player):
        if not self.interacted:
            SoundManager.getInstance().playSFX("Z2_beam.wav")
            self.interacted = True
            if INV["flameShard"] < 999:
                INV["flameShard"] += 1
            
            


class Key(Drop):
    """
    Parent class for item pickups
    """
    def __init__(self, position=vec(0,0)):
        super().__init__(position, 3)
        self.text = SPEECH["key"]

    def interact(self, player, engine):
        if not self.interacted:
            self.interacted = True
            INV["keys"] += 1
            engine.displayText(self.text)
    
    def update(self, seconds):
        ##Keys dont disappear after their lifetime
        Animated.update(self, seconds)