from pygame import Surface, Rect, transform
from .player import *
from utils import vec, RESOLUTION, INV

class MapElement:
    def __init__(self, position = vec(0,0), size = RESOLUTION):
        self.position = position
        self.image = Surface(size)
    
    def draw(self, surf):
        surf.blit(self.image, self.position)

class Floor(MapElement):
    """A drawable Floor"""
    def __init__(self, position = vec(0,0), size = RESOLUTION):
        super().__init__(position, size)

class Walls(MapElement):
    """A drawable Wall Image"""
    def __init__(self, position = vec(0,0), size = RESOLUTION):
        super().__init__(position, size)  

class Number:
    def __init__(self, position, number, row):
        self.position = position
        self.number = number
        self.row = row
        self.max_y = self.position[1] - 8
        self.image = SpriteManager.getInstance().getSprite("numbers.png",(number,row))

    def get_size(self):
        return self.image.get_size()
    
    def draw(self, surf):
        #   Break Down numbers > 10 #
        if self.number >= 10:
            currentPos = vec(self.position[0]-3, self.position[1])
            number = str(self.number)
            for char in number:
                self.position[0] -= self.get_size()[0] // 2
                num = Number(currentPos, int(char), self.row)
                num.draw(surf)
                currentPos[0] += 6
        
        #   Display the single digit number #
        else:
            self.position[0] -= self.get_size()[0] // 2
            surf.blit(self.image, self.position)



class NumberManager:
    def __init__(self):
        self._data = []
    
    def draw(self, surf):
        for n in self._data:
            n.draw(surf)
    
    def add(self, position, number, row):
        self._data.append(Number(position, number, row))

    def update(self, seconds):
        for num in self._data:
            num.position[1] -= 20 * seconds
            if num.position[1] <= num.max_y:
                del self._data[(self._data.index(num))]

class MajestusEngine():
    """An Abstract engine that controls the game's objects"""
    def __init__(self, size = RESOLUTION, enemies = [], max_enemies = 0, bgm = "01"):

        #   Metadata    #
        self.size = size
        self.floor = Floor()
        self.walls = Walls()

        #   States  #
        self.dead = False
        self.quitting = False   

        #   Fading Data #
        self.fading = False
        self.whiting = False
        
        #   Dialogue States and Objects #
        self.text_box = None
        self.text = ""

        #   Standalone Objects #
        self.player = None
        self.numbers = NumberManager()

        #   Object Lists #
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

        ##  Additional Layers to Draw   ##
        self.layer_1 = []
        self.layer_2 = []
        self.layer_3 = []
        self.layer_4 = []
        self.layer_5 = []

        return
    
    def remove(self, obj):
        if obj in self.loaded_enemies:
            del self.loaded_enemies[self.loaded_enemies.index(obj)]

        elif obj in self.weapons:
            del self.weapons[self.weapons.index(obj)]
        return
    
    def play_sound(self, sound):
        SoundManager.getInstance().playSFX(sound)

    def load_enemies(self):
        self.loaded_enemies = self.enemies

    def initialize_room(self, player = None, position=vec(0,0), keep_bgm=False, place_enemies=True):
        if keep_bgm:
            pass

        if place_enemies:
            pass

        if player is None:
            self.player = Player(position)
        else:
            self.player = player

        self.load_enemies()
    
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

        #   HUD #
        self.numbers.draw(surf)

    def handle_weapons(self):
        #   Arrow   #
        if self.player.bullet != None:
            self.weapons.append(self.player.getBullet())
            self.player.bullet = None

        #Flames
        if self.player.sword != None:
            self.weapons.append(self.player.getFlame())
            self.playSound(self.player.swordSound)
            self.player.sword = None
        
        #Thunder clap
        if self.player.clap != None:
            self.weapons.append(self.player.getClap())
            self.playSound(Clap.SOUND)
            self.player.clap = None
        
        #Gale slash
        if self.player.slash != None:
            self.weapons.append(self.player.getSlash())
            self.playSound("plasma_shot.wav")
            self.player.slash = None
        
        #Blizzard
        if self.player.blizzard != None and self.player.blizzard not in self.weapons:
            self.weapons.append(self.player.getBlizzard())
            #self.playSound("")

        if self.player.hook != None:
            self.weapons.append(self.player.getHook())
            self.player.hook = None


    def handle_events(self) -> None:
        self.player.handle_events()
        self.handle_weapons()
        self.handle_collision()
    
    
    def handle_collision(self):
        #   Player on Enemies   #
        for e in self.loaded_enemies:
            if self.player.doesCollide(e):
                if e.handle_player_collision(self.player):
                    self.player.handleCollision(e)

            #   Weapons on Enemies  #
            for w in self.weapons:
                if e.collides_with_projectile(w):
                    e.handle_projectile_collision(w)
                    w.hit = True
                    if w.hit:
                        ##   Display Damage  ##
                        damage = e.get_injury()

                        if damage == 0:
                            self.numbers.add(vec(e.getCenterX(), e.position[1]), damage, row=0)
                        elif damage < 0:
                            self.numbers.add(vec(e.getCenterX(), e.position[1]), damage * -1, row=2)
                        else:
                            self.numbers.add(vec(e.getCenterX(), e.position[1]), damage, row=3)

                        e.reset_injury()

                    w.handleCollision(self)

    def update(self, seconds) -> None:
        #   Floor   #
        #   Walls   #
        #   Draw Layer 1    #
        #   Draw Layer 2    #
        #   Draw Layer 3    #
        #   Draw Layer 4    #
        #   Draw Layer 5    #
        #   NPCs    #
        #   Drops   #
        for d in self.drops:
            d.update(seconds)

        #   Numbers #
        self.numbers.update(seconds)

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