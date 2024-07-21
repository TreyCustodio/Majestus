import pygame
from math import ceil
from UI import EventManager
from utils import SpriteManager
from . import (Drawable, HudImageManager, Slash, Blizzard, HealthBar, ElementIcon, EnergyBar, Blessing, Torch, AmmoBar, Fade, Drop, Heart, Text, Player, Enemy, NonPlayer, Sign, Chest, Key, Geemer, Switch, 
               WeightedSwitch, DamageIndicator, LightSwitch, TimedSwitch, LockedSwitch, Block, IBlock, Trigger, HBlock,
               PushableBlock, LockBlock, Bullet, Sword, Clap, Slash, Flapper, Number,
               Tile, Portal, Buck, Boulder, Map, BossHealth,
               Shadow, Walls, Floor, Camera)




from utils import SoundManager, vec, RESOLUTION, SPEECH, ICON, INV, COORD, FLAGS, EQUIPPED, UPSCALED
class DamageNumberManager(object):
    def __init__(self):
        self.numbers = []
        
    def addNumber(self, position, value):
        self.numbers.append(DamageNumber(position, value))
    
    def draw(self, engine, drawSurface):
        for num in self.numbers:
            engine.drawNumber(num.damagePos, num.damage, drawSurface, row = 3)
    
    def updateNumbers(self, engine, seconds):
        for num in self.numbers:
            num.damagePos[1] -= 20 * seconds
            if num.damagePos[1] <= num.maxDamagePos:
                self.numbers.pop(self.numbers.index(num))
    

class DamageNumber(object):
    def __init__(self, position, damage):
        self.damage = damage
        self.damagePos = position
        self.maxDamagePos = self.damagePos[1]-8


class AE(object):
    def __init__(self, room_dir = "", camera = False, size = vec(*RESOLUTION)):
        """
        __init__ is only ever called once
        """
        if room_dir != "":
            self.room_dir = room_dir
            self.walls = Walls(room_dir)
            self.floor = Floor(room_dir)
        
        if camera:
            self.camera = Camera()
        else:
            self.camera = None
        self.updatingPlayer = True
        self.textInt = 0
        self.timer = 0.0 #A universal timer; can be used for anything
        self.healthBarDrawn = False
        self.healthBarLock = False #If True, don't draw healthbar
        self.area = 0
        self.roomId = 0
        self.itemsToCollect = 0
        self.mapCondition = False #True if pink, False if green
        self.textBoxBackground = SpriteManager.getInstance().getSprite("TextBox2.png", (0,7))

        self.damageNums = DamageNumberManager()
        self.player = None
        self.resetting = False
        self.ignoreClear = False
        self.dropCount = 0
        self.pause_lock = False

        #Death
        self.dead = False
        self.dying = False
        self.deathTimer = 0

        #Room transitioning

        self.readyToTransition = False
        self.transporting = False
        self.transporting_area = False
        self.tra_room = None
        self.tra_pos = None
        self.tra_keepBGM = False
        self.enemyCounter = 0

        #Flash
        self.flashes = 0
        self.fading = False
        self.area_fading = False

        #Speaking
        self.textBox = False
        self.text = ""
        self.largeText = False
        self.icon = None
        self.boxPos = vec(30,64)
        self.promptResult = False
        ##Puzzle conditions
        self.room_set = False
        self.room_clear = False
        self.clearFlag = 0
        ##Object Lists
        self.enemies = [] #list of enemies to be used for placeEnemies()
        self.obstacles = []
        self.pushableBlocks = [] #pushable blocks
        self.npcs = [] #enemies that have been positioned properly
        self.spawning = [] #interactable objects and drops
        self.drops = []
        self.projectiles = [] #weapons
        self.switches = []
        self.blocks = []
        self.torches = []
        self.doors = []
        self.tiles = []
        self.drops = []
        self.topObjects = [] #Objects that need to be drawn after the player
        self.indicator = DamageIndicator()
        self.moneyImage = None
        self.keyImage = None
        self.transLock = True
        ##Boss
        self.bossTheme = None
        self.boss = None
        self.bossHealthbar = None
        self.fightingBoss = False
        self.drawBossHealth = False
        
        

        #Size of the room
        self.size = size#vec(*RESOLUTION)

        self.effects = []
        self.effects_behind_walls = []
        self.whiting = False
        #HUD
        self.healthBar = HealthBar.getInstance()
        self.ammoBar = AmmoBar.getInstance()
        self.elementIcon = ElementIcon.getInstance()
        self.energyBar = EnergyBar()
        #Unique room elements:
        #self.max_enemies
        #self.enemyPlacement
        #self.bgm
    
    """
    Getter Methods
    """

    """
    Returns:
    True if the healthbar is initialized.
    False otherwise
    """
    def getHealthbarInitialized(self):
        return self.healthBarDrawn

    """
    Returns:
    True if the healthbar is drawing damage.
    False otherwise
    """
    def getHealthBarDrawing(self):
        return self.healthBar.drawingHurt or self.healthBar.drawingHeal
    
    """
    Auxilary Methods
    """

    """
    Boss script load
    """
    def bsl(self, enemy, bossTheme):
        self.pause_lock = True
        self.bossTheme = bossTheme
        self.player.keyLock()
        self.boss = enemy
        self.bossHealthbar = BossHealth(enemyHealth= enemy.hp)
        self.fightingBoss = True
        self.drawBossHealth = True

    """
    Boss script end
    """
    def bse(self):
        self.fightingBoss = False

    def stopFadeIn(self):
        self.whiting = False
        self.transLock = False
        self.fading = False
        self.area_fading = False
        self.player.keyUnlock()
        self.player.keyDownUnlock()

    def reset(self):
        for n in self.npcs:
            n.respawn()
            if n.vanish:
                self.disappear(n)
        for d in self.drops:
            self.disappear(d)
        self.dropCount = 0

        self.textInt = 0
        self.fightingBoss = False
        self.boxPos = vec(30,64)
        self.drawBossHealth = False
        self.transLock = True
        self.promptResult = False
        self.indicator.setImage(0)
        self.readyToTransition = False
        self.transporting = False
        self.transporting_area = False
        self.whiting = False
        self.tra_room = None
        self.tra_pos = None
        self.tra_keepBGM = False
        if self.resetting:
            self.enemyCounter = 0
            self.room_clear = False
        if self.camera:
            self.camera.position = vec(0,0)
        

    def titleReset(self):
        self.reset()
        self.healthBar.drawn = False

    def deathReset(self):
        self.reset()
        self.healthBar.drawn = False
        self.player = None
        self.pause_lock = False
        self.dead = False
        self.dying = False
        self.deathTimer = 0

    def lockHealth(self):
        self.healthBarLock = True
    
    def unlockHealth(self):
        self.healthBarLock = False

    def renderObstacles(self):
        for o in self.obstacles:
            o.setRender()
    
    def vanishObstacles(self):
        for o in self.obstacles:
            o.vanish()

    def healPlayer(self, integer):
        if self.player.hp == INV["max_hp"]:
            return
        amountHealed = self.player.heal(integer)
        #self.healthBar.drawHeal(amountHealed)

    def getDrunk(self):
        self.player.drink()
    
    def getHigh(self):
        self.player.smoke()
    
    def zoom(self):
        self.player.zoom()
    
    def useSyringe(self):
        #player's hp = maxHp // 3
        #so damage is 2/3 of max_hp
        if self.player.hp == 1:
            return
        damage = (ceil((2 * INV["max_hp"])/3))
        if damage > self.player.hp:
            damage = self.player.hp - 1
        self.player.hurt(damage)
        self.healthBar.drawHurt(self.player.hp, damage)


    def initializeRoom(self, player= None, pos = None, keepBGM = False, placeEnemies = True):
        """
        Called every time you enter the room
        1. create wall boundaries
        2. adjust wall collision for doors in self.doors
        3. call createBlocks
        4. place the enemies in self.enemies
        """
        self.moneyImage = HudImageManager.getMoney()
        self.keyImage = HudImageManager.getKeys()
        self.bomboImage = HudImageManager.getBombos()
        EventManager.getInstance().toggleFetching()
        #SoundManager.getInstance().stopAllSFX()
        EQUIPPED["room"] = self.roomId
        if player != None:
            self.player = player
            self.player.position = pos 
        else:
            self.player = Player(vec(16*9, (16*11) - 8))

        self.createBounds()
        self.setDoors()
        self.createBlocks()
        if placeEnemies:
            self.placeEnemies(self.enemies)
        if not keepBGM:
            #SoundManager.getInstance().fadeoutBGM()
            if self.bgm != None:
                SoundManager.getInstance().playBGM(self.bgm)

    def initializeArea(self, player= None, pos = None, keepBGM = False, placeEnemies = True):
        """
        Called every time you enter the room
        1. create wall boundaries
        2. adjust wall collision for doors in self.doors
        3. call createBlocks
        4. place the enemies in self.enemies
        """
        self.moneyImage = HudImageManager.getMoney()
        self.keyImage = HudImageManager.getKeys()
        self.bomboImage = HudImageManager.getBombos()
        EventManager.getInstance().toggleFetching()
        #SoundManager.getInstance().stopAllSFX()
        EQUIPPED["room"] = self.roomId
        if player != None:
            self.player = player
            self.player.position = pos 
        else:
            self.player = Player(vec(16*9, (16*11) - 8))

        self.createBounds()
        self.setDoors()
        self.createBlocks()
        if placeEnemies:
            self.placeEnemies(self.enemies)
        if not keepBGM:
            #SoundManager.getInstance().fadeoutBGM()
            if self.bgm != None:
                SoundManager.getInstance().playBGM(self.bgm)

        self.area_fading = True
        self.whiting = True
        self.areaIntro.fadeIn()

    def createBounds(self):
        """
        Creates boundaries on the outer edge of the map
        """
        #Left side
        for i in range(1, 5):
            self.blocks.append(IBlock((8,i*16)))
        for i in range(8, 12):
            self.blocks.append(IBlock((8,i*16)))
        #Right side
        for i in range(1, 5):
            self.blocks.append(IBlock((RESOLUTION[0]-24,i*16)))
        for i in range(8, 12):
            self.blocks.append(IBlock((RESOLUTION[0]-24,i*16)))
        #Top side
        for i in range(1,8):
            self.blocks.append(IBlock((i*16, 0)))
        for i in range(11, 18):
            self.blocks.append(IBlock((i*16, 0)))
        #Bottom side
        for i in range(1,8):
            self.blocks.append(IBlock((i*16, RESOLUTION[1]-16)))
        for i in range(11, 18):
            self.blocks.append(IBlock((i*16, RESOLUTION[1]-16)))
    

    def setDoors(self):
        """
        Adjust the boundaries to fit doors
        """
        if 0 not in self.doors:
            self.blocks.append(IBlock((8*16, RESOLUTION[1]-16)))
            self.blocks.append(IBlock((9*16, RESOLUTION[1]-16)))
            self.blocks.append(IBlock((10*16, RESOLUTION[1]-16)))
        else:
            self.blocks.append(IBlock((16*8-8, RESOLUTION[1]-16)))
            self.blocks.append(IBlock((16*10+8, RESOLUTION[1]-16)))
        
        if 1 not in self.doors:        
            self.blocks.append(IBlock((RESOLUTION[0]-24, 5*16)))
            self.blocks.append(IBlock((RESOLUTION[0]-24, 6*16)))
            self.blocks.append(IBlock((RESOLUTION[0]-24, 7*16)))
        else:
            self.blocks.append(IBlock((RESOLUTION[0]-24, 16*7+8)))
            self.blocks.append(IBlock((RESOLUTION[0]-24, 16*5-8)))
        if 2 not in self.doors:   
            self.blocks.append(IBlock((8*16, 0)))
            self.blocks.append(IBlock((9*16, 0)))
            self.blocks.append(IBlock((10*16, 0)))
        else:
            self.blocks.append(IBlock((8*16-8, 0)))
            self.blocks.append(IBlock((16*10+8, 0)))
        if 3 not in self.doors:
            self.blocks.append(IBlock((8, 5*16)))
            self.blocks.append(IBlock((8, 6*16)))
            self.blocks.append(IBlock((8, 7*16)))
            
        else:
            self.blocks.append(IBlock((8, 16*7+8)))
            self.blocks.append(IBlock((8, 16*5-8)))
    
    #abstract
    def createBlocks(self):
        """
        Abstract method
        """
        pass
    
    def createStore(self):
        self.blocks.append(self.trigger1)
        for i in range(6, 13):
            if i == 9:
                pass
            else:
                self.blocks.append(IBlock((16*i, 16*9 + 8)))

        for i in range(6, 13):
            self.blocks.append(IBlock(COORD[i][2]))
        for i in range(3, 9):
            self.blocks.append(IBlock(COORD[5][i]))
        for i in range(3, 9):
            self.blocks.append(IBlock(COORD[13][i]))

    def placeEnemies(self, enemyLst):
        """
        Place the enemies according to a predetermined algorithm.
        The algorithm is selected based on the integer corresponding to
        self.enemyPlacement
        """
        self.enemyCounter = 0
        def refresh():
            for e in enemyLst:
                """ if e not in self.npcs:
                    if e.dead: """
                if e not in self.npcs:
                    self.npcs.append(e)
                e.respawn()
    
        if self.enemyPlacement > 0:
            if self.enemyPlacement == 1:
                """
                Four in the center
                """
                enemyLst[0].position = vec(16*6, 16*3)
                enemyLst[1].position = vec(16*11, 16*3)
                enemyLst[2].position = vec(16*6, 16*7)
                enemyLst[3].position = vec(16*11, 16*7)
                refresh()

            elif self.enemyPlacement == 2:
                """
                """
                
                enemyLst[0].position = COORD[6][3]
                enemyLst[1].position = COORD[11][3]
                enemyLst[2].position = COORD[6][7]
                enemyLst[3].position = COORD[11][7]

                enemyLst[4].position = COORD[14][3]
                enemyLst[5].position = COORD[3][3]
                enemyLst[6].position = COORD[14][7]
                enemyLst[7].position = COORD[3][7]
                refresh()

            elif self.enemyPlacement == 3:
                enemyLst[0].position = COORD[6][3]
                enemyLst[1].position = COORD[11][3]
                enemyLst[2].position = COORD[6][7]
                enemyLst[3].position = COORD[11][7]
                enemyLst[4].position = COORD[6][9]
                enemyLst[5].position = COORD[11][9]
                refresh()
                
            ##1 enemy in the center
            elif self.enemyPlacement == 4:
                enemyLst[0].setPosition(vec(16*9, 16*5))
                refresh()
        else:
            for i in range(self.max_enemies):
                enemyLst[i].position = enemyLst[i].initialPos
            refresh()
            """ for e in enemyLst:
                if not e.dead and e not in self.npcs:
                    self.npcs.append(e)
                if not e.frozen:
                    e.freeze(playSound=False)
                    e.freezeTimer = 4.0 """
                

                    

    def fade(self):
        """
        Initializes fadeout by locking
        player and setting self.fading to True
        """
        self.player.keyLock()
        self.fading = True

    def whiteOut(self):
        self.player.keyLock()
        self.whiting = True


    def transport(self, room=None, position=None, keepBGM = False, intro = False, fade_white = False):
        """
        Transport the player to a different room.
        room -> room (class) name in majestus.py
        position -> 0-3 representing cardinal direction, or a specific coordinate
        keepBgm -> keeps the bgm
        intro -> special properties for transport because no player yet
        """
        if not self.transporting and not self.transLock:
            
            EventManager.getInstance().startTransition()
            if intro:
                self.transporting = True
                self.tra_room = room.getInstance()
                return
            
            #self.player.keyDownLock()
            if fade_white:
                self.whiteOut()
            else:
                self.fade()
            self.transporting = True
            self.tra_room = room
            
            if position == 0:
                self.tra_pos = vec(16*9, 16*11)
            elif position == 1:
                self.tra_pos = vec(16*16, 16*6 - 8)
            elif position == 2:
                self.tra_pos = vec(16*9, 8)
            elif position == 3:
                self.tra_pos = vec(16*2, 16*6-8)
            else:
                self.tra_pos = position
                
            self.tra_keepBGM = keepBGM
            if not keepBGM:
                SoundManager.getInstance().fadeoutBGM()
            
            pygame.event.clear()

    def transportArea(self, room = None, position= None):
        if not self.transporting and not self.transLock:
            EventManager.getInstance().startTransition()
            self.whiteOut()
            self.transporting = True
            self.transporting_area = True
            self.tra_room = room
            
            if position == 0:
                self.tra_pos = vec(16*9, 16*11)
            elif position == 1:
                self.tra_pos = vec(16*16, 16*6 - 8)
            elif position == 2:
                self.tra_pos = vec(16*9, 8)
            elif position == 3:
                self.tra_pos = vec(16*2, 16*6-8)
            else:
                self.tra_pos = position
                
            self.tra_keepBGM = False
            SoundManager.getInstance().fadeoutBGM()
            
            pygame.event.clear()

    """
    Transports the player to a specified position
    """
    def transportPos(self, room = None, position = None, keepBGM = False):
        if not self.transporting:
            EventManager.getInstance().startTransition()
            
            self.fade()
            self.transporting = True
            self.tra_room = room
            
            self.tra_pos = position
                
            self.tra_keepBGM = keepBGM
            if not keepBGM:
                SoundManager.getInstance().fadeoutBGM()
            
            pygame.event.clear()

    def displayText(self, text = "", icon = None, large = True):
        """
        Display text
        """
        if icon != None:
            self.icon = icon
            self.boxPos = vec(self.player.position[0]-122, self.player.position[1]-32)
            if self.boxPos[0] < 16:
                self.boxPos[0] = 16
            elif self.boxPos[0]+244 > RESOLUTION[0]-16:
                self.boxPos[0] = (RESOLUTION[0] - 16) - 244

            if self.boxPos[1] < 32:
                self.boxPos[1] = 32
            elif self.boxPos[1]+64 > RESOLUTION[1]-16:
                self.boxPos[1] = (RESOLUTION[1] - 16)-64

        else:
            self.boxPos = vec(self.player.position[0]-122, self.player.position[1]-32)
            if self.boxPos[0] < 16:
                self.boxPos[0] = 16
            elif self.boxPos[0]+244 > RESOLUTION[0]-16:
                self.boxPos[0] = (RESOLUTION[0] - 16) - 244

            if self.boxPos[1] < 16:
                self.boxPos[1] = 16
            elif self.boxPos[1]+64 > RESOLUTION[1]-16:
                self.boxPos[1] = (RESOLUTION[1] - 16)-64

        self.textBox = True
        self.text = text
        self.largeText = large
        
        if self.player != None:
            self.player.stop()
    
    def flash(self, num = 0):
        """
        Flash the screen white
        """
        
        self.playSound("LA_Dungeon_Signal.wav")
        self.flashes = num

    def wait(self, time):
        """
        Halt the progression of the game for a certain amount of time
        """
        clock = pygame.time.Clock()
        seconds = 0
        while seconds < time:
            clock.tick(60)
            seconds += (clock.get_time() / 1000)
    
    def disappear(self, obj):
        if obj in self.drops:
            self.drops.pop(self.drops.index(obj))
        elif obj in self.spawning:
            self.spawning.pop(self.spawning.index(obj))
        elif obj in self.npcs:
            self.npcs.pop(self.npcs.index(obj))
        elif obj in self.projectiles:
            self.projectiles.pop(self.projectiles.index(obj))
        elif obj in self.blocks:
            self.blocks.pop(self.blocks.index(obj))
        elif obj in self.obstacles:
            self.obstacles.pop(self.obstacles.index(obj))
        elif obj in self.switches:
            self.switches.pop(self.switches.index(obj))
        
    def playSound(self, name):
        SoundManager.getInstance().playSFX(name)
    
    def stopSound(self, name):
        SoundManager.getInstance().stopSFX(name)
    
    def stopAllSounds(self):
        SoundManager.getInstance().stopAllSFX()

    def playBgm(self, name):
        SoundManager.getInstance().playBGM(name)
    
    def fadeBgm(self):
        SoundManager.getInstance().fadeoutBGM()

    """
    Event control methods
    """
    def weaponControl(self):
        #Basic bullet
        if self.player.bullet != None:
            self.projectiles.append(self.player.getBullet())
            self.player.bullet = None

        #Flames
        if self.player.sword != None:
            self.projectiles.append(self.player.getFlame())
            self.playSound(self.player.swordSound)
            self.player.sword = None
        
        #Thunder clap
        if self.player.clap != None:
            self.projectiles.append(self.player.getClap())
            self.playSound(Clap.SOUND)
            self.player.clap = None
        
        #Gale slash
        if self.player.slash != None:
            self.projectiles.append(self.player.getSlash())
            self.playSound("plasma_shot.wav")
            self.player.slash = None
        
        #Blizzard
        if self.player.blizzard != None and self.player.blizzard not in self.projectiles:
            self.projectiles.append(self.player.getBlizzard())
            #self.playSound("")

        if self.player.hook != None:
            self.projectiles.append(self.player.getHook())
            self.player.hook = None

    def interactableEvents(self, event):
        """
        Handles interaction from the player
        """
        if self.spawning:
            for n in self.spawning:
                if not n.drop and self.player.interactable(n):
                    self.player.handleEvent(event, n, self)
                    return 
                
        self.player.handleEvent(event)

    def interactableEvents_C(self, event):
        if self.spawning:
            for n in self.spawning:
                if not n.drop and self.player.interactable(n):
                    self.player.handleEvent_C(event, n, self)
                    return
                
        self.player.handleEvent_C(event)


    def handleEvent(self, event):
        self.interactableEvents(event)
    
    def handleEvent_C(self, event):
        self.interactableEvents_C(event)
    
    """
    Collision methods
    """
   


    def despawnOnPress(self, obj, switch):
        """
        Despawns object if the switch is pressed
        """
        if type(switch) == LightSwitch:
            if switch.pressed:
                if obj in self.blocks:
                    self.playSound("menuclose.wav")
                    self.blocks.pop(self.blocks.index(obj))
                    

            elif (obj not in self.blocks) and (obj not in self.spawning):
                if type(obj) == Block:
                    self.playSound("menuopen.wav")
                    self.blocks.append(obj)
                else:
                    self.playSound("menuopen.wav")
                    self.spawning.append(obj)

        elif switch.pressed and (obj in self.blocks or obj in self.spawning):
            if obj in self.blocks:
                self.blocks.pop(self.blocks.index(obj))
            else:
                self.spawning.pop(self.spawning.index(obj))

    def spawnOnPress(self, obj, switch):
        """
        Spawns an object if the corresponding switch is pressed
        """
        #Spawn if switch pressed
        if type(obj) == PushableBlock:
            if switch.pressed and (obj not in self.pushableBlocks):
                self.playSound("menuclose.wav")
                self.pushableBlocks.append(obj)
            return

        elif type(switch) == LightSwitch or type(switch) == TimedSwitch:
            if obj in self.spawning:
                if (not switch.pressed):
                    self.playSound("menuopen.wav")
                    self.disappear(obj)
            
        
        if (not obj.interacted) and switch.pressed and not(obj in self.spawning):
            self.playSound("menuclose.wav")
            self.spawning.append(obj)

    def pressSwitches(self):
        """
        Presses a switch if the player is on it
        """
        for n in self.switches:
            if self.player.doesCollide(n):
                if (not n.pressed) and type(n) != WeightedSwitch:
                    n.press()

    def npcCollision(self):

        for n in self.npcs:
        #Check if it collides with the player first
            if not self.player.ignoreCollision and self.player.doesCollide(n):
                if self.player.running:
                    if not n.freezeShield and not n.frozen:
                        if n.id == "noStop":
                            n.freeze()
                        else:
                            self.player.stop()
                            n.freeze()

                if not n.frozen:
                    if not self.player.invincible:
                        if n.handlePlayerCollision(self.player):
                            self.player.handleCollision(n)
                            #player should be invincible now
                            if self.player.invincible and not self.healthBar.drawingHurt:
                                self.healthBar.drawHurt(self.player.hp, n.damage)
           

            #Enemies
            if issubclass(type(n),Enemy):
                if self.projectiles:
                    for p in self.projectiles:
                        self.projectilesOnEnemies(p,n)
                        
    def pushableBlockCollision(self):
        if self.pushableBlocks:
            for block in self.pushableBlocks:
                self.projectilesOnBlocks(block)
                if self.player.doesCollide(block):
                    self.player.handleCollision(block)

                for b in self.blocks:
                    if block.doesCollide(b):
                        block.reset()


                for s in self.spawning:
                    if block.doesCollide(s):
                        block.reset()

                for n in self.npcs:
                    if block.doesCollide(n):
                        block.reset()
                
            #Press a switch if the block is on it
            switchIndex = block.doesCollideList(self.switches)
            if switchIndex != -1:
                if type(self.switches[switchIndex]) == WeightedSwitch:
                    self.switches[switchIndex].press(block)
                else:
                    self.switches[switchIndex].press()
            #elif *Other possible conditions for block collision could go here. (Walls)
            else:
                pass
    
    def enemyCollision(self, other):
        for e in self.npcs:
            if e.doesCollideBlock(other):
                e.inWall = True
                e.bounce(other)
            elif e.inWall:
                e.inWall = False

    def interactableCollision(self):
        if self.spawning:
            for n in self.spawning:
                if not n.ignoreCollision:
                    if self.player.doesCollide(n):
                        if type(n) == Key:
                            self.disappear(n)
                            n.interact(self.player, self)
                        else:
                            self.player.handleCollision(n)
    
        if self.drops:
            for n in self.drops:
                if not n.ignoreCollision:
                    if self.player.doesCollide(n):
                        self.disappear(n)
                        self.dropCount -= 1
                        n.interact(self.player)
                
    #abstract
    def blockCollision(self):
        """
        Abstract method
        """
        pass
    
    """
    projectile -> weapon
    other -> enemy
    """
    def projectilesOnEnemies(self, projectile, other):
        if other.doesCollideProjectile(projectile):
            if other.ignoreCollision:
                return
            if not projectile.hit:
                other.handleCollision(projectile)
                if other.hit:
                    ##Display the damage indicator
                    hp_after = other.hp
                    hp_before = other.hp + projectile.damage
                    #self.indicator.setImage(other.indicatorRow, hp_before, hp_after, other.maxHp, projectile.damage)
                    damage = other.getInjury()
                    other.resetInjury()
                    ##Display damage numbers appropriately
                    if projectile.id == "slash" or projectile.id == "blizz":
                        self.damageNums.addNumber(vec(other.getCenterX(), other.position[1]), damage)
                    else:
                        self.damageNums.addNumber(vec(other.getCenterX(), other.position[1]), damage)
                    other.hit = False
                    if projectile.id == "arrow":
                        projectile.handleOtherCollision(self)
                        return
                projectile.handleCollision(self)
                
                
               


    def projectilesOnSpawning(self, projectile, other):
        if projectile.doesCollide(other):
            if not projectile.hit:
                projectile.handleCollision(self)
            

    def projectilesOnBlocks(self, block):
        for p in self.projectiles:
            if not p.hit:
                if p.doesCollide(block):
                #p.handleCollision(self)
                    p.handleCollision(self)
    
    def projectilesOnTorches(self, torch):
        for p in self.projectiles:
            if p.type == 1 and p.doesCollide(torch):
                torch.light()

    def obstacleCollision(self):
        if self.obstacles:
            for o in self.obstacles:
                if o.render:
                    if self.player.doesCollide(o):
                        self.player.handleCollision(o)
                    self.enemyCollision(o)
                    for p in self.projectiles:
                        if not p.hit and p.doesCollide(o):
                            p.handleCollision(self)
                            o.handleCollision(p, self)

    def handleCollision(self):
        self.npcCollision()
        self.obstacleCollision()
        if not self.dying:
            self.blockCollision()
        self.interactableCollision()
        self.pressSwitches()
        self.pushableBlockCollision()
        
        #Call super().handleCollision()
        #Then self.spawn/despawn however you want
    """
    Update methods
    """
    def updateLightSwitch(self, switch, obj=None):
        if obj == None:
            switch.update(self.player)

    def outOfBoundsSafety(self, n):
        if n.boundsSafety():
            if n.position[0] >= RESOLUTION[0]:
                n.position[0] = RESOLUTION[0] - 64
                n.vel[0] = -n.speed
            elif n.position[0] <= 0:
                n.position[0] = 64
                n.vel[0] = n.speed

            if n.position[1] >= RESOLUTION[1]:
                n.position[1] = RESOLUTION[1] - 64
                n.vel[1] = -n.speed
            elif n.position[1] <= 0:
                n.position[1] = 64
                n.vel[1] = n.speed

    def update_Enemy(self, seconds, n):
        n.update(seconds, self.player.position)
        self.outOfBoundsSafety(n)

        if n.id == "spawn":
            if n.spawning:
                for i in n.getObjectsToSpawn():
                    self.npcs.append(i)
                n.resetObjects()
        if n.dead:
            self.disappear((n))
            if self.dropCount < 5:
                drop = n.getDrop()
                if drop != None:
                    if drop.id == "greenHeart":
                        self.spawning.append(drop)
                    elif (drop.id == "heart" or drop.id == "bigHeart") and self.player.hp == INV["max_hp"]:
                        drop = n.getMoney()
                        if drop != None:
                            self.drops.append(drop)
                    else:
                        self.drops.append(drop)
                    self.dropCount += 1
            if n.increaseCount():
                self.enemyCounter += 1
        elif n.fakeDead:
            if self.dropCount < 5:
                drop = n.getDrop()
                if drop != None:
                    self.drops.append(drop)
                    self.dropCount += 1
            else:
                n.readyToDrop = False
        
        
        if not self.ignoreClear and not self.room_clear and self.enemyCounter == self.max_enemies:
            self.playSound("room_clear.mp3")
            self.room_clear = True
    

    def updateNpcs(self, seconds):
        ##Enemies
        for n in self.npcs:
            self.update_Enemy(seconds, n)
            
        for n in self.topObjects:
            self.update_Enemy(seconds, n)
    
    #Most likely to be modified for cutscenes
    def updateSpawning(self, seconds):
        ##  NPCs
        if self.spawning:
            for n in self.spawning:
                n.update(seconds)
                if n.disappear:
                    self.disappear(n)
    
    def updateDrops(self, seconds):
        if self.drops:
            for n in self.drops:
                n.update(seconds)
                if n.disappear:
                    self.disappear(n)
                    self.dropCount -= 1
          

    def updatePlayer(self, seconds):
        """
        Updates the player's position and states as needed.
        Player is not updated during fading,
        but Player will still handle events in order
        to have the smoothest room transitions.
        """
        if self.player.dying:
            self.player.update(seconds)
            if self.player.headingOut:
                self.boxPos = vec(32,RESOLUTION[1]-74)
                self.displayText("Aight, Imma head out.&&")
                self.player.headingOut = False
                self.player.walking = True
                self.player.vel[1] = 0
                self.player.vel[0] = self.player.speed
        elif self.player.hp <= 0:
            #DIE
            self.player.die()
            self.pause_lock = True
            self.dying = True
            SoundManager.getInstance().fadeoutBGM()
            self.player.update(seconds)
        elif not self.fading:
            self.player.update(seconds)
    
    #abstract
    def updateSwitches(self, seconds):
        """
        Abstract method
        """
        pass

    def updateProjectiles(self, seconds):
        for p in self.projectiles:
            p.update(seconds, self)

    
    def updatePushableBlocks(self,seconds):
        if self.pushableBlocks:
            for block in self.pushableBlocks:
                block.update(seconds, self.player, self.player.row)

    def updateCamera(self,seconds):
        """ if self.camera.position[0] == 0:
            return
        elif self.camera.position[0] == 912:
            return """

        self.camera.position[0] = self.player.position[0] - (self.camera.getSize()[0] // 2)
        
        #self.camera.position += self.player.vel * seconds
        Drawable.updateOffset(self.camera, self.size)
        pass

    #abstract
    def handleClear(self):
        """
        Update the game once all enemies in the
        room are defeated.
        """
        pass
    
    def updateHealthBar(self, seconds):
        self.healthBar.update(seconds)

    def updateHUD(self, seconds):
        HudImageManager.update(seconds)
        self.indicator.update(seconds)
        self.damageNums.updateNumbers(self, seconds)
        if not self.healthBarLock:
            self.updateHealthBar(seconds)
        
        if self.drawBossHealth:
            if self.bossHealthbar.initializing:
                self.bossHealthbar.update(seconds)
                if not self.bossHealthbar.initializing:
                    self.player.keyUnlock()
                    self.pause_lock = False
                    if self.bossTheme != "None":
                        self.playBgm(self.bossTheme)
                    self.boss.moving = True
                    self.boss.ignoreCollision = False
            elif self.bossHealthbar.defeated and self.fightingBoss:
                self.bse()
                self.bossHealthbar.update(seconds)
            else:
                self.bossHealthbar.update(seconds)
        

    def handlePrompt(self):
        pass

    def handleStorePrompt(self):
        if self.selectedItem == "potion":
            INV["money"] -= 5
            self.displayText("You bought a potion!&&\nDrink it from the [ITM]\nrow in the pause menu!\n")
            INV["potion"] += 1
            self.promptResult = False
            self.selectedItem = ""
        elif self.selectedItem == "smoothie":
            INV["money"] -= 20
            self.displayText("Sweet! A delectable smoothie!&&\nDrink it from the [ITM]\nrow in the pause menu!\n        Delicioso!&&\n")
            INV["smoothie"] += 1
            self.promptResult = False
            self.selectedItem = ""
        elif self.selectedItem == "emblem":
            INV["money"] -= 60
            self.displayText("    You bought the\n    [Chance Emblem]!\nYou'll survive any attack\nas long as you're above 1 HP!\n")
            INV["chanceEmblem"] = True
            self.promptResult = False
            self.selectedItem = ""
        elif self.selectedItem == "syringe":
            INV["money"] -= 30
            self.displayText("      You bought the\n         [Syringe]!\nSap your health away in\nthe pause menu's [ITM] row.\n")
            INV["syringe"] = True
            self.promptResult = False
            self.selectedItem = ""

    def finishFade(self):
        """
        Sets self.readyToTransition to True.
        This lets the ScreenManager know
        to switch game engines.
        """
        self.fading = False
        self.readyToTransition = True



    def update(self, seconds, updateEnemies = True, updatePlayer = True):
        
        if self.transporting:
            return
        
        if self.area_fading:
            if self.areaIntro.fading:
                self.areaIntro.update(seconds)
                if not self.areaIntro.fading:
                    self.stopFadeIn()
            return
                    
        if not self.mapCondition:
            if self.itemsToCollect == 0:
                self.mapCondition = True
                Map.getInstance().rooms[self.area][self.roomId].clearRoom()
        
        ##Visual effects
        if self.effects:
            for e in self.effects:
                e.update(seconds)
        if self.effects_behind_walls:
            for e in self.effects_behind_walls:
                e.update(seconds)
        ##Pop-up messages
        if not FLAGS[17] and INV["flameShard"] > 0:
            FLAGS[17] = True
            self.displayText(SPEECH["flameShard"])

        if not FLAGS[18] and INV["frostShard"] > 0:
            FLAGS[18] = True
            self.displayText(SPEECH["frostShard"])

        if not FLAGS[19] and INV["boltShard"] > 0:
            FLAGS[19] = True
            self.displayText(SPEECH["boltShard"])

        if not FLAGS[20] and INV["galeShard"] > 0:
            FLAGS[20] = True
            self.displayText(SPEECH["galeShard"])
        
        ##Prompt Results
        if self.promptResult:
            self.handlePrompt()
        if self.dying:
            
            self.updatePlayer(seconds)
            if self.player.dead:
                self.deathTimer += seconds
                if self.deathTimer >= 2:
                    self.dead = True

            
        if self.torches:
            for t in self.torches:
                t.update(seconds)
        if self.obstacles:
            for o in self.obstacles:
                o.update(seconds)

        if self.updatingPlayer:
            self.updatePlayer(seconds)
        self.updateDrops(seconds)
        self.updateSpawning(seconds)
        if updateEnemies:
            self.updateNpcs(seconds)
        self.updatePushableBlocks(seconds)
        self.updateSwitches(seconds)
        self.updateProjectiles(seconds)
        self.updateHUD(seconds)
        if self.tiles:
            for t in self.tiles:
                t.update(seconds)
        if not self.ignoreClear:
            if self.room_clear and self.clearFlag == 0:
                self.clearFlag = 1
                self.handleClear()
        
        if self.camera:
            self.updateCamera(seconds)
        
        
    

    """
    Draw Methods
    """
    """
    Nonetype gets getting passed in
    """
    def drawNpcs(self, drawSurface):
        
        if self.spawning:
            for n in self.spawning:
                if n != None:
                    if self.player.interactable(n):
                        n.setInteractable()
                    else:
                        if n.interactable:
                            n.interactable = False
                    n.draw(drawSurface)
        
        if self.obstacles:
            for o in self.obstacles:
                o.draw(drawSurface)

        for n in self.npcs:
            if n.belowDrops:
                n.draw(drawSurface)

        if self.drops:
            for n in self.drops:
                n.draw(drawSurface)

        if self.torches:
            for n in self.torches:
                if not n.lit and self.player.interactableObjects(n):
                    n.setInteractable()
                elif n.interactable:
                    n.interactable = False

        if self.npcs:
            for n in self.npcs:
            #Consider making enemies appear right before the player
                if not n.top and not n.belowDrops:
                    n.draw(drawSurface)
        
    def drawProjectiles(self, drawSurface):
        #Projectiles/weapons
        if self.projectiles:
            for p in self.projectiles:
                p.draw(drawSurface)

    def drawFlash(self, drawSurface):
        self.flashes -= 1
        Drawable((0,0), "white.png").draw(drawSurface)

    def drawBlocks(self, drawSurface):
        for block in self.blocks:
            block.draw(drawSurface)
        if self.torches:
            for torch in self.torches:
                torch.draw(drawSurface)
        
    def drawArea(self, drawSurface):
        self.areaIntro.draw(drawSurface)

    def drawPushable(self, drawSurface):
        if self.pushableBlocks:
            for block in self.pushableBlocks:
                block.draw(drawSurface)

    def drawSwitches(self, drawSurface):
        for switch in self.switches:
            switch.draw(drawSurface)

    def drawDamage(self, drawSurface):
        self.damageNums.draw(self, drawSurface)
    
    def drawTopLayer(self, drawSurface):
        if self.topObjects:
            for o in self.topObjects:
                o.draw(drawSurface)
        
        for n in self.npcs:
            if n.top:
                n.drawTop(drawSurface)
        
    def drawHud(self, drawSurface):
        """
        Money
        """
        self.moneyImage.draw(drawSurface)        
        Number((14, self.moneyImage.position[1]), row = 1).draw(drawSurface)
        if INV["money"] == INV["wallet"]:
            self.drawNumber(vec(34, self.moneyImage.position[1]), INV["money"], drawSurface, row = 2)
        else:
            self.drawNumber(vec(34, self.moneyImage.position[1]), INV["money"], drawSurface)

        """
        Keys
        """
        self.keyImage.draw(drawSurface)
        Number((14, self.keyImage.position[1]), row = 1).draw(drawSurface)
        self.drawNumber(vec(34, self.keyImage.position[1]), INV["keys"], drawSurface)
        
        """
        Ammo
        """
        if EQUIPPED["Arrow"] == 1:
            self.bomboImage.draw(drawSurface)
            Number((14, self.bomboImage.position[1]), row = 1).draw(drawSurface)
            self.drawNumber(vec(34, self.bomboImage.position[1]), INV["bombo"], drawSurface)

        """
        Healthbar
        """
        ##  Heart Image to the left and HP count
        self.healthBar.drawHeart(drawSurface, self.player)

        
        ##  Rest of the bar
        if not self.healthBarLock:
            if self.healthBar.drawn:
                self.healthBarDrawn = True
                self.healthBar.draw(drawSurface, self.player)
            else:
                if not self.player.key_lock:
                    self.player.keyLock()
                self.healthBar.drawFirst(drawSurface, self.player)
        
        if self.drawBossHealth:
            self.bossHealthbar.draw(drawSurface, self.boss.hp)
            if self.bossHealthbar.doneDrawing:
                self.drawBossHealth = False
        
        self.ammoBar.draw(drawSurface, self.player)
        self.elementIcon.draw(drawSurface)
        self.indicator.draw(drawSurface)
        self.drawDamage(drawSurface)
        HudImageManager.draw(drawSurface)

        

        if EQUIPPED["C"] == 2:
            self.energyBar.drawThunder(self.player.clapTimer, drawSurface)

        elif EQUIPPED["C"] == 3:
            
            self.energyBar.drawWind(self.player.chargeTimer, drawSurface)
        else:
            self.energyBar.draw(drawSurface)
        
        if self.player.drunk:
            self.drawNumber(vec(8,64), int(self.player.drunkTimer), drawSurface, row = 3)

        
    def drawTiles(self, drawSurface):
        if self.tiles:
            for t in self.tiles:
                t.draw(drawSurface)


    def drawNumber(self, position, number, drawSurface, row = 0):
        if number >= 10:
            currentPos = vec(position[0]-3, position[1])
            number = str(number)
            for char in number:
                num = Number(currentPos, int(char), row)
                num.position[0] -= num.getSize()[0] // 2
                num.draw(drawSurface)
                currentPos[0] += 6
        else:
            num = Number(position, number, row)
            num.position[0] -= num.getSize()[0] // 2
            num.draw(drawSurface)


    def draw(self, drawSurface):
        """
        Draw the objects on the drawSurface after updating them
        """
    
        if self.dying:
            Drawable(fileName="b.png").draw(drawSurface)
            self.player.draw(drawSurface)
            return
        
        if self.flashes > 0:
            self.drawFlash(drawSurface)
            return
        
        #Background/Tiles
        self.floor.draw(drawSurface)
        
        
        self.drawTiles(drawSurface)
        
        #Switches
        self.drawSwitches(drawSurface)
        
        if self.effects_behind_walls:
            for e in self.effects_behind_walls:
                e.draw(drawSurface)
        self.walls.draw(drawSurface)

        #Blocks
        self.drawBlocks(drawSurface)
        #Pushable blocks
        self.drawPushable(drawSurface)
        #Npcs
        self.drawNpcs(drawSurface)

        self.drawProjectiles(drawSurface)
        
        #Player
        self.player.draw(drawSurface)

        

        #Objects above player
        self.drawTopLayer(drawSurface)

        if self.effects:
            for e in self.effects:
                e.draw(drawSurface)
        
        

        #HUD
        self.drawHud(drawSurface)
        
        #Weapons
        self.weaponControl()
    
    def drawText(self, drawSurface):
        self.draw(drawSurface)
        image = Drawable(self.boxPos, "TextBox2.png", (0,7))
        image.draw(drawSurface)

class AbstractEngine(object):

    """
    Abstract engine class for each room.
    """

    _INSTANCE = None
    

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._AE()
      
        return cls._INSTANCE

    @classmethod
    def tearDown(cls):
        if cls._INSTANCE != None:
            cls._INSTANCE = None
        return None
    
    class _AE(AE):
        def __init__(self, player = None):
            super().__init__(player)