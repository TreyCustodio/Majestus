from . import Bullet, Bombo, Sword, Dummy, Drop, David, Blizzard, Clap, Hook, Slash, Animated, Enemy, Geemer, PushableBlock, NonPlayer, Block, HBlock, LockBlock
from utils import SpriteManager, SoundManager, SCALE, RESOLUTION, INV, EQUIPPED, vec
import pygame



class Player(Animated):
    def __init__(self, position=vec(0,0), direction=2):
        super().__init__(position, "Link.png", (0, direction))
        self.ignoreCollision = False
        self.hp = INV["max_hp"]
        #Frames, vel, speed, and row
        #Must reach this far to move player
        self.analogTrack = 0.40
        self.drunk = False#Buff to attack, nerf to speed
        self.drunkTimer = 0
        self.height = 26
        self.width = 18
        self.framesPerSecond = 30
        self.frame = direction
        self.nFrames = 8
        self.vel = vec(0,0)
        self.speed = 100
        self.row = direction # (0 down), (1 right), (2 up), (3 left)
        self.dying = False
        self.dead = False
        #States
        
        
        self.headingOut = False
        self.movingTo = None
        self.moving = False
        self.pushing = False
        self.walking = False
        self.colliding = False
        self.shooting = False
        self.fired = False
        #Movement locks
        self.talking = False
        self.key_lock = False
        self.keyDown_lock = False
        self.directionLock = False
        self.positionLock = False
        self.collisionRect = pygame.Rect((self.position[0]+1,self.position[1]+7),(16,16))
        ##Weapons/items##
        #Bullet
        self.bullet = None
        self.arrowCount = 1
        self.arrowReady = True
        self.arrowTimer = 0
        #Gale slash
        self.slash = None
        self.chargeTimer = 0
        self.charged = False
        self.charging = False
        #Flame Sword
        self.sword = None
        self.swordReady = True
        self.swordSound = "DarkLink1.wav"
        self.swordCounter = 1
        self.swordRefresher = 0
        #Thunder clap
        self.clap = None
        self.clapTimer = 0.01
        self.clapReady = False
        #Ice cleats
        self.cleats = None
        self.running = False
        self.runningDirection = 0
        #Hook
        self.hook = None
        #Blizzard
        self.freezing = False
        self.blizzard = None
        self.slowing = False
        
        
        self.event = None
        self.invincible = False
        self.iframeTimer = 0
        self.idleTimer = 0#Timer used for having the player stand still
        self.idleFrame = 9##Integer used to display flashing idle sprite while charging
        
        
        
    def drink(self):
        self.drunkTimer += 30
        self.speed = 60
        self.drunk = True
    
    def undrink(self):
        self.drunkTimer = 0
        self.speed = 100
        self.drunk = False

    def smoke(self):
        self.high = True
    
    def heal(self, integer):
        INV["max_hp"]
        difference = INV["max_hp"] - self.hp
        if integer > difference:
            self.hp = INV["max_hp"]
            return difference
        else:
            self.hp += integer
            return integer
        
    def hurt(self, integer):
        self.hp -= integer
        
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
    
    def getDirection(self, row):
        """
        Return the direction of the player based on the row of its sprite
        """
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
        if direction == 1:#Right
            if self.vel[1] == 0:
                self.row = 1
            self.vel[0] = self.speed

        elif direction == 3:#Left
            #print(self.vel)
            if self.vel[1] == 0:
                self.row = 3
            self.vel[0] = -self.speed

        # Y -> vel[1]
        elif direction == 0:#Down
            self.row = direction
            self.vel[1] = self.speed
            
        elif direction == 2:#Up
            self.row = direction
            self.vel[1] = -self.speed


    def move_C(self, event):
        """
        Joystick movement routine
        Move diagonal.
        """
        ##  Directional Movement    ##
        if event.axis == 1 and event.value >= self.analogTrack: # 2
            self.move(0)
            return

        elif event.axis == 1 and event.value <= -self.analogTrack: # 0
            self.move(2)
            return
            
        elif event.axis == 0 and event.value <= -self.analogTrack: # 3
            self.move(3)
            return
            
        elif event.axis == 0 and event.value >= self.analogTrack: # 1
            self.move(1)
            return

    def setWeaponDamage(self, weapon):
        if self.drunk:
            weapon.setDrunk()


    def stopMoving(self, event):
        """
        Stop moving if |joystick value| is 0.2
        """
        ##Up motion
        if self.vel[1] < 0 and event.axis == 1 and event.value > -0.2:
            #Display the proper sprite for diagonal
            if self.vel[0] < 0:
                self.row = 3
            elif self.vel[0] > 0:
                self.row = 1
            #Stop upward velocity
            if self.vel[1] < 0:
                self.vel[1] = 0

        ##Down motion
        elif self.vel[1] > 0 and event.axis == 1 and event.value < 0.2:
            
            #Display the proper sprite for diagonal
            if self.vel[0] < 0:
                self.row = 3
            elif self.vel[0] > 0:
                self.row = 1
            #Stop downward velocity
            if self.vel[1] > 0:
                self.vel[1] = 0

        ##Left
        elif self.vel[0] < 0 and event.axis == 0 and event.value > -0.2:
            #Stop leftward velocity
            if self.vel[0] < 0:
                self.vel[0] = 0

        ##Right
        elif self.vel[0] > 0 and event.axis == 0 and event.value < 0.2:
        #Stop rightward velocity
            if self.vel[0] > 0:
                self.vel[0] = 0


    def buttonsUp(self, event):
        """
        Buttons up routine
        """
        if self.freezing:
            if event.button == 3:
                #print("C")
                #self.frame = 4
                self.freezing = False
            else:
                return
            
        elif self.running:
            if event.button == 0:
                #Stop running
                self.stop()
                

        else:
            if self.charging:
                if event.button == 3:
                    self.shootSlash()
    
    def shootArrow(self):
        equipped = EQUIPPED["Arrow"]
        if equipped == 0:
            self.bullet = Bullet(self.position, self.getDirection(self.row), self.hp)
            self.arrowCount -= 1
            self.arrowReady = False
            self.setWeaponDamage(self.bullet)

        elif equipped == 1:
            if INV["bombo"] > 0:
                self.bullet = Bombo(self.position, self.getDirection(self.row), self.hp)
                self.arrowCount -= 1
                self.arrowReady = False
                self.setWeaponDamage(self.bullet)
                INV["bombo"] -= 1

    def buttonsDown(self, event):
        if event.button == 2 and INV["shoot"] and self.arrowCount > 0 and self.arrowReady and not self.invincible: #and self.ammo > 0:
            #Fire bullet
            self.shootArrow()
        
        if event.button == 1:
            #Hook
            #SoundManager.getInstance().playSFX("OOT_DekuSeed_Shoot.wav")
            self.hook = Hook(self.position, self.getDirection(self.row))
            self.keyLock()
            
        if not self.running:
            if not self.charging:
                if event.button == 3 and not self.invincible:
                    equippedC = EQUIPPED["C"]
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
                            self.frame = 0
                            if self.blizzard == None:
                                self.blizzard = Blizzard(self.position, self.getDirection(self.row))
                                self.setWeaponDamage(self.blizzard)
                            self.stop()
                            self.freezing = True

                        elif equippedC == 2 and self.clapReady:
                            self.clap = Clap(self.position)
                            self.setWeaponDamage(self.clap)
                            self.clapReady = False
                            self.vel = vec(0,0)
                            self.positionLock = True

                        elif equippedC == 3:
                            self.charge()


                elif event.button == 0 and INV["cleats"] and not self.invincible  and ( self.walking and (not self.movingDiagonal()) ):
                    #Tackle
                    self.runningDirection = self.row
                    self.run()

        
    def analogMovement(self, event):
        if self.swordReady:
            self.move_C(event)
        
        """ elif event.key == pygame.K_RIGHT and self.runningDirection == 1:
            self.stop()
        elif event.key == pygame.K_UP and self.runningDirection == 2:
            self.stop()
        elif event.key == pygame.K_LEFT and self.runningDirection == 3:
            self.stop()
        elif event.key == pygame.K_DOWN and self.runningDirection == 0:
            self.stop() """

        self.stopMoving(event)
            
    def stopPushing(self, event):
        self.stopMoving(event)

    def handleEvent_C(self, event, interactableObject = None, engine = None):
        #print(self.key_lock)
        if not self.key_lock:
            #print(1)
            if not self.keyDown_lock and (not self.freezing):
                #print(2)
                if not self.pushing:
                    #print(3)
                    if interactableObject != None:
                        if event.type == pygame.JOYBUTTONDOWN and event.button == 0:
                            interactableObject.interact(engine)
                            self.stop()
                            return

                    if event.type == pygame.JOYBUTTONDOWN:
                        self.buttonsDown(event)
                        return
                    
                    elif event.type == pygame.JOYBUTTONUP:
                        self.buttonsUp(event)
                        return

                    elif event.type == pygame.JOYAXISMOTION:
                        self.analogMovement(event)
                        return
                    
                elif event.type == pygame.JOYAXISMOTION:
                    #print(4)
                    self.stopPushing(event)
                    return
                
            if event.type == pygame.JOYBUTTONUP:
                    self.buttonsUp(event)
                    return
            
        elif event.type != pygame.JOYAXISMOTION and (self.vel[0] != 0 or self.vel[1] != 0):
            self.stop()

    def handleEvent(self, event, interactableObject = None, engine = None):
        if not self.key_lock:
            if not self.keyDown_lock and event.type == pygame.KEYDOWN and (not self.freezing):
                if not self.pushing:
                    if interactableObject != None and event.key == pygame.K_z:
                        
                        interactableObject.interact(engine)
                        self.stop()

                    """ if event.key == pygame.K_f:
                        self.moveTo(vec(16*4,16*10)) """

                    if event.key == pygame.K_x and INV["shoot"] and self.arrowCount > 0 and self.arrowReady and not self.invincible: #and self.ammo > 0:
                        #Fire bullet
                        self.shootArrow()
                    
                    if event.key == pygame.K_a:
                        #Hook
                        #SoundManager.getInstance().playSFX("OOT_DekuSeed_Shoot.wav")
                        self.hook = Hook(self.position, self.getDirection(self.row))
                        self.keyLock()
                        
                    if not self.running:
                        if not self.charging:
                            if event.key == pygame.K_c and not self.invincible:
                                equippedC = EQUIPPED["C"]
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
                                        self.frame = 0
                                        if self.blizzard == None:
                                            self.blizzard = Blizzard(self.position, self.getDirection(self.row))
                                            self.setWeaponDamage(self.blizzard)
                                        self.stop()
                                        self.freezing = True

                                    elif equippedC == 2 and self.clapReady:
                                        self.clap = Clap(self.position)
                                        self.setWeaponDamage(self.clap)
                                        self.clapReady = False
                                        self.vel = vec(0,0)
                                        self.positionLock = True

                                    elif equippedC == 3:
                                        self.charge()


                            elif event.key == pygame.K_z and INV["cleats"] and not self.invincible  and ( self.walking and (not self.movingDiagonal()) ):
                                #Tackle
                                self.runningDirection = self.row
                                self.run()

                        
                        if self.swordReady:
                            ##  Directional Movement    ##
                            if event.key == pygame.K_UP: # 2
                                self.move(2)

                            elif event.key == pygame.K_DOWN: # 0
                                self.move(0)
                                
                            elif event.key == pygame.K_LEFT: # 3
                                self.move(3)
                                
                            elif event.key == pygame.K_RIGHT: # 1
                                self.move(1)



            ## Handle if a key is released  ##
            elif event.type == pygame.KEYUP:

                if self.freezing:
                    if event.key == pygame.K_c:
                        #print("C")
                        #self.frame = 4
                        self.freezing = False
                    else:
                        return
                elif self.running:
                    
                    """ if event.key == pygame.K_z:
                        #Stop running
                        self.stop() """
                    if event.key == pygame.K_RIGHT and self.runningDirection == 1:
                        self.stop()
                    elif event.key == pygame.K_UP and self.runningDirection == 2:
                        self.stop()
                    elif event.key == pygame.K_LEFT and self.runningDirection == 3:
                        self.stop()
                    elif event.key == pygame.K_DOWN and self.runningDirection == 0:
                        self.stop()
                    

                else:
                    if self.charging:
                        if event.key == pygame.K_c:
                            self.shootSlash()

                    if event.key == pygame.K_UP:
                        #Display the proper sprite for diagonal
                        if self.vel[0] < 0:
                            self.row = 3
                        elif self.vel[0] > 0:
                            self.row = 1
                        #Stop upward velocity
                        if self.vel[1] < 0:
                            self.vel[1] = 0

                    elif event.key == pygame.K_DOWN:
                        #Display the proper sprite for diagonal
                        if self.vel[0] < 0:
                            self.row = 3
                        elif self.vel[0] > 0:
                            self.row = 1
                        #Stop downward velocity
                        if self.vel[1] > 0:
                            self.vel[1] = 0

                    elif event.key == pygame.K_LEFT:
                        #Stop leftward velocity
                        if self.vel[0] < 0:
                            self.vel[0] = 0
                        
                    elif event.key == pygame.K_RIGHT:
                    #Stop rightward velocity
                        if self.vel[0] > 0:
                            self.vel[0] = 0
        
        elif event.type != pygame.KEYDOWN and (self.vel[0] != 0 or self.vel[1] != 0):
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
        
    def handleCollision(self, object):
        if self.dying:
            return
        
        elif self.running:
            self.stop()
        
        elif self.freezing:
            self.freezing = False
        
        elif type(object) == PushableBlock:
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

        elif type(object) == Geemer and object.ignoreCollision:
            return
        elif issubclass(type(object), Enemy) and object.id != "shot":
            if self.charging:
                self.shootSlash()
            side = self.calculateSide(object)
            self.enemyCollision(object, side)

        else:
            side = self.calculateSide(object)
            self.preventCollision(object, side)

    def enemyCollision(self, enemy, side):
        if self.invincible or enemy.frozen:
            pass
        else:
            if INV["chanceEmblem"]:
                if self.hp == 1:
                    self.hp = 0
                else:
                    self.hp -= enemy.getDamage()
                    if self.hp <= 0:
                        self.hp = 1
                    SoundManager.getInstance().playSFX("hurt.wav")
                    self.invincible = True
                    self.knockback(side)
            else:
                self.hp -= enemy.getDamage()
                SoundManager.getInstance().playSFX("hurt.wav")
                self.invincible = True
                self.knockback(side)
            
    def preventCollision(self, object, side):
        #print("object", object)
        #print(object.position)
        #Prevents overlapping collision rects based on side
        #self.position = vec(self.position)
        #print("position", self.position)

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
        #print("clip",rect)
        #print(collision1)
        #print(collision2)
        ##Calculate the side
        side = ""
        if clipRect.width < clipRect.height:
            #print("x")
            #X direction
            if collision2.collidepoint(collision1.right,collision1.top) or collision2.collidepoint(collision1.right, collision1.bottom):
                #print("RIGHT")
                side = "right"
            else:
                #print("Left")
                side = "left"
        else:
            #print("Y")
            #Y direction
            if collision2.collidepoint(collision1.right, collision1.top) or collision2.collidepoint(collision1.left,collision1.top):
                #print("Up")
                side = "top"
            else:
                #print("Bottom")
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
                    if self.idleTimer >= 3:
                        self.headingOut = True
                        self.row = 1
                        self.idleTimer = 0
                        
                
                
            return
        
        if self.drunk:
            self.drunkTimer -= seconds
            if self.drunkTimer <= 0:
                self.undrink()

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
            self.walking = False
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
        
        #Update clap cooldown
        if EQUIPPED["C"] == 2 and self.clapReady == False:
            self.clapTimer += seconds
            if self.clapTimer >= 5.0:
                self.clapTimer = 0
                self.clapReady = True
        
        super().updatePlayer(seconds)
        self.position += self.vel * seconds

    def updateMovement(self):
        pass