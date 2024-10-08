from . import Drawable, Animated, QuestIcon, IconManager, InteractIcon, HudImageManager
from utils import SpriteManager, SCALE, RESOLUTION, vec, rectAdd, SoundManager, SPEECH, ICON, INV, FLAGS
import pygame

class NonPlayer(Animated):
    """
    Non playable objects with an additional collision rect for interaction w/ player
    """

    def __init__(self, position = vec(0,0), fileName="", offset=None, mobster = False, nFrames = 6, fps = 8):
        super().__init__(position, fileName, offset)
        self.nFrames = nFrames
        self.framesPerSecond = fps
        self.interacted = False
        self.animate = False
        self.interactable = False
        self.interactIcon = InteractIcon((self.position[0],self.position[1]-16))
        self.drop = False
        self.disappear = False
        self.id = ""
        self.ignoreCollision = False

        self.mobster = mobster

    def updateIconPos(self):
        self.interactIcon.position = (self.position[0], self.position[1] - 16)

    def getInteractionRect(self):
        oldRect = self.getCollisionRect()
        newRect = pygame.Rect((oldRect.bottomleft),(oldRect.width,5))
        return newRect
    
    
        
    def draw(self, drawSurface, drawHitbox = False, drawIcon = True):
        super().draw(drawSurface, drawHitbox)
        if drawHitbox:
            interaction = rectAdd(-Drawable.CAMERA_OFFSET, self.getInteractionRect())
            pygame.draw.rect(drawSurface, (255,255,255), interaction, 1)
        if drawIcon:
            if self.interactable:
                self.updateIconPos()
                self.interactIcon.draw(drawSurface)

    def interact(self, player):
        pass

    def startMobster(self, engine):
        engine.displayText("Y/NWant to battle?")
        engine.selectedItem = "mobster"

    def vanish(self, lst):
        lst.pop(lst.index(self))
        return lst
    
    def setInteractable(self):
        self.interactable = True

    def update(self, seconds):
        super().update(seconds)
        if self.interactable:
            IconManager.update(self.interactIcon, seconds)

class Chest(NonPlayer):
    """
    Your typical chest. Remains
    opened once opened.
    """
    def __init__(self, position = vec(0,0), text = SPEECH["null"], icon = None):
        super().__init__(position, "Objects.png", (0,1))
        self.icon = icon
        #self.interactIcon = QuestIcon((self.position[0], self.position[1] -16))
        self.text = text

    def interact(self, engine):#drawSurface
        if self.interacted:
            engine.displayText("Empty.", large = False)

        else:
            self.interacted = True
            self.image = SpriteManager.getInstance().getSprite("Objects.png", (1,1))
            SoundManager.getInstance().playSFX("click1.wav")
            SoundManager.getInstance().playSFX("click2.wav")
            if self.icon != None:
                engine.displayText(self.text, self.icon)
                ##Plant
                if self.icon == ICON["plant"]:
                    INV["plant"] += 1
                ##Bombofauns
                elif self.icon == ICON["bombo"]:
                    if INV["hasBombo"] == False:
                        INV["hasBombo"] = True
                        return
                    else:
                        INV["maxBombo"] += 5
                        INV["bombo"] = INV["maxBombo"]
            else:
                engine.displayText(self.text)


class Sign(NonPlayer):
    def __init__(self, position = vec(0,0), text = SPEECH["null"], icon = None):
        super().__init__(position, "Objects.png", (1,2))
        self.text = text
        self.icon = icon

    def interact(self, engine):
        if self.icon:
            engine.displayText(self.text, icon = self.icon, box=3)
        else:
            engine.displayText(self.text, box=3)

class DarkCloak(NonPlayer):
    def __init__(self, position = vec(0,0), text = SPEECH["null"]):
        super().__init__(position, "npc_boner.png", (0,0),nFrames=6)
        self.text = text
        self.animate = True
        self.icon = (0,1)
    
    def interact(self, engine):
        self.interacted = True
        engine.displayText(self.text, self.icon)

class Grave(NonPlayer):
    def __init__(self, position = vec(0,0), text = SPEECH["null"]):
        super().__init__(position, "Objects.png", (7,0))
        self.text = text
    
    def interact(self, engine):
        engine.displayText(self.text)

class NpcBopper(NonPlayer):
    def __init__(self, position = vec(0,0), text = SPEECH["null"]):
        super().__init__(position, "npcBopper.png", (0,0))
        self.animate = True
        self.nFrames = 8
        self.framesPerSecond = 12
        self.text = text
    
    def interact(self, engine):
        engine.displayText(self.text)

    def getInteractionRect(self):
        return pygame.Rect((self.position[0]-2, self.position[1]), (20, 20))

class Barrier(NonPlayer):
    def __init__(self, position = vec(0,0), element = 0):
        super().__init__(position, "barrier.png", (0,element))
        if element == 0:
            self.text = SPEECH["ice"]
        elif element == 1:
            self.text = SPEECH["fire"]
            self.framesPerSecond = 8
            self.row = 1
        elif element == 2:
            self.text = SPEECH["thunder"]
            self.framesPerSecond = 40
            self.row = 2
        else:
            self.text = SPEECH["wind"]
            self.row = 3


    def interact(self,engine):
        engine.displayText(self.text)

class Blessing(NonPlayer):
    def __init__(self, position = vec(0,0), element=0):
        #0 -> ice
        #1 -> fire
        #2 -> thunder
        #3 -> wind
        super().__init__(position, "blessing.png", (0,element))
        if element == 1:
            self.cost = INV["frostCost"]
            self.text = "Y/NUpgrade ice for "+str(self.cost)+ " shards?"
            self.row = 1
        elif element == 0:
            self.cost = INV["flameCost"]
            self.text = "Y/NUpgrade flames for "+str(self.cost)+ " shards?"
            self.framesPerSecond = 8
            self.row = 0
        elif element == 2:
            self.cost = INV["boltCost"]
            self.text = "Y/NUpgrade bolt for "+str(self.cost)+ " shards?"
            self.framesPerSecond = 20
            self.row = 2

        else:
            self.cost = INV["galeCost"]
            self.text = "Y/NUpgrade wind for "+str(self.cost)+ " shards?"
            self.row = 3

        self.animate = True
        self.nFrames = 4
        self.element = element


    def updateCost(self):
        if self.element == 0:
            self.cost = INV["flameCost"]
            self.text = "Y/NUpgrade fire for "+str(self.cost)+ " shards?"
        elif self.element == 1:
            self.cost = INV["frostCost"]
            self.text = "Y/NUpgrade ice for "+str(self.cost)+ " shards?"
        elif self.element == 2:
            self.cost = INV["boltCost"]
            self.text = "Y/NUpgrade thunder for "+str(self.cost)+ " shards?"
        elif self.element == 3:
            self.cost = INV["galeCost"]
            self.text = "Y/NUpgrade wind for "+str(self.cost)+ " shards?"
    
    def getCollisionRect(self):
        return super().getCollisionRect()
    
    def interact(self, engine):
        engine.selectedItem = self.element
        engine.displayText(self.text)

class Mage(NonPlayer):
    def __init__(self, position = vec(0,0), text = SPEECH["null"], fps = 1):
        super().__init__(position, "mage.png", (0,0))
        self.animate = True
        self.framesPerSecond = fps
        self.nFrames = 2
        self.text = text
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+2, self.position[1]+5), (13,15))
    
    def interact(self, engine):
        engine.displayText(self.text)
    
    def update(self, seconds):
        super().update(seconds)

class Geemer(NonPlayer):
    def __init__(self, position = vec(0,0), text = SPEECH["null"], variant = None, maxCount = 0, fps = 16, color = 0, hungry = False, feedText = "", mobster = False):
        super().__init__(position, "geemer.png", (0, color), mobster=mobster)
        self.interactIcon.position = (self.position[0]+3, self.position[1]-16)
        self.vel = vec(0,0)
        self.position = position
        self.text = text
        self.row = color
        self.nFrames = 6
        self.animate = True
        self.framesPerSecond = fps
        self.hungry = hungry
        self.feedText = feedText
        self.fead = not hungry
        
        self.ignoreCollision = False
        self.max = maxCount
        self.variant = variant #Repeats same line of text over and over
        self.dialogueCounter = 0 #Helpful for displaying multiple different conversations
        self.icon = ICON["geemer"+str(color)]

    
    def updateIconPos(self):
        self.interactIcon.position = (self.position[0]+3, self.position[1] - 16)

    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+3, self.position[1]+2),(16,16))
    
    def getInteractionRect(self):
        return pygame.Rect((self.position[0]-1,self.position[1]+9), (24,11))
    
    def set_text(self, text=""):
        """
        For when characters display different dialogue after interaction
        """
        if text != "":
            self.text = text
        elif (self.interacted and (self.variant != None)):
            
            if self.dialogueCounter > self.max:
                self.dialogueCounter = 0

            if self.dialogueCounter == 0:
                if self.variant == 0:
                    self.text = SPEECH["intro_geemer1"]
                elif self.variant == 1:
                    self.text = SPEECH["intro_switches2"]
                elif self.variant == 2:
                    self.text = SPEECH["intro_plantgeemer3"]
                return
            
            elif self.dialogueCounter == 1:
                if self.variant == 0:
                    self.text = SPEECH["intro_geemer2"]

            elif self.dialogueCounter == 2:
                if self.variant == 0:
                    self.text = SPEECH["intro_geemer3"]
                return
            

    def interact(self, engine):
        if self.variant == "dispo":
            if INV["plant"] >= 1:
                self.text = SPEECH["flame_roll"]
            else:
                self.text = SPEECH["flame_dispo"]
            engine.displayText(self.text, self.icon)
            engine.selectedItem = "roll"
            return
        
        if not self.interacted:
            #Display based on variant and inventory
            if self.variant == 2:
                if INV["plant"] >= 1:
                    self.interacted = True
                    self.text = SPEECH["intro_plantgeemer2"]
                    INV["plant"] -= 1
                    self.ignoreCollision = True
                    self.framesPerSecond = 2
                    self.vel = vec(10, 0)
                else:
                    engine.displayText(self.text, self.icon)
                    return

            elif self.variant == 0 and not INV["shoot"]:
                INV["shoot"] = True
                self.interacted = True

            else:
                self.interacted = True
        elif self.hungry and INV["plant"] >= 1:
            engine.displayText(self.feedText)
            self.fead = True
            self.ignoreCollision = True
            self.framesPerSecond = 5
            self.vel = vec(10, 0)
            INV["plant"] -= 1
            self.text = self.feedText
            return
        
        elif (self.variant != None):
            self.set_text()
            self.dialogueCounter += 1

        engine.displayText(self.text, self.icon)
       
    
    def update(self, seconds):
        super().update(seconds)
        self.position += self.vel * seconds





"""
Pickups/replenishables
- instant recharge on thunderclap
- fill up wind meter
- health
- temporary infinite recharge
"""
class Drop(NonPlayer):
    """
    Parent class for item pickups
    """
    def __init__(self, position=vec(0,0), row=0, lifeTime=5):
        super().__init__(position, "drops.png", (0,row))
        self.id = ""
        self.timer = 0
        self.row = row
        self.drop = True
        self.nFrames = 4
        self.animate = True
        self.framesPerSecond = 8
        self.disappear = False
        self.lifeTime = lifeTime
    
    def setInteractable(self):
        pass
    
    """
    param drawIcon should always be false
    """
    def draw(self, drawSurf, drawIcon = False):
        if self.timer >= self.lifeTime-2:
            temp = self.lifeTime-2
            if (self.timer >= temp and self.timer <= temp+0.2) or (self.timer >= temp+0.4 and self.timer <= temp+0.6) or (self.timer >= temp+0.8 and self.timer <= temp+1.0) or (self.timer >= temp+1.2 and self.timer <= temp+1.4) or (self.timer >= temp+1.6 and self.timer <= temp+1.8):
                pass
            else:
                super().draw(drawSurf)
        else:
            super().draw(drawSurf)

    def interact(self, player):
        self.interacted = True

    
    def update(self, seconds):
        super().update(seconds)
        if self.lifeTime > 0:
            self.timer += seconds
            if self.timer >= self.lifeTime:
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


class GreenHeart(NonPlayer):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "drops.png", (0,5))
        self.animate = True
        self.row = 5
        self.nFrames = 4
        self.framesPerSecond = 8
        self.id = "greenHeart"
        self.ignoreCollision = True

    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+1), (16,14))
    
    def draw(self, drawSurface, drawHitbox = False, drawIcon = True):
        NonPlayer.draw(self, drawSurface, drawHitbox, drawIcon)

    def getInteractionRect(self):
        oldRect = self.getCollisionRect()
        newRect = pygame.Rect((oldRect.bottomleft),(oldRect.width,5))
        return pygame.Rect((self.position[0]-2, self.position[1]-2), (20,20))
    
    def interact(self, engine):
        if not self.interacted:
            SoundManager.getInstance().playSFX("solve.wav")
            self.interacted = True
            INV["max_hp"] += 1
            engine.healPlayer(INV["max_hp"])
            if not FLAGS[5]:
                FLAGS[5] = True
                engine.displayText("This is an [Emerald Heart]!&&\nYour maximum HP will go\n    up by 1 point!\nEach boss in Majestus will\ndrop a heart upon defeat.\nCan you defeat them all?&&\n")
            else:
                engine.displayText("Got an Emerald Heart!&&\n  Your maximum HP has\n   increased by 1!\n")
            engine.disappear(self)
    

class Buck(Drop):
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

class ShopItem(NonPlayer):
    def __init__(self, position=vec(0, 0), fileName="", offset=None, animate = False, row = 0, nFrames=6, fps=8, display = False):
        super().__init__(position, fileName, offset, nFrames=nFrames, fps=fps)
        self.display = display
        self.animate = animate
        self.row = row


class Potion(ShopItem):
    """
    Potion in the shop
    """
    def __init__(self, position=vec(0,0), display = False):
        super().__init__(position, "shop_items.png", (0,0), animate=True, nFrames=4, fps=8, display=display)

    def getInteractionRect(self):
        return pygame.Rect((self.position[0]-2, self.position[1]), (20, 20))
    
    def interact(self, engine):
        ##Displays in the shop
        if self.display:
            engine.displayText("A small potion.&&\nSmells like cherries.\nWashington would be proud.\n")
            return
        
        if INV["money"] < 5:
            engine.displayText("Not enough cash...&&\n")
        elif INV["potion"] <= 8:
            engine.displayText("Y/NSmall potion for 5 bucks?")
            engine.selectedItem = "potion"
        
        else:
            engine.displayText("Sorry, but you can't carry\nany more of those.\n")

class Smoothie(ShopItem):
    """
    Delectable Smoothie!
    """
    def __init__(self, position=vec(0,0), display = False):
        super().__init__(position, "shop_items.png", (0,1), animate=True, row=1, nFrames=4, fps=8, display=display)
    
    def getInteractionRect(self):
        return pygame.Rect((self.position[0]-2, self.position[1]), (20, 18))
    
    def interact(self, engine):
        if self.display:
            engine.displayText("A delectable smoothie!\nStraw lickin' good!\n")
            return
        if INV["money"] < 20:
            engine.displayText("A smoothie! Don't you\nwish you had 20 bucks?\n")
        elif INV["smoothie"] <= 8:
            engine.displayText("Y/N20 bucks for a smoothie?\n")
            engine.selectedItem = "smoothie"
        
        else:
            engine.displayText("Sorry, but you can't carry\nany more of those.\n")


class ShopKey(ShopItem):
    def __init__(self, position=vec(0,0), display = False):
        super().__init__(position, "drops.png", (0,3), animate=True, row=3, nFrames=4, fps=8, display= display)

    def getInteractionRect(self):
        return pygame.Rect((self.position[0]-2, self.position[1]), (20, 18))
    
    def interact(self, engine):
        if self.display:
            engine.displayText("A key that'll unlock\nmany locks in Majestus.\n")
            return
        if INV["money"] < 30:
            engine.displayText("Sorry. It's 30 bucks if\nyou want that key.\n")
        elif INV["keys"] <= 8:
            engine.displayText("Y/N30 bucks for that key?")
            engine.selectedItem = "key"
        else:
            engine.displayText("Sorry, but you can't carry\nany more of those.\n")


class Syringe(ShopItem):
    """
    Syringe for display
    """
    def __init__(self, position = vec(0,0), display = False):
        super().__init__(position, "Objects.png", (6,2), animate = False, display=display)
    
    def getInteractionRect(self):
        return pygame.Rect((self.position[0]-2, self.position[1]), (20, 18))
    
    def interact(self, engine):
        if self.display:
            engine.displayText("It appears to be an\nextensively used syringe.\nYou could probably use it\nto drain your own blood.\nFortune does indeed favor\nthe brave after all...\n")
            return
        if INV["syringe"]:
            engine.displayText("I already sold you\nmy special syringe.\n")
        elif INV["money"] < 50:
            engine.displayText("Not enough for my syringe.&&\n")
        else:
            engine.displayText("Y/NThat's my special syringe.&&\nI'll sell it for 50 bucks.\n")
            engine.selectedItem = "syringe"

class ChanceEmblem(NonPlayer):
    """
    Delectable Smoothie!
    """
    def __init__(self, position):
        super().__init__(position, "Objects.png", (6,3))
    
    def getInteractionRect(self):
        return pygame.Rect((self.position[0]-2, self.position[1]), (20, 18))
    
    def interact(self, engine):
        if INV["chanceEmblem"]:
            engine.displayText("Sorry, but you already\nown a chance emblem.\n")
        elif INV["money"] < 60:
            engine.displayText("This sparkling, gold emblem\nprotects those who wear it.\nCome back when you\nhave 60 bucks.\n")
        else:
            engine.displayText("Y/NThis emblem will save you\nfrom death, granting you\na second chance at life\nafter taking fatal damage.\nHow bout it? 60 bucks:\n")
            engine.selectedItem = "emblem"
            
    