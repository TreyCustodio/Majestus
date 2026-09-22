from pygame import Surface, Rect, transform
from gameObjects import *
from .player import *
from utils import vec, RESOLUTION, INV

from abc import ABC, abstractmethod
import os
import re


"""
Helper Classes
"""
class LevelElement:
    """An abstract element of the level"""
    def __init__(self, position = vec(0,0), size = RESOLUTION, room_dir = ""):
        self.position = position
        self.image = Surface(size, pygame.SRCALPHA)
        self.room_dir = room_dir
    
    def draw(self, surf):
        surf.blit(self.image, self.position - Drawable.CAMERA_OFFSET)

    def set_image(self):
        return
    
    def update(self, seconds):
        if not self.animate:
            return
        
        self.animation_timer += seconds

        if self.animation_timer > 1 / self.fps:
            self.frame += 1
            self.frame %= self.nFrames

            self.animation_timer -= 1 / self.fps
            self.set_image()

class Floor(LevelElement):
    """A drawable Floor"""
    def __init__(self, position = vec(0,0), size = RESOLUTION, room_dir = "", fps = 3, animate = False, nFrames = 0):
        super().__init__(position, size, room_dir)
        
        files = os.listdir(os.path.join("images", "levels", room_dir))
        pattern = re.compile(r'^tiles_(\d+).png$')
        matches = [f for f in files if pattern.match(f)]
        count = len(matches)

        if count > 1:
            self.animate = True
            self.fps = fps
            self.nFrames = count
            self.frame = 0
            self.animation_timer = 0.0
            self.image = SpriteManager.getInstance().getFx(room_dir, "tiles_0.png")

        else:
            self.animate = False
            self.image = SpriteManager.getInstance().getFx(room_dir, "tiles.png")

    def set_image(self):
        self.image = SpriteManager.getInstance().getFx(self.room_dir, "tiles_" + str(self.frame) + ".png")
    
    
    

class Walls(LevelElement):
    """A drawable Wall Image"""
    def __init__(self, position = vec(0,0), size = RESOLUTION, room_dir = "", fps = 3):
        super().__init__(position, size, room_dir)
        
        files = os.listdir(os.path.join("images", "levels", room_dir))
        pattern = re.compile(r'^walls_(\d+).png$')
        matches = [f for f in files if pattern.match(f)]
        count = len(matches)


        if count > 1:
            self.animate = True
            self.fps = fps
            self.nFrames = count
            self.frame = 0
            self.animation_timer = 0.0
            self.image = SpriteManager.getInstance().getFx(room_dir, "walls_0.png")

        else:
            self.animate = False
            self.image = SpriteManager.getInstance().getFx(room_dir, "walls.png")

    def set_image(self):
        self.image = SpriteManager.getInstance().getFx(self.room_dir, "walls_" + str(self.frame) + ".png")
    



"""
Engine Class
"""
class MajestusEngine(ABC):
    """An Abstract engine that controls the game's objects"""
    def __init__(self, size = RESOLUTION, enemies = [], max_enemies = 0, bgm = "01", room_dir = "",
                 roomId = -1):

        #   Metadata    #
        self.size = size
        self.floor = Floor(room_dir=room_dir)
        self.walls = Walls(room_dir=room_dir)
        self.roomId = -1
        self.bgm = bgm
        self.camera = Camera.getInstance()

        #   General States  #
        self.dead = False
        self.quitting = False
        self.fightingBoss = False 

        #   Dialogue States and Objects #
        self.speaking = False
        self.text_box = None
        self.text = ""

        #   Transition States   #
        self.readyToTransition = False
        self.lock_transition = False
        self.transporting = False
        self.transporting_area = False
        self.tra_room = None
        self.tra_pos = None
        self.tra_keepBGM = False
        self.enemyCounter = 0

        #   Fading Data #
        self.fading = False
        self.whiting = False
        
        #   Standalone Objects and Managers #
        self.player = None
        self.hud = HudManager.getInstance()

        #   === Object Lists === #
        ##  Interactable Entities   ##
        self.npcs = []
        
        ##  Enemies to Load ##
        self.enemies = enemies

        ##  Currently Loaded Enemies    ##
        self.loaded_enemies = []

        ##  Player's Weapons    ##
        self.weapons = []
        
        ##  Drops to Pickup ##
        self.drops = []

        ##  Collision Blocks ##
        self.blocks = []
        self.triggers = []

        ##  Doors   ##
        self.doors = []

        ##  Additional Layers to Draw   ##
        self.layer_1 = []
        self.layer_2 = []
        self.layer_3 = []
        self.layer_4 = []
        self.layer_5 = []
        return

    """
    === Abstract Methods ===
    """
    @abstractmethod
    def load_blocks(self):
        return

    @abstractmethod
    def trigger_collision(self, trigger_id):
        """Handle trigger collision based on the trigger's id"""
        return

    @abstractmethod
    def load_progress(self):
        """Load any additional data that is subject to change based on 
        the player's save data, such as puzzle completion, unlocked doors,
        one-time enemies, and collectable items"""
        return

    
    """
    === Auxiliary Functions ===
    """
    def reset(self):
        """Reset the room"""
        return
    
    def initialize_room(self, player = None, position=vec(0,0), keep_bgm=False, place_enemies=True):
        """Initialize the room's objects, including the player, collision blocks, and enemies"""
        #   Play the next song or keep playing the same one #
        if keep_bgm:
            pass
        else:
            SoundManager.getInstance().play_ost(self.bgm)

        if place_enemies:
            pass

        #   Initialize a new player if their is not one loaded  #
        if player is None:
            self.player = Player(position)
        else:
            self.player = player
        self.player.set_position(position)

        #   Load the enmies #
        self.load_enemies()

        #   Load the blocks #
        self.load_blocks()

        #   Load anything else  #
        self.load_progress()

    def transport(self, room=None, position=vec(0,0), position_int = -1, keepBGM = False):
        """
        Transport the player to a different room.
        position -> 0-3 representing cardinal direction, or a specific coordinate
        keepBgm -> keeps the bgm
        """
        if not self.transporting and not self.lock_transition:
            self.fade()

            self.transporting = True
            self.tra_room = room

            if position_int == -1:
                self.tra_pos = position
            elif position_int == 0:
                self.tra_pos = vec(16*9, 16*11)
            elif position_int == 1:
                self.tra_pos = vec(16*16, 16*6 - 8)
            elif position_int == 2:
                self.tra_pos = vec(16*9, 8)
            elif position_int == 3:
                self.tra_pos = vec(16*2, 16*6-8)
            else:
                self.tra_pos = position
                
            self.tra_keepBGM = keepBGM
            if not keepBGM:
                SoundManager.getInstance().fadeout_bgm()

    def remove(self, obj):
        """Remove an object from the room's references"""
        if obj in self.loaded_enemies:
            del self.loaded_enemies[self.loaded_enemies.index(obj)]

        elif obj in self.weapons:
            del self.weapons[self.weapons.index(obj)]
        return
    
    def play_sound(self, sound):
        """Play a sound effect"""
        SoundManager.getInstance().playSFX(sound)

    def fade(self):
        """
        Initializes fadeout by locking
        player and setting self.fading to True
        """
        if self.player:
            self.player.keyLock()
        self.fading = True

    def finish_fade(self):
        """Finish fade and transition.
        Lets DisplayManager know to switch rooms"""
        self.fading = False
        self.readyToTransition = True

    def stopFadeIn(self):
        """
        Finish the fadeIn process.
        """
        self.whiting = False
        self.transLock = False
        self.fading = False
        self.area_fading = False
        self.player.keyUnlock()
        self.player.keyDownUnlock()

    def load_enemies(self):
        """Load the room's enemies"""
        self.loaded_enemies = self.enemies

    def createSquare(self):
        ##Left, Right
        for i in range(1,5):
            #Left
            self.blocks.append(IBlock((0, i*16), width=42))
            self.blocks.append(IBlock((0, i*16 + 16*7), width=42))

            #Right
            self.blocks.append(IBlock((18*16 - 8 - 18, i*16), width=42))
            self.blocks.append(IBlock((18*16 - 8 - 18, i*16 + 16*7), width=42))

        ##Bottom, Top
        for i in range(8):
            #Bottom
            self.blocks.append(IBlock((i*16, 19*10 - 8 - 16), height=42))
            self.blocks.append(IBlock((i*16 +16*11, 19*10 - 8 - 16), height=42))

            #Top
            self.blocks.append(IBlock((i*16, 0), height=42))
            self.blocks.append(IBlock((i*16 +16*11, 0), height=42))

    def createVertical(self):
        ###Quadrant 1
        ##Left, Right
        for i in range(1,5):
            #Left
            self.blocks.append(IBlock((0, i*16), width=42))

            #Right
            self.blocks.append(IBlock((18*16 - 8 - 18, i*16), width=42))
        
        ##Gap in range(5-8)
        ##Middle section
        for i in range(8,12):
            #Left
            self.blocks.append(IBlock((0, i*16), width=42))

            #Right
            self.blocks.append(IBlock((18*16 - 8 - 18, i*16), width=42))
        
        ##Gap in range(12-15)
        ##Bottom section
        for i in range(15,19):
            #Left
            self.blocks.append(IBlock((0, i*16), width=42))

            #Right
            self.blocks.append(IBlock((18*16 - 8 - 18, i*16), width=42))
        
        
        ##Bottom, Top
        for i in range(8):
            #Bottom
            self.blocks.append(IBlock((i*16, 19*16 - 8 - 18), height=42))
            self.blocks.append(IBlock((i*16 +16*11, 19*16 - 8 - 18), height=42))

            #Top
            self.blocks.append(IBlock((i*16, 0), height=42))
            self.blocks.append(IBlock((i*16 +16*11, 0), height=42))
    
    
    def createHorizontal(self, gap = False):
        ##Left, Right
        for i in range(1,5):
            #Left
            self.blocks.append(IBlock((0, i*16), width=42))
            self.blocks.append(IBlock((0, i*16 + 16*7), width=42))


            #Right
            self.blocks.append(IBlock((18*16 - 8 - 18, i*16), width=42))
            self.blocks.append(IBlock((18*16 - 8 - 18, i*16 + 16*7), width=42))

        ##Bottom, Top
        for i in range(8):
            #Bottom
            self.blocks.append(IBlock((i*16, 19*10 - 8 - 16), height=42))
            self.blocks.append(IBlock((i*16 +16*11, 19*10 - 8 - 16), height=42))

            #Top
            self.blocks.append(IBlock((i*16, 0), height=42))
            self.blocks.append(IBlock((i*16 +16*11, 0), height=42))

        ### Quadrant 2
        ##Left, Right
        for i in range(1,5):
            #Left
            self.blocks.append(IBlock((0 + 304, i*16), width=42))
            self.blocks.append(IBlock((0 + 304, i*16 + 16*7), width=42))

            #Right
            self.blocks.append(IBlock((18*16 - 8 - 18 + 304, i*16), width=42))
            self.blocks.append(IBlock((18*16 - 8 - 18 + 304, i*16 + 16*7), width=42))

        ##Bottom, Top
        for i in range(8):
            #Bottom
            self.blocks.append(IBlock((i*16 + 304, 19*10 - 8 - 16), height=42))
            self.blocks.append(IBlock((i*16 +16*11 + 304, 19*10 - 8 - 16), height=42))

            #Top
            self.blocks.append(IBlock((i*16 + 304, 0), height=42))
            self.blocks.append(IBlock((i*16 +16*11 + 304, 0), height=42))

    def set_doors(self, shape: str ="square", quadrants: int = 1):
        """(WIP)
        quadrants -> the number of square quandrants the room will have"""

        #   Build Square Quadrants  #
        if shape == "sqaure":
            ###  Quadrant 1
            ##  Bottom
            if 0 not in self.doors:
                self.blocks.append(IBlock((16*8, 19*10 - 8 - 16), height=42))
                self.blocks.append(IBlock((16*9, 19*10 - 8 - 16), height=42))
                self.blocks.append(IBlock((16*10, 19*10 - 8 - 16), height=42))
    
            ##  Right - Also Middle
            if 1 not in self.doors:
                self.blocks.append(IBlock((16*16 + 6, 5*16), width=42))
                self.blocks.append(IBlock((16*16 + 6, 6*16), width=42))
                self.blocks.append(IBlock((16*16 + 6, 7*16), width=42))
    
            ##  Top
            if 2 not in self.doors:
                self.blocks.append(IBlock((16*8, 0), height=42))
                self.blocks.append(IBlock((16*9, 0), height=42))
                self.blocks.append(IBlock((16*10, 0), height=42))
    
            ##  Left
            if 3 not in self.doors:
                self.blocks.append(IBlock((0, 5*16), width=42))
                self.blocks.append(IBlock((0, 6*16), width=42))
                self.blocks.append(IBlock((0, 7*16), width=42))
            
            ###  Quadrant 2
            if quadrants > 1:
                ##  Bottom
                if 4 not in self.doors:
                    self.blocks.append(IBlock((16*8 + 304, 19*10 - 8 - 16), height=42))
                    self.blocks.append(IBlock((16*9 + 304, 19*10 - 8 - 16), height=42))
                    self.blocks.append(IBlock((16*10 + 304, 19*10 - 8 - 16), height=42))
    
                ##  Right - Middle
                if 5 not in self.doors:
                    self.blocks.append(IBlock((16*16 + 6 + 304, 5*16), width=42))
                    self.blocks.append(IBlock((16*16 + 6 + 304, 6*16), width=42))
                    self.blocks.append(IBlock((16*16 + 6 + 304, 7*16), width=42))
    
                ##  Top
                if 6 not in self.doors:
                    self.blocks.append(IBlock((16*8 + 304, 0), height=42))
                    self.blocks.append(IBlock((16*9 + 304, 0), height=42))
                    self.blocks.append(IBlock((16*10 + 304, 0), height=42))
    
                ##  Left - Middle
                if 7 not in self.doors:
                    self.blocks.append(IBlock((0+ 304, 5*16), width=42))
                    self.blocks.append(IBlock((0+ 304, 6*16), width=42))
                    self.blocks.append(IBlock((0+ 304, 7*16), width=42))
                
                ##  Right - End
                if 8 not in self.doors:
                    self.blocks.append(IBlock((16*16 + 6 + 608, 5*16), width=42))
                    self.blocks.append(IBlock((16*16 + 6 + 608, 6*16), width=42))
                    self.blocks.append(IBlock((16*16 + 6 + 608, 7*16), width=42))
                
                ##  Left - End
                if 9 not in self.doors:
                    self.blocks.append(IBlock((0 + 608, 5*16), width=42))
                    self.blocks.append(IBlock((0 + 608, 6*16), width=42))
                    self.blocks.append(IBlock((0 + 608, 7*16), width=42))

        #   Build Vertical Quadrants    #
        elif shape == "vertical":
            if 0 not in self.doors:
                self.blocks.append(IBlock((8*16, self.size[1]-42), width = 48,height = 48))
            
            if 1 not in self.doors:        
                self.blocks.append(IBlock((self.size[0]-42, 5*16), width = 42, height = 48))
            
            if 2 not in self.doors:
                self.blocks.append(IBlock((8*16, 0), width = 48, height = 42))
            
            if 3 not in self.doors:
                self.blocks.append(IBlock((0, 5*16), width = 42, height = 48))
            
            if 5 not in self.doors:
                self.blocks.append(IBlock((self.size[0]-42, 16*12), width = 42, height = 48))
            
            if 7 not in self.doors:
                self.blocks.append(IBlock((0, 16*12), width = 42, height = 48))    

        #   Build Default Quadrants #
        else:
            if 0 not in self.doors:
                self.blocks.append(IBlock((8*16, self.size[1]-16)))
                self.blocks.append(IBlock((9*16, self.size[1]-16)))
                self.blocks.append(IBlock((10*16, self.size[1]-16)))
            else:
                self.blocks.append(IBlock((16*8-8, self.size[1]-16)))
                self.blocks.append(IBlock((16*10+8, self.size[1]-16)))
            
            if 1 not in self.doors:        
                self.blocks.append(IBlock((self.size[0]-24, 5*16)))
                self.blocks.append(IBlock((self.size[0]-24, 6*16)))
                self.blocks.append(IBlock((self.size[0]-24, 7*16)))
            else:
                self.blocks.append(IBlock((self.size[0]-24, 16*7+8)))
                self.blocks.append(IBlock((self.size[0]-24, 16*5-8)))
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

    

    
    def check_memory(self):
        print("Enemies: " + str(len(self.loaded_enemies)) + "\n" + str(self.loaded_enemies), end="\n\n")
        print("Weapons:" + str(len(self.weapons)) + "\n" + str(self.weapons), end="\n\n")

    def draw(self, surf) -> None:
        # self.check_memory()

        #   Floor   #
        self.floor.draw(surf)

        #   Walls   #
        self.walls.draw(surf)

        #   Draw Layer 1    #
        #   Draw Layer 2    #
        #   Draw Layer 3    #
        #   Draw Layer 4    #
        #   Draw Layer 5    #
        #   NPCs    #
        #   Drops   #
        for d in self.drops:
            d.draw(surf)

        #   Enemies #
        for e in self.loaded_enemies:
            e.draw(surf)

        #   Player's Weapons    #
        for w in self.weapons:
            w.draw(surf)

        #   Player  #
        self.player.draw(surf)

        #   Blocks  #
        for b in self.blocks:
            b.draw(surf)

        #   HUD #
        self.hud.draw(surf, self.player)

    def handle_weapons(self):
        """Check if any of the player is using any of their weapons"""
        #   Arrow   #
        if self.player.bullet != None:
            self.weapons.append(self.player.getBullet())
            self.player.bullet = None
            self.play_sound("shoot.wav")


        #Flames
        if self.player.sword != None:
            self.weapons.append(self.player.getFlame())
            self.play_sound(self.player.swordSound)
            self.player.sword = None
        
        #Thunder clap
        if self.player.clap != None:
            self.weapons.append(self.player.getClap())
            self.play_sound(Clap.SOUND)
            self.player.clap = None
        
        #Gale slash
        if self.player.slash != None:
            self.weapons.append(self.player.getSlash())
            self.play_sound("plasma_shot.wav")
            self.player.slash = None
        
        #Blizzard
        if self.player.blizzard != None and self.player.blizzard not in self.weapons:
            self.weapons.append(self.player.getBlizzard())
            #self.play_sound("")

        if self.player.hook != None:
            self.weapons.append(self.player.getHook())
            self.player.hook = None


    def handle_events(self) -> None:
        self.player.handle_events()
        self.handle_weapons()
        self.handle_collision()
    

    """
    === Collision Detection ===
    """
    def block_collision(self):
        for b in self.blocks:
            #   Projectile Collision    #
            if b.popProjectiles:
                for w in self.weapons:
                    if not w.hit:
                        if w.doesCollide(b):
                            if w.id == "arrow":
                                w.handleCollision(self, b)
                            else:
                                w.handleCollision(self)

            #   Player Collision    #
            if self.player.doesCollide(b):
                #   Trigger Collision   #
                if isinstance(b, Trigger):
                    self.trigger_collision(b.id)

                #   Block Collision #
                else:
                    self.player.handleCollision(b)

    
    
    def handle_collision(self):
        #   Enemies   #
        for e in self.loaded_enemies:
            if self.player.doesCollide(e):
                if e.handle_player_collision(self.player):
                    self.player.handleCollision(e)

            ##   Weapons on Enemies  #
            for w in self.weapons:
                if e.collides_with_projectile(w):
                    e.handle_projectile_collision(w)
                    if w.hit:
                        ###   Display Damage  #
                        damage = e.get_injury()

                        if damage == 0:
                            self.hud.add_number(vec(e.getCenterX(), e.position[1]), damage, row=0)
                        elif damage < 0:
                            self.hud.add_number(vec(e.getCenterX(), e.position[1]), damage * -1, row=2)
                        else:
                            self.hud.add_number(vec(e.getCenterX(), e.position[1]), damage, row=3)

                        e.reset_injury()

                    w.handleCollision(self)


        #   Terrain #
        #   Blocks  #
        self.block_collision()
        # AE.lockCollision(self)



    """
    === Updating ===
    """
    def bsl(self, enemy, bossTheme):
        """
        Boss script load (bsl) para Cave Story.
        Loads up the boss fight.
        """
        self.pause_lock = True
        self.bossTheme = bossTheme
        self.player.keyLock()
        self.boss = enemy
        self.bossHealthbar = BossHealth(enemyHealth= enemy.hp)
        self.fightingBoss = True
        self.drawBossHealth = True

    def update_camera(self, seconds) -> None:
        """ 
        if self.camera.position[0] == 0:
            return
        elif self.camera.position[0] == 912:m
            return """
        # self.camera.position[0] = self.player.position[0] - (self.camera.getSize()[0] // 2)
        # self.camera.position[1] = self.player.position[1] - (self.camera.getSize()[1] // 2)

        # self.camera.position[0] = int(self.player.position[0]) + (self.player.get_width() // 2)
        # self.camera.position[1] = int(self.player.position[1]) + (self.player.get_height() // 2)

        self.camera.position[0] = int(self.player.position[0]) - (self.camera.getSize()[0] // 2)
        self.camera.position[1] = int(self.player.position[1]) - (self.camera.getSize()[1] // 2)

        Drawable.updateOffset(self.camera, self.size)

    def update(self, seconds) -> None:
        #   Floor   #
        self.floor.update(seconds)
        
        #   Walls   #
        self.walls.update(seconds)
        
        #   Draw Layer 1    #
        #   Draw Layer 2    #
        #   Draw Layer 3    #
        #   Draw Layer 4    #
        #   Draw Layer 5    #
        
        #   NPCs    #
        #   Drops   #
        for d in self.drops:
            d.update(seconds)

        #   Numbers + Hud   #
        self.hud.update(seconds, self.player)
        self.update_camera(seconds)

        #   Player's Weapons    #
        for w in self.weapons:
            w.update(seconds, self)

        #   Enemies #
        for e in self.loaded_enemies:
            e.update(seconds, self.player)

            ##  Enemy Death ##
            if e.dead:
                if self.player.hp == INV["max_hp"]:
                    drop = e.get_money()

                else:
                    drop = e.get_drop()

                self.drops.append(drop)

                del self.loaded_enemies[self.loaded_enemies.index(e)]

        #   Player  #
        self.player.update(seconds)