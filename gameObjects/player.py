from . import Bullet, Bombo, Sword, Dummy, Drop, David, Blizzard, Clap, Hook, Slash, Animated, Enemy, Geemer, PushableBlock, NonPlayer, Block,  LockBlock, \
HealthBar

from utils import SpriteManager, SoundManager, SCALE, RESOLUTION, INV, EQUIPPED, vec, SHORTCUTS, ACTIVE_SHORTCUT
from UI import ACTIONS, EventManager
from math import ceil, sqrt
import pygame



class Player(Animated):
    def __init__(self, position=vec(0,0), direction=2, fileName = "Link.png"):
        super().__init__(position, fileName, (0, direction))
        
        #   Movement, Animation, Damage Attributes-----------------------------------------------
        self.analogTrack = 0.20
        self.height = 26
        self.width = 18
        self.framesPerSecond = 30
        self.frame = direction
        self.nFrames = 8
        self.vel = vec(0,0)
        self.speed = 100
        self.row = direction # (0 down), (1 right), (2 up), (3 left)
        self.collisionRect = pygame.Rect((self.position[0]+1,self.position[1]+7),(16,16))
        self.invincible = False
        self.iframeTimer = 0
        self.idleTimer = 0#Timer used for having the player stand still
        self.idleFrame = 9##Integer used to display flashing idle sprite while charging
        self.targeting = False
        self.target = Animated(self.position, fileName="target.png", nFrames=4, fps=16)
        self.rot = 1
        self.key_delay = False
        self.drunkTimer = 0.0
        self.ignoreCollision = False
        self.hp = INV["max_hp"]

        
        #   States------------------------------------------------------------------------
        ##  Death
        self.dying = False
        self.dead = False
        self.headingOut = False

        ##  Movement/Collision
        self.movingTo = None
        self.moving = False
        self.pushing = False
        self.walking = False
        self.colliding = False
        self.shooting = False
        self.talking = False
        self.key_lock = False
        self.keyDown_lock = False
        self.directionLock = False
        self.positionLock = False

        ##  Special
        self.drunk = False  # Buff to attack, nerf to speed
        self.elevated = False   # Reveal secrets and sometimes take no damage
        self.fired = False
        

        #   Weapons/items----------------------------------------------------------------
        ##  Arrows
        self.bullet = None
        self.arrowCount = 1
        self.arrowReady = True
        self.arrowTimer = 0.0

        ##  Wind
        ### Slash
        self.slash = None
        self.chargeTimer = 0.0
        self.charged = False
        self.charging = False

        ##  Flames
        ### Sword
        self.sword = None
        self.swordReady = True
        self.swordSound = "DarkLink1.wav"
        self.swordCounter = 1
        self.swordRefresher = 0

        ##  Thunder
        ### Hook
        self.hook = None

        ### Clap
        self.clap = None
        self.clapTimer = 0.01
        self.clapReady = False

        ##  Ice
        ### Cleats
        self.cleats = None
        self.running = False
        self.runningDirection = 0

        ### Blizzard
        self.freezing = False
        self.blizzard = None
        self.slowing = False
        self.attacking = False

        
        
    def drink(self):
        self.drunkTimer += 30
        self.speed = 60
        self.drunk = True
    
    def undrink(self):
        self.drunkTimer = 0
        self.speed = 100
        self.drunk = False

    def see(self):
        self.elevated = True
    
    def heal(self, integer):
        SoundManager.getInstance().playSFX("solve.wav")
        INV["max_hp"]
        difference = INV["max_hp"] - self.hp
        if integer > difference:
            self.hp = INV["max_hp"]
            return difference
        else:
            self.hp += integer
            return integer
        
    def hurt(self, integer):
        if not self.invincible:
            if INV["chanceEmblem"]:
                ##Only die on 1 hp
                if self.hp <= 1:
                    self.hp = 0
                else:
                    ##Take damage, set to 1 hp if hp <= 0
                    self.hp -= integer
                    if self.hp <= 0:
                        self.hp = 1
                    self.invincible = True
                    SoundManager.getInstance().playSFX("hurt.wav")
            else:
                ##Regular damage routine
                self.hp -= integer
                SoundManager.getInstance().playSFX("hurt.wav")
                self.invincible = True
            HealthBar.getInstance().drawHurt(self.hp, integer)
    
    def hurtSyringe(self, integer):
        SoundManager.getInstance().playSFX("hurt.wav")
        self.hp -= integer
        if self.hp <= 0:
            damage = integer - (self.hp * -1 + 1)
            self.hp = 1
            HealthBar.getInstance().drawHurt(self.hp, damage)
        else:
            HealthBar.getInstance().drawHurt(self.hp, integer)
    """
    Getter methods
    """
    ###Get weapon instances###


    def getBullet(self):
        return self.bullet

    def getFlame(self):
        return self.sword
    
    def getBlizzard(self):
        return self.blizzard

    def getSlash(self):
        return self.slash
    
    def getDirection(self, row=None):
        """
        Return the direction of the player based on the row of its sprite
        """
        if row == None:
            row = self.row
        if row > 3:
            if row > 4 and row < 8:
                return row - 4
            elif row >= 8 and row < 12:
                return row - 8
            elif row >= 12 and row < 16:
                return row - 12
            elif row >= 16:
                return row - 16
        else:
            return row

    def getOppositeDirection(self):
        dir = self.getDirection()
        if dir == 0:
            return 2
        elif dir == 1:
            return 3
        elif dir == 2:
            return 0
        elif dir == 3:
            return 1

    def getHook(self):
        return self.hook
    
    def getClap(self):
        return self.clap
    
    def getSpeed(self):
        return self.speed
    
    def getTackleRect(self):
        return pygame.Rect(((self.position[0]-7),self.position[1]-2), (32,32))
    
    def getCollisionRect(self):
        if self.colliding:
            return self.collisionRect
        self.collisionRect = pygame.Rect((self.position[0]+2,self.position[1]+6),(14,16))
        return self.collisionRect
    
    def getHitBox(self):
        if self.row == 0:
            #Down
            newRect = pygame.Rect((self.position[0]+2,self.position[1]+7),(14,15))
        elif self.row == 1:
            #Right
            newRect = pygame.Rect((self.position[0]+6,self.position[1]+7),(10,15))
        elif self.row == 2:
            #Up
            newRect = pygame.Rect((self.position[0]+2,self.position[1]+6),(14,16))
        elif self.row == 3:
            #Left
            newRect = pygame.Rect((self.position[0]+1,self.position[1]+6),(11,16))
        return newRect

    def refreshAmmo(self):
        pass
        """ if self.ammo < self.max_ammo:
            self.ammo += 1 """

    def draw(self, drawSurface, drawHitbox = False, invis = False):
        
        if invis:
            drawSurface.blit(SpriteManager.getInstance().getSprite("null.png"), (0,0))
        else:
            super().draw(drawSurface, drawHitbox)
    
    """
    Movement and event handling
    """
    
    def movingDiagonal(self):
        return (self.vel[0] != 0 and self.vel[1] != 0)
    
    def keyDownLock(self):
        self.keyDown_lock = True
    
    def keyDownUnlock(self):
        self.keyDown_lock = False

    def keyLock(self):
        #self.stop()
        self.key_lock = True
    
    def keyUnlock(self):
        self.key_lock = False
    
    def moveTo(self, position):
        self.moving = True
        self.movingTo = position
        self.keyLock()

        
        

        


        #while self.position != 
    
    def isArrowKey(self, event):
        return (event == pygame.K_UP or event == pygame.K_DOWN or event == pygame.K_RIGHT or event == pygame.K_LEFT)
    
    def run(self):
        SoundManager.getInstance().stopSFX("screwattack_loop.wav")
        self.running = True
        self.vel *= 3
        #SoundManager.getInstance().stopSFX("footsteps.wav")
        SoundManager.getInstance().playSFX("screwattack_loop.wav", -1)

    def stop(self):
        self.slowing = False
        self.freezing = False
        self.running = False
        self.walking = False
        self.vel = vec(0,0)
        SoundManager.getInstance().stopSFX("screwattack_loop.wav")

    def stop_run(self, enemy):
        self.key_delay = True
        #self.keyLock()
        self.invincible = True
        self.stop()
        ACTIONS["interact"] = False
        ACTIONS["down"] = False
        ACTIONS["up"] = False
        ACTIONS["right"] = False
        ACTIONS["left"] = False
        EventManager.getInstance().buffCursor()
        side = self.calculateSide(enemy)
        self.knockback(side)
        SoundManager.getInstance().stopAllSFX()
        SoundManager.getInstance().playSFX("collide.wav")

    def slow(self):
        self.slowing = True
        self.vel /= 3
        SoundManager.getInstance().stopSFX("screwattack_loop.wav")

    def charge(self):
        self.charging = True


    def move(self, direction):
        """
        The player moves based on its direction.
        Updates self.row and self.vel accordingly
        """
        #SoundManager.getInstance().playSFX("footsteps.wav", -1)
        # X -> vel[0]
        if not self.running:
            if direction == 1:#Right
                if self.vel[1] == 0:
                    if not self.targeting:
                        self.row = 1
                self.vel[0] = self.speed

            elif direction == 3:#Left
                if self.vel[1] == 0:
                    if not self.targeting:
                        self.row = 3
                self.vel[0] = -self.speed

            # Y -> vel[1]
            elif direction == 0:#Down
                if not self.targeting:
                    self.row = direction
                self.vel[1] = self.speed
                
            elif direction == 2:#Up
                if not self.targeting:
                    self.row = direction
                self.vel[1] = -self.speed


    def setWeaponDamage(self, weapon):
        if self.drunk:
            weapon.setDrunk()


    def stopMoving(self, direction : int):
        """
        Stop moving if |joystick value| is 0.2
        """
        ##Up motion
        if direction == 2:
            #Display the proper sprite for diagonal
            if self.vel[0] < 0:
                if not self.targeting:
                    self.row = 3
            elif self.vel[0] > 0:
                if not self.targeting:
                    self.row = 1
            #Stop upward velocity
            if self.vel[1] < 0:
                self.vel[1] = 0

        ##Down motion
        elif direction == 0:
            
            #Display the proper sprite for diagonal
            if self.vel[0] < 0:
                if not self.targeting:
                    self.row = 3
            elif self.vel[0] > 0:
                if not self.targeting:
                    self.row = 1
            #Stop downward velocity
            if self.vel[1] > 0:
                self.vel[1] = 0

        ##Left
        elif direction == 3:
            #Stop leftward velocity
            if self.vel[0] < 0:
                self.vel[0] = 0

        ##Right
        elif direction == 1:
        #Stop rightward velocity
            if self.vel[0] > 0:
                self.vel[0] = 0

    
    def shootArrow(self, shortcut = False):
        if self.arrowReady:
            if shortcut:
                equipped = SHORTCUTS[ACTIVE_SHORTCUT[0]][1]
                if equipped == 0:
                    ACTIONS["shoot"] = False
                    self.bullet = Bullet(self.position, self.getDirection(self.row), self.hp)
                    #self.arrowCount -= 1
                    self.arrowReady = False
                    self.setWeaponDamage(self.bullet)

                elif equipped == 1:
                    ACTIONS["shoot"] = False
                    if INV["bombo"] > 0:
                        self.bullet = Bombo(self.position, self.getDirection(self.row), self.hp)
                        #self.arrowCount -= 1
                        self.arrowReady = False
                        self.setWeaponDamage(self.bullet)
                        INV["bombo"] -= 1
            else:
                equipped = EQUIPPED["Arrow"]
                #equipped = Shortcut[Active_shortcut]
                if equipped == 0:
                    ACTIONS["shoot"] = False
                    self.bullet = Bullet(self.position, self.getDirection(self.row), self.hp)
                    #self.arrowCount -= 1
                    self.arrowReady = False
                    self.setWeaponDamage(self.bullet)

                elif equipped == 1:
                    ACTIONS["shoot"] = False
                    if INV["bombo"] > 0:
                        self.bullet = Bombo(self.position, self.getDirection(self.row), self.hp)
                        #self.arrowCount -= 1
                        self.arrowReady = False
                        self.setWeaponDamage(self.bullet)
                        INV["bombo"] -= 1


            
    def stopPushing(self, event):
        self.stopMoving(event)

    def setDirection(self, dir):
        direction = self.getDirection()
        diff = (direction - dir) * -1
        self.row += diff
       
    def shiftDirection(self, side = "left"):
        SoundManager.getInstance().playSFX("shortcut.wav")
        if side == "left":
            if ACTIVE_SHORTCUT[0] == 0:
                ACTIVE_SHORTCUT[0] = 5
            else:
                ACTIVE_SHORTCUT[0] -= 1
        elif side == "right":
            if ACTIVE_SHORTCUT[0] == 5:
                ACTIVE_SHORTCUT[0] = 0
            else:
                ACTIVE_SHORTCUT[0] += 1
        

    def handleEvent(self, interactableObject = None, engine = None):
        if not self.key_lock:
            if interactableObject != None:
                if EventManager.getInstance().performAction("interact"):
                    interactableObject.interact(engine)
                    self.stop()
                    return
                elif interactableObject.mobster and EventManager.getInstance().performAction("element"):
                    interactableObject.startMobster(engine)
                    return

            if not self.attacking and self.swordReady:
                ##  Target
                if ACTIONS["target"]:
                    self.targeting = True
                elif self.targeting:
                    self.targeting = False


                ##  Bumpers
                if EventManager.getInstance().performAction("target_left"):
                    self.shiftDirection("left")
                
                if EventManager.getInstance().performAction("target_right"):
                    self.shiftDirection("right")

                
                ##  Right analog
                if ACTIONS["down_r"]:
                    self.setDirection(0)


                if ACTIONS["right_r"]:
                    self.setDirection(1)
      

                if ACTIONS["up_r"]:
                    self.setDirection(2)
      

                if ACTIONS["left_r"]:
                    self.setDirection(3)
                
            


                if EventManager.getInstance().getCursorReady():
                    ##  Movement
                    if ACTIONS["down"]:
                        self.move(0)
                    else:
                        self.stopMoving(0)

                    if ACTIONS["right"]:
                        self.move(1)
                    else:
                        self.stopMoving(1)

                    if ACTIONS["up"]:
                        self.move(2)
                    else:
                        self.stopMoving(2)

                    if ACTIONS["left"]:
                        self.move(3)
                    else:
                        self.stopMoving(3)
                    
                    ##  Item
                    if SHORTCUTS[ACTIVE_SHORTCUT[0]][0] == "item" and ACTIONS["trigger_r"]:
                        ACTIONS["trigger_r"] = False
                        EventManager.getInstance().buffCursor()
                        id = SHORTCUTS[ACTIVE_SHORTCUT[0]][1]
                        if id == 0:
                            if self.hp > 1:
                                damage = (ceil((2 * INV["max_hp"])/3))
                                self.hurtSyringe(damage)
                        elif id == 1:
                            if INV["potion"] > 0 and self.hp < INV["max_hp"]:
                                INV["potion"] -= 1
                                self.heal(3)

                        elif id == 2:
                            if INV["smoothie"] > 0 and self.hp < INV["max_hp"]:
                                INV["smoothie"] -= 1
                                self.heal(5)

                        elif id == 3:
                            if INV["beer"] > 0:
                                INV["beer"] -= 1
                                self.drink()

                        elif id == 4:
                            if INV["joint"] > 0:
                                INV["joint"] -= 1

                        elif id == 5:
                            if INV["speed"] > 0:
                                INV["speed"] -= 1
            
            ##  Shooting
            #pre reqs
            if INV["shoot"] and self.arrowCount > 0 and self.arrowReady and not self.invincible:
                ##  Shoot Button
                if (ACTIONS["shoot"]):
                    #Fire bullet
                    self.shootArrow()
                
                ##  Shortcut Shot
                elif EventManager.getInstance().getAttackReady() and (SHORTCUTS[ACTIVE_SHORTCUT[0]][0] == "shoot" and ACTIONS["trigger_r"]):
                    self.shootArrow(True)
                    EventManager.getInstance().buffAttack()
            
            ##  Element
            if not self.running:
                if ACTIONS["element"]:
                    if not self.invincible:
                        equippedC = EQUIPPED["C"]
                        if equippedC != None:
                            if self.charging and equippedC != 3:
                                self.shootSlash()
                                ACTIONS["trigger_r"] = False
                            if self.freezing and equippedC != 1:
                                self.freezing = False
                                ACTIONS["trigger_r"] = False

                            if equippedC == 0 and self.swordReady:
                                ACTIONS["element"] = False
                                self.sword = Sword(self.position, self.getDirection(self.row))
                                self.frame = -1
                                self.swordReady = False
                                self.vel = vec(0,0)
                                self.positionLock = True
                                self.directionLock = True
                                self.increaseSwordCounter()
                                self.setWeaponDamage(self.sword)

                            elif equippedC == 1 and self.freezing == False:
                                self.frame = 0
                                if self.blizzard == None:
                                    self.blizzard = Blizzard(self.position, self.getDirection(self.row))
                                    self.setWeaponDamage(self.blizzard)
                                self.stop()
                                self.attacking = True
                                self.freezing = True

                            elif equippedC == 2 and self.clapReady:
                                ACTIONS["element"] = False
                                self.clap = Clap(self.position)
                                self.setWeaponDamage(self.clap)
                                self.clapReady = False
                                self.vel = vec(0,0)
                                self.positionLock = True

                            elif not self.charging and equippedC == 3:
                                self.charge()
                

                elif ACTIONS["trigger_r"]:
                    if (SHORTCUTS[ACTIVE_SHORTCUT[0]][0] == "element") and EventManager.getInstance().getAttackReady():
                        EventManager.getInstance().buffAttack()
                        if not self.invincible:
                            equippedC = SHORTCUTS[ACTIVE_SHORTCUT[0]][1]
                            if self.freezing and equippedC != 1:
                                self.freezing = False
                            if self.charging and equippedC != 3:
                                self.shootSlash()
                                
                            if equippedC != None:
                                if equippedC == 0 and self.swordReady:
                                    self.sword = Sword(self.position, self.getDirection(self.row))
                                    self.frame = -1
                                    self.swordReady = False
                                    self.vel = vec(0,0)
                                    self.positionLock = True
                                    self.directionLock = True
                                    self.increaseSwordCounter()
                                    self.setWeaponDamage(self.sword)

                                elif equippedC == 1 and self.freezing == False:
                                    if not self.freezing:
                                        self.frame = 0
                                        if self.blizzard == None:
                                            self.blizzard = Blizzard(self.position, self.getDirection(self.row))
                                            self.setWeaponDamage(self.blizzard)
                                        self.stop()
                                        self.attacking = True
                                        self.freezing = True
                                        return
                                    else:
                                        return

                                elif equippedC == 2 and self.clapReady:
                                    self.clap = Clap(self.position)
                                    self.setWeaponDamage(self.clap)
                                    self.clapReady = False
                                    self.vel = vec(0,0)
                                    self.positionLock = True

                                elif not self.charging and equippedC == 3:
                                    self.charge()
                                    return
                                
                else:
                    if self.freezing:
                        self.freezing = False
                    if self.charging:
                        self.shootSlash()
                    self.attacking = False

                

            ##  Movement Modifier
            if ACTIONS["interact"]:
                if not self.running and self.walking and not self.movingDiagonal() and not self.invincible:
                    self.runningDirection = self.row
                    self.run()
            else:
                if self.running:
                    self.stop()

    
                    
        
    """
    Locking position and direction
    """
    def lockDirection(self):
        self.directionLock = True
    
    def unlockDirection(self):
        self.directionLock = False
    
    def lockPosition(self):
        self.positionLock = True
    
    def unlockPosition(self):
        self.positionLock = False

    def adjustDirection(self, side):
        if side == "bottom":
            self.row = 0
            self.vel[0] = 0
            #self.vel[1] = self.speed/2
        elif side == "right":
            self.row = 1
            self.vel[1] = 0
            #self.vel[0] = self.speed/2
        elif side == "top":
            self.row = 2
            self.vel[0] = 0
            #self.vel[1] = -self.speed/2
        elif side == "left":
            self.row = 3
            self.vel[1] = 0
            #self.vel[0] = -self.speed/2


    """
    Collision detection
    """
    def interactable(self, object):
        if object.id == "greenHeart" or not object.drop:
            return self.getCollisionRect().colliderect(object.getInteractionRect())
    
    def interactableObjects(self, object):
        return self.getCollisionRect().colliderect(object.getInteractionRect())
    
    def handleCollision(self, object):
        if self.dying:
            return
        
        
        elif type(object) == PushableBlock:
            if self.running:
                self.stop_run(object)
            side = self.calculateSide(object)
            self.pushing = True

            if object.resetting:
                if self.pushing:
                    self.pushing = False
                    if self.vel[1] > 0:
                        self.vel[1] = self.speed
                    elif self.vel[1] < 0:
                        self.vel[1] = -self.speed
                    elif self.vel[0] > 0:
                        self.vel[0] = self.speed
                    elif self.vel[0] < 0:
                        self.vel[0] = -self.speed
                    self.preventCollision(object, side)
                
            else:
                if not self.movingDiagonal():
                    self.adjustDirection(side)
                    if self.vel[1] > 0:
                        self.vel[1] = self.speed/3
                    elif self.vel[1] < 0:
                        self.vel[1] = -self.speed/3
                    elif self.vel[0] > 0:
                        self.vel[0] = self.speed/3
                    elif self.vel[0] < 0:
                        self.vel[0] = -self.speed/3
                    object.push()
                else:
                    self.preventCollision(object, side)
        elif issubclass(type(object), Enemy) and object.id != "shot":
            if self.charging:
                self.shootSlash()
            if self.freezing:
                ACTIONS["element"] = False
                self.freezing = False
            side = self.calculateSide(object)
            self.enemyCollision(object, side)

        else:
            if self.running:
                self.stop_run(object)
            self.pushing = (not self.targeting and not self.movingDiagonal())
            side = self.calculateSide(object)
            self.preventCollision(object, side)

    def enemyCollision(self, enemy, side):
        
        
        if enemy.frozen:
            if not enemy.id == "noStop":
                if self.running:
                    self.stop_run(enemy)
                self.pushing = (not self.targeting and not self.movingDiagonal())
                self.preventCollision(enemy, side)
        else:
            self.hurt(enemy.getDamage())
            if not enemy.id == "noStop":
                if self.running:
                    self.stop_run(enemy)
            self.knockback(side)
            
    def preventCollision(self, object, side = None):
       
        if side:
            pass
        else:
            self.pushing = True
            side = self.calculateSide(object)
                
        obj = object.getCollisionRect()
        coll = self.getCollisionRect()
        if side == "right":
            #self.position[0] = (obj.left) - (obj.width - (obj.width - coll.width)) - 2#Line up the rects and put player 1 pixel before colliding
            self.position[0] = (obj.left - 18) + 2

        elif side == "left":
            #self.position[0] = (obj.left) + (obj.width - (obj.width - coll.width)) + 1
            self.position[0] = (obj.right) - 1
    
        elif side == "top":
            #self.position[1] = (obj.top) + (obj.height - (obj.height - coll.height)) - 6
            self.position[1] = (obj.bottom) - 6
            
        elif side == "bottom":
            #2self.position[1] = (obj.top) - (obj.height - (obj.height - coll.height) + 6)
            self.position[1] = (obj.top -26) + 4
        
        if not pygame.mixer.get_busy():
            SoundManager.getInstance().playSFX("bump.mp3")


    def calculateSide(self, object):
        ##  Colliding with Block    ##
        collision1 = self.collisionRect
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

    def knockback(self,side):
        if side == "right":
            self.position[0] -= 5
        elif side == "left":
            self.position[0] += 5
        elif side == "top":
            self.position[1] += 5
        elif side == "bottom":
            self.position[1] -= 5

    def inPosition(self, position):
        return self.position[0] == position[0] and self.position[1] == position[1]

    def shootSlash(self):
        if self.chargeTimer > 0.5:
            if self.chargeTimer < 1.5:
                self.slash = Slash(self.position, self.getDirection(self.row), 0)
            elif self.chargeTimer < 2.5:
                self.slash = Slash(self.position, self.getDirection(self.row), 1)
            else:
                self.slash = Slash(self.position, self.getDirection(self.row), 2)
            self.setWeaponDamage(self.slash)
        if self.charged:
            self.charged = False
        self.charging = False
        self.chargeTimer = 0
        self.idleFrame = 9

    """
    Updating
    """
    def die(self):
        self.keyLock()
        self.dying = True
        self.row = 0
        self.frame = 0
        self.walking = False
        

        ##For special animations
        #self.framesPerSecond = 1
        #self.frame = 0
        #self.nFrames = 20
        #self.row = 56

    ##  Determining the sound that plays when sword is swung    ##
    def increaseSwordCounter(self):
        if self.swordCounter >= 3:
            self.swordCounter = 1
        
        else:
            self.swordCounter += 1

        if self.swordCounter == 1:
            self.swordSound = "DarkLink1.wav"
        elif self.swordCounter == 2:
            self.swordSound = "DarkLink2.wav"
        elif self.swordCounter == 3:
            self.swordSound = "DarkLink3.wav"

    def set_Image(self):
        self.image = SpriteManager.getInstance().getSprite(self.fileName, (self.frame, self.row))
    
    def face(self, direction=0):
        self.image = SpriteManager.getInstance().getSprite(self.fileName, (0, direction))
    
    def update(self, seconds):
        if self.dying:
            if not self.dead:
                if self.row == 1:
                    
                    
                    super().updatePlayer(seconds)
                    self.position += self.vel * seconds
                    if self.position [0] >= RESOLUTION[0]:
                        self.dead = True
                    """ if self.frame == 2:#19
                        self.dead = True """
                    
                elif self.row == 0:
                    super().updatePlayer(seconds)
                    self.idleTimer += seconds
                    if self.idleTimer >= 1:
                        self.headingOut = True
                        self.row = 1
                        self.idleTimer = 0
                        
                
                
            return
        
        if self.drunk:
            self.drunkTimer -= seconds
            if self.drunkTimer <= 0:
                self.undrink()

        #if self.key_delay:
            #self.keyTimer 
        if not self.arrowReady:
            self.arrowTimer += seconds
            if self.hp == INV["max_hp"]:
                if self.arrowTimer >= 0.1:
                    self.arrowReady = True
                    self.arrowTimer = 0
            else:
                if self.arrowTimer >= 0.25:
                    self.arrowReady = True
                    self.arrowTimer = 0

        #Update walking state
        if self.vel[0] == 0 and self.vel[1] == 0:
            #SoundManager.getInstance().stopSFX("footsteps.wav")
            self.pushing = False
            self.running = False
            self.walking = False
            SoundManager.getInstance().stopSFX("screwattack_loop.wav")
        else:
            #SoundManager.getInstance().playSFX("step.wav")
            self.walking = True

        if self.charging:
            self.chargeTimer += seconds
            if self.chargeTimer >= 2.5:
                if self.chargeTimer >= 2.9:
                    self.chargeTimer = 2.5
                if not self.charged:
                    self.charged = True
                
                #Play a sound or something?
            super().updatePlayer(seconds)
            self.position += self.vel * seconds
            return
            
            
            #Shoot an even bigger slash when charged for longer?
        elif self.freezing:
            super().updatePlayer(seconds)
            return
        
        elif self.blizzard != None:
            self.blizzard = None
        
       
        #Update invincibility if needed
        if self.invincible:
            self.iframeTimer += seconds 
            if self.iframeTimer >= 0.8:
                self.iframeTimer = 0
                self.invincible = False

            elif self.iframeTimer <= 0.7:
                self.image = SpriteManager.getInstance().getSprite("null.png")
        
        #   Update clap cooldown
        if self.clapReady == False:
            self.clapTimer += seconds
            if self.clapTimer >= 5.0:
                self.clapTimer = 0
                self.clapReady = True
        
        #  Diagonal Movement + Vector Normalization
        if self.movingDiagonal():

            if True:
                
                #   I have 2 ways to calculate the accurate diagonal velocity vector:

                ##  1. -> Normalizing the Vector
                ##  Multiply the velocity vector by
                ##  the absolute value of the normalized vector
                ##  to get more accurate diagonal movement.

                ##  2. -> Pythagorean Theorem
                ##  The diagonal vector = c.
                ##  a = x direction, b = y direction
                ##  c**2 = a**2 + b**2.
                ##  So c = sqrt(a**2 + b ** 2).
                ##  Dive c // 2 to get the x and y components of the diagonal vector.
                ##  Multiply each component by the sign (-1 / +1) of each component.

                ##  Calculate the magnitude of the velocity vector
                mag = lambda v: sqrt(v[0] ** 2 + v[1] ** 2)
                
                ##   Caclulate the normalized velocity vector
                norm = lambda v: v / mag(v)

                ##  Get the sign of each component of the velocity vector
                sign_vec = lambda v: vec( -1 if v[0] < 0 else (1 if v[0] > 0 else 0), -1 if v[1] < 0 else (1 if v[1] > 0 else 0) )

                ##  Using Method 1:
                #self.position += self.vel * abs(norm(self.vel)) * seconds

                ##  Using Method 2:
                self.position += (mag(self.vel)//2 * sign_vec(self.vel)) * seconds
            
            else:
                self.position += self.vel * seconds

        else:
            self.position += self.vel * seconds

        super().updatePlayer(seconds)
        
        
        

    def updateMovement(self):
        pass

class Firi(Player):
    def __init__(self, position=vec(0,0), direction=0):
        super().__init__(position, direction, "firi.png")
        self.nFrames = 16
        self.framesPerSecond = 6
        self.idle = True
        self.idleTimer = 0.0
        self.set_scale()

    def handleEvent(self, interactableObject=None, engine=None):
        return

    def updateAnimation(self, seconds, nFrames, fps, row):
        self.animationTimer += seconds
        
        if self.animationTimer > 1 / self.framesPerSecond:
            
            self.frame += 1
            self.frame %= nFrames
            
            self.animationTimer -= 1 / self.framesPerSecond
            self.image = SpriteManager.getInstance().getSprite(self.fileName,
                                                (self.frame, self.row))
            self.set_scale()

    def set_scale(self):
        #self.image = pygame.transform.scale_by(self.image, (1.2,1))
        #self.image = pygame.transform.scale2x(self.image)
        return

    def set_Image(self):
        super().set_Image()
        self.set_scale()

    def update(self, seconds):
        if self.idle:
            if self.idleTimer >= 2.0:
                self.updateAnimation(seconds, self.nFrames, self.framesPerSecond, self.row)
                if self.frame == 15:
                    self.idleTimer = 0.0
                    self.frame = 0
                    self.set_Image()
            else:
                self.idleTimer += seconds
                #self.playAnimation(seconds, 2, self.row)