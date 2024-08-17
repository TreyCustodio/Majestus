from . import (Drawable, Animated, Bullet, Element, Blizzard, Heart, BigHeart, 
                Buck, FireShard, GreenHeart, Buck_B, Buck_R, Bombodrop, LargeBombo, GiantBombo)
from utils import SoundManager, SpriteManager, SCALE, RESOLUTION, vec
from random import randint
import pygame
"""
The highest class in the enemy hierarchy.

Baller, Chiller, Viber, Rocker, Flower
"""

class Enemy(Animated):
    """
    Abstract Enemy Class
    """
    def __init__(self, position = vec(0,0), fileName: str ="", direction: int =0, nFrames: int = 6, hurtRow: int = 4, hp: int = 5, speed: int = 50, name: str = "", id: str = "", spawn = False, projectile: bool = False, damage: int = 1, type: Element = Element(0)):
        if fileName != "":
            self.image = SpriteManager.getInstance().getEnemy(fileName, direction)
        
        self.name = name
        self.id = id
        self.spawn = spawn
        self.spawning = False
        self.vanish = False
        self.ignoreCollision = False
        self.top = False #Boolean that controls what layer the enemy is drawn on
        self.hit = False
        self.frameTimer = 0.0
        #Animation properties
        self.indicatorRow = 0
        self.fileName = fileName
        self.row = direction
        self.frame = 0
        self.nFrames = nFrames
        self.totalFrames = nFrames
        self.animate = True
        self.framesPerSecond = 8
        self.animationTimer = 0
        self.FSManimated = None

        self.hurtRow = hurtRow
        self.freezeShield = False
        self.arrowShield = False
        self.arrowWeak = False
        self.position = vec(*position)
        self.vel = vec(0,0)
        self.speed = speed
        self.dead = False
        self.fakeDead = False
        self.flashTimer = 0
        self.initialPos = vec(*position)#position
        self.initialDir = direction
        self.walkTimer = 0
        self.walking = False
        self.freezeTimer = 4.2
        self.frozen = True
        self.belowDrops = False #Draw below drops
        #self.freeze(playSound=False)
        self.maxHp = hp
        self.hp = 5
        self.readyToDrop = False
        self.bouncing = False
        self.bounceTimer = 0.0
        self.inWall = False
        self.injury = 0
        ##Strengths and Weaknesses
        #0 -> Neutral
        #1 -> Fire
        #2 -> Ice
        #3 -> Thunder
        #4 -> Wind
        self.shield = 0
        self.type = type
        self.dying = False
        self.projectile = projectile
        self.damage = damage
        self.attacking = False
        self.attackTimer = 0.0
        self.rot = 0 #Rotation angle
    
    def increaseCount(self):
        return True
    
    def setImage(self, frame = None, row = None):
        if frame == None:
            frame = self.frame
        if row == None:
            row = self.row
        self.image = SpriteManager.getInstance().getSprite(self.fileName, (frame, row))

    def doesCollideBlock(self, block):
        return self.doesCollide(block)

    def boundsSafety(self):
        return True
    
    def doesCollideProjectile(self, projectile):
        return self.doesCollide(projectile)
    
    def setSpeed(self, row):
        if row == 0 or row == 4:
            self.vel[1] = self.speed
            self.vel[0] = 0
            
        elif row == 1 or row == 5:
            self.vel[0] = self.speed
            self.vel[1] = 0
            
        elif row == 2 or row == 6:
            self.vel[1] = -self.speed
            self.vel[0] = 0
        
        elif row == 3 or row == 7:
            self.vel[0] = -self.speed
            self.vel[1] = 0

    def getDamage(self):
        return self.damage

    def getObjectsToSpawn(self):
        return self.objects
    
    def getDrop(self):
        integer = randint(0,2)
        if integer == 0:
            return Heart((self.position[0]+3, self.position[1]+5))
        elif integer == 1:
            return Buck((self.position[0]+3, self.position[1]+5))
        elif integer == 2:
            return Buck_B((self.position[0]+3, self.position[1]+5))
    
    def getMoney(self):
        integer = randint(0,10)
        if integer == 1:
            return Buck((self.position[0]+3, self.position[1]+5))
        else:
            return Buck_B((self.position[0]+3, self.position[1]+5))
    
    def getInjury(self):
        return self.injury
    
    def resetInjury(self):
        self.injury = False

    def getCollisionRect(self):
        newRect = pygame.Rect(0,0,14,23)
        newRect.left = int(self.position[0]+2)
        newRect.top = int(self.position[1]+2)
        return newRect
    
    def setInitialPos(self, vector):
        self.initialPos = vector
        
    def respawn(self):
        self.vel = vec(0,0)
        self.dead = False
        self.frozen = True
        self.walking = False
        self.row = self.initialDir
        self.hp = self.maxHp
        self.flashTimer = 0
        self.walkTimer = 0
        self.freezeTimer = 4.2
        self.frame = 0
        #self.freeze(playSound=False)
    
    def resetObjects(self):
        self.spawning = False

    def handleEvent(self, event):
        pass
    
    def heal(self, integer):
        diff = self.maxHp - self.hp
        if integer < diff:
            self.hp += integer
        else:
            self.hp = self.maxHp

    def draw(self, drawSurface, drawHitbox=False, use_camera=True, drawFreeze = True):
        super().draw(drawSurface)
        if drawFreeze and self.frozen:
            Drawable(vec(self.position[0] + self.getSize()[0] // 2 - 8, self.position[1] + self.getSize()[1] // 2 - 8), "freeze.png").draw(drawSurface)
    """
    Play the hurt sfx and set state to dead if hp < 0
    """
    def playHurtSound(self):
        if self.hp > 0: 
            SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
        else:
            self.dead = True
            SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)

    """
    Sets the row to the hurtRow.
    Used for enemies that move in 1 direction
    """
    def hurt(self, damage, setHit = True):

        if self.row < self.hurtRow:
            self.row = self.hurtRow
            self.flashTimer = 0
        self.frameTimer = 0.0
        self.hit = setHit
        self.hp -= damage
        self.playHurtSound()
        self.injury = damage

    """
    Adds the value of hurtRow to the row.
    Used for enemies that move in multiple directions
    and have multiple hurtRows.
    """
    def hurtMult(self, damage, setHit = True):
        if self.row < self.hurtRow:
            self.row += self.hurtRow
            self.flashTimer = 0
        self.frameTimer = 0.0
        self.hit = setHit
        self.hp -= damage
        self.injury = damage
        self.playHurtSound()

    def handlePlayerCollision(self, player):
        """
        Expects a player
        Returns True if the Enemy hurts the Player

        Will be overriden by Enemies with multiple
        collision Rects
        """
        return True



    def handleCollision(self, other = None):
        """
        Enemy gets hurt, frozen, and healed.
        Damage = other.damage
        """
        ##Freeze
        if other.type == 2 and not self.freezeShield and self.type.getValue() != 2:
            self.freeze()

        ##Damage after I-frame
        if self.row < self.hurtRow:
            if self.type.getValue() == 0:
                if other.type == 0 and self.arrowWeak:
                    self.hurt(other.damage + int(other.damage * 1.5))
                else:
                    self.hurt(other.damage)
            else:
                if other.type == self.type.getValue():
                    self.heal(other.damage)
                elif self.type.weakTo(other.type):
                    self.hurt(other.damage + int(other.damage * 1.5))
                elif other.type == 0 and not self.arrowShield:
                    if self.arrowWeak:
                        self.hurt(other.damage + int(other.damage * 1.5))
                    else:
                        self.hurt(other.damage)
                else:
                    SoundManager.getInstance().playSFX("dink.wav")

        ##Bullets damage enemies even through i frames
        elif self.type.getValue() == 0 and other.type == 0:
            if self.arrowWeak:
                self.hurt(other.damage + int(other.damage * 1.5))
            else:
                self.hurt(other.damage)
    

    def freeze(self, playSound = True):
        if self.frozen:
            self.freezeTimer = 0.0
        else:
            self.frozen = True
            self.nFrames = 1
            if playSound:
                SoundManager.getInstance().playSFX("freeze.wav")
        
    
    #intended to be modified but could be used as is
    def move(self, seconds):
        if not self.frozen:
            self.position += self.vel * seconds
            
    def bounce(self, other, setRow = True):
        if not self.frozen and not self.bouncing:
            self.bouncing = True
            side = self.calculateSide(other)
            if side == "right":
                self.vel[0] = -self.speed
                if setRow:
                    if self.row >= 4:
                        self.row = 7
                    else:
                        self.row = 3
            elif side == "top":
                self.vel[1] = self.speed
                if setRow:
                    if self.row >= 4:
                        self.row = 4
                    else:
                        self.row = 0
            elif side == "left":
                self.vel[0] = self.speed
                if setRow:
                    if self.row >= 4:
                        self.row = 5
                    else:
                        self.row = 1
            elif side == "bottom":
                self.vel[1] = -self.speed
                if setRow:
                    if self.row >= 4:
                        self.row = 6
                    else:
                        self.row = 2

    def changeDirection(self):
        #Square code: 0 (down), 3 (left), 2 (up), 1 (right)
        if self.row == 0:
            self.row = 3
        elif self.row == 4:
            self.row = 7
        elif self.row == 3:
            self.row = 2
        elif self.row == 7:
            self.row = 6
        elif self.row == 2:
            self.row = 1
        elif self.row == 6:
            self.row = 5
        elif self.row == 1:
            self.row = 0
        elif self.row == 5:
            self.row = 4
        
    def calculateSide(self, object):
        ##  Colliding with Block    ##
        collision1 = self.getCollisionRect()
        collision2 = object.getCollisionRect()
        clipRect = collision1.clip(collision2)
        ##Calculate the side
        side = ""
        if clipRect.width < clipRect.height:
            #X direction
            if collision2.collidepoint(collision1.right,collision1.top) or collision2.collidepoint(collision1.right, collision1.bottom):
                side = "right"
            else:
                side = "left"
        else:
            #Y direction
            if collision2.collidepoint(collision1.right, collision1.top) or collision2.collidepoint(collision1.left,collision1.top):
                side = "top"
            else:
                side = "bottom"
        return side
    
    def unfreeze(self, seconds):
        if self.frozen:
            self.freezeTimer += seconds
            if self.freezeTimer >= 5.0:
                self.frozen = False
                self.freezeTimer = 0.0
                self.nFrames = self.totalFrames
                self.setSpeed(self.row)
    
    def updateFlash(self, seconds):
        if self.row >= self.hurtRow:
            self.flashTimer += seconds
            if self.flashTimer >= 0.4:
                self.row -= self.hurtRow

    
    def update(self, seconds, position = None, player = None, rotate = False, scale = False):
        if self.dead:
        #Add death animation here if self.hp = 0
            pass

        if self.bouncing:
            if not self.inWall:
                self.bouncing = False
        
        self.unfreeze(seconds)
        if rotate:
            super().rotateEnemy(seconds)
        else:
            super().updateEnemy(seconds)
        self.updateFlash(seconds)

        if scale:
            self.image = pygame.transform.scale(self.image, (32,32))
        ##Move
        self.move(seconds)




"""
Bosses
"""

class LavaKnight(Enemy):
    def __init__(self, position=vec(0,0), fall = False, boss = True):
        """
        Position of shadow does not move unless
        the knight moves its position.
        Moving its position is not the same as
        jumping up or down.
        """
        super().__init__(position, "knight.png", 0)
        self.name = "LavaKnight"
        self.id = "spawn"
        self.boss = boss
        ##Startup animation
        self.starting = False
        self.vibrationTick = 0
        self.startupTimer = 0.0
        self.fallTimer = 0.0 #timer for off screen
        self.shaking = False #vibrating bool
        self.moving = False #done with animation
        self.respawning = False
        self.falling = False
        self.targetPos = vec(0,0)

        self.desperate = False #True if final phase is active
        self.damage = 2
        self.nFrames = 1
        self.maxHp = 100
        self.hp = self.maxHp
        self.freezeShield = True
        self.jumpingUp = False
        self.jumpingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

        self.frozen = False
        self.jumpTimer = 0.5
        self.pause = True
        self.speed = 30
        self.freezeCounter = 10 #Once this gets to zero, it becomes vulnerable to Bombofauns
        self.maxCount = 10 #The maximum integer the freezeCount can be
        self.cold = False #Able to be blown up
        self.coldTimer = 0.0
        self.maxColdTime = 5.0
        self.vulnerable = False #Able to be frozen
        self.iframeTimer = 0.0
        self.shadow = Animated(vec(self.position[0], self.position[1]), "knight.png", (4,0))
        self.shadow.frame = 4
        self.xVals = [] #list of possible positions in the collisionRect
        self.yVals = []
        self.frameTimer = 0.0
        self.frameTime = 0.05
        self.frame = 3
        self.currentRow = 0
        self.initializing = True
        self.objects = []

        self.dying = False
        self.setImage()

    def getDrop(self):
        return GreenHeart((self.position[0]+16, self.position[1]+16))
    
    def getMoney(self):
        return self.getDrop()
    
    def boundsSafety(self):
        return False
    def setObjects(self):
        self.objects = [
            FireBall(vec(self.position[0]-8, self.position[1]), 2),
            FireBall(vec(self.position[0]+32, self.position[1]), 4),
            FireBall(vec(self.position[0]+32, self.position[1]+32), 0),
            FireBall(vec(self.position[0]-8, self.position[1]+32), 5)
        ]

    def resetObjects(self):
        self.spawning = False
    
    def setPosition(self, vector):
        vector2 = vec(vector[0], vector[1])
        self.position = vector
        self.shadow.position = vector2

    def reset(self):
        self.frozen = False
        self.starting = False
        self.vibrationTick = 0
        self.startupTimer = 0.0
        self.fallTimer = 0.0 #timer for off screen
        self.shaking = False #vibrating bool
        self.moving = False #done with animation
        self.respawning = False
        self.falling = False
        self.targetPos = vec(0,0)
        self.desperate = False #True if final phase is active
        self.hp = self.maxHp
        self.jumpingUp = False
        self.jumpingDown = False
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False
        self.frozen = False
        self.jumpTimer = 0.5
        self.pause = True
        self.freezeCounter = self.maxCount #Once this gets to zero, it becomes vulnerable to Bombofauns
        self.cold = False #Able to be blown up
        self.coldTimer = 0.0
        self.vulnerable = False #Able to be frozen
        self.iframeTimer = 0.0
        self.shadow.frame = 4
        self.xVals = [] #list of possible positions in the collisionRect
        self.yVals = []
        self.frameTimer = 0.0
        self.frameTime = 0.05
        self.frame = 3
        self.currentRow = 0
        self.initializing = True
        self.objects = []
        self.dying = False
        self.setImage()
        self.setPosition(vec(RESOLUTION[0]//2-16, RESOLUTION[1]//2-16))

    #override
    def hurt(self, damage, setHit = True):
        self.hit = setHit
        self.hp -= damage
        self.injury = damage
        if self.desperate:
            if self.hp <= 0:
                self.dying = True
                self.ignoreCollision = True
            else:
                SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)

        elif self.hp <= 0:
            self.desperate = True
            self.maxColdTime = 2.0
            self.hp = 25
            self.unsetCold()
        else:
            SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
        

    def bounce(self, other):
        if not self.cold and not self.falling and not self.respawning:
            self.fullStop()
            self.respawning = True
    
    def startRespawn(self):
        SoundManager.getInstance().playSFX("big_jump.wav")
        self.fullStop()
        self.ignoreCollision = True
        self.respawning = True
        self.top = True

    def fullStop(self):
        self.stop()
        self.jumpingUp = False
        self.jumpingDown = False
        self.jumpTimer = 0.0

    def stop(self):
        self.movingLeft = False
        self.movingRight = False
        self.movingUp = False
        self.movingDown = False

    def setCold(self):
        self.cold = True
        self.movingDown = False
        self.movingUp = False
        self.movingLeft = False
        self.movingRight = False
        self.row = 4
        self.currentRow = 4
        self.frame = 0
        self.setImage()
    
    def unsetCold(self):
        self.coldTimer = 0.0
        self.cold = False
        self.vulnerable = False
        self.freezeCounter = self.maxCount
        self.fullStop()
        self.respawning = True
        self.top = True
        self.row = 0
        self.currentRow = 0
        self.frame = 0
        self.frameTime = 0.05
        self.setImage()
    
    def stopMotion(self, position):
        self.setCollisionRange()
        if int(position[1]) in self.yVals:
            self.movingUp = False
            self.movingDown = False
        if int(position[0]) in self.xVals:
            self.movingRight = False
            self.movingLeft = False

    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+8), (32,24))
    def getStartupRect(self):
        return pygame.Rect((self.position[0]-200, self.position[1]+32), (400, 24))
    
    def getShadowRect(self):
        return pygame.Rect((self.shadow.position[0] + 7, self.shadow.position[1] + 27), (19,5))
    
    def setImage(self):
        self.image = SpriteManager.getInstance().getSprite("knight.png", (self.frame, self.row))
    
    def incrementFrame(self):
        self.frame += 1
        self.frame %= 3

    def draw(self, drawSurface):
        super().draw(drawSurface, False)
    
    def drawTop(self, drawSurface):
        self.shadow.draw(drawSurface)
        super().draw(drawSurface)

    """
    Only damage player when on the ground
    """
    def handlePlayerCollision(self, player):
        if self.ignoreCollision:
            return False
        else:
            return True
    
    def knockBack(self, other):
        ##Calculate side method is messed up.
        ##Properties of left and right are inversed
        side = self.calculateSide(other)
        if side == "left":
            self.setActualPos(0, False, 10)
        elif side == "top":
            self.setActualPos(1, True, 10)
        elif side == "right":
            self.setActualPos(0, True, 10)
        elif side == "bottom":
            self.setActualPos(1, False, 10)

    def handleCollision(self, other=None):
        if self.cold:
            if other.id == "bombo":
                #self.knockBack(other)
                self.hurt(other.damage)
                if not self.dying and self.coldTimer >= self.maxColdTime:
                    
                    self.unsetCold()
            return
        
        if not self.ignoreCollision:
            if self.vulnerable and other.id == "blizz":
                self.row = 5
                self.vulnerable = False
                self.freezeCounter -= 1
                self.frameTime += 0.05
                if self.freezeCounter <= 0:
                    self.setCold()
                    SoundManager.getInstance().playSFX("freeze.wav")
                else:
                    SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
                    if self.freezeCounter == 3:
                        self.currentRow = 3
                        self.setImage()
                    elif self.freezeCounter == 5:
                        self.currenRow = 2
                        self.setImage()
                    elif self.freezeCounter == 8:
                        self.currentRow = 1
                        self.setImage()
                    else:
                        pass
    
    def setTargetPos(self, position):
        if self.respawning:
            self.targetPos = vec(int(position[0]-8), int(position[1]-8))
        else:
            self.targetPos = vec(int(position[0]), int(position[1]+16))

    def setCollisionRange(self):
        self.xVals = []
        self.yVals = []
        pos = self.getShadowRect().topleft
        for i in range(19):
            self.xVals.append(pos[0] + i)
        for i in range(5):
            self.yVals.append(pos[1] + i)
        
        
    """
    Sets the position of the shadow and the knight
    """
    def setActualPos(self, axis = 0, add = True, value = 1, seconds = -1):
        if seconds == -1:
            if add:
                self.position[axis] += value
                self.shadow.position[axis] += value
            else:
                self.position[axis] -= value
                self.shadow.position[axis] -= value
        else:
            if add:
                self.vel[axis] = 200
            else:
                self.vel[axis] = -200
            self.position += self.vel * seconds
    """
    The knight chooses which direction 
    to move based on the player's position.

    position -> player's current position
    """
    def setDirection(self, position):
        if self.cold:
            return
        
        if int(position[0]) < int(self.position[0] + 16):
            self.movingLeft = True
            self.movingRight = False
        
        elif int(position [0]) > int(self.position[0] + 16):
            self.movingRight = True
            self.movingLeft = False

        if int(position[1]) < int(self.position[1] + 32):
            self.movingUp = True
            self.movingDown = False
        
        elif int(position [1]) > int(self.position[1] + 32):
            self.movingDown = True
            self.movingUp = False
    
    
    """
    Begin to fall down and crush the player
    """
    def crush(self):
        self.vel = vec(0,0)
        self.jumpingUp = False
        self.jumpingDown = True
        self.jumpTimer = 0.0
        

    def update(self, seconds, position = None, player = None):
        if self.cold:
            self.coldTimer += seconds
        ##Death Animation
        if self.dying:
            if self.startupTimer >= 1.0:
                if self.startupTimer >= 3.0:
                    if self.frame == 4:
                        self.startupTimer += seconds
                        if self.startupTimer >= 3.1:
                            self.dead = True
                            SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)
                    else:
                        self.frameTimer += seconds
                        if self.frameTimer >= 0.1:
                            self.frameTimer = 0.0
                            self.frame += 1
                            self.setImage()
                else:
                    self.startupTimer += seconds
                    if self.vibrationTick == 0:
                        self.setActualPos(0, True)
                        self.vibrationTick += 1
                        SoundManager.getInstance().playSFX("LA_Rock_Push.wav")
                    elif self.vibrationTick == 1:
                        self.setActualPos(0, False)
                        self.vibrationTick += 1
                    elif self.vibrationTick == 2:
                        self.setActualPos(0, False)
                        self.vibrationTick += 1
                    elif self.vibrationTick == 3:
                        self.setActualPos(0, True)
                        self.vibrationTick = 0
            else:
                self.startupTimer += seconds
            return

        ##Startup Animation
        if not self.moving:
            if self.starting:
                if not self.shaking:
                    self.startupTimer += seconds
                    if self.startupTimer >= 0.2:
                        self.startupTimer = 0.0
                        self.shaking = True
                else:
                    if self.startupTimer >= 2:
                        self.vibrationTick = 0
                        SoundManager.getInstance().stopSFX("LA_Rock_Push.wav")
                        self.frame = 0
                        self.setImage()
                        self.startupTimer += seconds
                        if self.startupTimer >= 3:
                            self.moving = True
                            self.startupTimer = 0.0
                    else:
                        self.startupTimer += seconds
                        if self.vibrationTick == 0:
                            SoundManager.getInstance().playSFX("LA_Rock_Push.wav")
                            self.setActualPos(0, True)
                            self.vibrationTick += 1
                        elif self.vibrationTick == 1:
                            self.setActualPos(0, False)
                            self.vibrationTick += 1
                        elif self.vibrationTick == 2:
                            self.setActualPos(0, False)
                            self.vibrationTick += 1
                        elif self.vibrationTick == 3:
                            self.setActualPos(0, True)
                            self.vibrationTick = 0
                        return
                return
            elif self.getStartupRect().collidepoint(position):
                self.starting = True

        else:
            
            ##Frame update
            if not self.cold and self.frame < 3:
                self.frameTimer += seconds
                if not self.vulnerable:
                    if self.frameTimer >= 0.01:
                        self.frameTimer = 0.0
                        self.incrementFrame()
                        self.setImage()
                else: 
                    if self.frameTimer >= self.frameTime:
                        self.frameTimer = 0.0
                        self.incrementFrame()
                        self.setImage()
            if self.initializing:
                return
            ##I-frame update
            if self.moving and not self.vulnerable:
                self.iframeTimer += seconds
                if self.iframeTimer >= 0.6:
                    self.vulnerable = True
                    self.iframeTimer = 0.0
                    self.row = self.currentRow
                    self.setImage()

            ##Respawn off screen
            if self.respawning and not self.pause:
                if self.falling:
                    ##Shadow reappears
                    if self.top:
                        if self.shadow.frame == 4:
                            self.fallTimer += seconds
                            ##Falling down
                            if self.fallTimer >= 0.2:
                                self.position[1] += 12
                                ##Crashed
                                if self.position[1] >= self.targetPos[1]:
                                    SoundManager.getInstance().stopAllSFX()                            
                                    SoundManager.getInstance().playSFX("crash.wav")
                                    self.position[1] = self.targetPos[1]
                                    self.falling = False
                                    self.top = False
                                    self.fallTimer = 0.0
                                    self.respawning = False
                                    self.pause = True
                                    if self.desperate:
                                        self.spawning = True
                                        self.setObjects()
                        ##Decrement shadow frame
                        else:
                            self.shadow.frame -= 1
                            self.shadow.image = SpriteManager.getInstance().getSprite("knight.png", (self.shadow.frame, 0))

                    ##Off screen, ready to set target
                    else:
                        self.fallTimer += seconds
                        if self.fallTimer >= 1.0:
                            self.fallTimer = 0.0
                            self.setTargetPos(position)
                            self.shadow.position = self.targetPos
                            self.position[0] = self.targetPos[0]
                            self.shadow.position[0] = self.targetPos[0]
                            self.top = True
                
                ##Jumping up  
                else:
                    self.position[1] -= 4
                    if self.position[1] + 32 <= -64:
                        self.shadow.frame += 1
                        self.shadow.frame %= 7
                        if self.shadow.frame == 0:
                            self.shadow.frame = 6
                            self.top = False
                            self.falling = True
                        self.shadow.image = SpriteManager.getInstance().getSprite("knight.png", (self.shadow.frame, 0))
                return
            
            
            
            ##Mid air movement
            if not self.pause:
                ##Jumping up
                self.jumpTimer += seconds
                if self.jumpingUp:
                    self.ignoreCollision = True
                    if self.position[1] <= self.shadow.position[1]-8:
                        self.setCollisionRange()
                        ##Player inside collision rect (able to be crushed)
                        if self.getCollisionRect().collidepoint((position[0]+8, position[1])):
                            self.crush()
                        
                        if self.jumpTimer >= 0.5 or (self.targetPos[0] in self.xVals and self.targetPos[1] in self.yVals):
                            self.crush()
                            
                        else:
                            if self.targetPos[1] < self.yVals[0]:
                                self.setActualPos(1, False, 2)
                            elif self.targetPos[1] > self.yVals[-1]:
                                self.setActualPos(1, True, 2)
                            
                            if self.targetPos[0] < self.xVals[0]:
                                self.setActualPos(0, False, 2)
                            elif self.targetPos[0] > self.xVals[-1]:
                                self.setActualPos(0, True, 2)

                        if self.cold:
                            if self.jumpTimer >= 0.1:
                                self.jumpingUp = False
                                self.jumpingDown = True
                                self.jumpTimer = 0.0
                    else:
                        self.position[1] -= 2

                    
                
                ##Falling down
                elif self.jumpingDown:
                    self.ignoreCollision = True
                    if self.cold:
                        self.position[1] += 6
                    else:
                        self.position[1] += 4
                    if self.position[1] >= self.shadow.position[1]:
                        SoundManager.getInstance().stopAllSFX()
                        SoundManager.getInstance().playSFX("crash.wav")
                        self.position[1] = self.shadow.position[1]
                        self.pause = True
                        self.top = False
                        self.jumpingDown = False
                        self.jumpTimer = 0.0
                        return

            ##Ground (no movement)
            else:
                self.ignoreCollision = False
                self.jumpTimer += seconds
                if self.jumpTimer >= 0.8:
                    self.jumpTimer = 0.0
                    self.pause = False
                    if self.desperate:
                        if self.cold:
                            self.setTargetPos(position)
                            SoundManager.getInstance().playSFX("big_jump.wav")
                            self.top = True
                            self.jumpingUp = True
                        else:
                            self.startRespawn()
                    else:
                        self.setTargetPos(position)
                        SoundManager.getInstance().playSFX("big_jump.wav")
                        self.top = True
                        self.jumpingUp = True
        


        
"""
Regular Enemies
"""        
class Shiver(Enemy):
    def __init__(self, position = vec(0,0), direction = 0):
        if direction == 2:
            super().__init__(position, "shiver.png", 2)
        else:
            super().__init__(position, "shiver.png", 0)
        
        self.maxHp = 30
        self.hp = self.maxHp
        self.hurtRow = 0
        self.blowing = False
        self.nFrames = 4
        self.totalFrames = 4
        self.framesPerSecond = 4
        self.damage = 2
        self.type = Element(2)
        self.hurtRow = 1
    
    def setSpeed(self, row):
        return
    

class Gleemer(Enemy):
    def __init__(self, position=vec(0, 0), fileName="gleemer.png"):
        super().__init__(position, fileName, speed = 0, nFrames=6, id="shot", hurtRow=0, spawn=True)
        self.id = "shot"

        self.damage = 0
        self.row = 0
        self.direction = 1
        self.freezeShield = True
        self.ready = True
        self.timer = 0.0

    def setSpeed(self, row):
        return
    
    def bounce(self, other):
        return
    
    def getObjectsToSpawn(self):
        SoundManager.getInstance().playSFX("laser.wav")
        self.ready = False
        #return [FireBall(self.position)]
        return [Laser(vec(self.position[0] + 18, self.position[1] + 9))]
    
    def hurt(self, damage, setHit=True):
        return
    
    def draw(self, drawSurface, drawHitbox=False, use_camera=True, drawFreeze=True):
        return super().draw(drawSurface, drawHitbox, use_camera, False)
    
    def update(self, seconds, position=None, player = None):
        super().update(seconds, position)
        if player.getDirection() == 3:
            self.spawning = False
        else:
            if self.ready:
                for i in range(10):
                    if int(position[1] + i) == int(self.position[1]) or int(position[1] - i) == int(self.position[1]):
                        self.spawning = True
                        return
            elif self.spawning:
                self.spawning = False
        
        if not self.ready:
            self.timer += seconds
            if self.timer >= 0.5:
                self.timer = 0.0
                self.ready = True
            
"""
Change name to Boner.
Sticks to its square-shaped walking route.
Throws a bone at you everytime you attack it.
Weak to arrow.
"""
class Mofos(Enemy):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, "mofos.png", direction, spawn=True)
        self.framesPerSecond = 20
        self.indicatorRow = 3
        self.speed = 20
        self.maxHp = 30
        self.hp = self.maxHp
        self.damage = 1
        self.hurtRow = 4
        self.arrowWeak = True
        self.player_row = 0
        self.current_row = self.row

    
    def bounce(self, other):
        return super().bounce(other, True)

    def getObjectsToSpawn(self):
        
        if not self.frozen:
            row = self.row
            self.setImage(0,row)
            self.attacking = True
            if row == 0 + 4:
                self.row = self.current_row
                return [Bone(vec(self.position[0], self.position[1]), vel=vec(0,200), angle=90)]
            elif row == 1 + 4:
                self.row = self.current_row
                return [Bone(vec(self.position[0], self.position[1]), vel = vec(200,0))]
            elif row == 2 + 4:
                self.row = self.current_row
                return [Bone(vec(self.position[0], self.position[1]), vel = vec(0, -200), angle=90)]
            elif row == 3 + 4:
                self.row = self.current_row
                return [Bone(vec(self.position[0], self.position[1]), vel = vec(-200,0))]
            

    def hurt(self, damage, setHit = True):
        
        self.spawning = True
        super().hurtMult(damage, setHit)
        self.current_row = self.row
        self.row = self.player_row + 4

    #override
    def move(self, seconds):
        
        
        if not self.frozen and not self.spawning:
            if self.frame == 5:
                self.changeDirection()
                self.setSpeed(self.row)
                self.frame = 0
            self.position += self.vel * seconds

    #override
    def updateFlash(self, seconds):
        if self.row >= 4:
            self.flashTimer += seconds
            if self.flashTimer >= 0.4:
                self.row -= 4

    def update(self, seconds, position = None, player = None):
        if self.attacking:
            self.attackTimer += seconds
            if self.attackTimer >= 0.2:
                self.attacking = False
                self.attackTimer = 0.0
            return
        self.player_row = player.getOppositeDirection()
        super().update(seconds)


"""
A fire version of the skeller/boner.
Needs to be frozen in order to damage it.
Similar to how you have to freeze the LavaKnight
before you can damage it.
"""
class FireMofos(Mofos):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, direction)

    def getDrop(self):
        return FireShard((self.position[0]+3, self.position[1]+5))     
       
"""
Dancing plants that always drop bombofauns.
"""
class Bopper(Enemy):
    def __init__(self, position):
        super().__init__(position, "bopper.png")
        self.hurtRow = 1
        self.nFrames = 8
        self.totalFrames = 8
        self.maxHp = 2
        self.hp = self.maxHp
        self.damage = 1
        self.speed = 0
        self.regenTimer = 0.0
        self.belowDrops = True
        self.freezeShield = True

    def handleCollision(self, other=None):
        if not self.fakeDead:
            super().handleCollision(other)

    def handlePlayerCollision(self, player):
        if not self.fakeDead:
            super().handlePlayerCollision(player)
    

    def getDrop(self):
        if self.readyToDrop:
            self.readyToDrop = False
            rand = randint(0,8)
            if rand == 0 or rand == 1 or rand == 2 or rand == 3:
                return Bombodrop(self.position)
            elif rand == 4 or rand == 5 or rand == 6:
                return LargeBombo(self.position)
            elif rand == 7 or rand == 8:
                return GiantBombo(self.position)
            
    
    def playHurtSound(self):
        if self.hp > 0: 
            SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
        else:
            self.ignoreCollision = True
            self.fakeDead = True
            self.readyToDrop = True
            self.row = 2
            self.frame = 0
            self.image = SpriteManager.getInstance().getSprite(self.fileName, (0,2))
            SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)

    def update(self, seconds, position = None, player = None):
        if self.fakeDead:
            self.regenTimer += seconds
            if self.regenTimer >= 4.0:
                self.row = 0
                self.frame = 0
                self.image = SpriteManager.getInstance().getSprite(self.fileName, (0,0))
                self.hp = self.maxHp
                self.fakeDead = False
                self.ignoreCollision = False
                self.regenTimer = 0.0
        else:
            super().update(seconds)

class Stomper(Enemy):
    def __init__(self, position=vec(0,0), boss = False):
        super().__init__(position, "stomper.png")
        self.hurtRow = 1
        self.nFrames = 1
        if boss:
            self.maxHp = 50
        else:
            self.maxHp = 25
        self.hp = self.maxHp
        self.freezeShield = True
        self.frozen = False
        self.cold = False
        self.coldTimer = 0.0
        self.coldTime = 5.0
        self.damage = 2
        self.speed = 0
        self.freezeCounter = 5
        self.maxCount = 5
        self.vulnerable = True
        self.iframeTimer = 0.0
        self.frameTimer = 0.0
        self.shadow = Animated(vec(self.position[0], self.position[1]), "stomper.png", (0,3))
        self.jumpTimer = 0.0
        self.pause = True
        self.falling = False
        self.secondsPerFrame = 0.3
        self.targetPos = vec(0,0)
        self.boss = boss

        self.initialPos = self.position

    def respawn(self):
        self.vel = vec(0,0)
        self.cold = False
        self.jumpTimer = 0.0
        self.falling = False
        self.pause = True
        self.coldTimer = 0.0
        self.freezeCounter = 5
        self.dead = False
        self.walking = False
        self.row = self.initialDir
        self.hp = self.maxHp
        self.flashTimer = 0
        self.walkTimer = 0
        self.freezeTimer = 4.2
        self.setPosition(self.initialPos)

    def bounce(self, other):
        return
    
    def drawTop(self, drawSurface):
        self.shadow.draw(drawSurface)
        super().draw(drawSurface)

    def getDrop(self):
        if self.boss:
            return GreenHeart((self.position[0]+9, self.position[1]+13))
        else:
            return FireShard((self.position[0]+9, self.position[1]+13))
    
    """
    Great example of why you need attention to detail
    for objects in memory.
    If you assign both positions to the same vector,
    whenever you change 1 position, it changes both.
    """
    def setPosition(self, vector):

        """ 
        Incorrect code
        self.position = vector
        self.shadow.position = vector
        """
        self.position = vector
        vec2 = vec(vector[0], vector[1])
        self.shadow.position = vec2

    def setActualPos(self, axis, add = True, integer = 1):
        if add:
            self.position[axis] += integer
            self.shadow.position[axis] += integer
        else:
            self.position[axis] -= integer
            self.shadow.position[axis] -= integer


    def hurt(self, damage, setHit = True):
        if self.coldTimer >= self.coldTime:
            self.unsetCold()
        self.hit = setHit
        self.hp -= damage
        self.injury = damage
        if self.hp <= 0:
            self.dead = True
            if not self.boss:
                SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)
        else:
            SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)

    def handlePlayerCollision(self, player):
        if self.ignoreCollision:
            return False
        else:
            return True
    
    def setCold(self):
        self.vulnerable = True
        self.cold = True
        SoundManager.getInstance().playSFX("freeze.wav")
        self.row = 2
        self.setImage()
    
    def unsetCold(self):
        self.coldTimer = 0.0
        self.cold = False
        self.row = 0
        self.setImage()
        self.freezeCounter = self.maxCount

    def handleCollision(self, other=None):
        if self.cold:
            if other.id == "bombo":
                self.hurt(other.damage)
        elif not self.ignoreCollision:
            if self.vulnerable and other.id == "blizz":
                self.vulnerable = False
                self.row = 1
                self.secondsPerFrame = 0.01
                self.setImage()
                self.freezeCounter -= 1
                if self.freezeCounter <= 0:
                    self.setCold()
                else:
                    SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)

    def setImage(self):
        self.image = SpriteManager.getInstance().getSprite(self.fileName, (self.frame, self.row))


    def setTargetPos(self, position):
        self.targetPos = vec(int(position[0]), int(position[1])-8)


    def move(self):
        if int(self.targetPos[0]) > int(self.position[0]):
            self.setActualPos(0, True, 1)
        elif int(self.targetPos[0]) < int(self.position[0]):
            self.setActualPos(0, False, 1)
        
        if int(self.targetPos[1]) > int(self.position[1]):
            self.setActualPos(1, True, 1)
        elif int(self.targetPos[1]) < int(self.position[1]):
            self.setActualPos(1, False, 1)
        
        ##If its above the player, fall = True, jumpTimer = 0.0
    def setFrame(self):
        self.frame += 1
        self.frame %= 3

    def update(self, seconds, position = None, player = None):
        if self.cold:
            if self.coldTimer < self.coldTime:
                self.coldTimer += seconds
        if not self.vulnerable:
            self.frameTimer += seconds
            if self.frameTimer >= 0.01:
                self.frameTimer = 0.0
                self.setFrame()
                self.setImage()
        ##I-frame update
        if not self.vulnerable:
            self.iframeTimer += seconds
            if self.iframeTimer >= 0.6:
                self.row = 0
                self.vulnerable = True
                self.iframeTimer = 0.0
                self.secondsPerFrame = 0.3
                if self.falling or self.pause:
                    self.frame = 0
                else:
                    self.frame = 1
                self.setImage()
        
        ##Fall and crush the player
        if self.falling:
            if self.position[1] >= self.shadow.position[1]:
                self.position[1] = self.shadow.position[1]
                SoundManager.getInstance().playSFX("crash.wav")
                self.falling = False
                self.top = False
                self.ignoreCollision = False
                self.pause = True
            else:
                self.position[1] += 2

            return


        if not self.pause:
            ##Jump up until its above the shadow
            if self.position[1] <= self.shadow.position[1] - 8:
                self.jumpTimer += seconds
                if self.cold:
                    if self.jumpTimer >= 0.2:
                        self.frame = 0
                        self.setImage()
                        self.falling = True
                        self.jumpTimer = 0.0
                    else:
                        self.move()
                else:
                    if self.jumpTimer >= 0.5:
                        self.frame = 0
                        self.setImage()
                        self.falling = True
                        self.jumpTimer = 0.0
                    else:
                        ##Mid-air movement
                        self.move()
            else:
                self.position[1] -= 2
        else:
            self.jumpTimer += seconds
            if self.jumpTimer >= 0.5:
                SoundManager.getInstance().playSFX("big_jump.wav")
                self.unPause(position)
    
    def unPause(self, position):
        self.setTargetPos(position)
        self.frame = 1
        self.setImage()
        self.top = True
        self.ignoreCollision = True
        self.pause = False
        self.jumpTimer = 0.0

class FireBall(Enemy):
    def __init__(self, position=vec(0,0), direction=0):
        super().__init__(position, "fireball.png")
        self.id = "noStop"
        self.extinguishing = False
        self.hurtRow = 0
        self.damage = 1
        self.nFrames = 4
        self.maxHp = 1
        self.hp = 1
        self.type = Element(1)
        self.arrowShield = True
        self.lifeTimer = 0.0
        self.lifeTime = 1.25
        self.frozen = False
        self.motionTick = 0
        self.direction = direction
        self.angle = 0
        self.secondsPerFrame = 0.0

    def respawn(self):
        self.vanish = True

    def increaseCount(self):
        return False
    
    def boundsSafety(self):
        return False
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+2, self.position[1] + 3), (12,11))
    
    def bounce(self, other):
        return
    
    def setSpeed(self, row):
        return
    
    def getDrop(self):
        return

    def extinguish(self):
        self.extinguishing = True
        self.ignoreCollision = True
        self.row = 1
        self.secondsPerFrame = 0.04

    def update(self, seconds, position=None, player = None):
        if not self.extinguishing:
            if self.frozen:
                self.extinguish()
            else:
                if self.lifeTimer >= self.lifeTime:
                    self.extinguish()
                else:
                    self.lifeTimer += seconds
        
        
        if not self.extinguishing:
            if self.direction == 0:
                if self.motionTick == 0:
                    self.position[0] += 1
                    self.motionTick = 1
                elif self.motionTick == 1:
                    self.position[0] += 1
                    self.position[1] += 1
                    self.motionTick = 2
                elif self.motionTick == 2:
                    self.position[0] += 1
                    self.motionTick = 0
            elif self.direction == 5:
                if self.motionTick == 0:
                    self.position[0] -= 1
                    self.motionTick = 1
                elif self.motionTick == 1:
                    self.position[0] -= 1
                    self.position[1] += 1
                    self.motionTick = 2
                elif self.motionTick == 2:
                    self.position[0] -= 1
                    self.motionTick = 0
            elif self.direction == 4:
                if self.motionTick == 0:
                    self.position[0] += 1
                    self.motionTick = 1
                elif self.motionTick == 1:
                    self.position[0] += 1
                    self.position[1] -= 1
                    self.motionTick = 2
                elif self.motionTick == 2:
                    self.position[0] += 1
                    self.motionTick = 0
            elif self.direction == 2:
                if self.motionTick == 0:
                    self.position[0] -= 1
                    self.motionTick = 1
                elif self.motionTick == 1:
                    self.position[0] -= 1
                    self.position[1] -= 1
                    self.motionTick = 2
                elif self.motionTick == 2:
                    self.position[0] -= 1
                    self.motionTick = 0
            elif self.direction == 1:
                if self.motionTick == 0:
                    self.position[1] += 1
                    self.motionTick = 1
                elif self.motionTick == 1:
                    self.position[1] += 1
                    self.position[0] -= 1
                    self.motionTick = 2
                elif self.motionTick == 2:
                    self.position[1] += 1
                    self.motionTick = 0
            elif self.direction == 3:
                if self.motionTick == 0:
                    self.position[1] -= 1
                    self.motionTick = 1
                elif self.motionTick == 1:
                    self.position[1] -= 1
                    self.position[0] += 1
                    self.motionTick = 2
                elif self.motionTick == 2:
                    self.position[1] -= 1
                    self.motionTick = 0

        if self.frameTimer >= self.secondsPerFrame:
            self.frameTimer = 0.0
            if self.extinguishing:
                self.frame += 1
                if self.frame == 5:
                    self.dead = True
                else:
                    self.setImage()
            self.angle += 90
            self.angle %= 360
            self.image = pygame.transform.rotate(self.image, self.angle)
        else:
            self.frameTimer += seconds

class Laser(Enemy):
    def __init__(self, position=vec(0,0), direction=1, vel = vec(500,0)):
        super().__init__(position, "laser.png", nFrames=3, projectile=True)
        self.row = 0
        self.id = "noStop"
        self.hurtRow = 0
        self.damage = 1
        self.maxHp = 1
        self.hp = 1
        self.vel = vel
        self.arrowShield = True
        self.lifeTimer = 0.0
        self.lifeTime = 1.25
        self.frozen = False
        self.motionTick = 0
        self.direction = direction
        self.angle = 0
        self.secondsPerFrame = 0.0
    
    def setSpeed(self, row):
        return
    
    def getDrop(self):
        return None
    
    def bounce(self, other, setRow=True):
        self.dead = True

    def hurt(self, damage, setHit=True):
        return
    
    def update(self, seconds, position=None, player = None):
        return super().update(seconds, position)

class Projectile(Enemy):
    def __init__(self, position=vec(0,0), fileName = "", nFrames = 3, damage = 1, hp = 1, vel = vec(100,0), rotate = False, spf: float = 0.0):
        super().__init__(position, fileName, nFrames = nFrames, projectile=True, hp=hp, damage=damage)
        self.vel = vel
        self.frozen = False
        self.secondsPerFrame = spf
        if rotate:
            self.rotating = rotate
            self.angle = 0
        
    def rotate(self, seconds):
        self.frameTimer += seconds
        if self.frameTimer >= self.secondsPerFrame:
            self.frameTimer = 0.0
            self.angle += 90
            self.angle %= 180
            self.image = pygame.transform.rotate(self.image, self.angle)

class Bone(Projectile):
    def __init__(self, position=vec(0, 0), vel = vec(0,0), angle = 0):
        super().__init__(position, "bone.png", nFrames = 1, damage = 1, hp = 1, vel = vel, spf=0.2)
        self.angle = angle
        if angle > 0:
            self.image = pygame.transform.rotate(self.image, self.angle)

    def hurt(self, damage, setHit=True):
        self.dead = True
    
    def bounce(self, other, setRow=True):
        self.dead = True

    def getDrop(self):
        return
    
    def update(self, seconds, position=None, player=None):
        #super().update(seconds, position, player)
        self.position += self.vel * seconds
        #self.image = pygame.transform.rotate(self.image, self.angle)

class Heater(Enemy):
    def __init__(self, position=vec(0,0)):
        super().__init__(position, "heater.png")
        self.id = "spawn"
        self.spawning = False
        self.hurtRow = 0
        self.damage = 1
        self.nFrames = 34
        self.totalFrames = 3
        self.maxHp = 10
        self.hp = self.maxHp
        self.type = Element(1)
        self.fireBallTimer = 0.0
        self.fireBallTime = 0.5
        self.objects = [FireBall(vec(self.position[0]-2, self.position[1]))]
        self.ballDirection = 0
        self.frozen = False
        self.extinguishing = False
        self.igniting = False

    def freeze(self, playSound = True):
        if self.frozen:
            return
            #self.freezeTimer = 0.01
            

        else:
            self.frozen = True
            self.freezeTimer = 0.0
            SoundManager.getInstance().playSFX("freeze.wav")

    def resetObjects(self):
        self.spawning = False
        self.ballDirection += 1
        self.ballDirection %= 5
        self.objects = [FireBall(vec(self.position[0]-2, self.position[1]), self.ballDirection)]

    def draw(self, drawSurface):
        super().draw(drawSurface)
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+2, self.position[1]+12), (18*2-4, 26*2 - 16))
    
    def getObjectsToSpawn(self):
        return self.objects
    
    def setSpeed(self, row):
        return
    
    def setImage(self):
        self.image = SpriteManager.getInstance().getSprite(self.fileName, (self.frame, self.row))
        self.image = pygame.transform.scale(self.image, (18*2,26*2))
    
    def extinguish(self):
        self.extinguishing = True
        self.row = 2
        self.frame = 0
        self.frameTimer = 0.0
        self.setImage()

    def update(self, seconds, position = None, player = None):
        
        if self.frozen:
            if not self.extinguishing and self.freezeTimer == 0.0:
                self.extinguish()
            
            if self.extinguishing:
                if self.frameTimer >= 0.03:
                    self.frameTimer = 0.0
                    self.frame += 1
                    if self.frame == 3:
                        self.row = 1
                        self.frame = 0
                        self.extinguishing = False
                        self.freezeTimer += seconds
                        self.setImage()
                    else:
                        self.setImage()
                else:
                    self.frameTimer += seconds
                return
            
            if self.igniting:
                if self.frameTimer >= 0.03:
                    self.frameTimer = 0.0
                    self.frame -= 1
                    if self.frame == -1:
                        self.row = 0
                        self.frame = 0
                        self.igniting = False
                        self.frozen = False
                        self.freezeTimer = 0.0
                        self.setImage()
                    else:
                        self.setImage()
                else:
                    self.frameTimer += seconds
                return
            
            if self.freezeTimer >= 4.0:
                self.row = 2
                self.frame = 2
                self.frameTimer = 0.0
                self.igniting = True
                self.setImage()
            elif self.freezeTimer >= 2.0:
                self.frame += 1
                self.frame %= 3
                self.setImage()
                self.freezeTimer += seconds
            else:
                self.freezeTimer += seconds

            
        else:
            if self.fireBallTimer >= self.fireBallTime:
                self.fireBallTimer = 0.0
                self.spawning = True
            else:
                self.fireBallTimer += seconds
            Animated.updateEnemy(self, seconds)
            self.setImage()
"""
Cute little walking fireball.
Requires Ice to damage it.
"""
class Baller(Enemy):
    def __init__(self, position=vec(0,0), direction = 3, hp = 10, speed = 50, type: Element = Element(1), fileName: str = "baller.png"):
        super().__init__(position, fileName, direction, hp = hp, speed = speed)
        self.indicatorRow = 8
        self.row = direction
        self.hurtRow = 4
        self.nFrames = 4
        self.totalFrames = 4
        self.direction = direction
        self.damage = 1
        self.type = type
        self.setSpeed()

    

    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+1, self.position[1]+1), (14,15))
    
    def getMoney(self):
        return self.getDrop()
    
    def getDrop(self):
        integer = randint(0,3)
        if integer == 3:
            return FireShard((self.position[0]+3, self.position[1]+5))
        elif integer == 2:
            return Heart((self.position[0]+3, self.position[1]+5))
        elif integer == 1:
            return Buck((self.position[0]+3, self.position[1]+5))
        elif integer == 0:
            return Buck_B((self.position[0]+3, self.position[1]+5))
    
    def bounce(self, other):
        Gremlin.bounce(self, other)
    

    def hurt(self, damage, setHit=True):
        return super().hurtMult(damage, setHit)
    
    def setSpeed(self, row=0):
        if self.direction == 3:
            self.vel[0] = -self.speed
        elif self.direction == 1:
            self.vel[0] = self.speed


    def update(self, seconds, position = None, player = None):
        super().update(seconds, rotate=True)

"""
Cute little walking rock.
Requires Bombofauns to damage it.
"""
class Rocker(Baller):
    def __init__(self, position=vec(0, 0), direction=3, hp = 20, speed = 35, type = Element(0)):
        super().__init__(position, direction, hp, speed, fileName="rocker.png")
        self.row = 1
        self.rot = 0
        self.rotTimer = 0.0

    def getCollisionRect(self):
        return pygame.Rect(self.position[0], self.position[1], 32,32)
    
    def bounce(self, other):
        if not self.frozen and not self.bouncing:
            side = self.calculateSide(other)
            if side == "right":
                self.position[0] = other.position[0] - self.getSize()[0] * 2
                self.vel[0] = -self.speed
                
            
            elif side == "left":
                self.position[0] = (other.position[0] + other.getSize()[0]) + (self.getSize()[0] * 2)
                self.vel[0] = self.speed
                

    def update(self, seconds, position=None, player=None):
        Enemy.update(self, seconds, position, player, rotate=True, scale=True)
        

"""
Sharp, spinning enemy that can't be damaged.
Spinners should be drawn before any other enemy
so that other enemies walk above it.
"""    
class Spinner(Enemy):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "spinner.png", 0)
        
        self.nFrames = 2#current max frames
        self.totalFrames = 2#Total frames
        self.indicatorRow = 7
        self.speed = 50
        self.maxHp = 10
        self.row = 0
        self.hp = self.maxHp
        self.damage = 1
        self.hurtRow = 0
        self.freezeShield = True
        self.framesPerSecond = 32

    def handleCollision(self, other=None):
        SoundManager.getInstance().playSFX("dink.wav")
   
    def bounce(self, other):
        pass
    
    def draw(self, drawSurface, drawHitbox=False, use_camera=True, drawFreeze=True):
        return super().draw(drawSurface, drawHitbox, use_camera, False)
    
    def updateFlash(self, seconds):
        return

    def setSpeed(self, row=0):
        return
    
    def move(self, seconds):
        MovementPatterns.diamond(self, seconds)



"""
Small creatures that fly diagonally and bounce off walls.
Come in different elemental flavors.
"""
class Flapper(Enemy):
    """
    The direction refers to the direction it moves in,
    not to be confused with the direction it faces,
    which is how direction is used for Mofos.
    Flappers always face down.
    """
    def __init__(self, position = vec(0,0), typeRow = 0, direction = 0, fileName = "flapper.png"):
        super().__init__(position, fileName, typeRow)
        self.indicatorRow = 1
        self.typeRow = typeRow
        self.row = self.typeRow
        self.speed = 70
        self.maxHp = 5
        self.hp = self.maxHp
        self.damage = 1
        self.direction = direction
        self.hurtRow = 5
        ##Set velocity based on direction
        self.setSpeed()


    def getCollisionRect(self):
        return pygame.Rect((self.position[0], self.position[1]+3), (16,12))
    

    def move(self, seconds):
        if not self.frozen:
            self.position += self.vel * seconds


    def setSpeed(self, direction=None):
        if self.direction == 0:
            self.vel[0] = self.speed
            self.vel[1] = self.speed
        elif self.direction == 1:
            self.vel[0] = self.speed
            self.vel[1] = -self.speed
        elif self.direction == 2:
            self.vel[0] = -self.speed
            self.vel[1] = -self.speed
        elif self.direction == 3:
            self.vel[0] = -self.speed
            self.vel[1] = self.speed
        else:
            return

    def bounce(self, other):
        if not self.frozen:
            self.bouncing = True
            side = self.calculateSide(other)
            if side == "right":
                self.vel[0] = -self.speed
            elif side == "top":
                self.vel[1] = self.speed
            elif side == "left":
                self.vel[0] = self.speed
            elif side == "bottom":
                self.vel[1] = -self.speed

    def updateFlash(self, seconds):
        if self.row == self.hurtRow:
            self.flashTimer += seconds
            if self.flashTimer >= 0.2:
                self.row = self.typeRow

    def update(self, seconds, position = None, player = None):
        super().update(seconds)

class FireFlapper(Flapper):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, 1, direction)
        self.type = Element(1)
        self.arrowShield = True
    
    def getDrop(self):
        integer = randint(0,5)
        if integer == 0 or integer == 1:
            return Heart((self.position[0]+3, self.position[1]+5))
        elif integer == 2 or integer == 3:
            return Buck((self.position[0]+3, self.position[1]+5))
        elif integer == 4:
            return FireShard((self.position[0]+3, self.position[1]+5))
        elif integer == 5:
            return Buck_B((self.position[0]+3, self.position[1]+5))
class IceFlapper(Flapper):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, 2, direction)
        self.type = Element(2)
    
class ThunderFlapper(Flapper):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, 3, direction)
        self.type = Element(3)

class WindFlapper(Flapper):
    def __init__(self, position = vec(0,0), direction = 0):
        super().__init__(position, 4, direction)
        self.type = Element(4)

class AlphaFlapper(Enemy):
    def __init__(self, position=vec(0,0), typeRow = 0, direction = 0, boss = False):
        super().__init__(position, "alphaflapper.png", typeRow)
        self.typeRow = typeRow
        self.speed = 20
        self.initial_speed = 20
        self.hurtRow = 1
        self.maxHp = 60
        self.hp = self.maxHp
        self.boss = boss
        self.damage = 1
        self.moving = False
        self.ignoreCollision = True
        self.secondsPerFrame = 0.1
        self.fading = False

    def reset(self, position):
        self.position = position
        self.hp = self.maxHp
        self.moving = False
        self.ignoreCollision = True
        self.speed = self.initial_speed

    def getCollisionRect(self):
        return pygame.Rect((self.position[0] + 4, self.position[1] + 8), (24,20))
    

    def draw(self, drawSurface, drawHitbox=False, use_camera=True, drawFreeze=True):
        if self.ignoreCollision:
            super().draw(drawSurface, drawHitbox, use_camera, False)
        else:
            super().draw(drawSurface, drawHitbox, use_camera, drawFreeze)

    def getDrop(self):
        return GreenHeart((self.position[0]+16, self.position[1]+16))
    
    

    def move(self, seconds):
        if self.moving:
            Flapper.move(self, seconds)
    
    def adjustVelocity(self):
        if self.vel[0] > 0:
            self.vel[0] = self.speed
        elif self.vel[0] > 0:
            self.vel[0] = -self.speed
        if self.vel[1] > 0:
            self.vel[1] = self.speed
        elif self.vel[1] > 0:
            self.vel[1] = -self.speed
    
 
    def playHurtSound(self):
        if self.hp > 0: 
            SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
        else:
            SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
            self.dying = True
            self.frame = 0
            self.row = 2
            self.setImage()
            

    def hurt(self, damage, setHit=True):
        super().hurt(damage, setHit)
        self.speed += (self.injury * 2)
        self.adjustVelocity()

    def setSpeed(self, direction):
        Flapper.setSpeed(self, direction)
    
    def bounce(self, other):
        Flapper.bounce(self, other)

    def update(self, seconds, position=None, player = None):
        if self.dying:
            ##Fading away
            if self.fading:
                if self.frameTimer >= self.secondsPerFrame:
                    self.frameTimer = 0.0
                    self.frame += 1
                    if self.frame == 4:
                        SoundManager.getInstance().playLowSFX("enemydies.wav", volume = 0.2)
                        self.fading = False
                        self.dying = False
                        self.dead = True
                    else:
                        self.setImage()
                else:
                    self.frameTimer += seconds

            ##Turning gray
            else:
                if self.frameTimer >= self.secondsPerFrame:
                    self.frameTimer = 0.0
                    self.frame += 1
                    if self.frame == 6:
                        self.fading = True
                        self.frame = 0
                        self.row = 3
                        self.setImage()
                    else:
                        self.setImage()
                else:
                    self.frameTimer += seconds
            return
        super().update(seconds)

    def updateFlash(self, seconds):
        Flapper.updateFlash(self, seconds)

"""
Puffs up and damages the player if they
get too close. Must be damaged with
ranged attacks.
"""
class Puffer(Enemy):
    
    def __init__(self, position):
        pass
    
    def puff(self):
        pass

"""
Runs across the screen when you enter his
line of sight. Immune to elemental attacks.
"""
class David(Enemy):
    
    def __init__(self, position, direction = 1, boss = False):
        super().__init__(position, "david.png", direction)
        self.indicatorRow = 2
        self.nFrames = 1
        self.totalFrames = 1
        self.speed = 200
        self.maxHp = 30
        self.hp = self.maxHp
        self.damage = 1
        self.running = False
        self.freezeShield = True
        self.ready = True
        self.boss = boss

    def getDrop(self):
        return BigHeart((self.position[0]+3, self.position[1]+5))

    def doesCollideProjectile(self, other):
        return self.getHitBox().colliderect(other.getCollisionRect())

    def doesCollideBlock(self, block):
        if self.getHitBox().colliderect(block.getCollisionRect()):
            return True
        else:
            return False
        
    def getCollisionRect(self):
        if self.row == 1 or self.row == 5:
            return pygame.Rect((self.position), (64, 26))
        elif self.row == 3 or self.row == 7:
            return pygame.Rect((self.position[0] - (64-19), self.position[1]), (64, 26))

    def getHitBox(self):
        return pygame.Rect((self.position), (19,26))
    
    def getRunRect(self):
        if self.row == 1:
            return pygame.Rect((self.position[0] + 19, self.position[1]), (64, 26))
        elif self.row == 3:
            return pygame.Rect((self.position[0] - 64, self.position[1]), (64-19, 26))
        
    def run(self):
        if not self.running:
            self.running = True
            self.nFrames = 3
            self.totalFrames = 3
            
            if self.row == 1 or self.row == 5:
                self.vel[0] = self.speed
            elif self.row == 3 or self.row == 7:
                self.vel[0] = -self.speed
        

    def move(self, seconds):
        if self.running:
            self.position += self.vel * seconds
    
    def updateFlash(self, seconds):
        if self.row >= 4:
            self.flashTimer += seconds
            if self.flashTimer >= 0.5:
                self.row -= 4


    def handlePlayerCollision(self, player):
        """
        Hurts the player if it collides with its hitbox
        Runs at the player if it collides with its runRect
        """
        if self.row < 4:
            if self.getRunRect().colliderect(player.getCollisionRect()):#player collides with runRect
                if not self.running:
                    SoundManager.getInstance().playSFX("run.wav")
                self.run()
                
                

            else:
                player.handleCollision(self)
    

    def handleCollision(self, other):
        """
        Only gets damaged by arrows
        """
        if not self.running and other.type == 0:
            if self.row < self.hurtRow:
                self.row += self.hurtRow
                self.flashTimer = 0
                self.hp -= other.damage
                if self.hp > 0:
                    SoundManager.getInstance().playSFX("david.wav")
                    self.run()
                    
                else:
                    self.dead = True


    def bounce(self, other):
        """
        David turns around once he collides with a wall.
        Logic gets a little iffy here.
        """
        if self.running == False:#Stopped
            
            ##If he's in the wall
            if self.getHitBox().colliderect(other.getCollisionRect()):
                ##Get him out the wall
                if self.row == 3:
                    self.position[0] -= 1

                elif self.row == 1:
                    self.position[0] += 1

        
        else:##Runs first, stop movement, reset animation
            self.running = False
            self.totalFrames = 1
            self.nFrames = 1
            self.vel = vec(0,0)
            if self.row == 1:
                self.row = 3
            elif self.row == 3:
                self.row = 1

        



    def update(self, seconds, position = None, player = None):
        if self.dead:
        #Add death animation here if self.hp = 0
            pass

        self.unfreeze(seconds)


        super().update(seconds)

        self.updateFlash(seconds)

        ##Move
        self.move(seconds)



"""
Grimers walk across the screen and change direction
upon colliding with a wall.
Come in a few different flavors.
"""
class Gremlin(Enemy):
    def __init__(self, position = vec(0,0), direction = 1, fileName = "gremlin.png"):
        super().__init__(position, fileName, direction)
        self.indicatorRow = 4
        self.speed = 50
        self.maxHp = 15
        self.hp = self.maxHp
        self.damage = 1
    
    def getCollisionRect(self):
        newRect = pygame.Rect(0,0,12,34)
        newRect.left = int(self.position[0]+3)
        newRect.top = int(self.position[1]+1)
        return newRect

    
    def bounce(self, other):
        if not self.frozen and not self.bouncing:
            side = self.calculateSide(other)
            if side == "right":
                self.position[0] = other.position[0] - self.getSize()[0]
                self.vel[0] = -self.speed
                if self.row == 1:
                    self.row = 3
                elif self.row == 5:
                    self.row = 7
            
            elif side == "left":
                self.position[0] = (other.position[0] + other.getSize()[0]) + (self.getSize()[0] * 2)
                self.vel[0] = self.speed
                if self.row == 3:
                    self.row = 1
                elif self.row == 7:
                    self.row = 5

    
    def hurt(self, damage, setHit=True):
        return super().hurtMult(damage, setHit)

        
class GremlinB(Gremlin):
    def __init__(self, position= vec(0,0), direction = 1):
        super().__init__(position, direction, "gremlin_blue.png")
        self.maxHp = 30
        self.hp = 30
        self.damage = 2
        self.speed = 75

    def getMoney(self):
        return Buck_R((self.position[0]+3, self.position[1]+5))
    
    def getDrop(self):
        integer = randint(0,1)
        if integer == 0:
            return BigHeart((self.position[0]+3, self.position[1]+5))
        elif integer == 1:
            return Buck_R((self.position[0]+3, self.position[1]+5))


"""
Dipshots require ranged attacks to be damaged.
"""
class Dummy(Enemy):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "dummy.png", 0)
        self.id = "shot"
        self.indicatorRow = 5
        self.freezeShield = True
        self.nFrames = 1
        self.totalFrames = 1
        self.speed = 0
        self.maxHp = 5
        self.hp = self.maxHp
        self.damage = 0
        self.hurtRow = 1
    
    def getCollisionRect(self):
        return pygame.Rect(self.position, (16,16))
    
    def handleCollision(self, other):
        if other.type == 0:
            if self.row < 1:
                self.row = 1
                self.flashTimer = 0
                self.hurt(other.damage)
    
    def draw(self, drawSurface, drawHitbox=False, use_camera=True, drawFreeze=True):
        super().draw(drawSurface, drawHitbox, use_camera, False)
    #override
    def updateFlash(self, seconds):
        if self.row > 0:
            self.flashTimer += seconds
            if self.flashTimer >= 1.0:
                self.row = 0

"""
Bullshots require 20 Bombofauns to kill.
"""
class Bullshot(Enemy):
    def __init__(self, position = vec(0,0)):
        super().__init__(position, "bullshot.png")
        self.id = "shot"
        self.frozen = False
        self.freezeShield = True
        self.maxHp = 20
        self.hp = self.maxHp
        self.damage = 0
        self.vibtick = 0
    
    def getDrop(self):
        return GreenHeart((self.position[0]+8, self.position[1]+16))
    
    def getCollisionRect(self):
        return pygame.Rect((self.position[0]+4, self.position[1]+8), (24,24))
    
    def playHurtSound(self):
        if self.hp > 0: 
            SoundManager.getInstance().playLowSFX("enemyhit.wav", volume=0.5)
        else:
            self.dying = True
            SoundManager.getInstance().playSFX("LA_Rock_Push.wav")
            

    def handleCollision(self, other):
        if other.id == "bombo":
            self.hp -=1
            self.hit = True
            self.playHurtSound()
            self.injury = self.hp
    
    def update(self, seconds, position=None, player = None):
        self.frozen = False
        if self.dying:
            if self.frameTimer >= 0.2:
                self.frame += 1
                if self.frame == 10:
                    self.dead = True
                    SoundManager.getInstance().stopSFX("LA_Rock_Push.wav")
                    SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)
                    return
                else:
                    self.setImage()
            else:
                self.frameTimer += seconds

            if self.vibtick == 0:
                self.position[0] += 1
            elif self.vibtick == 1:
                self.position[0] -= 1
            elif self.vibtick == 2:
                self.position[0] -= 1
            elif self.vibtick == 3:
                self.position[0] += 1
            
            self.vibtick += 1
            self.vibtick %= 4
             


"""
Code for different movement patterns
lies below.
"""
class MovementPatterns(object):
    def changeDirectionSquare(enemy):
        if enemy.row == 0:
            enemy.row = 3
        elif enemy.row == 4:
            enemy.row = 7
        elif enemy.row == 3:
            enemy.row = 2
        elif enemy.row == 7:
            enemy.row = 6
        elif enemy.row == 2:
            enemy.row = 1
        elif enemy.row == 6:
            enemy.row = 5
        elif enemy.row == 1:
            enemy.row = 0
        elif enemy.row == 5:
           enemy.row = 4


    def diamond(enemy, seconds):
        """
        adjust enemy.frame == condition to lengthen or shrink the range
        """
        if enemy.frame == 2:
            MovementPatterns.changeDirectionSquare(enemy)
            
            if enemy.row == 0 or enemy.row == 4:
                enemy.vel[1] = enemy.speed
                
            elif enemy.row == 1 or enemy.row == 5:
                enemy.vel[0] = enemy.speed
                
            elif enemy.row == 2 or enemy.row == 6:
                enemy.vel[1] = -enemy.speed
            
            elif enemy.row == 3 or enemy.row == 7:
                enemy.vel[0] = -enemy.speed

            enemy.frame = 0
        if not enemy.frozen:
            enemy.position += enemy.vel * seconds
