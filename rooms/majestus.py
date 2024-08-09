from gameObjects import *

"""
This file contains all data pertaining
to each room's engine. Each class represents
a room's engine, and they all inherit from
AbstractEngine.
"""

"""
Intro Cutscene
"""
class Intro_Cut(AbstractEngine):

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._Intro_Cut()
        return cls._INSTANCE
    
    class _Intro_Cut(AE):
        def __init__(self):
            """
            Does not call super().__init()
            """
            self.fading = False
            self.player = None
            self.largeText = False
            self.introDone = False
            self.textBox = False
            self.text = ""
            self.icon = None
            self.boxPos = vec(32,64)
            self.textInt = 0
            self.background = Level("intro_cut.png")
            self.timer = 0
            self.playingBgm = False
            self.light = Drawable(vec(16*4, 16*3), fileName="light.png", offset=(0,0))
            self.red = Level(fileName = "introcut_1.png")
            self.frameTimer = 0.0
            self.frame = 0
            self.dark = Drawable(vec(16*12, 16*3), fileName="light.png", offset=(4,0))
            self.darkFrame = 4
        
        def reset(self):
            self.playingBgm = False
            self.fading = False
            self.player = None
            self.introDone = False
            self.textBox = False
            self.text = ""
            self.icon = None
            self.boxPos = vec(32,64)
            self.textInt = 0
            self.timer = 0

        def playBgm(self):
            SoundManager.getInstance().playBGM("still-dreaming.mp3")
            self.playingBgm = True

        def displayText(self, text = "", icon = None, large = True):
            """
            Display text
            """
            self.textBox = True
            self.text = text
            self.largeText = large
          

        def draw(self, drawSurface):
            
            if self.fading:
                Fade.getInstance().draw(drawSurface)
                return
            elif self.textInt >= 8:
                Level(fileName="intro_cut.png").draw(drawSurface)
            elif self.textInt >= 6:
                Level(fileName="majestus.png").draw(drawSurface)
            elif self.textInt == 4:
                Level(fileName="intro_cut.png").draw(drawSurface)
            elif self.textInt == 3:
                self.boxPos = vec(32, RESOLUTION[1]-(64+32))
                self.red.draw(drawSurface)
                self.light.draw(drawSurface)
                self.dark.draw(drawSurface)
            elif self.textInt == 2:
                self.boxPos = vec(32, RESOLUTION[1]-(64+32))
                Level(fileName = "gods.png").draw(drawSurface)
            else:
                self.background.draw(drawSurface)

            if self.textInt < 2:
                Text(vec(0,0), text = "Press SPACE to skip").draw(drawSurface)
            
        
        
        def handleEvent(self):
            pass

        def handleCollision(self):
            pass

        def update(self, seconds):
            """
            Fade within Intro engine,
            ScreenManager fades In after introDone == True
            """
            if self.textInt == 3:
                if self.timer >= 2.0:
                    self.timer = 0.0
                    self.textInt += 1
                    return
                else:
                    self.timer += seconds
                    return
            
            elif self.textInt == 5:
                if self.timer >= 1.0:
                    self.timer = 0.0
                    self.textInt += 1
                    return
                else:
                    self.timer += seconds
                    return
            elif self.textInt == 7:
                if self.timer >= 2.0:
                    self.timer = 0.0
                    self.textInt += 1
                    return
                else:
                    self.timer += seconds
                    return
                
            elif self.textInt > 10:
                if Fade.getInstance().frame == 8:
                    self.timer += seconds
                    if self.timer >= 0.5:
                        self.timer = 0.0
                        SoundManager.getInstance().fadeoutBGM()
                        self.introDone = True
                        return
                    return
                else:
                    Fade.getInstance().update(seconds)
                    return
                
            self.timer += seconds
            if self.timer >= 1:
                self.displayText(INTRO[self.textInt], large = True)
                self.timer = 0
                self.textInt += 1



class Test(AbstractEngine):

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._T()
      
        return cls._INSTANCE
    
    class _T(AE):
        def __init__(self):
            super().__init__("test")
            self.bgm = "MSM_Castle.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.firi = Firi(vec(16*9, 16*6), 1)
            self.npcs = [

            ]

            self.doors = [0]
            self.trigger1 = Trigger(door = 0)
            self.spawning = [ 
                Geemer(vec(16*5, 16*9), text=SPEECH["lava_knight"],mobster=True)#GreenHeart(vec(16*2, 16*10))
                ]

            self.obstacles = [
            ]

        def initializeRoom(self, player=None, pos=None, keepBGM=False, placeEnemies=True):
            super().initializeRoom(player, pos, keepBGM, placeEnemies)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        pass
                        #self.transport(Flame_9, 2, keepBGM=True)
                    else:
                        self.player.handleCollision(b)

                
                    
"""
Testing
"""

class Knight(AbstractEngine):

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Kn()
      
        return cls._INSTANCE
    
    class _Kn(AE):
        def __init__(self):
            super().__init__("knight")
            self.bgm = "tension.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.knight = LavaKnight(vec(RESOLUTION[0]//2-16, RESOLUTION[1]//2-16))
            self.knight.ignoreCollision = True
            self.enemies = [
                
                Bopper(COORD[2][2]),
                Bopper(COORD[16][2]),
                Bopper(COORD[2][10]),
                Bopper(COORD[16][10]),
            ]
            self.doors = [0, 2]
            self.trigger1 = Trigger(door = 0)
            self.spawning = [ 
                #GreenHeart(vec(16*2, 16*10))
                ]
            self.playingMusic = False

            self.floor = Floor("knight", animate=True, nFrames=3)
            
            self.effects_behind_walls = [
                Floor("knight")
            ]
            self.textInt = -2
            self.tileFrame = 0

        def reset(self):
            super().reset()
            self.textInt = -2
            self.tileFrame = 0
            self.effects_behind_walls = [
                    Floor("knight")
                ]
            if not FLAGS[111]:
                self.knight.reset()
                self.vanishObstacles()
                
        def on_enter(self):
            if not FLAGS[111]:
                self.npcs.append(self.knight)
        def renderObstacles(self):
            for i in range(8,11):
                self.blocks.append(IBlock(vec(16*i, 16*12), vanish=True))
                self.blocks.append(IBlock(vec(16*i, 0), vanish=True))
        
        def vanishObstacles(self):
            self.vanishBlocks()

        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            for i in range(1,12):
                self.terrain.append(Lava(vec(16*3, 16*i), width=8))
                self.terrain.append(Lava(vec(16*4 - 8, 16*i)))
                self.terrain.append(Lava(vec(16*14 + 8, 16*i)))
                self.terrain.append(Lava(vec(16*15 + 8, 16*i), width=8))
            for i in range(3,10):
                self.terrain.append(Lava(vec(16*2, 16*i)))
                self.terrain.append(Lava(vec(16*2 - 8, 16*i), width=8))

                self.terrain.append(Lava(vec(16*16, 16*i)))
                self.terrain.append(Lava(vec(16*17, 16*i), width=8))
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Flame_9, 2, keepBGM=True)
                    else:
                        self.player.handleCollision(b)

        def bsl(self, enemy, bossTheme):
            super().bsl(enemy, bossTheme)
            self.renderObstacles()
        
        def bse(self):
            super().bse()
            FLAGS[111] = True

        def update(self, seconds):
            if FLAGS[111]:
                if self.textInt == 3:
                    if self.timer >= 0.1:
                        self.timer = 0.0
                        self.effects_behind_walls[0] = Floor("knight", "ground_"+str(self.tileFrame-1))
                        self.tileFrame -= 1
                        if self.tileFrame == 1:
                            self.textInt += 1
                    else:
                        self.timer += seconds
                elif self.textInt == 4:
                    self.textInt = -2
                    self.effects_behind_walls[0] = Floor("knight")

                super().update(seconds)
                return
            if self.fightingBoss:
                if self.knight.initializing and not self.bossHealthbar.initializing:
                    self.knight.initializing = False
                if self.knight.desperate and self.textInt == 1:
                    self.knight.initializing = True
                    self.bsl(self.knight, "None")
                    self.displayText(SPEECH["lava_knight2"], icon=ICON["knight"])
                    self.textInt += 1
                elif self.knight.dying and self.textInt == 2:
                    self.vanishObstacles()
                    self.displayText(SPEECH["lava_knight3"], icon=ICON["knight"])
                    self.textInt += 1
                super().update(seconds)
            elif self.knight.starting:
                if self.textInt == 1:
                    if self.knight.moving:
                        self.bsl(self.knight, "megalomania.mp3")
                    else:
                        super().update(seconds)
                elif self.textInt == 0:
                    self.knight.ignoreCollision = False
                    self.displayText(SPEECH["lava_knight"], icon=ICON["knight"])
                    self.textInt += 1
                
                elif self.textInt == -1:
                    if self.timer >= 0.1:
                        self.timer = 0.0
                        self.effects_behind_walls[0] = Floor("knight", "ground_"+str(self.tileFrame+1))
                        self.tileFrame += 1
                        if self.tileFrame == 4:
                            self.textInt += 1
                    else:
                        self.timer += seconds

                elif self.textInt == -2:
                    self.player.stop()
                    self.player.keyLock()
                    SoundManager.getInstance().fadeoutBGM()
                    self.textInt += 1
            else:
                super().update(seconds)

class Tutorial_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._T1()
      
        return cls._INSTANCE
    
    class _T1(AE):
        def __init__(self):
            super().__init__("tut_1")
            #self.player = Player(vec(146, 276))
            self.roomId = 4
            self.bgm = None
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.doors = [2]
            self.trigger1 = Trigger(vec(16*8, -12), width=48)


        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)

        def setDoors(self):
            self.setDoors_square()

        def createBounds(self):
            """
            Creates boundaries on the outer edge of the map
            """
            self.createSquare()

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        if SoundManager.getInstance().currentlyPlaying:
                            self.transportPos(Tutorial_2, vec(16*28, 16*11), True)
                        else:
                            self.transportPos(Tutorial_2, vec(16*28, 16*11), False)
                    else:
                        self.player.handleCollision(b)

class Tutorial_2(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._T2()
      
        return cls._INSTANCE
    
    class _T2(AE):
        def __init__(self):
            super().__init__("tut_2", True, vec(608, 208))
            #self.player = Player(vec(146, 276))
            self.roomId = 4
            self.bgm = "forget_me_nots.mp3"
            self.ignoreClear = True
            self.max_enemies = 2
            self.enemyPlacement = 0
            self.areaIntro = AreaIntro("tut_2", position=self.camera.position)
            self.enemies = [
                Gremlin(vec(16*3, 16*6)),
                Gremlin(vec(16*20, 16*6))
            ]
            
            self.doors = [1,2,4,7,6]
            
            self.trigger1 = Trigger(vec(16*27,208-2), width=48)
            self.trigger2 = Trigger(vec(16*8,-14), width=48)
            self.trigger3 = Trigger(vec(16*27, -14), width = 48)

            self.blocks = [
                self.trigger1,
                self.trigger2,
                self.trigger3
            ]
        

        #override
        def createBlocks(self):
            return

        def setDoors(self):
            self.setDoors_horizontal()

        def createBounds(self):
            """
            Creates boundaries on the outer edge of the map
            """
            self.createHorizontal()

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Tutorial_1, 2, keepBGM=True)
                    elif b == self.trigger2:
                        self.transportPos(Tutorial_3, vec(16*9, 16*18), keepBGM=True)
                    elif b == self.trigger3:
                        self.transport(Tutorial_Shop, 0, keepBGM=True)
                    else:
                        self.player.handleCollision(b)


class Tutorial_Shop(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._TS()
      
        return cls._INSTANCE
    
    class _TS(AE):
        def __init__(self):
            super().__init__("tut_shop")
            self.roomId = 4
            self.bgm = None
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.enemies = []
            self.inCutscene = False
            self.potion = Potion(vec(16*4, 16*4), display=True)
            self.smoothie = Smoothie(vec(16*7, 16*4), display=True)
            self.key = ShopKey(vec(16*11, 16*4), display= True)
            #self.map = ShopMap(vec(16*5, 16*4), True)
            
            
            if FLAGS[10]:
                self.cloak = DarkCloak(vec(16*9, 16*5), text = "Y/NWelcome in, kid.&&\nAnything catch your eye?\n")
            else:
                self.cloak = DarkCloak(vec(16*9, 16*5), text = SPEECH["darkcloak_1"])
            
            self.spawning = [
                self.potion,
                self.key,
                self.smoothie,
                self.cloak
            ]
            self.doors = [0]

            self.trigger1 = Trigger(vec(16*8,206), width=48)

            self.blocks = [
                self.trigger1,
            ]
        

        #override
        def createBlocks(self):
            return

        def setDoors(self):
            self.setDoors_square()

        def createBounds(self):
            """
            Creates boundaries on the outer edge of the map
            """
            self.createSquare()
            for i in range(3,10):
                self.blocks.append(IBlock(vec(16*i, 16*4)))
                self.blocks.append(IBlock(vec(16*i + (16*7), 16*4)))

        def buyRoutine(self):
            if self.highlight.position[0] == 16*4:
                Potion().interact(self)
            elif self.highlight.position[0] == 16*7:
                Smoothie().interact(self)
            elif self.highlight.position[0] == 16*11:
                ShopKey().interact(self)
            elif self.highlight.position[0] == 16*14:
                pass
        
        def showInfo(self):
            if self.highlight.position[0] == 16*4:
                self.potion.interact(self)
            elif self.highlight.position[0] == 16*7:
                self.smoothie.interact(self)
            elif self.highlight.position[0] == 16*11:
                self.key.interact(self)
            elif self.highlight.position[0] == 16*14:
                pass

        def handlePrompt(self):
            if self.inShop:
                self.handleStorePrompt()
            else:
                self.cloak.interactable = False
                self.inShop = True
                #Drawable.CAMERA_OFFSET[1] -= 16
                self.promptResult = False
                self.highlight.position = vec(16*4, 16*4)

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transportPos(Tutorial_2, vec(16*28, 16), keepBGM=True)
                    else:
                        self.player.handleCollision(b)

        def update(self, seconds, updateEnemies=True, updatePlayer=True):
            if self.inCutscene:
                if FLAGS[10]:
                    self.cloak.interacted = False
                else:
                    if self.textInt == 0:
                        if self.text == "":
                            self.displayText(SPEECH["darkcloak_2"])
                            self.textInt = 1
                    elif self.textInt == 1:
                        if self.text == "":
                            self.displayText(SPEECH["darkcloak_3"])
                            self.textInt = 2
                    elif self.textInt == 2:
                        if self.text == "":
                            self.displayText(SPEECH["darkcloak_4"])
                            self.textInt = 3
                    elif self.textInt == 3:
                        if self.text == "":
                            self.displayText(SPEECH["darkcloak_5"])
                            self.textInt = 4
                    elif self.textInt == 4:
                        if self.text == "":
                            self.player.keyUnlock()
                            self.inCutscene = False
                            FLAGS[10] = True
                            self.cloak.interacted = False
                            self.textInt = 0
                            self.cloak.text = "Y/NWelcome in, kid.&&\nAnything catch your eye?\n"


            elif self.cloak.interacted:
                if FLAGS[10]:
                    pass
                else:
                    self.player.keyLock()
                    self.inCutscene = True

            return super().update(seconds, updateEnemies, updatePlayer)

class Tutorial_3(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._T3()
      
        return cls._INSTANCE
    
    class _T3(AE):
        def __init__(self):
            super().__init__("tut_3", True, vec(304, 320))
            self.roomId = 4
            self.bgm = "forget_me_nots.mp3"
            self.ignoreClear = True
            self.max_enemies = 4
            self.enemyPlacement = 0
            self.enemies = [
                Gleemer(vec(16*3, 16*11)),
                Gleemer(vec(16*3, 16*9 - 8)),
                Gleemer(vec(16*3, 16*6)),
                Gremlin(vec(16*9, 16*13)),
                Gremlin(vec(16*9, 16*5), direction = 3)
            ]
            self.locks = [
                Lock(vec(16*8, 0), "tut_3")
            ]

            self.doors = [0, 2, 1]
            self.trigger1 = Trigger(vec(16*8, self.size[1]-2), width=48)
            self.trigger2 = Trigger(vec(16*8, -14), width=48)
            self.trigger3 = Trigger(vec(16*18 + 14, 16*5), height=48)
            self.blocks = [
                self.trigger1, self.trigger2, self.trigger3
            ]

            self.spawning = [
                Sign(vec(16*7, 16*15), text= "Hi there!")
            ]
        

        #override
        def createBlocks(self):
            return

        def setDoors(self):
            self.setDoors_vertical()

        def createBounds(self):
            """
            Creates boundaries on the outer edge of the map
            """
            self.createVertical()

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Tutorial_2, 2, keepBGM=True)
                    else:
                        self.player.handleCollision(b)


"""
Entrance Hall
"""

class Intro_1(AbstractEngine):
    """
    Initialization
    """
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Intro_1()
      
        return cls._INSTANCE

    class _Intro_1(AE):
        def __init__(self):

            """
            Initial conditions
            """
            super().__init__()
            self.itemsToCollect = 1
            self.roomId = 1
            #Music
            self.bgm = "Furious_Anger.mp3"
            #Puzzle conditions
            self.enemyPlacement = 0
            self.max_enemies = 2
            
            """
            Puzzle objects
            """
            #Blocks
            self.block = LockBlock((144,80))#Locked block
            self.block1 = Block((144,64),(5,4))#Middle disappearing block
            self.block2 = Block((128,64),(5,4))#Left
            self.block3 = Block((160,64),(5,4))#Right
            
            self.blockP = PushableBlock((16*6,16*8))#PushableBlock((96, 112))#Pushable Block
            
            self.rblock1 = Block((16*3, 16*5), (5,2))
            self.rblock2 = Block((16*5, 16*5), (5,2))
            self.rblock3 = Block((16*4, 16*6), (5,2))
            #self.rblock4 = Block((16*11, 16*5), (5,2))
            #self.rblock5 = Block((16*12, 16*6), (5,2))
            #self.rblock6 = Block((16*14, 16*5), (5,2))
            #self.rblock7 = Block((16*13, 16*6), (5,2))

            self.gblock1 = Block((16*8, 16*5), (5,3))
            self.gblock2 = Block((16*8, 16*6), (5,3))
            self.gblock3 = Block((16*9, 16*6), (5,3))
            self.gblock4 = Block((16*10, 16*6), (5,3))
            self.gblock5 = Block((16*10, 16*5), (5,3))
            
            self.yblock1 = Block((144,16*1), (5,5))
            self.yblock2 = Block((144-16,16*1), (5,5))
            self.yblock3 = Block((144+16,16*1), (5,5))

            self.trigger1 = Trigger(door = 0)
            
            self.trigger2 = Trigger(door = 2)
            self.trigger2.position[1] -= 6
            
            self.doors = [0,2]
            #add self.yblock1-3 back
            self.blocks = [self.trigger1,  self.trigger2, 
                           self.block, self.block1, self.block2, self.block3,
                            #self.yblock1, self.yblock2, self.yblock3,
                           self.rblock1, self.rblock2, self.rblock3]

            #Switches
            self.weightedSwitch = WeightedSwitch((16*4,16*10))
            self.lockedSwitch = LockedSwitch(COORD[7][6])
            self.lightSwitch = LightSwitch(COORD[11][6])
            self.timedSwitch = TimedSwitch((16*14,16*10))
            self.switch = Switch((16*15,16*7))
            
            self.switches = [self.switch, self.weightedSwitch, self.lightSwitch, self.timedSwitch, self.lockedSwitch]
            
            #Npcs
            self.npcs = []
            for i in range(4, 5):
                self.enemies.append(Gremlin((16*i,26), direction = 1))

            for i in range(14, 15):
                self.enemies.append(Gremlin((16*i,26), direction = 3))

            #Spawnable Objects
            self.chest = Chest(COORD[2][5], SPEECH["intro_chest"], ICON["plant"])
            #self.sign = Sign((COORD[8][2]), SPEECH["intro_sign"])
            self.key = Key((COORD[4][5]))
            
            self.geemer2 = Geemer(((16*7)-3, (16*5)-4), SPEECH["intro_switches"], 1)
            self.geemer2.frame = 2
            self.geemer2.framesPerSecond = 8


            self.geemer3 = Geemer((self.lightSwitch.position[0]-2, self.lightSwitch.position[1]-2), SPEECH["intro_plantgeemer"], 2)
            self.geemer3.framesPerSecond = 6
            self.geemer4 = Geemer((COORD[2][8]), SPEECH["intro_pushableblocks"])
            self.spawning = [
                            self.geemer2, self.geemer3, self.geemer4,
                            ]
            
            #Projectiles/weapons
            

            """
            Display elements
            """
            #Background/room
            self.walls = Walls("intro_1")
            self.floor = Floor("intro_1")
            self.effects = [
                Shadow("intro_1", alpha=50), Shadow("intro_1", "chest_light.png", alpha=50)
            ]
            self.effects_behind_walls = [
                Shadow(room_dir="intro_1", alpha=64, animate=True, nFrames=1)
            ]


        def drawText(self, drawSurface):
            self.draw(drawSurface)
            image = Drawable(self.boxPos, "TextBox2.png", (0,7))
            image.draw(drawSurface)



        """
        Auxilary
        """
        #override
        def createBlocks(self):
            for i in range(2,8):
                self.blocks.append(Block((i*16, 64)))

            for i in range(11,17):
                self.blocks.append(Block((i*16 + 8, 64)))   

        """
        Draw
        """
        def draw(self, drawSurface):
            super().draw(drawSurface)
        
        

        """
        Collision
        """
        #override
        def blockCollision(self):
            for b in self.blocks:
                self.enemyCollision(b)
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if type(b) == LockBlock and INV["keys"] > 0:
                        self.playSound("LA_Dungeon_Teleport_Appear.wav")
                        self.disappear(b)
                        self.disappear(self.blocks)
                        self.disappear(self.block1)
                        self.disappear(self.block2)
                        self.disappear(self.block3)
                        INV["keys"] -= 1
                    elif type(b) == Trigger:
                        if b == self.trigger1:
                            self.transport(Entrance, 2)
                        elif b == self.trigger2:
                            self.transport(Intro_2, 0, keepBGM=True)
                    else:
                        self.player.handleCollision(b)

        

        def handleCollision(self):
            """
            Handles collision between the player and objects,
            including puzzle objects like switches and blocks.
            """
            super().handleCollision()


            self.spawnOnPress(self.key, self.timedSwitch)

            self.spawnOnPress(self.blockP, self.switch)

            self.spawnOnPress(self.chest, self.weightedSwitch)
            self.despawnOnPress(self.rblock1, self.lightSwitch)
            self.despawnOnPress(self.yblock1, self.lockedSwitch)

            if self.yblock1 not in self.blocks:
                self.itemsToCollect = 0
                self.disappear(self.yblock2)
                self.disappear(self.yblock3)
            if self.rblock1 not in self.blocks:
                self.disappear(self.rblock2)
                self.disappear(self.rblock3)
                # self.disappear(self.rblock4)
                # self.disappear(self.rblock5)
                # self.disappear(self.rblock6)
                # self.disappear(self.rblock7)
            elif self.rblock2 not in self.blocks:
                self.blocks.append(self.rblock2)
                self.blocks.append(self.rblock3)
                # self.blocks.append(self.rblock4)
                # self.blocks.append(self.rblock5)
                # self.blocks.append(self.rblock6)
                # self.blocks.append(self.rblock7)
            
     

        """
        Update
        """
        #override
        def handleClear(self):
            self.lockedSwitch.unlock()
            self.geemer2.set_text(SPEECH["intro_roomclear"])
        
        #override
        def updateSpawning(self,seconds):
            ##  NPCs
            super().updateSpawning(seconds)

            if self.geemer3.position[0] >= 16*13:
                self.geemer3.vel = vec(0,0)
                self.geemer3.ignoreCollision = False
            
        
        #override
        def updateSwitches(self, seconds):
            for s in self.switches:
                _type = type(s)
                if _type == WeightedSwitch:
                    s.update(self.blockP)
                elif _type == LightSwitch:
                    s.update(self.player, self.blockP)
                elif _type == LockedSwitch:
                    s.update()
                elif _type == TimedSwitch:
                    s.update(seconds)

        def update(self, seconds):
            
            """
            Update the objects that need to be updated
            """
            super().update(seconds)
            self.effects[0].position = vec(self.blockP.position[0]-(16*6), self.blockP.position[1]-(16*8))
            
                

class Intro_2(AbstractEngine):
    
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Intro_2()
      
        return cls._INSTANCE

    class _Intro_2(AE):
        """
        Initialization
        """
        def __init__(self):

            """
            Initial conditions
            """
            super().__init__()
            self.roomId = 2
            self.ignoreClear = True
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.trigger3 = Trigger(door = 3)
            self.doors = [0,2,3]
            

           
            #Music
            self.bgm = None
            self.bgm = "Furious_Anger.mp3"
            #Puzzle conditions
            self.resetting = True
            self.enemyPlacement = 2
            self.max_enemies = 4
            """
            Puzzle objects
            """
            #Blocks
            self.blockP = PushableBlock((16*6,16*8))#PushableBlock((96, 112))#Pushable Block
            

            #Switches
            
            #Npcs
            self.npcs = [#Spinner(COORD[5][7]), 
                         #GremlinB(COORD[5][7])
                         #Flapper(COORD[2][9]), 
                         #FireFlapper(COORD[3][9]),
                         #FireFlapper(COORD[4][9]),
                         #FireFlapper(COORD[5][9]),
                         #FireFlapper(COORD[6][9]),
                         #IceFlapper(COORD[4][9]), 
                         #ThunderFlapper(COORD[5][9]), 
                         #WindFlapper(COORD[6][9])
                         ]

            #Spawnable Objects
            self.spawning = [Geemer(COORD[2][9], SPEECH["intro_combat"], fps = 32),
                             Geemer(COORD[12][2], SPEECH["skipping_text"], fps = 50)]
            
            #Projectiles/weapons

            """
            Display elements
            """
            #Background/room
            self.floor = Floor("intro_2")
            self.walls = Walls("intro_2")
            self.areaIntro = AreaIntro("intro_2", "area_intro.png")
            self.effects = [
                Shadow(room_dir="intro_2", alpha= 54, animate=False),
                
            
            ]
            self.effects_behind_walls = [
                Shadow(room_dir="intro_2", alpha=140, animate=True)
            ]

            for i in range(2):
                self.enemies.append(Mofos(direction = 1))
            for i in range(2):
                self.enemies.append(Mofos(direction = 3))

            self.enemies.append(Spinner())
            self.enemies.append(Spinner())
            self.enemies.append(Spinner())
            self.enemies.append(Spinner())
            


            """ 
            self.enemies.append(Flapper(direction = 1))#Right, Top
            
            self.enemies.append(Flapper(direction = 2))#Left, Bottom

            self.enemies.append(Flapper(direction = 1))#Right, Top

            self.enemies.append(Flapper(direction = 0))#Left, Top """

            


            
            


        """
        Auxilary
        """
        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            self.blocks.append(self.trigger3)

        """
        Draw
        """
        
        
        """
        Collision
        """
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if type(b) == Trigger:
                        if b == self.trigger1:
                            self.transport(Intro_1, 2, keepBGM=True)
                        elif b == self.trigger2:
                            self.transport(Alpha_Flapper, 0)
                        elif b == self.trigger3:
                            self.transportArea(Stardust_1, 1)
                    else:
                        self.player.handleCollision(b)

        
        #override
        def handleClear(self):
            pass


class Stardust_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Geemer_1()
      
        return cls._INSTANCE
    
    class _Geemer_1(AE):
        def __init__(self):
            super().__init__("stardust_1")
            self.roomId = 9
            self.bgm = "stardust.mp3"
            self.ignoreClear = True
            self.resetting = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.doors = [1,2]
            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 2)
            self.spawning = [
                Geemer((16*11, 16*5 - 4), text = SPEECH["town_1"], color = 1)
            ]
            self.enemies = [
                Baller(COORD[3][6], direction = 1)
            ]
            self.max_enemies = 1
            self.enemyPlacement = 0
            self.areaIntro = AreaIntro("stardust_1","stardust.png")
  
        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            for i in range(2,8):
                self.blocks.append(IBlock(COORD[i][4]))
            for i in range(11,17):
                self.blocks.append(IBlock(COORD[i][4]))
            for i in range(2,17):
                self.blocks.append(IBlock(COORD[i][8]))
            
            
            for i in range(1,4):
                self.blocks.append(IBlock(COORD[7][i]))
            for i in range(1,4):
                self.blocks.append(IBlock(COORD[11][i]))
            for i in range(9,12):
                self.blocks.append(IBlock(COORD[7][i]))
            for i in range(9,12):
                self.blocks.append(IBlock(COORD[11][i]))
           
        #override
        def blockCollision(self):
           for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transportArea(Intro_2, 3)
                    elif b == self.trigger2:
                        self.transport(Shop, 0, keepBGM=True)
                    else:
                        self.player.handleCollision(b)
        
        def draw(self, drawSurface):
            super().draw(drawSurface)
        
        def update(self, seconds, updateEnemies=True, updatePlayer=True):
            #print(self.readyToTransition)
            return super().update(seconds, updateEnemies, updatePlayer)

class Shop(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Shop()
      
        return cls._INSTANCE
    
    class _Shop(AE):
        def __init__(self):
            super().__init__()
            self.roomId = 10
            self.bgm = "Nujabes_Decade.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("test.png")
            self.trigger1 = Trigger(door = 0)
            self.doors = [0]

            self.shopKeep = Geemer((16*9-2,16*6), text = SPEECH["shopkeep"])
            self.potion = Potion(COORD[4][6])
            self.spawning = [
                self.shopKeep,
                self.potion
            ]

            self.selectedItem = ""

        def handlePrompt(self):
            if self.selectedItem == "potion":
                INV["money"] -= 5
                self.displayText("You bought a potion!&&\nUse it on the pause menu\nto restore a bit of health.\n")
                INV["potion"] += 1
                self.promptResult = False
                self.selectedItem = ""

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Geemer_1, 2, keepBGM=True)
                    else:
                        self.player.handleCollision(b)

class Alpha_Flapper(AbstractEngine):

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._AF()
      
        return cls._INSTANCE
    
    class _AF(AE):
        def __init__(self):
            super().__init__("alpha_flapper")
            self.bgm = "tension.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.effects = [
                Shadow("alpha_flapper")
            ]
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.doors = [0,2]

            if not FLAGS[110]:
                self.flapper = AlphaFlapper(vec(16*8 + 8, 16*3))
                
            self.textInt = -1
            self.tileFrame = 0
            self.obstacles = [
            ]
            for i in range(3):
                self.obstacles.append(ForceField(COORD[8+i][1], render=False))
            for i in range(3):
                self.obstacles.append(ForceField(COORD[8+i][11], render = False))
            if FLAGS[110]:
                self.floor = Floor("alpha_flapper", "tiles_8")

        def on_enter(self):
            if not FLAGS[110]:
                self.npcs.append(self.flapper)

        def reset(self):
            super().reset()
            if not FLAGS[110]:
                self.flapper.reset(vec(16*8 + 8, 16*3))
                self.vanishObstacles()
                self.tileFrame = 0
                self.textInt = -1
                self.floor = Floor("alpha_flapper")

        def bsl(self, enemy, bossTheme):
            super().bsl(enemy, bossTheme)
            self.renderObstacles()
        
        def vanishObstacles(self):
            self.blocks = [b for b in self.blocks if not b.vanish]
            

        def renderObstacles(self):
            for i in range(8,11):
                self.blocks.append(IBlock(vec(16*i, 16*10), popProjectiles=False, vanish=True))
            for i in range(8,11):
                self.blocks.append(IBlock(vec(16*i, 16*2), popProjectiles=False, vanish=True))
        
        def bse(self):
            super().bse()

        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            for i in range(3,8):
                self.blocks.append(IBlock(vec(16*i, 16*10), popProjectiles=False))
            for i in range(11,16):
                self.blocks.append(IBlock(vec(16*i, 16*10), popProjectiles=False))
            for i in range(3,8):
                self.blocks.append(IBlock(vec(16*i, 16*2), popProjectiles=False))
            for i in range(11,16):
                self.blocks.append(IBlock(vec(16*i, 16*2), popProjectiles=False))
            for i in range(3,10):
                self.blocks.append(IBlock(vec(16*2, 16*i), popProjectiles=False))
            for i in range(3,10):
                self.blocks.append(IBlock(vec(16*16, 16*i), popProjectiles=False))

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                self.enemyCollision(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Intro_2, 2)
                    elif b == self.trigger2:
                        self.transport(Intro_3, 0)
                    else:
                        self.player.handleCollision(b)

        def update(self, seconds):
            if FLAGS[110]:
                super().update(seconds)
                return
            if self.fightingBoss:
                if self.flapper.dying and self.textInt == 1:
                    self.displayText(SPEECH["alpha_flapper"])
                    self.textInt += 1
                super().update(seconds)
            elif self.textInt == 2:
                if self.timer >= 0.1:
                    self.timer = 0.0
                    #3, 2, 1, 5, 6, 7, 8
                    self.floor = Floor("alpha_flapper", "tiles_"+str(self.tileFrame-1))
                    self.tileFrame -= 1
                    if self.tileFrame == 1:
                        self.textInt = 3
                        self.tileFrame = 4
                else:
                    self.timer += seconds
            elif self.textInt == 3:
                if self.timer >= 0.1:
                    self.timer = 0.0
                    ##Fall
                    if self.tileFrame == 8:
                        self.textInt = 4
                    else:
                        #5, 6, 7, 8
                        self.floor = Floor("alpha_flapper", "tiles_"+str(self.tileFrame+1))
                        self.tileFrame += 1
                else:
                    self.timer += seconds
            elif self.textInt == 4:
                super().update(seconds)
                if self.flapper.dead:
                    self.vanishObstacles()
                    FLAGS[110] = True
            elif self.player.position[1] <= 16*6:
                if self.textInt == 1:
                    self.bsl(self.flapper, "ing.mp3")
                elif self.textInt == 0:
                    self.player.stop()
                    self.player.keyUnlock()
                    SoundManager.getInstance().fadeoutBGM()
                    self.displayText("Skreeeeeeee!&&\nOutsider, begone!&&\n")
                    self.textInt += 1
                elif self.textInt == -1:
                    if self.timer >= 0.1:
                        self.timer = 0.0
                        ##Fall
                        if self.tileFrame == 4:
                            self.textInt = 0
                        else:
                            self.floor = Floor("alpha_flapper", "tiles_"+str(self.tileFrame+1))
                            self.tileFrame += 1
                    else:
                        self.timer += seconds
            else:
                super().update(seconds)
                

class Intro_3(AbstractEngine):

    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Intro_3()
      
        return cls._INSTANCE

    class _Intro_3(AE):

        def __init__(self):
            super().__init__("intro_3")
            self.roomId = 3
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.torches = []
            self.enemies = [
                Dummy((COORD[8][5])), 
                Dummy((COORD[9][5])), 
                Dummy((COORD[10][5]))
            ]
            self.doors = [0,2]

            
        
       
        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            for i in range(2,11):
                self.blocks.append(Block(COORD[7][i], offset = (5,6)))
            for i in range(2,11):
                self.blocks.append(Block(COORD[2][i], offset = (5,6)))
            for i in range(2,11):
                self.blocks.append(Block(COORD[11][i], offset = (5,6)))
            for i in range(2,11):
                self.blocks.append(Block(COORD[16][i], offset = (5,6)))

            for j in range(3,6,2):
                for i in range(2,11):
                    self.torches.append(Torch((COORD[j][i])))
            for j in range(4,7,2):
                for i in range(2,11):
                    self.torches.append(Torch((COORD[j][i]),2))
            for j in range(13, 17, 2):
                for i in range(2,11):
                    self.torches.append(Torch((COORD[j][i]),3))
            for j in range(12, 16, 2):
                for i in range(2,11):
                    self.torches.append(Torch((COORD[j][i]),1))


        
        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if type(b) == Trigger:
                        if b == self.trigger1:
                            self.transport(Alpha_Flapper, 2)
                        elif b == self.trigger2:
                            self.transportPos(Grand_Chapel, vec(16*28,16*11))
                            
                    else:
                        self.player.handleCollision(b)

        

        def update(self, seconds):
            super().update(seconds)
            

""" class Grand_Chapel_L(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._ChapelL()
      
        return cls._INSTANCE
    
    class _ChapelL(AE):
        def __init__(self):
            super().__init__()
            self.roomId = 7
            self.bgm = "hymn.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("grand_chapel_L.png")
            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 0)
            self.trigger3 = Trigger(door = 2)
            self.doors = [0,1,2]

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Grand_Chapel, 3, keepBGM=True)
                    elif b == self.trigger2:
                        self.transport(Flame_entrance, 2)
                    elif b == self.trigger3:
                        self.transport(Frost_1, 0)
                    else:
                        self.player.handleCollision(b)


class Grand_Chapel_R(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
            cls._INSTANCE = cls._ChapelR()
      
        return cls._INSTANCE
    
    class _ChapelR(AE):
        def __init__(self):
            super().__init__()
            self.roomId = 8
            self.bgm = "hymn.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("grand_chapel_R.png")
            self.trigger1 = Trigger(door = 3)
            self.trigger2 = Trigger(door = 0)
            self.trigger3 = Trigger(door = 2)
            self.doors = [0,2,3]

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Grand_Chapel, 1, keepBGM=True)
                    elif b == self.trigger2:
                        self.transport(Thunder_1, 3)
                    elif b == self.trigger3:
                        self.transport(Gale_1, 0)
                    else:
                        self.player.handleCollision(b) """

class Grand_Chapel(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Intro_4()
      
        return cls._INSTANCE
    
    class _Intro_4(AE):
        def __init__(self):
            super().__init__("grand_chapel", True, vec(912,208))
            self.roomId = 4
            self.bgm = "LA_SwordSearch.wav"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0

            self.trigger1 = Trigger(door = 10)
            self.trigger2 = Trigger(door = 13)
            self.trigger3 = Trigger(door = 12)
            self.trigger4 = Trigger(door = 11)

            self.toLeft = Trigger(door = 1)
            self.toFlame = Trigger(door = 0)
            self.toIce = Trigger(door = 2)

            self.toRight = Trigger(door = 23)
            self.toThunder = Trigger(door = 20)
            self.toGale = Trigger(door = 22)


            self.fire = Blessing(vec(16*7, 16*4), 0)
            self.ice = Blessing(vec(16*11, 16*4), 1)
            self.thunder = Blessing(vec(16*45, 16*4), 2)
            self.wind = Blessing(vec(16*49, 16*4), 3)


            self.geemer = Geemer((16*9 - 4 + 304, 16*6), text = SPEECH["chapel_geemer"], color = 1)
            self.prompt = Geemer((16*11-4 + 304, 16*9), text = "Praise be to Majestus&&")
            

            self.spawning = [self.ice,
                             self.fire,
                             self.thunder,
                             self.wind,
                             self.geemer,
                             self.prompt
                             ]
            
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            self.blocks.append(self.trigger3)
            self.blocks.append(self.trigger4)

            self.blocks.append(self.toLeft)
            self.blocks.append(self.toFlame)
            self.blocks.append(self.toIce)

            self.blocks.append(self.toRight)
            self.blocks.append(self.toThunder)
            self.blocks.append(self.toGale)

            self.doors = [0,2]
        
        def handlePrompt(self):
            if self.promptResult:
                if self.selectedItem == 0:
                    if INV["flameShard"] >= INV["flameCost"]:
                        INV["flameShard"] -= INV["flameCost"]
                        if INV["flameCost"] == 1:
                            INV["flameCost"] = 5
                            self.fire.updateCost()
                        self.displayText("Flames upgraded!")
                    else:
                        self.displayText("Not enough shards.")
                    self.promptResult = False

                elif self.selectedItem == 1:
                    if INV["frostShard"] >= INV["frostCost"]:
                        INV["frostShard"] -= INV["frostCost"]
                        if INV["frostCost"] == 1:
                            INV["frostCost"] = 5
                            self.fire.updateCost()
                        self.displayText("Ice upgraded!")
                    else:
                        self.displayText("Not enough shards.")
                    self.promptResult = False

                elif self.selectedItem == 2:
                    if INV["boltShard"] >= INV["boltCost"]:
                        INV["boltShard"] -= INV["boltCost"]
                        if INV["boltCost"] == 1:
                            INV["boltCost"] = 5
                            self.fire.updateCost()
                        self.displayText("Bolt upgraded!")
                    else:
                        self.displayText("Not enough shards.")
                    self.promptResult = False

                if self.selectedItem == 3:
                    if INV["galeShard"] >= INV["galeCost"]:
                        INV["galeShard"] -= INV["galeCost"]
                        if INV["galeCost"] == 1:
                            INV["galeCost"] = 5
                            self.fire.updateCost()
                        self.displayText("Gale upgraded!")
                    else:
                        self.displayText("Not enough shards.")
                    self.promptResult = False

            

        def on_enter(self):
            self.fire.updateCost()

        #override
        def createBlocks(self):
            return

        def setDoors(self):
            return
        
        def createBounds(self):
            """
            Creates boundaries on the outer edge of the map
            """
            return
            #Left side
            for i in range(1, 5):
                self.blocks.append(IBlock((8,i*16)))
            for i in range(8, 12):
                self.blocks.append(IBlock((8,i*16)))
            #Right side
            for i in range(1, 5):
                self.blocks.append(IBlock((912-24,i*16)))
            for i in range(8, 12):
                self.blocks.append(IBlock((912-24,i*16)))
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
            

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Intro_3, 2)
                    else:
                        self.player.handleCollision(b)
        
        def update(self, seconds):
            super().update(seconds)

class Chamber_Access(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Access()
      
        return cls._INSTANCE
    
    class _Access(AE):
        def __init__(self):
            super().__init__()
            self.roomId = 5
            self.bgm = None
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("intro_3.png")
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.doors = [0,2]
            self.npcs = [ForceField(COORD[7][8], 1), ForceField(COORD[8][8], 1), ForceField(COORD[9][8], 1), ForceField(COORD[10][8], 1), ForceField(COORD[11][8], 1),
                         ForceField(COORD[7][6], 2), ForceField(COORD[8][6], 2), ForceField(COORD[9][6], 2), ForceField(COORD[10][6], 2), ForceField(COORD[11][6], 2),
                         ForceField(COORD[7][4], 3), ForceField(COORD[8][4], 3), ForceField(COORD[9][4], 3), ForceField(COORD[10][4], 3), ForceField(COORD[11][4], 3),
                         ForceField(COORD[7][2],4), ForceField(COORD[8][2], 4), ForceField(COORD[9][2], 4), ForceField(COORD[10][2], 4), ForceField(COORD[11][2], 4)]
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            for i in range(1,12):
                self.blocks.append(Block(COORD[6][i], offset=(5,6)))
                self.blocks.append(Block(COORD[12][i], offset=(5,6)))

           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Grand_Chapel, 2)
                    else:
                        self.player.handleCollision(b)

class Freeplay(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._FP()
        return cls._INSTANCE
    
    class _FP(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "fire.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("entrance.png")
            self.npcs = [
                David((COORD[2][5]), 1),
                Flapper(COORD[5][5]),
                Mofos(COORD[12][5]),
                Gremlin(COORD[8][1], direction = 1)
            ]
        
        
        

        #override
        def createBlocks(self):
            pass
            

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    self.player.handleCollision(b)
                self.enemyCollision(b)
        
        def update(self, seconds):
            super().update(seconds)




class Entrance(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._EN()
        return cls._INSTANCE
    
    class _EN(AE):
        def __init__(self):
            super().__init__("entrance")
            self.healthBarLock = True
            self.bgm = "droplets.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.door1 = Trigger(door = 2)
            self.trigger1 = Trigger(text = SPEECH["intro_entrance"], door = 0)

            self.geemer = Geemer((16*8, 16*4), SPEECH["intro_geemer"], 0, 2)
            self.spawning.append(self.geemer)
            self.npcs = [
                ]
            self.doors = [0,2]

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)
        
        #override
        def createBlocks(self):
            self.blocks.append(self.door1)
            self.blocks.append(self.trigger1)
            #self.blocks.append(self.door2)
            for i in range(1,12):
                self.blocks.append(IBlock(COORD[7][i]))

            for i in range(1,12):
                self.blocks.append(IBlock(COORD[11][i]))
            

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.door1:
                        self.transport(Intro_1, (16*9, (16*11) - 8))
                    elif b == self.trigger1:
                        self.player.position[1] = 16*11
                        b.interact(self.player, self)
                    else:
                        self.player.handleCollision(b)
                self.enemyCollision(b)
        
        def update(self, seconds):
            if self.healthBarLock:
                self.player.keyLock()
                if self.timer >= 1.3:
                    self.player.keyUnlock()
                    self.healthBarLock = False
                    self.timer = 0
                else:
                    self.timer += seconds
            super().update(seconds)





"""
Fire
"""
class Flame_entrance(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_entrance()
      
        return cls._INSTANCE
    
    class _Flame_entrance(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pso.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_entrance.png")
            self.doors = [2,3]
            self.trigger1 = Trigger(door = 3)
            self.trigger2 = Trigger(door = 2)
            self.trigger3 = Trigger(vec(16*13 - 2, 16*5), width = 20, height = 12)
            self.motionTick = 0
            self.motionTimer = 0.0
            self.geemer = Geemer(COORD[4][3], text = SPEECH["flame_entrance_geemer"])
            self.spawning = [self.geemer,
                             Geemer((COORD[15][6]), text = SPEECH["flame_entrance_geemer2"])
            ]
            self.enemies = [Baller(COORD[8][10]),
                         Baller(COORD[10][10], 1)]
        #override
        def createBlocks(self):
           for i in range(11, 16):
               for j in range(3, 6):
                if i == 13 and j == 5:
                    pass
                elif j == 5:
                    if i == 12:
                        self.blocks.append(IBlock(COORD[i][j], width = 14))
                    elif i == 14:
                        self.blocks.append(IBlock((16*i +2, 16*j), width = 14))
                    else:
                        self.blocks.append(IBlock(COORD[i][j]))
                else:
                    self.blocks.append(IBlock(COORD[i][j]))
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Flame_1, 1, keepBGM=False)
                    elif b == self.trigger2:
                        self.transport(Grand_Chapel_L, 0)
                    elif b == self.trigger3:
                        pass
                        #self.transportPos(Flame_dispensary, vec(16*9, 16*8))
                    else:
                        self.player.handleCollision(b)

        def update(self, seconds):
            super().update(seconds)
            if self.motionTick == 0:
                self.geemer.position[0] += 0.2
            elif self.motionTick == 1:
                pass
            elif self.motionTick == 2:
                self.geemer.position[0] -= 0.2
            elif self.motionTick == 3:
                pass
            """ elif self.motionTick == 2:
                self.geemer.position[0] -= 0.2
            elif self.motionTick == 3:
                self.geemer.position[1] -= 0.2 """
            self.motionTimer += seconds
            if self.motionTimer >= 2.0:
                self.motionTimer = 0.0
                self.motionTick += 1
                self.motionTick %= 4

class Flame_dispensary(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._FD()
      
        return cls._INSTANCE
    
    class _FD(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "Jhene.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("dispensary_flame.png")
            self.trigger1 = Trigger(vec(16*9, 16*9 + 12), height = 12)
            self.shopkeep = Geemer(vec(16*9 - 2, 16*4), variant = "dispo")
            self.spawning = [self.shopkeep]

        #override
        def createBlocks(self):
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



        #override
        def blockCollision(self):
            for b in self.blocks:
                for n in self.npcs:
                    if n.doesCollide(b):
                        n.bounce(b)

                self.projectilesOnBlocks(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transportPos(Flame_entrance, vec(16*13, 16*6))
                    else:
                        self.player.handleCollision(b)

        def handlePrompt(self):
            if self.selectedItem == "roll":
                INV["plant"] -= 1
                self.displayText("He rolled you a blunt!&&\nSmoke it to see things\nunseen by the sober eye!\n")
                INV["joint"] += 1
                self.promptResult = False
                self.selectedItem = ""

class Flame_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_1()
      
        return cls._INSTANCE
    
    class _Flame_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = False
            self.max_enemies = 8
            self.enemyPlacement = 2
            self.background = Level("flame_1.png")
            self.enemies = [FireFlapper() for i in range(6)]
            self.enemies.append(Flapper())
            self.enemies.append(Flapper())
            self.doors = [1,2,3]
            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 2)
            self.trigger3 = Trigger(door=3)

            self.obstacles = [
                Boulder((16*2 -10, 16*4 - 8)),
                Boulder((16*4 -10, 16*6 - 8)),
                Boulder((16*2 -10, 16*7 + 8))
                ]

            self.lockedSwitch = LockedSwitch(COORD[9][6])
            
            self.switches.append(self.lockedSwitch)
            self.yblock1 = Block((144,16*1), (5,5))
            self.yblock2 = Block((144-16,16*1), (5,5))
            self.yblock3 = Block((144+16,16*1), (5,5))
            self.blocks.append(self.yblock1)
            self.blocks.append(self.yblock2)
            self.blocks.append(self.yblock3)



        def handleClear(self):
            self.lockedSwitch.unlock()
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_entrance, 3, keepBGM=False)
                elif b == self.trigger2:
                    self.transport(Flame_2, 0, keepBGM=True)
                elif b == self.trigger3:
                    self.transport(Flame_4, 1)
                else:
                    self.player.handleCollision(b)        

        def handleCollision(self):
            super().handleCollision()
            self.despawnOnPress(self.yblock1, self.lockedSwitch)
            if self.yblock1 not in self.blocks:
                self.disappear(self.yblock2)
                self.disappear(self.yblock3)

class Flame_2(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_2()
      
        return cls._INSTANCE
    
    class _Flame_2(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = False
            self.max_enemies = 4
            self.enemyPlacement = 1
            self.background = Level("flame_2.png")
            self.enemies = [FireFlapper(), Mofos(), FireFlapper(), GremlinB()]
            

            self.doors = [0,2,3]
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.trigger3 = Trigger(door = 3)

            self.portal = Portal(COORD[9][6], 0)
            self.chest = Chest(COORD[9][9], SPEECH["first_bombo"], ICON["bombo"])
            
            self.obstacles = [Boulder((16*2 -10, 16*4 - 8)),
                Boulder((16*4 -10, 16*6 - 8)),
                Boulder((16*2 -10, 16*7 + 8))
                ]
            

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)


        def handleClear(self):
            
            #self.displayText("The raging flames have\nbeen graciously doused!\n")
            self.spawning.append(self.chest)

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_1, 2, keepBGM=True)
                elif b == self.trigger2:
                    self.transport(Flame_5, 0, keepBGM=True)
                elif b == self.trigger3:
                    self.transport(Flame_3, 1, keepBGM=True)
                elif b == self.portal:
                    self.transport(Grand_Chapel, 0)
                else:
                    self.player.handleCollision(b)        

        def update(self, seconds):
            super().update(seconds)
            self.portal.update(seconds)

class Flame_5(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_5()
      
        return cls._INSTANCE
    
    class _Flame_5(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = True
            self.background = Level("flame_5.png")
            self.enemyPlacement = 0
            self.max_enemies = 0
            #self.enemies = [FireFlapper(), Mofos(), FireFlapper(), GremlinB()]
            self.npcs = [Bopper(COORD[9][3]),
                         Bopper(COORD[5][5]),
                         Bopper(COORD[13][5])]

            self.doors = [0]
            
            self.chest = Chest(COORD[13][9], SPEECH["bombo_expansion"], ICON["bombo"])
            self.spawning = [
                Sign(COORD[7][9], SPEECH["boppers"]),
                self.chest
            ]
            self.obstacles = [
                Boulder((16*12 + 8, 16*9 - 8))
            ]
            self.trigger1 = Trigger(door = 0)
            

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)


        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_2, 2, keepBGM=True)
                else:
                    self.player.handleCollision(b)        

        def update(self, seconds):
            super().update(seconds)

class Flame_3(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_3()
      
        return cls._INSTANCE
    
    class _Flame_3(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "pun.mp3"
            self.ignoreClear = True
            self.background = Level("flame_3.png")
            self.enemyPlacement = 3
            self.max_enemies = 4
            self.enemies = [Mofos(direction=0), Mofos(direction=2), Baller(direction=1), Baller(direction=3),
                            Mofos(direction = 0), Mofos(direction = 2)]
            self.npcs = [
                         #Bopper(COORD[9][3]),
                         #Bopper(COORD[5][5]),
                         #Bopper(COORD[13][5])
                         ]

            self.doors = [0, 1]
            
            #self.chest = Chest(COORD[13][9], SPEECH["bombo_expansion"], ICON["bombo"])
            self.spawning = [
                #Sign(COORD[7][9], SPEECH["boppers"]),
                #self.chest
            ]
            self.obstacles = [
                #Boulder((16*12 + 8, 16*9 - 8))
            ]

            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 0)
            

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            super().initializeRoom(player, pos, keepBGM)


        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_2, 3, keepBGM=True)
                elif b == self.trigger2:
                    self.transport(Flame_4, 2)
                else:
                    self.player.handleCollision(b)        

        def update(self, seconds):
            super().update(seconds)

class Flame_Store(AbstractEngine):
        @classmethod
        def getInstance(cls):
            if cls._INSTANCE == None:
                cls._INSTANCE = cls._S()
        
            return cls._INSTANCE
        
        class _S(AE):
            def __init__(self):
                super().__init__()
                self.bgm = "Nujabes_Decade.mp3"
                self.ignoreClear = True
                self.max_enemies = 0
                self.enemyPlacement = 0
                self.background = Level("dispensary_flame.png")
                self.trigger1 = Trigger(vec(16*9, 16*9+8))
                self.potion = Potion(vec(16*6, 16*7-8))
                self.smoothie = Smoothie(vec(16*6, 16*4+8))
                self.emblem = ChanceEmblem(vec(16*12, 16*7 - 8))
                self.syringe = Syringe(vec(16*12, 16*4+8))
                self.spawning = [
                    Geemer(vec(16*9-4, 16*3), text="How's it going, man?&&\nSee anything ya like?&&\n",color = 1),
                    self.potion,
                    self.smoothie,

                ]
            #override
            def createBlocks(self):
                self.createStore()
            
            def handlePrompt(self):
                if self.selectedItem == "syringe":
                    self.spawning.pop(self.spawning.index(self.syringe))
                elif self.selectedItem == "emblem":
                    self.spawning.pop(self.spawning.index(self.emblem))
                self.handleStorePrompt()
            #override
            def blockCollision(self):
                for b in self.blocks:
                    self.projectilesOnBlocks(b)
                    self.enemyCollision(b)
                    if self.player.doesCollide(b):
                        if b == self.trigger1:
                            self.transportPos(Flame_4, vec(16*13 + 8, 16*6), keepBGM=True)
                        else:
                            self.player.handleCollision(b)

            def initializeRoom(self, player=None, pos=None, keepBGM=False, placeEnemies=True):
                if not INV["syringe"]:
                    if self.syringe not in self.spawning:
                        self.spawning.append(self.syringe)
                if not INV["chanceEmblem"]:
                    if self.emblem not in self.spawning:
                        self.spawning.append(self.emblem)
                super().initializeRoom(player, pos, keepBGM, placeEnemies)


class Flame_4(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_4()
      
        return cls._INSTANCE
    
    
    class _Flame_4(AE):
        
        
        ##class _Flame_4:
        def __init__(self):
            super().__init__()
            self.bgm = "Nujabes_Decade.mp3"
            self.ignoreClear = True
            self.background = Level("flame_4.png")
            self.enemyPlacement = 0
            self.max_enemies = 0
            #self.enemies = [FireFlapper(), Mofos(), FireFlapper(), GremlinB()]
            self.npcs = [
                        #Heater(COORD[8][5])
                         Bopper(COORD[9][5]),
                         Bopper(COORD[9][9]),
                         Bopper(COORD[7][7]),
                         Bopper(COORD[8][8]),
                         Bopper(COORD[8][6]),
                         Bopper(COORD[11][7]),
                         Bopper(COORD[10][8]),
                         Bopper(COORD[10][6])
                         ]

            self.doors = [0, 1, 2]
            
            self.spawning = [
                NpcBopper((COORD[9][7]), text="Come on! Keep killin' us!&&\nYa can't hate a playa\nfor reproducin' like crazy!\nY'ain't got no idea what\ngoes on in this dirt!\n"),
                Geemer(),
                Geemer(),
                Geemer(),
                Geemer(),
                Grave(COORD[2][8], text = "Crushed to dust too soon.\nIn embers and ashes.\nGeemer 5,987&&\n"),
                Grave(COORD[5][8], text = "An unrivaled reverend,\nGeemer 4,999 stated so:\n\"I fear naught but the\nGods and their choices!\"\n   He was then stomped\n       to death.\n"),
                Grave(COORD[2][5], text = "Xavier Renegade Angel.\nGo watch that show.\nOh... That's right...&&\n             RIP       &&\n"),
                Sign(COORD[12][6], text="Stomper threat sale!&&\nBuy your smoothies\nwhile their cheap!\n")
            ]
            self.obstacles = [
            ]
           
            self.trigger1 = Trigger(door = 1)
            self.trigger2 = Trigger(door = 0)
            self.trigger3 = Trigger(door = 2)
            self.barTrigger = Trigger(COORD[3][3], width=32)
            self.shopTrigger = Trigger(COORD[13][5], width = 32, height = 16)
            

           

        #override
        def createBlocks(self):
            self.blocks.append(self.trigger1)
            self.blocks.append(self.trigger2)
            self.blocks.append(self.trigger3)
            self.blocks.append(self.barTrigger)
            self.blocks.append(self.shopTrigger)
            for i in range(4):
                self.blocks.append(IBlock(COORD[2][1+i]))
                self.blocks.append(IBlock(COORD[5][1+i]))
            for i in range(3):
                self.blocks.append(IBlock(COORD[6][1+i]))
                self.blocks.append(IBlock(COORD[7][1+i]))
            for i in range(5):
                self.blocks.append(IBlock(COORD[11][1+i]))
                self.blocks.append(IBlock(COORD[12][1+i]))
                self.blocks.append(IBlock(COORD[15][1+i]))
                self.blocks.append(IBlock(COORD[16][1+i]))
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_1, 3)
                elif b == self.trigger2:
                    self.transport(Flame_6, 2)
                elif b == self.trigger3:
                    self.transport(Flame_3, 0)
                elif b == self.barTrigger:
                    pass
                elif b == self.shopTrigger:
                    self.transportPos(Flame_Store, COORD[9][8], keepBGM=True)
                else:
                    self.player.handleCollision(b)       

        def update(self, seconds):
            super().update(seconds)
        

        
    

class Flame_6(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame_6()
      
        return cls._INSTANCE
    
    class _Flame_6(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "lava_reef.mp3"
            self.ignoreClear = True
            self.background = Level("flame_6.png")
            self.enemyPlacement = 0
            self.max_enemies = 1
            self.stomper = Stomper(vec(16*9, 16*5),boss=True)
            self.stomper.unPause(position = vec(16*8 - 6, 16*5))
            self.enemies = [
                        self.stomper
                        ]
            
            self.npcs = [
                Bopper(COORD[3][10]),
                Bopper(COORD[15][10])
            ]
            self.stomperTimer = 0.0

            self.doors = [0,2,3]
            
            if not FLAGS[41]:
                self.spawning = [
                    Geemer(vec(16*8 - 8, 16*5 + 8))
                ]
            
            if FLAGS[42]:
                self.spawning = [
                    Geemer(vec(16*10, 16*5 + 8), text = SPEECH["post_stomper"])
                ]

            self.obstacles = [
            ]
            for i in range(3):
                self.obstacles.append(ForceField(COORD[8+i][1], render=False))
            for i in range(3):
                self.obstacles.append(ForceField(COORD[2][5+i], render = False))
            for i in range(3):
                self.obstacles.append(ForceField(COORD[8+i][11], render=False))
            
            self.trigger1 = Trigger(door = 3)
            self.trigger2 = Trigger(door = 0)
            self.trigger3 = Trigger(door = 2)

            self.inCutscene = False
            self.textInt = 0
            self.miniBoss = False
        
        def deathReset(self):
            super().deathReset()
            self.vanishObstacles()
            if self.miniBoss:
                self.miniBoss = False

        

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            if not FLAGS[42]:
                
                super().initializeRoom(player, pos, keepBGM)
                self.stomper.setPosition(vec(16*9, 16*5))
            else:
                if len(self.spawning) == 0:
                    self.spawning = [
                    Geemer(vec(16*10, 16*5 + 8), text = SPEECH["post_stomper"])
                ]
                super().initializeRoom(player, pos, keepBGM, placeEnemies=False)

 
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           self.blocks.append(self.trigger3)
           
           
        #override
        def blockCollision(self):
           for b in self.blocks:
              self.projectilesOnBlocks(b)
              self.enemyCollision(b)
              if self.player.doesCollide(b):
                if b == self.trigger1:
                   self.transport(Flame_10, 1, keepBGM=True)
                elif b == self.trigger2:
                    self.transport(Flame_7, 2, keepBGM=True)
                elif b == self.trigger3:
                    self.transport(Flame_4, 0)
                else:
                    self.player.handleCollision(b)        

        def beginMiniBoss(self):
            self.miniBoss = True
            self.bsl(self.stomper, "None")
            self.renderObstacles()
            self.stomper.ignoreCollision = False
            self.stomper.frozen = False

        def update(self, seconds):
            if FLAGS[42]:
                if self.miniBoss:
                    SoundManager.getInstance().playLowSFX("enemydies.wav", volume=0.2)
                    SoundManager.getInstance().playBGM(self.bgm)
                    self.vanishObstacles()
                    self.miniBoss = False

                else:
                    super().update(seconds)

            elif FLAGS[41]:
                if self.stomper.dead:
                    if self.stomperTimer == 0.0:
                        SoundManager.getInstance().fadeoutBGM()
                        self.displayText("The goddess's ice...&&\nWhy.........&&\nDid she.......&&\nChoose........&&\nYou.......?&&\n", icon=ICON["stomper"])
                        self.stomperTimer += seconds
                    elif self.stomperTimer >= 0.3:
                        FLAGS[42] = True
                        super().update(seconds)
                    else:
                        self.stomperTimer += seconds
                    return
                elif self.miniBoss:
                    if self.bossHealthbar.initializing:
                        if self.textInt == 3:
                            self.playBgm("8mile.mp3")
                            self.textInt = 2
                        super().update(seconds, updateEnemies=False)
                    else:
                        if self.stomper.cold and self.textInt == 2:
                            self.displayText("Blast! I'm C-c-cold\nas s-s-stone!\n", icon=ICON["stomper"])
                            self.textInt += 1
                        super().update(seconds)
                elif self.player.position[1] >= 20:
                    self.player.stop()
                    self.beginMiniBoss()
                else:
                    super().update(seconds, updateEnemies=False)
            else:
                super().update(seconds, updateEnemies=False)
                if self.inCutscene:
                    if self.textInt == 2:
                        self.stomper.update(seconds, position = vec(16*8 - 6, 16*5))
                        if self.stomper.pause:
                            self.spawning.pop(0)
                            self.inCutscene = False
                            return
                        

                    if self.stomperTimer >= 1.0:
                        if self.textInt == 0:
                            self.displayText("Whoa, man! Chill out!&&\nPlease, my Goddess Estelle,\nsave me from this fiend!\n", icon=ICON["geemer0"])
                            self.stomper.pause = False
                        elif self.textInt == 1:
                            self.displayText("Shutup, ant.&&\nYour Goddess can't save you.&&\nWithout the power of ice,\nyou're a feeble creature!\n", icon=ICON["stomper"])
                        self.textInt += 1
                        self.stomperTimer = 0.0
                    else:
                        self.stomperTimer += seconds

                elif len(self.spawning) == 0:
                    if self.miniBoss:
                        if self.stomperTimer >= 1.0:
                            self.beginMiniBoss()                            
                            self.stomperTimer = 0.0
                            FLAGS[41] = True
                            self.player.keyUnlock()
                            self.inCutscene = False
                        else:
                            self.stomperTimer += seconds

                    elif self.stomperTimer >= 2.0:
                        self.stomperTimer = 0.0
                        self.displayText("Ah! Yet another human!&&\nCrushing you is way more\nfun than crushing Geemers!\nThe boss won't even have\nto waste his time with you!\nGood riddance, outsider!&&\n", icon=ICON["stomper"])
                        self.textInt = 3
                        self.miniBoss = True
                    else:
                        self.stomperTimer += seconds
                
                elif self.player.position[1] >= 20:
                    self.inCutscene = True
                    self.player.stop()
                    self.player.keyLock()
                    SoundManager.getInstance().fadeoutBGM()

class Flame_10(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame10()
      
        return cls._INSTANCE
    
    class _Flame10(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "lava_reef.mp3"
            self.ignoreClear = False
            self.max_enemies = 4
            self.enemyPlacement = 1
            self.background = Level("flame_10.png")
            self.trigger1 = Trigger(door = 1)
            self.chest = Key(vec(16*9, 16*9))
            self.upgrade = Chest(COORD[9][2], text=SPEECH["bombo_expansion"], icon = ICON["bombo"])
            self.doors = [1]
            self.enemies = [
                
                FireFlapper(),
                GremlinB(),
                FireFlapper(),
                Baller(),
            ]
            self.npcs = [

                Heater(vec(16*9-8, 16*5-8))
            ]
            self.light = LightSwitch(COORD[15][2])
            self.switch = LockedSwitch(COORD[3][2], row = 5, locked=False)
            self.switches = [
                self.light,
                self.switch
            ]
            self.obstacles = [
                Boulder(vec(16*15 - 8, 16*2 - 8))
            ]

        def handleClear(self):
            self.spawning.append(self.chest)
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                self.enemyCollision(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Flame_6, 3, keepBGM=True)
                    else:
                        self.player.handleCollision(b)

        def updateSwitches(self, seconds):
            self.updateLightSwitch(self.light)
        
        def update(self, seconds):
            super().update(seconds)
            if self.upgrade not in self.spawning:
                if self.light.pressed and self.switch.pressed:
                    self.spawning.append(self.upgrade)


class Flame_7(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame7()
      
        return cls._INSTANCE
    
    class _Flame7(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "lava_reef.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_7.png")
            self.trigger1 = Trigger(door = 0)
            self.trigger2 = Trigger(door = 2)
            self.doors = [0,2]
            self.block = LockBlock((COORD[9][10]))#Locked block
            self.yblock1 = Block((COORD[8][11]), (5,5))
            self.yblock2 = Block((COORD[9][11]), (5,5))
            self.yblock3 = Block((COORD[10][11]), (5,5))
            self.blocks.append(self.block)
            self.blocks.append(self.yblock1)
            self.blocks.append(self.yblock2)
            self.blocks.append(self.yblock3)
            self.bull = Bullshot(COORD[4][3])
            self.npcs = [
                self.bull,
                Bopper(COORD[10][4]),
                Bopper(COORD[11][3]),
                Bopper(COORD[11][5]),
                Bopper(COORD[12][2]),
                Bopper(COORD[13][3]),
                Bopper(COORD[14][4]),
                Bopper(COORD[12][6]),
                Bopper(COORD[13][5]),
                Bopper(COORD[15][3]),
                Bopper(COORD[15][5]),
                Bopper(COORD[16][2]),
                Bopper(COORD[16][6]),
                Bopper(COORD[16][5]),
                Bopper(COORD[16][4]),
                Bopper(COORD[16][3]),
                #Bopper(COORD[13][2]),
                

            ]

            self.spawning = [
                NpcBopper(COORD[3][6], SPEECH["flame_7_bopper1"]),
                NpcBopper(COORD[12][4], SPEECH["flame_7_bopper2"])
            ]

        def initializeRoom(self, player=None, pos=None, keepBGM=False, placeEnemies=True):
            if not self.bull.dead:
                self.bull.hp = 20
            return super().initializeRoom(player, pos, keepBGM, placeEnemies)
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
        
        def popBlocks(self):
            INV["keys"] -= 1
            self.playSound("LA_Dungeon_Teleport_Appear.wav")
            self.blocks.pop(self.blocks.index(self.block))
            self.blocks.pop(self.blocks.index(self.yblock1))
            self.blocks.pop(self.blocks.index(self.yblock2))
            self.blocks.pop(self.blocks.index(self.yblock3))

        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                self.enemyCollision(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Flame_8, 2, keepBGM=True)
                    elif b == self.trigger2:
                        self.transport(Flame_6, 0, keepBGM=True)
                    elif b == self.block:
                        if INV["keys"] >= 1:
                            self.popBlocks()
                    else:
                        self.player.handleCollision(b)

class Flame_8(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame8()
      
        return cls._INSTANCE
    
    class _Flame8(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "lava_reef.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_8.png")
            self.doors = [1,2]
            self.trigger1 = Trigger(door = 2)
            self.trigger2 = Trigger(door = 1)
            self.firstDead = False
            self.secondDead = False
            self.stomper1 = Stomper(vec(16*5, 16*6))
            self.stomper1.jumpTimer = -0.5
            self.stomper2 = Stomper(vec(16*13, 16*6))
            self.stomper2.jumpTimer = -1.0
            #self.stomper3 = Stomper(vec(16*9, 16*6))
            self.enemies = [
                #Flapper(),FireFlapper(),Flapper(),FireFlapper()
            ]
            self.npcs = [
                self.stomper1,
                self.stomper2,
                Bopper(COORD[7][1]),
                Bopper(COORD[11][1]),
            ]
            self.lockedSwitch = LockedSwitch(COORD[9][8])
            self.switches.append(self.lockedSwitch)
            self.yblock1 = Block((COORD[17][5]), (5,5))
            self.yblock2 = Block((COORD[17][7]), (5,5))
            self.yblock3 = Block((COORD[17][6]), (5,5))
            self.blocks.append(self.yblock1)
            self.blocks.append(self.yblock2)
            self.blocks.append(self.yblock3)

        def initializeRoom(self, player=None, pos=None, keepBGM=False, placeEnemies=True):
            if not self.room_clear:
                if not self.stomper1.dead:
                    #self.stomper1.hp = 25
                    self.stomper1.setPosition(vec(16*5, 16*6))
                    self.stomper1.jumpTimer = -0.5

                if not self.stomper2.dead:
                    #self.stomper2.hp = 25
                    self.stomper2.setPosition(vec(16*13, 16*6))
                    self.stomper2.jumpTimer = -1.0

            super().initializeRoom(player, pos, keepBGM, placeEnemies)

        def handleClear(self):
            self.room_clear = True
            self.lockedSwitch.unlock()

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                self.enemyCollision(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Flame_7, 0, keepBGM=True)
                    elif b == self.trigger2:
                        self.transport(Flame_9, 3)
                    else:
                        self.player.handleCollision(b)
        
        def handleCollision(self):
            super().handleCollision()
            self.despawnOnPress(self.yblock1, self.lockedSwitch)
            if self.yblock1 not in self.blocks:
                self.disappear(self.yblock2)
                self.disappear(self.yblock3)
            
        
        def update(self, seconds, updateEnemies=True, updatePlayer=True):
            if self.room_clear:
                super().update(seconds, updateEnemies, updatePlayer)
                return

            if not self.firstDead:
                if self.stomper1.dead:
                    self.displayText("Gah! Damn you, outsider!&&\nIf only......&&\nThe boss was here.....&&\n", icon=ICON["stomper"])
                    self.firstDead = True
            if not self.secondDead:
                if self.stomper2.dead:
                    self.displayText("There was so much...&&\nSo much more...&&\nThat I wanted to see...&&\n", icon=ICON["stomper"])
                    self.secondDead = True
            if not self.room_clear:
                if self.stomper1.dead and self.stomper2.dead:
                    self.handleClear()
            super().update(seconds, updateEnemies, updatePlayer)

class Flame_9(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Flame9()
      
        return cls._INSTANCE
    
    class _Flame9(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "tension.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("flame_9.png")
            self.trigger1 = Trigger(door = 3)
            self.trigger2 = Trigger(door = 2)
            self.doors = [2,3]

        #override
        def createBlocks(self):
           self.blocks.append(self.trigger1)
           self.blocks.append(self.trigger2)
           
        #override
        def blockCollision(self):
            for b in self.blocks:
                self.projectilesOnBlocks(b)
                self.enemyCollision(b)
                if self.player.doesCollide(b):
                    if b == self.trigger1:
                        self.transport(Flame_8, 1)
                    elif b == self.trigger2:
                        self.transport(Knight, 0, keepBGM=True)
                    else:
                        self.player.handleCollision(b)
"""
Thunder
"""
class Thunder_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Thun_1()
      
        return cls._INSTANCE
    
    class _Thun_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "voyager.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("thunder_1.png")
            self.doors = [3, 0, 2]
            self.toChapel = Trigger(door = 3)
            self.trigger = Trigger(door = 0)
            self.trigger2 = Trigger(door=2)
            self.geemer = Geemer((16*2, 16*5-8), text = SPEECH["menu_reminder"])
            self.geemer2 = Geemer(COORD[9][6], text = SPEECH["thunder_1"])
            self.geemer3 = Geemer((16*9-4, 16), text = SPEECH["thunder_2"], hungry = True, feedText=SPEECH["thunder_fead"])
            self.geemer3.framesPerSecond = 1
            self.spawning.append(self.geemer)
            self.spawning.append(self.geemer2)
            self.spawning.append(self.geemer3)
            for j in range(1,12):
                for i in range(2,17):
                    self.tiles.append(Tile((i*16, j*16)))

            #self.trigger1 = Trigger(door = 0)
        
            
            super().initializeRoom(player, pos, keepBGM)
        
        
        #override
        def createBlocks(self):
           self.blocks.append(self.toChapel)
           self.blocks.append(self.trigger)
           self.blocks.append(self.trigger2)
               
           
        #override
        def blockCollision(self):
           for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.toChapel:
                       self.transport(Grand_Chapel_R, 0)
                    elif b == self.trigger:
                        self.transport(Thunder_2, 2, keepBGM=True)
                    elif b == self.trigger2:
                        self.transport(Thunder_3, 0, keepBGM=True)
                    else:
                       self.player.handleCollision(b)

        def update(self,seconds):
            super().update(seconds)
            if self.geemer3.fead:
                if self.geemer3.position[0] >= 16*11:
                    self.geemer3.ignoreCollision = False
                    self.geemer3.vel = vec(0,0)

class Thunder_2(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Thun_2()
      
        return cls._INSTANCE
    
    class _Thun_2(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "voyager.mp3"
            self.ignoreClear = False
            self.max_enemies = 8
            self.enemyPlacement = 2
            self.background = Level("thunder_2.png")
            self.doors = [2]
            
            self.chest = Chest(COORD[9][6], SPEECH["plant"], ICON["plant"])
            
            self.trigger = Trigger(door = 2)
            self.enemies = [
                ThunderFlapper(),ThunderFlapper(),ThunderFlapper(),ThunderFlapper(),
                IceFlapper(),IceFlapper(),IceFlapper(),IceFlapper()
            ]

            self.npcs = [
                Dummy(COORD[7][6]),
                Dummy(COORD[9][4]),
                Dummy(COORD[11][6]),
                Dummy(COORD[9][8])
            ]
            self.tiles = [
                Tile(COORD[7][4]),Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),Tile(COORD[11][4]),
                Tile(COORD[7][5]),Tile(COORD[8][5]),Tile(COORD[9][5]), Tile(COORD[10][5]),Tile(COORD[11][5]),
                Tile(COORD[7][6]),Tile(COORD[8][6]),Tile(COORD[9][6]), Tile(COORD[10][6]),Tile(COORD[11][6]),
                Tile(COORD[7][7]),Tile(COORD[8][7]),Tile(COORD[9][7]), Tile(COORD[10][7]),Tile(COORD[11][7]),
                Tile(COORD[7][8]),Tile(COORD[8][8]),Tile(COORD[9][8]), Tile(COORD[10][8]),Tile(COORD[11][8])
                #Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),
                #Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),

            ]
            

            #self.trigger1 = Trigger(door = 0)
        

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            
            super().initializeRoom(player, pos, keepBGM)
        
        
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger)
           
               
        def handleClear(self):
            self.spawning.append(self.chest)

        #override
        def blockCollision(self):
           for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.trigger:
                        self.transport(Thunder_1, 0, keepBGM=True)
                    else:
                       self.player.handleCollision(b)


class Thunder_3(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Thun_3()
      
        return cls._INSTANCE
    
    class _Thun_3(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "voyager.mp3"
            self.ignoreClear = True
            self.resetting = True
            self.max_enemies = 26
            self.enemyPlacement = 0
            self.background = Level("thunder_3.png")
            self.doors = [0]
            
           
            
            self.trigger = Trigger(door = 0)
            
            self.portal = Portal(COORD[9][6], 2)
            self.blocks.append(self.portal)
            self.sign = Sign(COORD[9][3], text = SPEECH["thunder_sign"])
            self.spawning.append(self.sign)
            self.enemies = [
                Dummy(COORD[7][8]),
                Dummy(COORD[8][8]),
                Dummy(COORD[9][8]),
                Dummy(COORD[10][8]),
                Dummy(COORD[11][8]),

                Dummy(COORD[7][7]),
                Dummy(COORD[8][7]),
                Dummy(COORD[9][7]),
                Dummy(COORD[10][7]),
                Dummy(COORD[11][7]),

                Dummy(COORD[7][6]),
                Dummy(COORD[8][6]),
                Dummy(COORD[10][6]),
                Dummy(COORD[11][6]),

                Dummy(COORD[7][5]),
                Dummy(COORD[8][5]),
                Dummy(COORD[9][5]),
                Dummy(COORD[10][5]),
                Dummy(COORD[11][5]),

                Dummy(COORD[7][4]),
                Dummy(COORD[8][4]),
                Dummy(COORD[9][4]),
                Dummy(COORD[10][4]),
                Dummy(COORD[11][4]),

                GremlinB(COORD[2][9], direction = 1),
                GremlinB(COORD[16][9], direction = 3),
                GremlinB(COORD[2][2], direction = 1),
                GremlinB(COORD[16][2], direction = 3)
            ]
            self.tiles = [
                Tile(COORD[7][4]),Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),Tile(COORD[11][4]),
                Tile(COORD[7][5]),Tile(COORD[8][5]),Tile(COORD[9][5]), Tile(COORD[10][5]),Tile(COORD[11][5]),
                Tile(COORD[7][6]),Tile(COORD[8][6]), Tile(COORD[10][6]),Tile(COORD[11][6]),
                Tile(COORD[7][7]),Tile(COORD[8][7]),Tile(COORD[9][7]), Tile(COORD[10][7]),Tile(COORD[11][7]),
                Tile(COORD[7][8]),Tile(COORD[8][8]),Tile(COORD[9][8]), Tile(COORD[10][8]),Tile(COORD[11][8])
                #Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),
                #Tile(COORD[8][4]),Tile(COORD[9][4]), Tile(COORD[10][4]),

            ]
            

            #self.trigger1 = Trigger(door = 0)
        

        def initializeRoom(self, player=None, pos=None, keepBGM=False):
            
            super().initializeRoom(player, pos, keepBGM)
        
        
        #override
        def createBlocks(self):
           self.blocks.append(self.trigger)
           
               

        #override
        def blockCollision(self):
           for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.trigger:
                        self.transport(Thunder_1, 2, keepBGM=True)
                    elif b == self.portal:
                        self.transport(Grand_Chapel, 0)
                    else:
                       self.player.handleCollision(b)

        def update(self, seconds):
            super().update(seconds)
            self.portal.update(seconds)

"""
Frost
"""
class Frost_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Frost_1()
      
        return cls._INSTANCE
    
    class _Frost_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "LA_color.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("frost_1.png")
            self.doors = [0]
            self.toChapel = Trigger(door = 0)
            #self.trigger1 = Trigger(door = 0)
            self.torch1 = Torch((COORD[7][5]), lit = False)
            self.torch2 = Torch((COORD[11][5]), lit = False)

            self.chest = Chest(COORD[9][3], text = SPEECH["david"])
            self.spawning.append(self.chest)
            self.weightedSwitch = WeightedSwitch((16*9,16*8))
            self.switches.append(self.weightedSwitch)
            self.blockP = PushableBlock((16*6,16*8))
            self.david = David(COORD[9][6], boss = True)
            #self.david.hp = 1
            self.portal = Portal(COORD[9][6], 1)
            self.torches.append(self.torch1)
            self.torches.append(self.torch2)

        #override
        def createBlocks(self):
           self.blocks.append(self.toChapel)
           
           
        #override
        def blockCollision(self):
            for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.toChapel:
                       self.transport(Grand_Chapel_L, 2)
                    elif b == self.portal:
                        self.transport(Grand_Chapel, 0)
                    else:
                       self.player.handleCollision(b)


            for t in self.torches:
                if self.player.doesCollide(t):
                    self.player.handleCollision(t)
                self.projectilesOnTorches(t)
        
        def handleCollision(self):
            super().handleCollision()
            if self.blockP not in self.pushableBlocks and (self.torch1.lit and self.torch2.lit):
                self.playSound("menuclose.wav")
                self.pushableBlocks.append(self.blockP)
            if not self.david.dead:
                if self.weightedSwitch.pressed:
                    if self.david not in self.npcs:
                        self.npcs.append(self.david)
        
        def update(self, seconds):
            super().update(seconds)
            if self.david.dead:
                if self.portal not in self.blocks:
                    self.blocks.append(self.portal)
                    self.playSound("room_clear.mp3")
                    self.displayText("David has been slain!&&")
                self.portal.update(seconds)


class Frost_2(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Frost_2()
      
        return cls._INSTANCE
    
    class _Frost_2(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "LA_color.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("frost_1.png")
            self.doors = [0]
            self.npcs = [
                Shiver(position=vec(16*9, 16*5))
            ]
            self.toChapel = Trigger(door = 0)
            #self.trigger1 = Trigger(door = 0)
            self.torch1 = Torch((COORD[7][5]), lit = False)
            self.torch2 = Torch((COORD[11][5]), lit = False)

            self.chest = Chest(COORD[9][3], text = SPEECH["david"])
            self.spawning.append(self.chest)
            self.weightedSwitch = WeightedSwitch((16*9,16*8))
            self.switches.append(self.weightedSwitch)
            self.blockP = PushableBlock((16*6,16*8))
            self.david = David(COORD[9][6], boss = True)
            #self.david.hp = 1
            self.portal = Portal(COORD[9][6], 1)
            self.torches.append(self.torch1)
            self.torches.append(self.torch2)

    
        #override
        def createBlocks(self):
           self.blocks.append(self.toChapel)
           
           
        #override
        def blockCollision(self):
            for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.toChapel:
                       self.transport(Grand_Chapel_L, 2)
                    elif b == self.portal:
                        self.transport(Grand_Chapel, 0)
                    else:
                       self.player.handleCollision(b)
            for t in self.torches:
                if self.player.doesCollide(t):
                    self.player.handleCollision(t)
                self.projectilesOnTorches(t)
        
        def handleCollision(self):
            super().handleCollision()
            if self.blockP not in self.pushableBlocks and (self.torch1.lit and self.torch2.lit):
                self.playSound("menuclose.wav")
                self.pushableBlocks.append(self.blockP)
            if not self.david.dead:
                if self.weightedSwitch.pressed:
                    if self.david not in self.npcs:
                        self.npcs.append(self.david)
        
        def update(self, seconds):
            super().update(seconds)
            if self.david.dead:
                if self.portal not in self.blocks:
                    self.blocks.append(self.portal)
                    self.playSound("room_clear.mp3")
                    self.displayText("David has been slain!&&")
                self.portal.update(seconds)


"""
Gale
"""
class Gale_1(AbstractEngine):
    @classmethod
    def getInstance(cls):
        if cls._INSTANCE == None:
         cls._INSTANCE = cls._Gale_1()
      
        return cls._INSTANCE
    
    class _Gale_1(AE):
        def __init__(self):
            super().__init__()
            self.bgm = "windFortress.mp3"
            self.ignoreClear = True
            self.max_enemies = 0
            self.enemyPlacement = 0
            self.background = Level("gale_1.png")
            self.doors = [0,2]
            self.portal = Portal(COORD[8][10], 3)
            self.trigger1 = Trigger(door = 0)
            self.sign = Sign(COORD[9][4], text = SPEECH["gale_sign"])
            self.spawning.append(self.sign)
            self.npcs = [
                David(COORD[2][8]),
                David(COORD[16][6], direction = 3),
                David(COORD[2][4]),
                David(COORD[16][2], direction = 3),
                GremlinB(COORD[8][5], direction = 1),
                GremlinB(COORD[10][5], direction = 3)
            ]
            #self.trigger1 = Trigger(door = 0)
        

        #override
        def createBlocks(self):
           self.blocks.append(self.portal)
           self.blocks.append(self.trigger1)
           
        #override
        def blockCollision(self):
           for b in self.blocks:
               self.enemyCollision(b)
               self.projectilesOnBlocks(b)
               if self.player.doesCollide(b):
                    if b == self.portal:
                       self.transport(Grand_Chapel, COORD[14][4])
                    elif b == self.trigger1:
                        self.transport(Grand_Chapel_R, 2)
                    else:
                       self.player.handleCollision(b)


        def update(self, seconds):
            super().update(seconds)
            self.portal.update(seconds)